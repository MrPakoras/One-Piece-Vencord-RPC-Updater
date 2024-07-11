from datetime import datetime, timedelta
import re, json, shutil, os, subprocess
from os import path
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from datetime import datetime, timedelta
import re, json, shutil, os, subprocess


# currtime = datetime.now()
# print(currtime)

# timenow = datetime.strptime(currtime, '%B %d, %Y')

# print(timedelta(days=currtime.weekday()))

# formatdt = currtime.strftime('%B %d, %Y')
# print(formatdt)

# changedt = datetime.strptime(formatdt, '%B %d, %Y')
# print(changedt)

# print(re.search(r"[A-Z][a-z]* [0-9][0-9]?, [0-9][0-9][0-9][0-9]", formatdt))

# shutil.copy('settings.json', 'settings_backup.json')
# f = open('settings.json','r')
# fj = json.load(f)
# f.close()

# maintext = fj['plugins']['CustomRPC']['details']
# subtext = fj['plugins']['CustomRPC']['state']

# print(f'{maintext}: {subtext}')

# fj['plugins']['CustomRPC']['details'] = 'Testing 1'
# fj['plugins']['CustomRPC']['state'] = 'Testing 2'

# maintext = fj['plugins']['CustomRPC']['details']
# subtext = fj['plugins']['CustomRPC']['state']

# print(f'{maintext}: {subtext}')

# f = open('settings.json','w')
# fjd = json.dump(fj, f, indent=4)
# f.close()


# try:
# 	os.system("taskkill /im discord.exe /f")
# except:
# 	pass

# subprocess.call('C:/Users/Anas/AppData/Local/Discord/app-1.0.9023/Discord.exe')

# subprocess.Popen('C:/Users/Anas/AppData/Local/Discord/app-1.0.9023/Discord.exe')

# day = '14/Nov/2023'
# tn = datetime.now()
# dt = datetime.strptime(day, '%d/%b/%Y')
# start = dt - timedelta(days=dt.weekday())
# end = start + timedelta(days=6)
# print(start)
# print(end)


# if start <= tn <= end:
# 	print('Yes')
# else:
# 	print('No')

# print(os.getenv('LOCALAPPDATA'))

# PATH = 'W:/Python/Python Web Scraping/chromedriver.exe' # Chrome Driver path
# url = f"https://claystage.com/one-piece-chapter-release-schedule-for-2024"
# print('>> Connecting...')

# options = wd.ChromeOptions()
# options.add_argument('--headless') # Run Chrome in headless mode (no browser)
# options.add_argument('window-size=1920x1080')
# options.add_argument('log-level=3')

# service = Service(executable_path=PATH)

# driver = wd.Chrome(service=service,options=options)
# driver.get(url) # Opens URL in browser

# # Search on page for the next date that a chapter will release

# dt = datetime.now()
# currdt = dt.strftime('%B %d, %Y')

# # Accept cookies
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div.fc-consent-root > div.fc-dialog-container > div.fc-dialog.fc-choice-dialog > div.fc-footer-buttons-container > div.fc-footer-buttons > button.fc-button.fc-cta-consent.fc-primary-button'))).click()

# # https://stackoverflow.com/questions/75552030/how-can-i-print-out-all-text-in-a-web-table-column-in-python-using-selenium
# table = driver.find_element(By.XPATH, '//*[@id="post-4130"]/div/div[2]/figure/table') # Data table
# rows = table.find_elements(by=By.TAG_NAME, value="tr")

# weeks = []
# chapters = []
# dates = []

# tdfiller = timedelta(days=1000) # fill blank indexes with timedelta so that min func can work on list


# for x in rows:
# 	cells = x.find_elements(by=By.TAG_NAME, value='td')
# 	for x in cells:
# 		print(x)

# driver.quit()


a = ['a','b','c']
b = [4,5,6]

print(b[a.index('a')])