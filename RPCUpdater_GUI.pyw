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

from RPCUpdater.py import *

## Vencord settings file
defaultrpcpath = os.path.expandvars(f'%APPDATA%/Vencord/settings/settings.json') # Appdata/Roaming/ folder

master = CTk()
master.geometry("600x500")
set_default_color_theme('green')
rows = ['title', 'pathselect', 'fileselect', 'correction', 'message', 'run'] # Index of rows so I dont have to manually update each .grid

colourmain = '#8d73ff'
colourdark = '#3b2b7d'

## Title
title_label = CTkLabel(master, text='OP Vencord RPC Updater', font=('Calibri', 30), text_color=colourmain)
title_label.grid(row=rows.index('title'), column=0)

## Default path selection
pathselect_frame = CTkFrame(master)
pathselect_frame.grid(row=rows.index('pathselect'),column=0,padx=10,pady=10)

path_label = CTkLabel(pathselect_frame, text='Choose your settings.json file path location', font=('Calibri', 20), text_color=colourmain, justify='center')
path_label.grid(row=0, column=0)

def setpath():
	if pathvar.get() == 0:
		vencordrpcfile = defaultrpcpath
		openfolder_button.configure(state='disabled')
	if pathvar.get() == 1:
		openfolder_button.configure(state='normal')

pathvar = IntVar(value=0)

radio_frame = CTkFrame(pathselect_frame) # frame for radio buttons
radio_frame.grid(row=2, column=0)

default_select = CTkRadioButton(radio_frame, text=f'Use Default Path', command=setpath, variable=pathvar, value=0, fg_color=colourmain, border_color=colourmain, hover_color=colourdark)#, border_width_unchecked=2, border_width_checked=3)
default_select.grid(row=0, column=0, padx=10)

custom_select = CTkRadioButton(radio_frame, text=f'Set Custom Path', command=setpath, variable=pathvar, value=1, fg_color=colourmain, border_color=colourmain, hover_color=colourdark)#, border_width_unchecked=2, border_width_checked=3)
custom_select.grid(row=0, column=1, padx=10)

## File select
file_frame = CTkFrame(master)
file_frame.grid(row=rows.index('fileselect'),column=0,padx=10,pady=10)
file_frame.columnconfigure(0, weight=5)
file_frame.columnconfigure(1, weight=1)
file_frame.pack_propagate(0)

file_label = CTkLabel(file_frame, text='Choose settings.json', width=400, anchor='w', wraplength=0)
file_label.grid(row=0,column=0,padx=10)

def openfile():
	global jsonfilepath
	jsonfilepath = filedialog.askopenfilename(initialdir = "./", title = "Select a File", filetypes=[("JSON File", "*.json")])
	file_label.configure(text=jsonfilepath)

	vencordrpcfile = jsonfilepath

	run_button.configure(state='normal')

openfolder_button = CTkButton(file_frame, text='Open File', command=openfile, fg_color=colourmain, hover_color=colourdark, text_color='white', text_color_disabled='black', state='disabled')
openfolder_button.grid(row=0,column=1)

## Date Correction
correction_frame = CTkFrame(master)
correction_frame.grid(row=rows.index('correction'),column=0,padx=10,pady=10)

# Insert todays date for chapter release
today_label = CTkLabel(correction_frame, text='Was a chapter released today?')
today_label.grid(row=0, column=0, padx=10)

today_check = CTkCheckBox(correction_frame, text='')
today_check.grid(row=0, column=1)

today_label = CTkLabel(correction_frame, text='Break next week?')
today_label.grid(row=0, column=3)

break_check = CTkCheckBox(correction_frame, text='')
break_check.grid(row=0, column=4, padx=10)

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