# linkedin_scrape



This is a script based on [this](https://www.youtube.com/watch?v=twRQNSFXiYs&t=384s) video.


### Prerequisites
* Python3
* BeautifulSoup
* Selenium



### Usage

  

```
usage: view_linkedin_profiles.py [-h] [--email EMAIL] [--password PASSWORD]
                                 [-a] [-k KEYWORD] [-t TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  --email EMAIL, -e EMAIL
                        Linkedin email.
  --password PASSWORD, -p PASSWORD
                        Linkedin password.
  -a, --auto            Automatic login (provide email and password by
                        changing the values in the CONFIG section of this
                        script).
  -k KEYWORD, --keyword KEYWORD
                        (Optional) All linkedin users will be related to this
                        specific keyword. If a keyword is not provided a
                        keyword list can be set in the CONFIG section of this
                        script.
  -t TIMEOUT, --timeout TIMEOUT
                        (Optional) Time in seconds this script will run before
                        stopping. It is recommended to set a timeout of at
                        most 15 minutes (900 seconds) to prevent Linkedin from
                        suspending your account. The default time is 5 minutes
                        (300 seconds).
```



### Config
In the file you will find the configuration for the script.


```



# ======================================================
#                   CONFIG
# ======================================================
# 
# email and password
auto_email = "linkedin@email.com"
auto_password = "password"
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

```

* auto_email: This is requred for the `-a` parameter for the automatic login.
* auto_password: This is required for the `-a` parameter for the automatic login.
* keywords: (Optional) List of keywords to ramdomly select a a topic/subject/skill that all linkedin users will be related to.
* PERIOD_OF_TIME: (Optional) Time in seconds this script will run before
                        stopping. It is recommended to set a timeout of at
                        most 15 minutes (900 seconds) to prevent Linkedin from
                        suspending your account. The default time is 5 minutes
                        (300 seconds)
 * CHROME_DRIVER_PATH: (Optional) Absolute path to the chromedriver for google chrome (linux). 
 
 
 ### Examples
 This is the default usage with the email and password as parameters.
 * `python view_linkedin_profiles.py -e YOUR_LINKEDIN_EMAIL -p YOUR_LINKEDIN_PASSWORD`
 
 The -t, --timeout is the numbers of seconds that the script will run.
 * `python view_linkedin_profiles.py -e YOUR_LINKEDIN_EMAIL -p YOUR_LINKEDIN_PASSWORD -t 900`
 
 The -k, --keyword parameter will help you search/view other users related to the keyword.
 * `python view_linkedin_profiles.py -e YOUR_LINKEDIN_EMAIL -p YOUR_LINKEDIN_PASSWORD -k django`
 
 The --auto parameter helps skip the email and password parameters. This will only work with both the auto_email and auto_password values set in the CONFIG section in the script. 
 * `python view_linkedin_profiles.py -a -t 500 -k software`
 
