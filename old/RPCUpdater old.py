# Gets next OP chapter number and break status from https://claystage.com/one-piece-chapter-release-schedule-for-2023
# Changes discord RPC text to info from above


from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import SessionNotCreatedException as chromedriver_outdated
from datetime import datetime, timedelta
from colorama import Fore
import re, json, shutil, os, subprocess, chromedriver_autoinstaller

## Vencord settings file
appdata = os.getenv('APPDATA')
vencordrpcfile = f'{appdata}/Vencord/settings/settings.json'

os.system("taskkill /im discord.exe /f") # Close Discord

def debug():
	n = 1
	for x in ['Last', 'Current', 'Next']:
		debuginfo = f'{Fore.MAGENTA}>> {x} Chapter: {chapters[thisweekindex-n]}\n{Fore.YELLOW}- Date: {Fore.GREEN}{dates[thisweekindex-n]} - {weeks[thisweekindex-n]}'
		print(debuginfo)
		n -= 1

def prog(urldate):
	# PATH = 'W:/Python/Python Web Scraping/chromedriver.exe' # Chrome Driver path
	url = f"https://claystage.com/one-piece-chapter-release-schedule-for-{urldate}"
	print(f'{Fore.CYAN}>> Connecting...')

	options = wd.ChromeOptions()
	options.add_argument('--headless') # Run Chrome in headless mode (no browser)
	options.add_argument('window-size=1920x1080')
	options.add_argument('log-level=3')

	# service = Service(executable_path=PATH) - not needed anymore because chromedriver_autoinstaller adds chromedriver to PATH

	# driver = wd.Chrome(service=service,options=options)
	driver = wd.Chrome(options=options)
	driver.get(url) # Opens URL in browser

	# Search on page for the next date that a chapter will release

	dt = datetime.now()
	currdt = dt.strftime('%B %d, %Y')
	print(currdt)

	# Accept cookies
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div.fc-consent-root > div.fc-dialog-container > div.fc-dialog.fc-choice-dialog > div.fc-footer-buttons-container > div.fc-footer-buttons > button.fc-button.fc-cta-consent.fc-primary-button'))).click()

	# https://stackoverflow.com/questions/75552030/how-can-i-print-out-all-text-in-a-web-table-column-in-python-using-selenium
	table = driver.find_element(By.XPATH, '//*[@id="post-4130"]/div/div[2]/figure/table') # Data table
	rows = table.find_elements(by=By.TAG_NAME, value="tr")

	global weeks, chapters, dates
	weeks = []
	chapters = []
	dates = []

	tdfiller = timedelta(days=1000) # fill blank indexes with timedelta so that min func can work on list

	print(f'{Fore.CYAN}>> Scraping info...')

	# https://stackoverflow.com/questions/75552030/how-can-i-print-out-all-text-in-a-web-table-column-in-python-using-selenium
	for row in rows:
		columns = row.find_elements(by=By.TAG_NAME, value='td')
		
		for index, col in enumerate(columns):
			if index == 0:
				weeks.append(col.text)
			if index == 1:
				chapters.append(col.text)
			if index == 2:
				if col.text == '—': # End of year
					break
					prog(datetime.now().strftime('%Y')+1)
				elif re.search(r"[A-Z][a-z]* [0-9][0-9]?, [0-9][0-9][0-9][0-9]", col.text):
					dates.append(col.text)
				else:
					dates.append(tdfiller)

	print(f'{Fore.CYAN}>> Calculating...')
	dtlist = [datetime.strptime(x, '%B %d, %Y') if x != tdfiller else tdfiller for x in dates] # List comprehension of dates in datetime format

	timenow = datetime.strptime(currdt, '%B %d, %Y')
	dtdifflist = [x-timenow if x != tdfiller else tdfiller for x in dtlist] # list of datetime differences from time now
	# [print(f'nth: {x[0]} - value: {x[1]}') for x in enumerate(dtdifflist)] - checking list

	latest = max(n for n in dtdifflist if n.days<=0) # find the timedela for the latest released chapter
	global latestindex
	latestindex = dtdifflist.index(latest) # Index for latest chapter
	daysnext = min(n for n in dtdifflist if n.days>0) # find days until next chapter

	### Editing Vencord Settings File
	shutil.copy(vencordrpcfile, 'settings_backup.json') # Create backup of settings file

	f = open(vencordrpcfile,'r')
	fj = json.load(f)
	f.close()


	# Set image
	fj['plugins']['CustomRPC']['imageBig'] = f'https://i.imgur.com/Ev64NP6.gif'

	# Set Days until next chapter text
	fj['plugins']['CustomRPC']['details'] = f'{daysnext.days} days until Chapter {chapters[dtdifflist.index(daysnext)]}'

	

	## Set break/no break text

	# https://stackoverflow.com/questions/19216334/python-give-start-and-end-of-week-data-from-a-given-date

	## Check table for items surrounding current date

	# Get the start and end dates of this week
	# currentweekstart = dt - timedelta(days=dt.weekday())
	# currentweekend = dt + timedelta(days=dt.weekday())

	currentweekstart = dt - timedelta(days=dt.weekday())
	currentweekend = currentweekstart + timedelta(days=6)

	print(f'>> {datetime.strftime(currentweekstart, '%B %d, %Y')} to {datetime.strftime(currentweekend, '%B %d, %Y')}')

	for d in dates:
		if re.search(r'1000.*', str(d)): # If BREAK week			
			nextweekchapter = chapters[latestindex+2] # If break week, next chapter is 2 weeks from last released chapter
			pass
		else:
			if currentweekstart <= datetime.strptime(d, '%B %d, %Y') <= currentweekend: # If chapter lies in current week
				global thisweekindex
				thisweekindex = dates.index(d) # Index of item in table for this week
				lcws = datetime.strptime(dates[thisweekindex], '%B %d, %Y') # Latest chapter week start - changed to this week
				nextweekchapter = chapters[thisweekindex+1]


	if re.search(r'.* Break', nextweekchapter): # Search what is happening next week
		
		# We know next week is break, therefore:
		# If today is in latest chapter week - BREAK NEXT WEEK
		# Else - BREAK THIS WEEK
		
		
		# lcws = datetime.strptime(dates[latestindex], '%B %d, %Y') # Latest chapter week start
		weekstart = lcws - timedelta(days=dt.weekday()-1) # Start of week containing break
		weekend = weekstart + timedelta(days=6) # End of week containing next chapter

		# print(f'{Fore.YELLOW}1) {weekstart}\n2) {dt}\n3) {weekend}')

 		# Get current dt
 		# Find which week lies in current dt
 		# Get index

		if weekstart <= dt <= weekend: # If current date is in the week of the latest released chapter, then next chapter is break
			fj['plugins']['CustomRPC']['state'] = 'BREAK NEXT WEEK! 😢'
		else: # Date is not therefore this is a break week
			fj['plugins']['CustomRPC']['state'] = 'BREAK THIS WEEK! 😢'

		# Get current chapter (closest date before today)
		# Get next chapter date
		# Get week of current chapter
		# Get week of next chapter
		# If today lies in next week chapter week then break

	else:
		fj['plugins']['CustomRPC']['state'] = 'NO BREAK NEXT WEEK! 😃'

	# Set Read button to latest chapter
	fj['plugins']['CustomRPC']['buttonOneText'] = f'Read Ch. {chapters[dtdifflist.index(latest)]}'
	fj['plugins']['CustomRPC']['buttonOneURL'] = f'https://mangareader.to/read/one-piece-3/en/chapter-{chapters[dtdifflist.index(latest)]}'


	f = open(vencordrpcfile,'w')
	fjd = json.dump(fj, f, indent=4)
	f.close()

	driver.quit()

	# Finding latest folder - When Discord updates it creates a new folder
	appdatalocal = os.getenv('LOCALAPPDATA') # Get %APPDATA%/Local folder path
	subprocess.Popen(f'{appdatalocal}/Discord/Update.exe --processStart Discord.exe') # Open Discord
	
	debug()


try:
	prog(datetime.now().strftime('%Y'))
except chromedriver_outdated:
	print(f'{Fore.RED}>> Error. Outdated Chromedriver.\n{Fore.CYAN}>> Installing new Chromedriver...')
	chromedriver_autoinstaller.install() # Gets latest chromedriver and adds it to path
	print(f'{Fore.GREEN}>> Done.{Fore.CYAN}')