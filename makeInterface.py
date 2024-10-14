#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 15:26:31 2024

@author: Ronja Rösner

This module constructs the interface for CRYtabia
"""

#import tkinter for managing GUI
import tkinter as tk
from tkinter import ttk
#import image libraries for rendering images inside the GUI
from PIL import Image, ImageTk

import getInfo
from complexMap import MapInterface

class MainInterface(tk.Tk):
	
	def resizeWindow(self,x: int, y: int):
		self.geometry(f'{x}x{y}')
		self.minsize(x,y)
		self.maxsize(x,y)
	
	def __init__(self,app_title: str, app_version: str):
		super().__init__()
		self.title(f'{app_title} {app_version}')
		self.resizeWindow(1510, 920)
		
		self.main_frame=tk.Frame(self)
		self.main_frame.pack(fill='both',expand=True)
		
		WindowContent(self.main_frame)


class WindowContent(tk.Frame):
	
	def __init__(self,main_frame):
		super().__init__(main_frame)
		
		# option frame (top)
		self.option_frame=tk.LabelFrame(main_frame, text='Options',border=2,relief='solid',font='Helvetica 14 bold')
		self.option_frame.pack(side='top',ipadx=20,ipady=20,padx=20,pady=20,fill='x')
		self.option_frame.columnconfigure(0,weight=1)
		self.option_frame.columnconfigure(1,weight=1)
		self.option_frame.columnconfigure(2,weight=1)
		#self.option_frame.rowconfigure(1,minsize=50)
		#self.option_frame.rowconfigure(2,minsize=50)
		
		self.inputselect_frame=tk.LabelFrame(self.option_frame,text="Search Library by",font="Arial 14",border=0)
		self.input_frame=tk.LabelFrame(self.option_frame,text="",relief='solid',border=1)
		self.button_frame=tk.Frame(self.input_frame,relief='solid',border=0)
		self.extraoptions_frame=tk.LabelFrame(self.option_frame,text="Additional Options",border=0)
		
		self.inputselect_frame.grid(column=0,row=1,padx=50,pady=20,rowspan=2,sticky='enw')
		self.input_frame.grid(column=1,row=1,padx=30,pady=20,sticky='enw')
		self.button_frame.grid(column=1,row=2,padx=30,pady=20,sticky='enw')
		self.extraoptions_frame.grid(column=2,row=1,padx=50,pady=20,rowspan=2,sticky='enw')
		
		# output frame (bottom)
		self.output_frame=tk.LabelFrame(main_frame, text='Requested Information will show up below',border=0,relief='solid',font='Helvetica 14 bold')
		self.output_frame.pack(side='bottom',padx=20,pady=20,fill='x')
		
		self.optionsArea()
		self.textArea()
	
	def optionsArea(self):
		
		def getUserInput(selection):
			
			# input field for text
			text_input=tk.Entry(self.input_frame,width=40,border=2,relief="sunken")
			text_input.grid(row=1,column=1,sticky='enw',pady=20,padx=20)
			self.input_frame.columnconfigure(1, weight=1)
			
			return text_input
		
		def buttonRow(gbif_onoff,wiki_onoff,simplemap_onoff,complexmap_onoff,selector,user_input):
			
			def clearText():
				self.text_field.config(state="normal")
				self.text_field.delete(1.0,tk.END)
				self.text_field.config(state="disabled")
				user_input.delete(0,tk.END)
				self.output_frame.config(text='Requested Information will show up below')
			
			# function for resetting all inputs and fields
			def reset():
				clearText()
				gbif_onoff.set(0)
				wiki_onoff.set(0)
				simplemap_onoff.set(0)
				complexmap_onoff.set(0)
				selector.set("Genome Index")
				self.input_frame.config(text="Input Genome Index")
				self.text_field.config(width=250,height=40)
				#self.map_field.config(width=0,height=0,border=0,relief="flat")
				#self.map_label.config(text="")
				#self.map_image.paste(self.background_image)
				#self.render_map.config(image="")
			
			def confirm():
				gbif_state=gbif_onoff.get()
				wiki_state=wiki_onoff.get()
				#simplemap_state=simplemap_onoff.get()
				text=getInfo.getText(selector, user_input, gbif_state, wiki_state)
				
				self.output_frame.config(text=f"Information for {selector.get()} {user_input.get()}")
				self.text_field.config(state="normal")
				self.text_field.insert(1.0,''.join(text))
				self.text_field.config(state="disabled")
			
			
			ttk.Separator(self.button_frame,orient='horizontal').pack(side='top',pady=10,fill='x',expand=1)
			ttk.Button(self.button_frame,text='Confirm',command=lambda: confirm()).pack(side='top',padx=5,fill='x',expand=1)
			ttk.Button(self.button_frame,text='Clear',command=lambda: clearText()).pack(side='left',padx=5,fill='x',expand=1)
			ttk.Button(self.button_frame,text='Reset',command=lambda: reset()).pack(side='right',padx=5,fill='x',expand=1)
			
			# make it so the input can be cofirmed by pressing return
			self.button_frame.bind_all("<Return>",lambda x: confirm())
			# make it so that the content can be cleared by pressing escape
			self.button_frame.bind_all("<Escape>",lambda x: reset())
			# make it so that all text is cleared by pressing command and backspace
			self.button_frame.bind_all("<Command-Key-BackSpace>",lambda x: clearText())
			
			
		
		# function for choosing the input method and getting the user input
		def chooseInputMethod():
			
			# set variable for storing the radiobutton selection
			selector=tk.StringVar()
			selector.set("Genome Index")
			
			# set label for above the input box
			self.input_frame.config(text=f"Input {selector.get()}",font="Arial 14")
			
			# function for when selection changes
			def clicked(event):
				if selector.get()=="Genome Index":
					self.input_frame.config(text="Input Genome Index (0-379)")
				else:
					self.input_frame.config(text=f"Input {selector.get()}")
			
			
			options_list=["Accession Number", "Genome Index", "Scientific Name", "Taxon Group"]
			options_menu=tk.OptionMenu(self.inputselect_frame, selector, *(options_list), command=clicked)
			options_menu.pack(side='top',expand=0,fill='x',padx=10,pady=10)
			
			
			# function for binding keyboard shortcuts
			def select_option(selector: tk.StringVar, selection: str, event=None):
				selector.set(selection)
				clicked(event)

			# bind keyboard shortcuts for switching between selections
			self.inputselect_frame.bind_all("<Command-Key-1>", lambda event: select_option(selector, "Accession Number"))
			self.inputselect_frame.bind_all("<Command-Key-2>", lambda event: select_option(selector, "Genome Index"))
			self.inputselect_frame.bind_all("<Command-Key-3>", lambda event: select_option(selector, "Scientific Name"))
			self.inputselect_frame.bind_all("<Command-Key-4>", lambda event: select_option(selector, "Taxon Group"))
			
			return selector
		
		def buttonColumn(user_input, selection):
			from tkinter.filedialog import asksaveasfilename
			
			def saveOutput():
				FILE_TYPES=[("Simple Text Files","*.txt"),("Complex Text Files","*.rtf")]
				filepath=asksaveasfilename(filetypes=FILE_TYPES)
				
				if not filepath:
					return
				
				with open(filepath,"w") as file:
					content=self.text_field.get(1.0,tk.END)
					file.write(content)
			
			def editMap(user_input, selection):
				if getInfo.internetConnection():
					if user_input.get()!="":
						sci_name=getInfo.getSciName(user_input, selection)
						MapInterface(sci_name)
					else:
						self.text_field.config(state="normal")
						self.text_field.insert(1.0,"\nPlease enter something.\n\n-------------------------------------------------------------\n")
						self.text_field.config(state="disabled")
				else:
					self.text_field.config(state="normal")
					self.text_field.insert(1.0,"\nNo Internet Connection available, map creation not possible.\n\n-------------------------------------------------------------\n")
					self.text_field.config(state="disabled")
				
			ttk.Button(self.inputselect_frame,text="Open Map Editor (WIP)",command=lambda: editMap(user_input, selection))
			ttk.Button(self.inputselect_frame,text="Open Table Editor (WIP)")
			ttk.Button(self.inputselect_frame,text="Save Output to File",command=lambda: saveOutput())
			
			for widget in self.inputselect_frame.winfo_children():
				if '!labelframe.!button' in str(widget):
					widget.pack(side='top',expand=0,fill='x',padx=10,pady=5)
		
		#function for the checkbuttons in the Options column
		def chooseOptions():
			
			# checkbox for enabling GBIF search
			gbif_onoff=tk.IntVar()
			enable_gbif=tk.Checkbutton(self.extraoptions_frame,text='Search GBIF Backbone*',variable=gbif_onoff, onvalue=1, offvalue=0)
			enable_gbif.grid(row=1,column=3,padx=20,sticky="nw")
			
			# checkbox for enabling Wikipedia search
			wiki_onoff=tk.IntVar()
			enable_wiki=tk.Checkbutton(self.extraoptions_frame,text='Get Wikipedia summary*',variable=wiki_onoff, onvalue=1, offvalue=0)
			enable_wiki.grid(row=2,column=3,padx=20,sticky="nw")
			
			# checkbox for enabling simple map generation
			simplemap_onoff=tk.IntVar()
			enable_simplemap=tk.Checkbutton(self.extraoptions_frame,text="Generate simple map (nonfunctional)*",variable=simplemap_onoff, onvalue=1, offvalue=0)
			enable_simplemap.grid(row=3,column=3,padx=20,sticky="nw")
			
			# checkbox for enabling complex map generation
			complexmap_onoff=tk.IntVar()
			enable_complexmap=tk.Checkbutton(self.extraoptions_frame,text="Generate complex map (nonfunctional)*",variable=complexmap_onoff, onvalue=1, offvalue=0)
			enable_complexmap.grid(row=4,column=3,padx=20,sticky="nw")
			
			# subtitle of column
			tk.Label(self.extraoptions_frame,text="*requires internet access",font="Arial 12").grid(row=5,column=3,padx=20,sticky="nw")
			
			# function for switching the checkbuttons on or of with hotkeys
			def switchState(stateswitch: tk.IntVar, event=None):
				if stateswitch.get()==1:
					stateswitch.set(0)
				elif stateswitch.get()==0:
					stateswitch.set(1)
			
			# keybindings for checkbutton-switching
			self.extraoptions_frame.bind_all("<Command-Key-j>", lambda event: switchState(gbif_onoff, event))
			self.extraoptions_frame.bind_all("<Command-Key-k>", lambda event: switchState(wiki_onoff, event))
			self.extraoptions_frame.bind_all("<Command-Key-l>", lambda event: switchState(simplemap_onoff, event))
			self.extraoptions_frame.bind_all("<Command-Key-p>", lambda event: switchState(complexmap_onoff, event))
			
			
			return gbif_onoff,wiki_onoff,simplemap_onoff,complexmap_onoff
		
		
		selector=chooseInputMethod()
		user_input=getUserInput(selector)
		gbif_onoff,wiki_onoff,simplemap_onoff,complexmap_onoff=chooseOptions()
		buttonRow(gbif_onoff,wiki_onoff,simplemap_onoff,complexmap_onoff,selector,user_input)
		buttonColumn(user_input,selector)
	
	def textArea(self):
		self.text_field=tk.Text(self.output_frame,width=250,height=40,state="disabled",border=2,relief="solid",font="Arial 13",cursor="cross")
		self.text_field.pack(side='left')



if __name__ == "__main__":
	main_window=MainInterface('CRYtabia','[only for testing]')
	main_window.focus_set()
	main_window.mainloop()
