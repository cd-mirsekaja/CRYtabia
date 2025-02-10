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
import os, sqlite3

from getInfo import SearchGBIF,internetConnection

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

TABLE_ADDON_VERSION = "0.1.0"

class TableInterface(tk.Toplevel):
	
	def resizeWindow(self,x: int, y: int):
		self.geometry(f'{x}x{y}')
		self.minsize(x,y)
		#self.maxsize(x,y)
	
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
		
		self.option_frame.grid(column=1,row=1,sticky='wne',padx=25,pady=25)
		self.table_frame.grid(column=2,row=1,sticky='enw',padx=25,pady=25)

		db_conn = sqlite3.connect(os.path.join(SCRIPT_DIR, "data/genotree_master_library.db"))
		self.cursor = db_conn.cursor()

		self.column_names = {
			"taxonomy": ("IDX","Kingdom","Phylum","Class","Order","Family","Genus","Species","Subspecies","ScientificName","Authority","Vernacular_Eng","Vernacular_Ger","taxGroup"),
			"habitats": ("IDX","isMarine","isBrackish","isFresh","isTerrestrial","isAllWater","isMarineFresh"),
			"ids": ("IDX","AccessionNumber","usageKey","IRMNG_ID","TSN","AphiaID","GUID_PESI","LSID_WORMS","TaxonID","Projects","SeqType")
		}

		self.optionsArea()
		self.tableView()

	def updateTableView(self):
		query="SELECT * FROM taxonomy"
		self.cursor.execute(query)
		rows=self.cursor.fetchall()
		for row in rows:
			self.tax_tree.insert("", tk.END, values=row)
	
	def tableView(self):
		
		tree_scroll_x = ttk.Scrollbar(self.table_frame, orient="horizontal")
		tree_scroll_x.pack(side='bottom',fill='x')
		tree_scroll_y = ttk.Scrollbar(self.table_frame,orient='vertical')
		tree_scroll_y.pack(side="left", fill="y")

		self.tax_tree = ttk.Treeview(self.table_frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set, columns=(self.column_names["taxonomy"]), show="headings",height=20)

		for i, col in enumerate(self.column_names["taxonomy"]):
			self.tax_tree.heading(i, text=col)
		
		self.tax_tree.pack(fill='both')
		tree_scroll_x.config(command=self.tax_tree.xview)
		tree_scroll_y.config(command=self.tax_tree.yview)

		self.updateTableView()	
		
	
	def optionsArea(self):
		tk.Label(self.option_frame,text="Choose Table").pack()

		self.table_selector=tk.StringVar()
		tk.OptionMenu(self.option_frame, self.table_selector, *self.column_names.keys()).pack()
		



		

if __name__ == "__main__":
	map_window=MapInterface("[only for testing]")
	map_window.focus_set()
	map_window.mainloop()

