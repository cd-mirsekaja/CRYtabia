#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:45:33 2024

@author: Ronja Roesner

Program for getting info on a given species from the included reference table.
Now includes internet (GBIF) search and map making.
Comments are always above the commented line.

"""


#import tkinter for managing GUI
import tkinter as tk
#import image libraries for rendering images inside the GUI
from PIL import Image, ImageTk
# import library for accessing the os
import os
# import library for internet connections
import requests

# get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# class for searching the input table
class SearchLibrary:
	
	def __init__(self,query,selection):
		# import required packages
		import pandas as pd
		import os
		
		# set reference table
		INPUT_TABLE = os.path.join(SCRIPT_DIR, "infolib.xlsx")
		# get specific columns containing either taxonomic info or habitat info from reference table
		self.TAXO_LIBRARY = pd.read_excel(INPUT_TABLE,usecols="A:O")
		
		self.HABITAT_LIBRARY = pd.read_excel(INPUT_TABLE,usecols="A,B,K,P:S")
		
		self.query=query
		self.selection=selection
	
	# function for checking whether the query is available in the table or not
	def inTable(self):
		table=self.TAXO_LIBRARY
		
		if self.selection=="Accession Number":
			# search for accession number in table
			matched_lines = table[table[table.columns[1]] == self.query].index.tolist()
			
		elif self.selection=="Genome Index":
			# search for Genome Index in table. Data type set to int, important!
			matched_lines = table[table[table.columns[0]] == int(self.query)].index.tolist()
			
		elif self.selection=="Scientific Name":
			# search for the scientific name in the table
			matched_lines = table[table[table.columns[10]] == self.query].index.tolist()
		
		if matched_lines!=[]:
			return True
		else:
			return False
	
	# function for retrieving taxonomic information for one species from the table
	def getSpeciesInfo(self):
		table=self.TAXO_LIBRARY
		
		if self.selection=="Accession Number":
			# search for accession number in table
			matched_lines = table[table[table.columns[1]] == self.query].index.tolist()
		
		elif self.selection=="Genome Index":
			# search for Genome Index in table. Data type set to int, important!
			matched_lines = table[table[table.columns[0]] == int(self.query)].index.tolist()
		
		elif self.selection=="Scientific Name":
			# search for the scientific name in the table
			matched_lines = table[table[table.columns[10]] == self.query].index.tolist()
		
		# save the species and taxon group to list variables
		acc_values=table.iloc[matched_lines,1].values.tolist()
		species_values = table.iloc[matched_lines,10].values
		authority_values = table.iloc[matched_lines,11].values
		taxgroup_values = table.iloc[matched_lines,14].values
		engName_values = table.iloc[matched_lines,12].values.tolist()
		gerName_values = table.iloc[matched_lines,13].values.tolist()
		taxpath_values = table.iloc[matched_lines,2:8].values
		
		# join the individual list elements into strings
		species_str = ''.join(map(str, species_values[0]))
		authority_str = ''.join(map(str, authority_values[0]))
		taxgroup_str = ''.join(map(str, taxgroup_values[0]))
		taxpath_str = ' > '.join(map(str, taxpath_values[0].flatten()))
		
		# check length of english name value list to get only one value
		if len(engName_values)>1:
			engName_str = ''.join(map(str, engName_values[0]))
		else:
			engName_str = ''.join(map(str, engName_values))
		
		# check length of german name value list to get only one value
		if len(gerName_values)>1:
			gerName_str = ''.join(map(str, gerName_values[0]))
		else:
			gerName_str = ''.join(map(str, gerName_values))

		return species_str,authority_str,taxpath_str,taxgroup_str,engName_str,gerName_str,acc_values
	
	# function for matching a given accession number with the reference table and returning extracted habitat information
	def getHabitat(self):
		table=self.HABITAT_LIBRARY
		out_list=[]
		
		if self.selection=="Accession Number":
			# search for accession number in table
			matched_lines = table[table[table.columns[1]] == self.query].index.tolist()
		
		elif self.selection=="Genome Index":
			# search for Genome Index in table. Data type set to int, important!
			matched_lines = table[table[table.columns[0]] == int(self.query)].index.tolist()
		
		elif self.selection=="Scientific Name":
			# search for the scientific name in the table
			matched_lines = table[table[table.columns[2]] == self.query].index.tolist()
		
		if matched_lines!=[]:
			# check if habitat is marine
			if table.iloc[matched_lines,3].values.size>0:
				out_list.append("marine")
			
			# check if habitat is brackish
			if table.iloc[matched_lines,4].values.size>0:
				out_list.append("brackish")
			
			# check if habitat is fresh
			if table.iloc[matched_lines,5].values.size>0:
				out_list.append("freshwater")
			
			# check if habitat is terrestrial
			if table.iloc[matched_lines,6].values.size>0:
				out_list.append("terrestrial")
			
			# make the output string
			if out_list!=[]:
				out_string=', '.join(map(str,out_list))
			else:
				out_string=''.join("unknown")
				
			return out_string
		else:
			return ""
	
	# function for matching a given taxon group with the reference table and returning the species belonging to that taxon
	def getTaxgroupInfo(self):
		table=self.TAXO_LIBRARY
		taxGroup=self.query
		
		
		matched_lines_kingdom=table[table[table.columns[2]] == taxGroup].index.tolist()
		if matched_lines_kingdom!=[]: matched_title=table.columns[2]
		matched_lines_phylum=table[table[table.columns[3]] == taxGroup].index.tolist()
		if matched_lines_phylum!=[]: matched_title=table.columns[3]
		matched_lines_class=table[table[table.columns[4]] == taxGroup].index.tolist()
		if matched_lines_class!=[]: matched_title=table.columns[4]
		matched_lines_order=table[table[table.columns[5]] == taxGroup].index.tolist()
		if matched_lines_order!=[]: matched_title=table.columns[5]
		matched_lines_family=table[table[table.columns[6]] == taxGroup].index.tolist()
		if matched_lines_family!=[]: matched_title=table.columns[6]
		matched_lines_genus=table[table[table.columns[7]] == taxGroup].index.tolist()
		if matched_lines_genus!=[]: matched_title=table.columns[7]
		# searches for taxGroup. Does not work for some reason
		matched_lines_taxgroup=table[table[table.columns[14]] == taxGroup].index.tolist()
		if matched_lines_taxgroup!=[]: matched_title=table.columns[14]
	
		matched_lines = matched_lines_taxgroup+matched_lines_kingdom+matched_lines_phylum+matched_lines_class+matched_lines_order+matched_lines_family+matched_lines_genus
		
		if matched_lines!=[]:
			sciNames=table.iloc[matched_lines,10].values.tolist()
			sciNames = list(set(sciNames))
			
			return sciNames,matched_title
		else:
			return [],""

# class for searching the GBIF (Global Biodiversity Information Facility, https://gbif.org) Database
class SearchGBIF:
	def __init__(self,sciName,):
		from pygbif import species as sp
		self.sciName=sciName
		self.backbone=sp.name_backbone(sciName)
		#self.lookup=sp.name_lookup(sciName,limit=1)
		#self.lookup_results=self.lookup['results'][0]
		
	# function for retrieving the taxonomic path from GBIF
	def getTaxpath(self):
		lkingdom,lphylum,lclass,lorder,lfamily,lgenus="","","","","",""
		tkingdom,tphylum,tclass,torder,tfamily,tgenus="","","","","",""
		
		if 'kingdom' in self.backbone:
			lkingdom="Kingdom"
			tkingdom=self.backbone['kingdom']
		if 'phylum' in self.backbone:
			lphylum=" > Phylum"
			tphylum=" > "+self.backbone['phylum']
		if 'class' in self.backbone:
			lclass=" > Class"
			tclass=" > "+self.backbone['class']
		if 'order' in self.backbone:
			lorder=" > Order"
			torder=" > "+self.backbone['order']
		if 'family' in self.backbone:
			lfamily=" > Family"
			tfamily=" > "+self.backbone['family']
		if 'genus' in self.backbone:
			lgenus=" > Genus"
			tgenus=" > "+self.backbone['genus']
		if 'scientificName' in self.backbone:
			tsciName=self.backbone['scientificName']
		else:
			tsciName="not available."
		
		if lkingdom!="":
			taxGuide=("as "+lkingdom+lphylum+lclass+lorder+lfamily+lgenus)
			taxPath=tkingdom+tphylum+tclass+torder+tfamily+tgenus
		else:
			taxGuide="not available."
			taxPath=""
		out_list=[
			f"Full name {tsciName}\n"
			f"Taxonomic path {taxGuide}\n",
			f"{taxPath}"
			]
		return ''.join(out_list)

	# function for generating a map png from the GBIF database
	def makeMap(self):
		from pygbif import maps
		if 'usageKey' in self.backbone:
			taxkey=self.backbone['usageKey']
			outmap=maps.map(taxonKey=taxkey,source="density",bin="hex",hexPerTile="200",style="purpleYellow-noborder.poly",format="@1x.png",srs="EPSG:3857",x=0,y=0)
			map_path=outmap.path
			return map_path
		else:
			return ""

# class for getting information from Wikipedia
class SearchWikipedia:
	
	def __init__(self,sciName):
		import wikipediaapi as wiki
		self.wiki_en=wiki.Wikipedia('CryptochromeCoSegregation (ronja.roesner@uni-oldenburg.de','en')
		self.sciName=sciName
	
	def getSummary(self):
		wiki_query=f"{self.sciName}"
		wiki_page=self.wiki_en.page(wiki_query)
		
		if wiki_page.exists():
			summary=wiki_page.summary
		else:
			summary="Wikpedia page does not exist."
		
		return summary

# class contatining the button functions
class Buttons:
	# function for initialising the class
	def __init__(self,text_field,text_input,text_label,chooselabel,map_field,map_image,background_image,render_map,map_label,gbif_onoff,wiki_onoff,map_onoff,selector,selection,query):
		self.text_field=text_field
		self.text_input=text_input
		self.text_label=text_label
		self.chooselabel=chooselabel
		self.map_field=map_field
		self.map_image=map_image
		self.background_image=background_image
		self.render_map=render_map
		self.map_label=map_label
		self.gbif_onoff=gbif_onoff
		self.wiki_onoff=wiki_onoff
		self.map_onoff=map_onoff
		self.selector=selector
		self.selection=selection
		self.query=query

	# function for resetting all inputs and fields
	def reset(self):
		self.text_field.config(state="normal")
		self.text_field.delete(1.0,tk.END)
		self.text_field.config(state="disabled")
		self.text_input.delete(0,tk.END)
		self.text_label.config(text="Requested Information will show up below")
		self.gbif_onoff.set(0)
		self.wiki_onoff.set(0)
		self.map_onoff.set(0)
		self.selector.set("Accession Number")
		self.chooselabel.config(text="Input Accession Number")
		self.text_field.config(width=250,height=40)
		self.map_field.config(width=0,height=0,border=0,relief="flat")
		self.map_label.config(text="")
		self.map_image.paste(self.background_image)
		self.render_map.config(image="")
	
	# function for clearing out the text and input fields as well as checkboxes
	def clearText(self):
		self.text_field.config(state="normal")
		self.text_field.delete(1.0,tk.END)
		self.text_field.config(state="disabled")
		self.text_input.delete(0,tk.END)
		self.text_label.config(text="Requested Information will show up below")
	
	# function to get currently entered values and print the search results in the text box
	def confirm(self):
		self.selection.set(self.selector.get()[:])
		self.query.set(self.text_input.get()[:])
		gbif_state=self.gbif_onoff.get()
		wiki_state=self.wiki_onoff.get()
		map_state=self.map_onoff.get()
		
		self.text_field.config(state="normal")
		setText(self.selection, self.query, self.text_field, self.text_label,gbif_state,wiki_state)
		self.text_field.config(state="disabled")
		
		generateMap(map_state,self.selection,self.query,self.text_field,self.map_field,self.map_image,self.background_image,self.render_map,self.map_label)


# function for checking if the user is connected to the internet
def internetConnection():
	try:
		requests.get("https://api.gbif.org/", timeout=5)
		return True
	except requests.ConnectionError:
		return False

# function for choosing the input method and getting the user input
def getInput(selectorframe,chooselabel):
	
	# input choosing label
	tk.Label(selectorframe,text="Search Library by",font="Arial 14").grid(row=0,column=0,padx=20,sticky="nw")
	
	# set variable for storing the radiobutton selection
	selector=tk.StringVar()
	selector.set("Accession Number")
	
	# set label for above the input box
	chooselabel.config(text=f"Input {selector.get()}",font="Arial 14")
	chooselabel.grid(row=0,column=1,sticky="nw")
	
	# function for when the radiobuttons change
	def clicked():
		if selector.get()=="Genome Index":
			chooselabel.config(text="Input Genome Index (0-379)")
		else:
			chooselabel.config(text=f"Input {selector.get()}")
		
		
	
	# set radiobuttons and render them into the selection grid
	option_accNumber=tk.Radiobutton(selectorframe,text="Accession Number",variable=selector,value="Accession Number",cursor="circle",command=lambda:clicked())
	option_accNumber.grid(row=1,column=0,padx=20,sticky="nw")
	option_speciesID=tk.Radiobutton(selectorframe,text="Genome Index",variable=selector,value="Genome Index",cursor="circle",command=lambda:clicked())
	option_speciesID.grid(row=2,column=0,padx=20,sticky="nw")
	option_sciName=tk.Radiobutton(selectorframe,text="Scientific Name",variable=selector,value="Scientific Name",cursor="circle",command=lambda:clicked())
	option_sciName.grid(row=3,column=0,padx=20,sticky="nw")
	option_taxGroup=tk.Radiobutton(selectorframe,text="Taxon Group",variable=selector,value="Taxon Group",cursor="circle",command=lambda:clicked())
	option_taxGroup.grid(row=4,column=0,padx=20,sticky="nw")
	
	# functions for binding keyboard shortcuts
	def select_option_accNumber(event=None):
		selector.set("Accession Number")
		clicked()
	def select_option_speciesID(event=None):
		selector.set("Genome Index")
		clicked()
	def select_option_sciName(event=None):
		selector.set("Scientific Name")
		clicked()
	def select_option_taxGroup(event=None):
		selector.set("Taxon Group")
		clicked()
	
	# bind keyboard shortcuts for switching between radiobuttons
	selectorframe.bind_all("<Command-Key-1>", select_option_accNumber)
	selectorframe.bind_all("<Command-Key-2>", select_option_speciesID)
	selectorframe.bind_all("<Command-Key-3>", select_option_sciName)
	selectorframe.bind_all("<Command-Key-4>", select_option_taxGroup)
	
	
	return selector

# function for putting search results into the text field
def setText(selection,query,text_field,text_label,gbif_state,wiki_state):
	sciName=""
	sciNames=[]
	# create an object for the table search class
	search_table=SearchLibrary(query.get().capitalize(),selection.get())
	
	# function for changing the output sentence on vernaculars depending on which are available
	def vernacular_text(engName,gerName):
		if engName=="nan" and gerName=="nan":
			text_out="There are no vernaculars available."
		elif engName=="nan" and gerName!="nan":
			text_out=f"There is no english vernacular available, but the german vernacular is {gerName}."
		elif engName!="nan" and gerName=="nan":
			text_out=f"The english vernacular is {engName}. There is no german vernacular available."
		else:
			text_out=f"The english vernacular is {engName}, the german vernacular is {gerName}."
		
		return text_out
	
	# if GBIF search is enabled and an internet connection is available, output search results
	if gbif_state==1 and internetConnection()==True:
		if selection.get()!="Accession Number" and selection.get()!="Genome Index":
			gbif_search=SearchGBIF((query.get()))
			gbif_results=gbif_search.getTaxpath()
			gbif_out=f"\nInformation from GBIF backbone:\n{gbif_results}\n"
		elif selection.get()=="Accession Number" or selection.get()=="Genome Index":
			gbif_out=f"\nNo GBIF information available for {selection.get()}s.\n"
	elif gbif_state==1 and internetConnection()==False:
		gbif_out="\nNo internet connection available, GBIF search impossible.\n"
	elif gbif_state==0:
		gbif_out=""
	
	# if Wikipedia search is enabled and an internet connection is available, output page summary
	if wiki_state==1 and internetConnection()==True:
		if selection.get()!="Accession Number" and selection.get()!="Genome Index":
			wiki_search=SearchWikipedia(query.get())
			wiki_summary=wiki_search.getSummary()
			wiki_out=f"\nInformation from Wikipedia page:\n{wiki_summary}\n"
		elif selection.get()=="Accession Number" or selection.get()=="Genome Index":
			wiki_out=f"\nNo Wikipedia information for {selection.get()}s.\n"
	elif wiki_state==1 and internetConnection()==False:
		wiki_out="\nNo internet connection available, Wikipedia search impossible.\n"
	elif wiki_state==0:
		wiki_out=""
	
	# check for input of radio buttons
	if selection.get()!="Taxon Group":
		# check if species is available in reference table
		is_in_table=search_table.inTable()
		
		if is_in_table:
			# get taxonomic information
			sciName,authority,taxPath,taxGroup,engName,gerName,accList=search_table.getSpeciesInfo()
			# get habitats the species lives in
			habitats=search_table.getHabitat()
			
			# combine available accession numbers into string
			if selection.get()=="Accession Number":
				acc_text=""
			elif selection.get()=="Genome Index":
				acc_text=f"Accession Number for this index is {accList[0]}\n\n"
			elif selection.get()!="Accession Number" and len(accList)==1:
				acc_text=f"One available Accession Number, {accList[0]}\n\n"
			elif selection.get()!="Accession Number" and len(accList)>1:
				acc_text=f"Available Accession Number are {', '.join(accList)}\n\n"
			
			# get vernacular name string
			vern_text=vernacular_text(engName, gerName)
			# set main output text
			main_text=[
				f"\n{sciName} {authority} belongs to the {taxGroup}.\n",
				vern_text+"\n",
				f"\nThe Species is known to live in {habitats} habitats.\n\n",
				f"{acc_text}"
				"Taxonomic Path as kingdom > phylum > class > order > family > genus:\n",
				f"{taxPath}\n",
				f"{gbif_out}",
				f"{wiki_out}",
				"\n---------------------------------------------------"+"\n"
				]
		else:
			# set main output text
			main_text=[
				f"\nNo information on {selection.get().lower()} {query.get()} available from reference table.\n",
				f"{gbif_out}",
				f"{wiki_out}",
				"\n---------------------------------------------------"+"\n"
				]
	
	elif selection.get()=="Taxon Group":
		# get scientific names and name of taxon group
		sciNames,col_title=search_table.getTaxgroupInfo()
		# get the number of species belonging to the taxon
		speciescount=len(sciNames)
		
		if speciescount>0:
			# set main output text
			main_text=[
				f"\n{speciescount} species found in table belonging to {col_title.lower()} {query.get().capitalize()}:\n",
				f"{', '.join(sciNames)}\n",
				f"{gbif_out}",
				f"{wiki_out}",
				"\n---------------------------------------------------"+"\n"
				]
		else:
			# set main output text
			main_text=[
				f"\nNo information on taxon group {query.get()} available from reference table.\n",
				f"{gbif_out}",
				f"{wiki_out}",
				"\n---------------------------------------------------"+"\n"
				]

	# set text for when no input was given
	none_text=[
		"\nPlease enter something.\n"
		"\n---------------------------------------------------"+"\n"
		]
	
	# check if an input was given and modifify text field accordingly
	if query.get()=="":
		text_label.config(text=f"No {selection.get()} given")
		text_field.insert(1.0,''.join(none_text))
	else:
		text_label.config(text=f"Available information on {selection.get()} {query.get()}:")
		text_field.insert(1.0,''.join(main_text))

# function for generating a map png for the current taxon
def generateMap(map_state,selection,query,text_field,map_field,map_image,background_image,render_map,map_label):
	
	if map_state==1 and selection.get()!="Accession Number" and selection.get()!="Genome Index":
		# check for internet connection
		if internetConnection():
			search_map=SearchGBIF(query.get())
			map_path=search_map.makeMap()
			
			if map_path!="":
				# set parameteres of text and map fields, set name of map label
				text_field.config(width=100,height=40)
				map_field.config(width=150,height=40,padx=20,border=2,relief="solid")
				map_label.config(text=f"Occurrence Map for {query.get()}:")
				
				# save png of occurrence map to variable
				occurrence_map=Image.open(map_path)
				# save png of world map to variable
				world_map=Image.open(SCRIPT_DIR+"/images/world_map.png")
				# overlay the world map with the occurrence map
				world_map.paste(occurrence_map, (-12,60), mask=occurrence_map)
				
				# set the overlayed image to be rendered in window
				map_image.paste(world_map)
				render_map.config(image=map_image)
				occurrence_map.close()
				world_map.close()
				
			else:
				# insert error message
				text_field.insert(1.0,"\nNo usage key available, map creation failed.\n")
		else:
			text_field.insert(1.0,"\nNo internet connection available, map creation impossible.\n")
			map_image.paste(background_image)
	elif map_state==0:
		# set parameteres so that the map disappears again
		text_field.config(width=250,height=40)
		map_field.config(width=0,height=0,border=0,relief="flat")
		map_label.config(text="")
		map_image.paste(background_image)
		render_map.config(image="")

#function for the checkbuttons in the Options column
def optionsMenu(selectorframe):
	# title of column
	tk.Label(selectorframe,text="Other Options",font="Arial 14").grid(row=0,column=3,padx=20,sticky="nw")
	
	# checkbox for enabling GBIF search
	gbif_onoff=tk.IntVar()
	enable_gbif=tk.Checkbutton(selectorframe,text='Search GBIF Backbone*',variable=gbif_onoff, onvalue=1, offvalue=0)
	enable_gbif.grid(row=1,column=3,padx=20,sticky="nw")
	
	# checkbox for enabling Wikipedia search
	wiki_onoff=tk.IntVar()
	enable_wiki=tk.Checkbutton(selectorframe,text='Get Wikipedia summary*',variable=wiki_onoff, onvalue=1, offvalue=0)
	enable_wiki.grid(row=2,column=3,padx=20,sticky="nw")
	
	# checkbox for enabling map generation
	map_onoff=tk.IntVar()
	enable_maps=tk.Checkbutton(selectorframe,text="Generate Map*",variable=map_onoff, onvalue=1, offvalue=0)
	enable_maps.grid(row=3,column=3,padx=20,sticky="nw")
	
	# subtitle of column
	tk.Label(selectorframe,text="*requires internet access",font="Arial 12").grid(row=4,column=3,padx=20,sticky="nw")
	
	# function for switching the map_state
	def switchMap(event=None):
		if map_onoff.get()==1:
			map_onoff.set(0)
		elif map_onoff.get()==0:
			map_onoff.set(1)
	
	# function for switching the wiki_state
	def switchWiki(event=None):
		if wiki_onoff.get()==1:
			wiki_onoff.set(0)
		elif wiki_onoff.get()==0:
			wiki_onoff.set(1)
	
	# function for switching the gbif_state
	def switchGBIF(event=None):
		if gbif_onoff.get()==1:
			gbif_onoff.set(0)
		elif gbif_onoff.get()==0:
			gbif_onoff.set(1)
	
	# keybindings for map and gbif search switching
	selectorframe.bind_all("<Command-Key-l>", switchMap)
	selectorframe.bind_all("<Command-Key-k>", switchWiki)
	selectorframe.bind_all("<Command-Key-j>", switchGBIF)
	
	
	return gbif_onoff,wiki_onoff,map_onoff



# main function and window loop
def main():
	# set name of the program
	program_title="CRYtabia"
	program_version="0.6.0"
	
	# make root window
	window=tk.Tk()
	window.title(f"{program_title} {program_version}")
	window.geometry("1510x920")
	
	# lable for title
	title_label=tk.Label(window,text=program_title,font="Arial 18 bold")
	title_label.pack(padx=20,pady=20)
	
	# frame for selection and input
	selectorframe=tk.Frame(window)
	selectorframe.columnconfigure(0,weight=1)
	selectorframe.columnconfigure(1,weight=2)
	selectorframe.columnconfigure(2,weight=1)
	selectorframe.pack()
	chooselabel=tk.Label(selectorframe)
	
	# input field for text
	text_input=tk.Entry(selectorframe,width=30,border=2,relief="sunken")
	text_input.grid(row=1,column=1)
	
	# get the selection und get the data from there
	selector=getInput(selectorframe,chooselabel)
	
	# make empty tkinter variables to later store the selection
	selection=tk.StringVar()
	query=tk.StringVar()
	
	# frame for output
	outputframe=tk.Frame(window)
	outputframe.columnconfigure(0,weight=1)
	outputframe.columnconfigure(1,weight=1)
	outputframe.pack(pady=20,padx=20)
	
	
	# text field for output text
	text_field=tk.Text(outputframe,width=250,height=40,state="disabled",border=2,relief="solid",font="Arial 13",cursor="cross")
	
	# heading for the map
	map_label=tk.Label(outputframe,text="",font="Arial 14")
	# empty text field for the map
	map_field=tk.Text(outputframe,width=0,height=0,state="disabled",cursor="cross")
	
	# empty label to attach the map to
	render_map=tk.Label(map_field)

	# empty PhotoImage to provide an image for the map
	background_image=Image.open(SCRIPT_DIR+"/images/transparent_background.png")
	map_image=ImageTk.PhotoImage(background_image)

	
	# get the output of the checkboxes
	gbif_onoff,wiki_onoff,map_onoff=optionsMenu(selectorframe)
	
	# heading for the text field
	text_label=tk.Label(outputframe,text="Requested Information will show up below",font="Arial 14")
	
	# prepare class Buttons
	press_button = Buttons(text_field,text_input,text_label,chooselabel,map_field,map_image,background_image,render_map,map_label,gbif_onoff,wiki_onoff,map_onoff,selector,selection,query)
	
	# confirm button
	tk.Button(selectorframe,text="confirm",command=lambda: press_button.confirm()).grid(row=2,column=1,sticky="wne")

	# clear button
	tk.Button(selectorframe,text="clear",command=lambda: press_button.clearText(),width=11).grid(row=3, column=1,sticky="nw")
	
	# reset button
	tk.Button(selectorframe,text="reset",command=lambda: press_button.reset(),width=11).grid(row=3, column=1,sticky="ne")

	
	# render the output field and map frame inside the window
	text_label.grid(row=0,column=0,sticky="s")
	text_field.grid(row=1,column=0,sticky="sn")
	map_label.grid(row=0,column=1,sticky="s")
	map_field.grid(row=1,column=1,sticky="sn")
	render_map.pack(pady=50)
	
	# make it so the input can be cofirmed by pressing return
	window.bind("<Return>",lambda x: press_button.confirm())
	# make it so that the content can be cleared by pressing escape
	window.bind("<Escape>",lambda x: press_button.reset())
	# make it so that all text is cleared by pressing command and backspace
	window.bind("<Command-Key-BackSpace>",lambda x: press_button.clearText())
	
	
	# loop the main function while the window is open
	window.mainloop()



# run the main loop
if __name__ == "__main__":
	main()








