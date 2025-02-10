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

TABLE_ADDON_VERSION = "0.1.1"

class TableInterface(tk.Toplevel):
	
	def resizeWindow(self,x: int, y: int):
		self.geometry(f'{x}x{y}')
		self.minsize(x,y)
		self.maxsize(x,y)
	
	def __init__(self, comment: str):
		super().__init__()
		self.title(f"Database Viewer {comment}")
		self.resizeWindow(1080, 720)
		
		main_frame=tk.Frame(self)
		main_frame.pack(fill='both',expand=True)
		
		WindowContent(main_frame)


class WindowContent(tk.Frame):
	
	def __init__(self,main_frame):
		super().__init__(main_frame)
		
		self.table_frame=tk.LabelFrame(main_frame,text="Table",height=650,width=800)
		self.table_frame.pack_propagate(False)
		self.option_frame=tk.LabelFrame(main_frame,text="Options",height=250,width=150)
		self.option_frame.pack_propagate(False)

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
		selection=self.table_selector.get()
		query=f"SELECT * FROM {selection}"
		self.cursor.execute(query)
		rows=self.cursor.fetchall()
		self.tax_tree
		self.tax_tree.config(columns=(self.column_names[selection]))
		for i, col in enumerate(self.column_names[selection]):
			self.tax_tree.heading(i, text=col)

			# set the column width to the longest item in the column
			max_width = len(col) * 10  # start with the header width
			for row in rows:
				cell_value = str(row[i])
				cell_width = len(cell_value) * 8
				if cell_width > max_width:
					max_width = cell_width

			self.tax_tree.column(i, minwidth=0, width=max_width, stretch=False)


		self.tax_tree.delete(*self.tax_tree.get_children())
		for row in rows:
			self.tax_tree.insert("", tk.END, values=row)
	
	def tableView(self):

		tree_scroll_x = ttk.Scrollbar(self.table_frame, orient='horizontal')
		tree_scroll_y = ttk.Scrollbar(self.table_frame,orient='vertical')

		tree_scroll_x.pack(side='bottom',fill='x')
		tree_scroll_y.pack(side='left', fill='y')
		
		self.tax_tree = ttk.Treeview(self.table_frame, xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set,  show="headings",height=20)
		
		self.tax_tree.pack(side='top',fill='both',expand=True)


		tree_scroll_x.config(command=self.tax_tree.xview)
		tree_scroll_y.config(command=self.tax_tree.yview)

		self.updateTableView()	
		
	
	def optionsArea(self):
		tk.Label(self.option_frame,text="Choose Table").pack(side='top',fill='x')

		self.table_selector=tk.StringVar()
		self.table_selector.set("taxonomy")
		table_menu=tk.OptionMenu(self.option_frame, self.table_selector, *self.column_names.keys(), command=lambda event: self.updateTableView())
		table_menu.pack(side='top',fill='x',pady=10,padx=10)

		def switchSelection(selector, selection):
			selector.set(selection)
			self.updateTableView()

		# bind keyboard shortcuts for switching between selections
		self.option_frame.bind_all("<Command-Key-1>", lambda event: switchSelection(self.table_selector, "taxonomy"))
		self.option_frame.bind_all("<Command-Key-2>", lambda event: switchSelection(self.table_selector, "habitats"))
		self.option_frame.bind_all("<Command-Key-3>", lambda event: switchSelection(self.table_selector, "ids"))



if __name__ == "__main__":
	table_window=TableInterface("[only for testing]")
	table_window.focus_set()
	table_window.mainloop()

