import argparse, os, time
from selenium import webdriver
from bs4 import BeautifulSoup
import random
from collections import deque



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









def getJobLinks(page):
	links = []
	for link in page.find_all('a'):
		url = link.get('href')
		if url:		
			if '/jobs' in url:
				links.append(url)
	return links










def getUsername(url):
    return url.split("/")[2]
    









def ViewBot(browser, param_keyword=None, timeout=None):
    visited = {}
    pList = deque()
    count = 0
    start = time.time()

    if timeout:
        PERIOD_OF_TIME = timeout

    if len(visited) == 0 and len(pList) == 0 and count == 0:
        if param_keyword != None or len(keywords) > 0:
            time.sleep(random.uniform(3.5, 6.9))
            if param_keyword:
                searchword = param_keyword
            else: 
                searchword = random.choice(keywords)
            search_link =  "{}/search/results/all/?keywords={}&origin=GLOBAL_SEARCH_HEADER".format(base, str(searchword).replace(" ", "%20"))
            print("Searching for {} connections".format(searchword))
            browser.get(search_link)

    while True:
        time.sleep(random.uniform(3.5, 6.9))
        page = BeautifulSoup(browser.page_source, "html.parser")
        people = getPeopleLinks(page)

        if people:
            for person in people:
                username = getUsername(person)
                if not username in visited:
                    pList.append(person)
                    visited[username] = 1
        if pList:
            person = pList.popleft()
            profile = "{}{}".format(base, person)
            browser.get(profile)
            count += 1
        else:
            jobs = getJobLinks(page)
            if jobs:
                job = random.choice(jobs)
                root = 'http://www.linkedin.com'
                roots = 'https://www.linkedin.com'
                if root not in job or roots not in job:
                    job = 'https://www.linkedin.com'+job
                browser.get(job)
            else:
                print("I'm Lost Exiting")
                break
        #Output (Make option for this)			
        print( "[+] "+str(browser.title)+" Visited! \n("+str(count)+"/"+str(len(pList))+") Visited/Queue)")
        if time.time() > start + PERIOD_OF_TIME : break







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
    ViewBot(browser, param_keyword, timeout)
    browser.close()







if __name__ == "__main__":
    main()






