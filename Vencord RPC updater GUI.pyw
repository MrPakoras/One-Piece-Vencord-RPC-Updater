# Gets next OP chapter number and break status from https://claystage.com/one-piece-chapter-release-schedule-for-2023
# Changes discord RPC text to info from above

import re, json, shutil, os, subprocess, chromedriver_autoinstaller, threading
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
from customtkinter import *
from customtkinter import filedialog

## Vencord settings file
vencordrpcfile = 'C:/Users/Administrator/AppData/Roaming/Vencord/settings/settings.json'

os.system("taskkill /im discord.exe /f") # Close Discord

def debug():
	n = 1
	for x in ['Last', 'Current', 'Next']:
		debuginfo = f'>> {x} Chapter: {chapters[thisweekindex-n]}\n- Date: {dates[thisweekindex-n]} - {weeks[thisweekindex-n]}\n'
		message_label.insert(END, debuginfo)
		n -= 1
	message_label.insert(END, f'Done.\n')

def prog(urldate):
	# PATH = 'W:/Python/Python Web Scraping/chromedriver.exe' # Chrome Driver path
	url = f"https://claystage.com/one-piece-chapter-release-schedule-for-{urldate}"
	message_label.insert(END, f'>> Connecting...\n')

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
	message_label.insert(END, currdt+'\n')

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

	message_label.insert(END, f'>> Scraping info...\n')

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

	message_label.insert(END, f'>> Calculating...\n')
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

	# Set Days until next chapter text
	fj['plugins']['CustomRPC']['details'] = f'{daysnext.days} days until Chapter {chapters[dtdifflist.index(daysnext)]}'

	

	## Set break/no break text

	# https://stackoverflow.com/questions/19216334/python-give-start-and-end-of-week-data-from-a-given-date

	## Check table for items surrounding current date

	# Get the start and end dates of this week
	currentweekstart = dt - timedelta(days=dt.weekday())
	currentweekend = dt + timedelta(days=dt.weekday())
	message_label.insert(END, f'>> {currentweekstart} to {currentweekend}\n')

	for d in dates:
		if re.search(r'1000.*', str(d)): # If BREAK week
			continue
		else:
			if currentweekstart <= datetime.strptime(d, '%B %d, %Y') <= currentweekend: # If chapter lies in current week
				global thisweekindex
				thisweekindex = dates.index(d) # Index of item in table for this week
				lcws = datetime.strptime(dates[thisweekindex], '%B %d, %Y') # Latest chapter week start - changed to this week

	nextweekchapter = chapters[thisweekindex+1]
	if re.search(r'.* Break', nextweekchapter):
		
		# We know next week is break, therefore:
		# If today is in latest chapter week - BREAK NEXT WEEK
		# Else - BREAK THIS WEEK
		
		
		# lcws = datetime.strptime(dates[latestindex], '%B %d, %Y') # Latest chapter week start
		weekstart = lcws - timedelta(days=dt.weekday()-1) # Start of week containing break
		weekend = weekstart + timedelta(days=6) # End of week containing next chapter

		# print(f'1) {weekstart}\n2) {dt}\n3) {weekend}')

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
	
	if openvar.get() == 1:
		subprocess.Popen(f'{appdatalocal}/Discord/Update.exe --processStart Discord.exe') # Open Discord
	
	debug()




def run():
	try:
		prog(datetime.now().strftime('%Y'))
	except chromedriver_outdated:

		message_label.insert(END, f'>> Error. Outdated Chromedriver.\n>> Installing new Chromedriver...\n')
		chromedriver_autoinstaller.install() # Gets latest chromedriver and adds it to path

		message_label.insert(END, f'>> Done.\n')




def openfile():
	global jsonfilepath
	jsonfilepath = filedialog.askopenfilename(initialdir = "./", title = "Select a File", filetypes=[("JSON File", "*.json")])
	file_label.configure(text=jsonfilepath)

	vencordrpcfile = jsonfilepath

	run_button.configure(state='normal')


###########
### GUI ###
###########


master = CTk()
master.geometry("600x400")
set_default_color_theme('green')
rows = ['title', 'fileselect', 'message', 'run'] # Index of rows so I dont have to manually update each .grid

colourmain = '#8d73ff'
colourdark = '#3b2b7d'

## Title
title_label = CTkLabel(master, text='OP Vencord RPC Updater', font=('Calibri', 30), text_color=colourmain)
title_label.grid(row=rows.index('title'), column=0)

## File select
file_frame = CTkFrame(master)
file_frame.grid(row=rows.index('fileselect'),column=0,padx=10,pady=10)
file_frame.pack_propagate(0)

file_label = CTkLabel(file_frame, text='Choose settings.json', width=400, anchor='w', wraplength=0)
file_label.grid(row=0,column=0,padx=10)

openfolder_button = CTkButton(file_frame, text='Open File', command=openfile, fg_color=colourmain, hover_color=colourdark, text_color='black')
openfolder_button.grid(row=0,column=1)

## Messages
message_frame = CTkFrame(master, width=550)
message_frame.grid(row=rows.index('message'),column=0)
message_frame.pack_propagate(0)

message_label = CTkTextbox(message_frame, width=550, text_color=colourmain)
message_label.grid(row=rows.index('message'), column=0)

## Run button
run_frame = CTkFrame(master)
run_frame.grid(row=rows.index('run'),column=0, pady=10)

run_button = CTkButton(run_frame, text='Update Vencord', command=lambda:threading.Thread(target=run).start(), fg_color=colourmain, hover_color=colourdark, text_color='black', state='disabled', text_color_disabled=colourdark)
run_button.grid(row=0,column=0, padx=30)

# Open Discord toggle
openvar = IntVar(value=0)
open_switch = CTkSwitch(run_frame, text='Open Discord when done.', variable=openvar, onvalue=1, offvalue=0, progress_color=colourmain)
open_switch.grid(row=0,column=1)

master.mainloop()