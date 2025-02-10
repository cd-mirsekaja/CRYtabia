#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 15:33:09 2024

@author: Ronja Rösner
"""

#import tkinter for managing GUI
import tkinter as tk
from tkinter import ttk
#import image libraries for rendering images inside the GUI
from PIL import Image, ImageTk
from datetime import datetime
from tkinter.filedialog import asksaveasfilename
import os

from getInfo import SearchGBIF,internetConnection

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

MAP_ADDON_VERSION = "0.3.0"

class MapInterface(tk.Toplevel):
	
	def resizeWindow(self,x: int, y: int):
		self.geometry(f'{x}x{y}')
		self.minsize(x,y)
		self.maxsize(x,y)
	
	def __init__(self, selection: str, comment: str):
		super().__init__()
		self.title(f"Occurence Map Editor {comment}")
		self.resizeWindow(1000, 600)
		
		self.main_frame=tk.Frame(self)
		self.main_frame.pack(fill='both',expand=True)
		self.main_frame.columnconfigure(1, weight=1)
		self.main_frame.columnconfigure(2, weight=1)
		
		WindowContent(self.main_frame,selection)
		

class WindowContent(tk.Frame):
	
	def __init__(self,main_frame,selection):
		super().__init__(main_frame)
		
		self.selection=selection
		self.year_input=None
		
		self.map_frame=tk.LabelFrame(main_frame,text="",height=512,width=512)
		self.option_frame=tk.LabelFrame(main_frame,text="Options")
		
		self.map_frame.grid(column=1,row=1,sticky='enw',padx=25,pady=25)
		self.option_frame.grid(column=2,row=1,sticky='wne',padx=25,pady=25)
		
		self.map_render=tk.Label(self.map_frame)
		self.background_image=Image.open(SCRIPT_DIR+"/images/transparent_background.png")
		self.map_image=ImageTk.PhotoImage(self.background_image)
		
		self.getOptions()
		self.generateMap()
		
	
	
	def generateMap(self):
		if internetConnection():
			search_map=SearchGBIF(self.name_input.get(),self.selection)
			self.map_path=search_map.makeMap(style=self.style_selector.get(),bin=self.aggregation_selector.get(),year=self.year_input)
			
			if self.map_path!="":
				# set parameteres of text and map fields, set name of map label
				self.map_frame.config(text=f"Occurrence Map for {self.name_input.get()}:")
				
				if "!labelframe.!label" in self.map_frame.winfo_children():
					self.map_render.destroy()
				
				# save png of occurrence map to variable
				occurrence_map=Image.open(self.map_path)
				# save png of world map to variable
				world_map=Image.open(SCRIPT_DIR+"/images/world_map_512.png")
				# overlay the world map with the occurrence map
				world_map.paste(occurrence_map, (-12,60), mask=occurrence_map)
				
				self.export_map=world_map
				
				# set the overlayed image to be rendered in window
				self.map_image.paste(world_map)
				self.map_render.config(image=self.map_image)
				
				self.map_render.pack()
				occurrence_map.close()
				
			else:
				# insert error message
				pass
	
	def getOptions(self):
		
		def clicked(event=None):
			if year_onoff.get()==0:	
				self.year_input=None
			else:
				self.year_input=self.year_selection.get()
			
			self.generateMap()
		
		def saveImage():
			FILE_TYPES=[("Image 1","*.png"),("Image 2","*.jpeg")]
			savepath=asksaveasfilename(filetypes=FILE_TYPES,defaultextension=FILE_TYPES,initialfile=f"{self.name_input.get()}")
			print(savepath)
			
			if not savepath:
				return
			
			
			self.export_map.save(savepath)
			
			
		
		tk.Label(self.option_frame,text="Input Taxon")
		# field to input new species
		self.name_input=tk.Entry(self.option_frame,width=25)
		self.name_input.insert(0, self.selection)
		
		ttk.Separator(self.option_frame,orient='horizontal')
		
		tk.Label(self.option_frame,text="Choose Map Style")
		# options menu for choosing the map style
		style_list=[
			"classic.point",
			"classic.poly",
			"classic-noborder.poly",
			"purpleYellow.point",
			"purpleYellow.poly",
			"purpleYellow-noborder.poly",
			#"green.point",# nope
			"green.poly",
			#"green-noborder.poly",# nope
			"purpleHeat.point",
			"blueHeat.point",
			"orangeHeat.point",
			"greenHeat.point",
			"fire.point",
			"glacier.point",
			"green2.poly",
			#"green2-noborder.poly",# nope
			"iNaturalist.poly",
			"purpleWhite.poly",
			"red.poly",
			"blue.marker",
			"orange.marker",
			"outline.poly",
			#"scaled.circles"# nope
			]
		self.style_selector=tk.StringVar()
		self.style_selector.set(style_list[5])
		tk.OptionMenu(self.option_frame, self.style_selector, *(style_list))
		
		
		tk.Label(self.option_frame,text="Choose count aggregation")
		aggregation_list=["hex","square",]
		self.aggregation_selector=tk.StringVar()
		self.aggregation_selector.set(aggregation_list[0])
		
		tk.Radiobutton(self.option_frame,text=aggregation_list[0],variable=self.aggregation_selector,value=aggregation_list[0])
		tk.Radiobutton(self.option_frame,text=aggregation_list[1],variable=self.aggregation_selector,value=aggregation_list[1])
		
		year_onoff=tk.IntVar()
		tk.Checkbutton(self.option_frame,text="Input year?",variable=year_onoff,onvalue=1,offvalue=0)
		
		current_year=datetime.now().year
		self.year_selection=tk.IntVar()
		self.year_selection.set(current_year)
		
		ttk.LabeledScale(self.option_frame,variable=self.year_selection,from_=1800,to=current_year)
		
		ttk.Button(self.option_frame,text="Update Map",command=lambda: clicked())
		
		ttk.Separator(self.option_frame,orient='horizontal')
		
		ttk.Button(self.option_frame,text="Save Map as Image", command=lambda: saveImage())
		
		
		self.option_frame.columnconfigure(0, weight=1)
		
		widget_index=0
		for widget in self.option_frame.winfo_children():

			if "!labelframe2.!radiobutton" in str(widget) or "!labelframe2.!checkbutton" in str(widget):
				widget.grid(column=0,row=widget_index,padx=10,pady=5,sticky='wn')
				widget_index=widget_index+1
			elif "!labelframe2.!labeledscale" in str(widget):
				widget.grid(column=0,row=widget_index,padx=30,pady=0,sticky='wne')
				widget_index=widget_index+1
			elif "!labelframe2.!button" in str(widget):
				widget.grid(column=0,row=widget_index,padx=10,pady=5,sticky='wne')
				widget_index=widget_index+1
			elif "!labelframe2.!label" in str(widget):
				widget.grid(column=0,row=widget_index,padx=10,pady=0,sticky='ws')
				widget_index=widget_index+1
			elif "!labelframe2.!separator" in str(widget):
				widget.grid(column=0,row=widget_index,padx=5,pady=5,sticky='wne')
				widget_index=widget_index+1
			else:
				widget.grid(column=0,row=widget_index,padx=10,pady=5,sticky='wne')
				widget_index=widget_index+1

		# make it so the input can be cofirmed by pressing return
		self.option_frame.bind_all("<Return>",lambda x: clicked())


if __name__ == "__main__":
	map_window=MapInterface("Calidris alpina","[only for testing]")
	map_window.focus_set()
	map_window.mainloop()
