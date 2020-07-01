import time
import random
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd



class LinkedInBot:


    base = "https://www.linkedin.com"
    ELLIPSE = .75
    blacklist = ["Staffigo"]


    def __init__(self, browser, param_keyword=None, timeout=None, keywords=None, keyword_file=None, file_column=None):
        print("LinkedInBot")
        self.browser = browser
        self.keywords = []
        self.timeout = timeout
        self.param_keyword = None
        if timeout == None:
            self.timeout = 12000


        if keywords != None and keyword_file != None:
            #raise Exception("Cannot use both keywords and keyword_file")
            print("Cannot use both keywords and keyword_file")
        elif keywords != None:
            self.keywords = keywords
        elif keyword_file != None and file_column == None:
            #raise Exception("When using keyword_file you must also enter the target column name in file_column")
            print("When using keyword_file you must also enter the target column name in file_column")
        elif keyword_file != None and file_column != None:
            self.keywords = self.get_targets(keyword_file, file_column)

        print(self.keywords)
        if len(self.keywords) > 0 and self.param_keyword == None:
            self.param_keyword = random.choice(self.keywords)
        else:
            print("Please provide a keyword or include some keywords in the CONFIG section in this script.")
            quit()
        if param_keyword != None:
            self.param_keyword = param_keyword


    def __str__(self):
        message = "LinkedInBot: \n"
        message += "\t-param_keyword: {}\n".format(self.param_keyword)
        message += "\t-timeout: {}\n".format(self.timeout)
        message += "\t-keywords: {}".format(self.keywords)
        return message


    def get_targets(self, filename, column):
        print("Parsing File...")
        df = pd.read_csv(filename,
                        header=None,
                        names=['timestamp', 'jobID', 'job', 'company', 'attempted', 'result'])
        print(f"length: {len(df)}")
        targets = list(set(list(df[column])))
        targets = [target for target in targets if target not in self.blacklist]
        return targets


    def get_people_links(self, page):
        links = []
        urls =  page.find_all("a")

        for link in urls:
            url = link.get('href')
            if url:
                if "www.linkedin.com" in url and "miniProfileUrn" in url:
                    url = "{}/".format(str(url.replace(self.base, "").split("?")[0]))
                if '/in' in url and not "www.linkedin.com" in url:
                    if url not in links:
                        links.append(url)
        return links


    def get_job_links(self, page):
        links = []
        for link in page.find_all('a'):
            url = link.get('href')
            if url:		
                if '/jobs' in url:
                    links.append(url)
        return links


    def get_username(self, url):
        return url.split("/")[2]        


    def visit_profiles(self):
        visited = {}
        pList = deque()
        count = 0
        start = time.time()

        if self.timeout:
            PERIOD_OF_TIME = self.timeout
            
        print("This script will run for {} minutes.".format(str(self.timeout//60)))

        first_run = (len(visited) == 0 and len(pList) == 0 and count == 0)

        while True:
            if first_run or random.random() > self.ELLIPSE:
                self.param_keyword = random.choice(self.keywords)
                time.sleep(random.uniform(3.5, 6.9))
                search_link =  "{}/search/results/all/?keywords={}&origin=GLOBAL_SEARCH_HEADER".format(self.base, str(self.param_keyword).replace(" ", "%20"))
                print("Searching for {} connections".format(self.param_keyword))
                self.browser.get(search_link)

            time.sleep(random.uniform(3.5, 6.9))
            page = BeautifulSoup(self.browser.page_source, "html.parser")
            people = self.get_people_links(page)

            if people:
                for person in people:
                    username = self.get_username(person)
                    if not username in visited:
                        pList.append(person)
                        visited[username] = 1
            if pList:
                person = pList.popleft()
                profile = "{}{}".format(self.base, person)
                self.browser.get(profile)
                count += 1
            else:
                jobs = self.get_job_links(page)
                if jobs:
                    job = random.choice(jobs)
                    root = 'http://www.linkedin.com'
                    roots = 'https://www.linkedin.com'
                    if root not in job or roots not in job:
                        job = 'https://www.linkedin.com'+job
                    self.browser.get(job)
                else:
                    print("I'm Lost Exiting")
                    break
                    
            #Output (Make option for this)			
            print( "[+] "+str(self.browser.title)+" Visited! \n("+str(count)+"/"+str(len(pList))+") Visited/Queue)")
            if time.time() > start + PERIOD_OF_TIME : break

            if random.random() > self.ELLIPSE:
                    sleepTime = random.randint(60, 500)
                    print(f'\n\n********************\n\n')
                    print(f"Time for a nap - see you in:{int(sleepTime/60)} min")
                    print('\n\n****************************************\n\n')
                    time.sleep (sleepTime)









