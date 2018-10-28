import argparse, os, time
from selenium import webdriver
from bs4 import BeautifulSoup
import random



base = "https://www.linkedin.com"



def getPeopleLinks(page):
    links = []
    urls =  page.find_all("a")

    for link in urls:
        url = link.get('href')
        if url:
            if "www.linkedin.com" in url and "miniProfileUrn" in url:
                url = "{}/".format(str(url.replace(base, "").split("?")[0]))
            if '/in' in url and not "www.linkedin.com" in url:
                if url not in links:
                    links.append(url)
    return links









def ViewBot(browser):
    visited = {}
    pList = []
    count = 0
    while True:
        time.sleep(random.uniform(3.5, 6.9))
        page = BeautifulSoup(browser.page_source, "html.parser")
        people = getPeopleLinks(page)

        print(people)
        quit()






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

    if not email or not password:
        print("Arguments missing, please try \n linkedinBot.py -h for help")
        quit()

    browser = webdriver.Chrome("{}/chromedriver".format(os.getcwd()))
    browser.get("https://linkedin.com/uas/login")
    login(email, password, browser)
    os.system('clear')
    print("[+] Success! Logged In, Bot Starting!")
    ViewBot(browser)
    browser.close()







if __name__ == "__main__":
    main()






