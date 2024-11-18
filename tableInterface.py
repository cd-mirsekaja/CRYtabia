#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 12:58:07 2024

@author: Ronja Rösner
"""

 
#import tkinter for managing GUI
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter.filedialog import asksaveasfilename
import os

from getInfo import SearchGBIF,internetConnection

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

TABLE_ADDON_VERSION = "0.1.0"

class MapInterface(tk.Toplevel):
	
	def resizeWindow(self,x: int, y: int):
		self.geometry(f'{x}x{y}')
		self.minsize(x,y)
		self.maxsize(x,y)
	
	def __init__(self, comment: str):
		super().__init__()
		self.title(f"Table Editor {comment}")
		self.resizeWindow(1000, 600)
		
		main_frame=tk.Frame(self)
		main_frame.pack(fill='both',expand=True)
		
		WindowContent(main_frame)


class WindowContent(tk.Frame):
	
	def __init__(self,main_frame):
		super().__init__(main_frame)
		
		self.table_frame=tk.LabelFrame(main_frame,text="Table",height=512,width=512)
		self.option_frame=tk.LabelFrame(main_frame,text="Options")
		
		self.table_frame.grid(column=1,row=1,sticky='enw',padx=25,pady=25)
		self.option_frame.grid(column=2,row=1,sticky='wne',padx=25,pady=25)

if __name__ == "__main__":
	map_window=MapInterface("[only for testing]")
	map_window.focus_set()
	map_window.mainloop()

