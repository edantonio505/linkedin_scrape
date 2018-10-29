import argparse, os
from selenium import webdriver
from linkedinBot import LinkedInBot






# ======================================================
#                   CONFIG
# ======================================================
# 
# email and password
auto_email = ""
auto_password = ""
# 
#keywords to search for specific topics, skills, fields, jobs, etc ... 
# provide keywords in (string) separated by commas.
keywords = [
    "php",
    "python",
    "software",
    "django",
    "machine learning",
    "data analysis",
    "Google",
    "web development", 
    "programming"
]

# Time to run
PERIOD_OF_TIME = 300
# Chrome driver path
# Only provide this if you would like this script to run on a cronjob. 
CHROME_DRIVER_PATH = ""
# =========================================================





def login(email, password, browser):
    try:
        emailElement = browser.find_element_by_id("session_key-login")
        emailElement.send_keys(email)
        passElement = browser.find_element_by_id("session_password-login")
        passElement.send_keys(password)
    except:
        emailElement = browser.find_element_by_id("username")
        emailElement.send_keys(email)
        passElement = browser.find_element_by_id("password")
        passElement.send_keys(password)
    passElement.submit()







def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", "-e",  help="Linkedin email.")
    parser.add_argument("--password", "-p", help="Linkedin password.")
    parser.add_argument("-a", "--auto", action="store_true", help="Automatic login (provide email and password by changing the values in the CONFIG section of this script).")
    parser.add_argument("-k", "--keyword", help="(Optional) All linkedin users will be related to this specific keyword. If a keyword is not provided a keyword list can be set in the CONFIG section of this script.")
    parser.add_argument("-t", "--timeout", help="(Optional) Time in seconds this script will run before stopping. It is recommended to set a timeout of at most 15 minutes (900 seconds) to prevent Linkedin from suspending your account. The default time is 5 minutes (300 seconds).")
    param_keyword = None
    timeout = PERIOD_OF_TIME
    args = parser.parse_args()
    email = args.email
    password = args.password

    if (not email or not password) and (not args.auto):
        print("Please include email and password using the -p and -e options or automate the task by providing auto_email and auto_password in the CONFIG section of this script.")
        args = parser.parse_args(["-h"])
        quit()

    if args.auto:
        if auto_email == "" or auto_password == "":
            print("Please set auto_email and auto_password in the CONFIG section of this script")
            quit()
        email = auto_email
        password = auto_password

    if args.keyword:
        param_keyword = args.keyword

    if args.timeout:
        timeout = int(args.timeout)

    try:
        browser = webdriver.Chrome("{}/chromedriver".format(os.getcwd()))
    except:
        browser = webdriver.Chrome(CHROME_DRIVER_PATH)
    browser.get("https://linkedin.com/uas/login")
    login(email, password, browser)
    os.system('clear')
    print("[+] Success! Logged In, Bot Starting!")
    bot = LinkedInBot(browser, param_keyword, keywords=keywords, timeout=timeout)
    bot.visit_profiles()
    browser.close()







if __name__ == "__main__":
    main()

