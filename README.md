# Jack Advanced Web Bruteforcer
jawb is a tool for bruteforcing login pages. I created this mainly for CTFs.

# Configure
Just run the `configure.sh` script to create the virtualenv and install the dependencies 
```bash
./configure.sh
```
# Usage
```
usage: jawb.py [-h] -u URL [-t THREADS] [-H HEADERS] -pf PASSWORD_FILE -pn PASSWORD_NAME -su SINGLE_USERNAME -ic
               IN_TEXT_CHECK -un USERNAME_NAME [-ev EXTRACT_VALUE] [--ip-spoof]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Url of the target.
  -t THREADS, --threads THREADS
                        Number of parallel requests.
  -H HEADERS, --headers HEADERS
                        Set headers values separated by a semicolon.
  -pf PASSWORD_FILE, --password-file PASSWORD_FILE
                        Read passwords from file. If the value is a dash, reads from stdin.
  -pn PASSWORD_NAME, --password-name PASSWORD_NAME
                        Name of the variable that will receive the password.
  -su SINGLE_USERNAME, --single-username SINGLE_USERNAME
                        Use a single username
  -ic IN_TEXT_CHECK, --in-text-check IN_TEXT_CHECK
                        Detect if credentials succeeded or failed. Put a esclamationmark at the beginning to detect failed
                        login if the followingtext is present
  -un USERNAME_NAME, --username-name USERNAME_NAME
                        Name of the variable that will receive the username.
  -ev EXTRACT_VALUE, --extract-value EXTRACT_VALUE
                        Specifies a custom post parameter from HTML page. Extract it by using the following rule: <HTML
                        tag>;<attribute to extract>;<attribute identifier name>;<attribute identifier value> <attribute
                        reference> is the tag attribute that helps the program to recognize the right tag to pick
  --ip-spoof            Adds X-Forwarded-For header with random generated IP for every request

```