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
import os

from getInfo import SearchGBIF,internetConnection

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class MapInterface(tk.Tk):
	
	def resizeWindow(self,x: int, y: int):
		self.geometry(f'{x}x{y}')
		self.minsize(x,y)
		self.maxsize(x,y)
	
	def __init__(self, selection: str):
		super().__init__()
		self.title(f"Edit Map for - {selection} -")
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
			search_map=SearchGBIF(self.selection)
			map_path=search_map.makeMap(style=self.style_selector.get())
			
			if map_path!="":
				# set parameteres of text and map fields, set name of map label
				#self.map_field.config(width=150,height=40,padx=20,border=2,relief="solid")
				self.map_frame.config(text=f"Occurrence Map for {self.selection}:")
				
				if "!labelframe.!label" in self.map_frame.winfo_children():
					self.map_render.destroy()
				
				# save png of occurrence map to variable
				occurrence_map=Image.open(map_path)
				# save png of world map to variable
				world_map=Image.open(SCRIPT_DIR+"/images/world_map.png")
				# overlay the world map with the occurrence map
				world_map.paste(occurrence_map, (-12,60), mask=occurrence_map)
				
				# set the overlayed image to be rendered in window
				self.map_image.paste(world_map)
				self.map_render.config(image=self.map_image)
				
				self.map_render.pack()
				occurrence_map.close()
				world_map.close()
				
			else:
				# insert error message
				pass
	
	def getOptions(self):
		
		def clicked(event):
			self.generateMap()
		
		# field to input new species
		input_field=tk.Entry(self.option_frame,width=25)
		# button for confirming the new selection
		ttk.Button(self.option_frame,text="Confirm (WIP)")
		
		ttk.Separator(self.option_frame,orient='horizontal')
		
		# options menu for choosing the map style
		style_list=[
			"classic.point",
			"classic.poly",
			"classic-noborder.poly",
			"purpleYellow.point",
			"purpleYellow.poly",
			"purpleYellow-noborder.poly",
			#"green.point",#nope
			"green.poly",
			#"green-noborder.poly",#nope
			"purpleHeat.point",
			"blueHeat.point",
			"orangeHeat.point",
			"greenHeat.point",
			"fire.point",
			"glacier.point",
			"green2.poly",
			#"green2-noborder.poly",#nope
			"iNaturalist.poly",
			"purpleWhite.poly",
			"red.poly",
			"blue.marker",
			"orange.marker",
			"outline.poly",
			#"scaled.circles"#nope
			]
		self.style_selector=tk.StringVar()
		self.style_selector.set(style_list[5])
		tk.OptionMenu(self.option_frame, self.style_selector, *(style_list),command=clicked)
		
		
		
		for widget in self.option_frame.winfo_children():
			widget.pack(padx=10,pady=5,fill='x',expand=1)
			


if __name__ == "__main__":
	map_window=MapInterface("Calidris alpina")
	map_window.focus_set()
	map_window.mainloop()
