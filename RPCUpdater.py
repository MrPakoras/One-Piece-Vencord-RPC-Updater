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
appdata = os.getenv('APPDATA') # %APPDATA%
vencordrpcfile = f'{appdata}/Vencord/settings/settings.json'

## Date
dt = datetime.now()
currdt = dt.strftime('%B %d, %Y')

def discord_process(option): # made it a function so its easier to debug
	# pass
	if option == 0:
		os.system("taskkill /im discord.exe /f") # Close Discord
	if option == 1:
		# Finding latest folder - When Discord updates it creates a new folder
		appdatalocal = os.getenv('LOCALAPPDATA') # Get %APPDATA%/Local folder path
		subprocess.Popen(f'{appdatalocal}/Discord/Update.exe --processStart Discord.exe') # Open Discord

discord_process(0) # close discord

def debug():
	n = 1
	for x in ['Last', 'Current', 'Next']:
		# debuginfo = f'{Fore.MAGENTA}>> {x} Chapter: {chapters[thisweekindex-n]}\n{Fore.YELLOW}- Date: {Fore.GREEN}{dates[thisweekindex-n]} - {weeks[thisweekindex-n]}'
		print(debuginfo)
		n -= 1

def get_week(date): # Gets the start and end dates of the week which date falls within
	date = datetime.strptime(date, '%B %d, %Y')
	weekstart = date - timedelta(days=date.weekday())
	weekend = weekstart + timedelta(days=6)

	print(f'>> {Fore.CYAN}{datetime.strftime(weekstart, '%B %d, %Y')} {Fore.YELLOW}to {Fore.CYAN}{datetime.strftime(weekend, '%B %d, %Y')}')

	week = (weekstart, weekend)
	return week


def prog(urldate):
	# PATH = 'W:/Python/Python Web Scraping/chromedriver.exe' # Chrome Driver path
	url = f"https://claystage.com/one-piece-chapter-release-schedule-for-{urldate}"
	print(f'{Fore.CYAN}>> Connecting...')

	options = wd.ChromeOptions()
	options.add_argument('--headless') # Run Chrome in headless mode (no browser)
	options.add_argument('window-size=1920x1080')
	options.add_argument('log-level=3')

	driver = wd.Chrome(options=options)
	driver.get(url) # Opens URL in browser

	# Search on page for the next date that a chapter will release

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
	


	dtdl_cleaned = [] # dtdifflist with break weeks replaced with "break" instead of "1000 days"
	# [dtdl_cleaned.append(re.sub(r'1000 days.*', 'Break', str(x))) for x in dtdifflist]
	for x in dtdifflist:
		if re.match(r'1000 days.*', str(x)):
			dtdl_cleaned.append('Break')
		else:
			dtdl_cleaned.append(x)

	

	# Finding the highest dt difference thats < 0 and the lowest dt diff thats >0 - current week lies within these values
	latest_chapter = max(n for n in dtdifflist if n.days<=0)
	next_chapter = min(n for n in dtdifflist if n.days>=0)
	
	latest_index = dtdifflist.index(latest_chapter)
	latest_date = dates[latest_index]
	next_date = dates[dtdifflist.index(next_chapter)]

	for x in dtdl_cleaned[latest_index+1:]: # dtdl list starting from latest chapter+1 (skip latest to get to next chapter)
		if x == 'Break':
			pass 
		else:
			next_chap_index = dtdl_cleaned.index(x)
			break

	[print(x) for x in dtdl_cleaned[latest_index:next_chap_index+1]] # Print dtdl from last chapter to next chapter (inclusive)

	next_chap_date = dates[next_chap_index] # get next event skipping "Break"
	print(f'Latest: {latest_date} | Next: {next_date}')

	currentweekstart = dt - timedelta(days=dt.weekday())
	currentweekend = currentweekstart + timedelta(days=6)

	# print(f'>> {datetime.strftime(currentweekstart, '%B %d, %Y')} to {datetime.strftime(currentweekend, '%B %d, %Y')}')

	latest_week = get_week(latest_date) # Week of latest chapter
	current_week = get_week(currdt) # Current week
	next_week = get_week(next_date) # Week of next event (chapter/break)
	next_chap_week = get_week(next_chap_date) # Week of next chapter

	latest = max(n for n in dtdifflist if n.days<=0) # find the timedela for the latest released chapter
	global latestindex
	latestindex = dtdifflist.index(latest) # Index for latest chapter
	daysnext = min(n for n in dtdifflist if n.days>0) # find days until next chapter

	### Editing Vencord Settings File
	shutil.copy(vencordrpcfile, 'settings_backup.json') # Create backup of settings file

	f = open(vencordrpcfile,'r')
	fj = json.load(f)
	f.close()


	## Set image
	fj['plugins']['CustomRPC']['imageBig'] = f'https://i.imgur.com/Ev64NP6.gif'

	## Set Days until next chapter text
	fj['plugins']['CustomRPC']['details'] = f'{daysnext.days} days until Chapter {chapters[dtdifflist.index(daysnext)]}'

	
	## Setting break text

	##################################################################################
	## NEEDS HANDLING FOR WHEN CURRENT WEEK IS CHAPTER WEEK, THEN CHECK WEEK AFTER ###
	##################################################################################

	if current_week == next_chap_week: # If the upcoming chapter is this week, check next event
		next_event = dtdl_cleaned[dtdifflist.index(next_chapter)+1]
		print(f'>> {Fore.CYAN}Next event: {Fore.MAGENTA}{chapters[dtdl_cleaned.index(next_event)]} {Fore.CYAN}in {Fore.YELLOW}{next_event}')
		if next_event == 'Break':
			status = 'BREAK NEXT WEEK! 😢' 
		else:
			status = 'NO BREAK NEXT WEEK! 😃'
	elif next_week == next_chap_date: # No break next week
		status = 'NO BREAK NEXT WEEK! 😃'
	elif current_week == latest_week and next_week != next_chap_week: # Break next week
		status = 'BREAK NEXT WEEK! 😢' 
	elif current_week != next_chap_week and current_week != latest_week: # Break this week
		status = 'BREAK THIS WEEK! 😢'
	else:
		status = 'IDK when tf the break is cuh.'
	
	# Set RPC status
	fj['plugins']['CustomRPC']['state'] = status
	print(status)


	# Set Read button to latest chapter
	fj['plugins']['CustomRPC']['buttonOneText'] = f'Read Ch. {chapters[dtdifflist.index(latest)]}'
	fj['plugins']['CustomRPC']['buttonOneURL'] = f'https://mangareader.to/read/one-piece-3/en/chapter-{chapters[dtdifflist.index(latest)]}'


	f = open(vencordrpcfile,'w')
	fjd = json.dump(fj, f, indent=4)
	f.close()

	driver.quit()

	discord_process(1) # Open Discord


try:
	prog(datetime.now().strftime('%Y'))
except chromedriver_outdated:
	print(f'{Fore.RED}>> Error. Outdated Chromedriver.\n{Fore.CYAN}>> Installing new Chromedriver...')
	chromedriver_autoinstaller.install() # Gets latest chromedriver and adds it to path
	print(f'{Fore.GREEN}>> Done.{Fore.CYAN}')