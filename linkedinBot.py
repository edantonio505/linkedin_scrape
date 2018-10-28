import argparse, os, time
from selenium import webdriver
from bs4 import BeautifulSoup






def ViewBot(browser):
    visited = {}
    pList = []
    count = 0
    print(browser)








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
    parser.add_argument("--email", "-e",  help="linkedin email")
    parser.add_argument("--password", "-p", help="linkedin password")
    args = parser.parse_args()
    email = args.email
    password = args.password
    browser = webdriver.Chrome("{}/chromedriver".format(os.getcwd()))
    browser.get("https://linkedin.com/uas/login")
    login(email, password, browser)
    os.system('clear')
    print("[+] Success! Logged In, Bot Starting!")
    ViewBot(browser)
    browser.close()







if __name__ == "__main__":
    main()






