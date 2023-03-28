import requests, shutil, os, pyperclip, json, random, string
from selenium import webdriver
from contextlib import suppress
from time import sleep
from urllib.parse import urlparse
#############################################################
# \/\/ Webdriver & browser stuff \/\/
driver_path = 'drivers/chromedriver.exe'
chrome_path = 'drivers/brave/brave-portable.exe'
option = webdriver.ChromeOptions()
option.binary_location = chrome_path
option.add_argument("--disable-gpu, --window-size=640,480")
option.add_experimental_option("excludeSwitches", ["enable-logging"])
with suppress(Exception): # Load prefrences file
    with open('drivers/Preferences') as jsonFile:
        pref = json.load(jsonFile)
    option.add_experimental_option("prefs", pref)
# /\/\ Webdriver & browser stuff /\/\
# \/\/\/ Constants \/\/\/
siteSet = "https://my.harmonytx.org/idp/AuthnEngine#/authn/"
loggedIn = "https://my.harmonytx.org/ui/applications/" # Logged in page, you can tell from the "app" subdomain.
tCount = 0
ranAlready = False
foundWorking = False
Debug = False
noscrape = False
threwWarning = False
# /\/\/\ Constants /\/\/\
print("Starting Script")
if (noscrape):
    print("!!!WARNING!!!")
    print(" noscrape is TRUE")
    threwWarning = True
if (Debug):
    print("!!!WARNING!!!")
    print(" Debug is TRUE")
    threwWarning = True 
if (threwWarning):
    print("Continuing in 3 seconds", end="")
    for i in range(3):
        sleep(1)
        print(".", end="")
    print()
print("Starting browser...")
browser = webdriver.Chrome(executable_path=driver_path, options=option)
# \/\/\/ Cleaning \/\/\/
print("Cleaning...")
tCount = 1
for i in range(1000):
    try:
        finalfilename = "cookie" + str(tCount) + ".txt"
        os.remove(finalfilename)
        print("FINAL_FILE Deleted", finalfilename)
        tCount += 1
    except:
        tCount +=1
tCount = 1
for i in range(1000):
    try:
        tempfilename = "temp" + str(tCount) + ".json"
        os.remove(tempfilename)
        print("TEMP_FILE Deleted", tempfilename)
    except:
        tCount +=1
tCount = 0
print("Finished cleaning")
# /\/\/\ Cleaning /\/\/\
# \/\/\/ Classes \/\/\/
class SiteScrape:
    def __init__(self, siteList, xpath):
        self.siteList = siteList
        self.xpath = xpath
        global tCount
        global xPathTxt
        print("Starting to scrape...")
        try: 
            if (noscrape):
                raise Exception("  noscrape is True")
            if (foundWorking == True):
                raise Exception("  Already found working cookie.")
            domain = urlparse(siteList[0]).netloc
            print("Using site:", domain)
            for site in siteList:
                browser.get(site)
                print(" URL: ", browser.current_url)
                xPathTxt = browser.find_element_by_xpath(xpath) # Get cookie found in xpath provided
                print("Got text")
                Verify(xPathTxt.text)
                tCount += 1
            print("Scraped through", tCount, "pages")
        except Exception as e:
            print(e)
            pass
class Verify:
    def __init__(self, verifyThis):
        global siteSet
        global foundWorking
        self.verifyThis = verifyThis
        try:
            print("\nVerifying JSON cookie...")
            browser.get(siteSet)
            print("Importing cookie")
            # with suppress(Exception):
            cookieList = json.loads(verifyThis)
            for cookie in cookieList:
                browser.add_cookie({k: cookie[k] for k in {'name','value'}})
            print("Imported Cookie")
            browser.get(siteSet)
            print("\nChecking login status...")
            print("Current URL =", browser.current_url)
            print("================")
            if (loggedIn == browser.current_url):
                print("URL OK, working.\n================")
                pyperclip.copy(verifyThis)
                print("Copied cookie to clipboard.")
                foundWorking = True
                browser.close()
                raise Exception("End script. Found working cookie.")
                quit()
            elif (loggedIn != browser.current_url):
                print("URL BAD, Cookie didn't work\n================")
        except Exception as e:
            print("Found exception:", e)
            browser.close()
# /\/\/\ Classes /\/\/\
sites = ["https://www.linkstricks.com/p/grammarly-cookie-1.html", "https://www.linkstricks.com/p/grammarly-cookie-2.html", "https://www.linkstricks.com/p/grammarly-cookie-3.html", "https://www.linkstricks.com/p/grammarly-cookie-4.html", "https://www.linkstricks.com/p/grammarly-cookie-5.html", "https://www.linkstricks.com/p/grammarly-cookie-6.html"]
xpath = "/html/body/div[1]/main/div[2]/div/div[1]/div/div/div/article/div[1]/div[2]/div[7]/div/form/textarea"
SiteScrape(sites, xpath)
sites = ["https://freefirereviews.com/grammarly-cookies-1-updated/", "https://freefirereviews.com/grammarly-cookie-2-updated/", "https://freefirereviews.com/grammarly-cookie-3-updated/", "https://freefirereviews.com/grammarly-cookie-4-updated/", "https://freefirereviews.com/grammarly-cookie-5-updated/"]
xpath = "/html/body/div/div/div/div[1]/main/article/div/pre/code"
SiteScrape(sites, xpath)
# \/\/\/ Final Section \/\/\/
# This is pretty much redundant. Don't want to remove it just in case.  
if(foundWorking == False):
    print("Could not find any cookies.")
elif(foundWorking == True):
    print("Found working cookies! Check your clipboard. Ctrl + V")
try:
    print("Trying to close browser...")
    browser.close()
    print(" Browser closed.")
except Exception as e:
    print(" Exception when running browser.close():", e)
    if ('invalid' in str(e)):
        print(" Browser was most likely already closed.")
print("Script Finished.")
exit()
# /\/\/\ Final Section /\/\/\
