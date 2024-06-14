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

# class for searching the input table
class SearchLibrary:
	
	def __init__(self,query,selection):
		# import required packages
		import pandas as pd
		import os
		# set script directory
		script_directory = os.path.dirname(os.path.abspath(__file__))
		# set reference table
		INPUT_TABLE = os.path.join(script_directory, "infolib.xlsx")
		# get specific columns containing either taxonomic info or habitat info from reference table
		self.TAXO_LIBRARY = pd.read_excel(INPUT_TABLE,usecols="B:O")
		self.HABITAT_LIBRARY = pd.read_excel(INPUT_TABLE,usecols="B,P:S")
		
		self.query=query
		self.selection=selection
		
	
	# function returns the accession numbers matched to a given scientific name
	def sciname_to_accnumber(self):
		table=self.TAXO_LIBRARY
		matched_lines = table[table[table.columns[9]] == self.query].index.tolist()
		if matched_lines!=[]:
			acc_values=table.iloc[matched_lines,0].values.tolist()
			acc_out=''.join(map(str, acc_values[0]))
			return acc_out,acc_values
		else:
			return "",""
	
	# function for matching a given accession number with the reference table and returning extracted taxonomic information
	def get_info_by_accnumber(self,acc_number):
		table=self.TAXO_LIBRARY
		# search for accession number in table
		matched_lines = table[table[table.columns[0]] == acc_number].index.tolist()
		
		if matched_lines!=[]:
			# save the species and taxon group to list variables
			species_values = table.iloc[matched_lines,9].values
			authority_values = table.iloc[matched_lines,10].values
			taxgroup_values = table.iloc[matched_lines,13].values
			engName_values = table.iloc[matched_lines,11].values
			gerName_values = table.iloc[matched_lines,12].values
			taxpath_values = table.iloc[matched_lines,1:7].values
			
			# join the individual list elements into strings
			species_str = ''.join(map(str, species_values))
			authority_str = ''.join(map(str, authority_values))
			taxgroup_str = ''.join(map(str, taxgroup_values))
			taxpath_str = ' > '.join(map(str, taxpath_values.flatten()))
			
			engName_str = ''.join(map(str, engName_values))
			gerName_str = ''.join(map(str, gerName_values))
			
			return species_str,authority_str,taxpath_str,taxgroup_str,engName_str,gerName_str
		else:
			return "","","","","",""
	
	def get_info_from_table(self):
		table=self.TAXO_LIBRARY
		
		if self.selection=="Accession Number":
			# search for accession number in table
			matched_lines = table[table[table.columns[0]] == self.query].index.tolist()
			
		elif self.selection=="Scientific Name":
			# search for the scientific name in the table
			matched_lines = table[table[table.columns[9]] == self.query].index.tolist()
		
		if matched_lines!=[]:
			# save the species and taxon group to list variables
			acc_values=table.iloc[matched_lines,0].values.tolist()
			species_values = table.iloc[matched_lines,9].values
			authority_values = table.iloc[matched_lines,10].values
			taxgroup_values = table.iloc[matched_lines,13].values
			engName_values = table.iloc[matched_lines,11].values
			gerName_values = table.iloc[matched_lines,12].values
			taxpath_values = table.iloc[matched_lines,1:7].values
			
			# join the individual list elements into strings
			
			species_str = ''.join(map(str, species_values[0]))
			authority_str = ''.join(map(str, authority_values[0]))
			taxgroup_str = ''.join(map(str, taxgroup_values[0]))
			taxpath_str = ' > '.join(map(str, taxpath_values[0].flatten()))
			#acc_str = ', '.join(map(str, acc_values))
			engName_str = ''.join(map(str, engName_values[0]))
			gerName_str = ''.join(map(str, gerName_values[0]))
			
			return species_str,authority_str,taxpath_str,taxgroup_str,engName_str,gerName_str,acc_values
		else:
			return "","","","","",""
	
	# function for matching a given taxon group with the reference table and returning the species belonging to that taxon
	def get_info_by_taxon_group(self):
		table=self.TAXO_LIBRARY
		taxGroup=self.query
		
		matched_lines_taxgroup=table[table[table.columns[13]] == taxGroup].index.tolist()
		if matched_lines_taxgroup!=[]: matched_title=table.columns[13]
		matched_lines_kingdom=table[table[table.columns[1]] == taxGroup].index.tolist()
		if matched_lines_kingdom!=[]: matched_title=table.columns[1]
		matched_lines_phylum=table[table[table.columns[2]] == taxGroup].index.tolist()
		if matched_lines_phylum!=[]: matched_title=table.columns[2]
		matched_lines_class=table[table[table.columns[3]] == taxGroup].index.tolist()
		if matched_lines_class!=[]: matched_title=table.columns[3]
		matched_lines_order=table[table[table.columns[4]] == taxGroup].index.tolist()
		if matched_lines_order!=[]: matched_title=table.columns[4]
		matched_lines_family=table[table[table.columns[5]] == taxGroup].index.tolist()
		if matched_lines_family!=[]: matched_title=table.columns[5]
		matched_lines_genus=table[table[table.columns[6]] == taxGroup].index.tolist()
		if matched_lines_genus!=[]: matched_title=table.columns[6]
	
		matched_lines = matched_lines_taxgroup+matched_lines_kingdom+matched_lines_phylum+matched_lines_class+matched_lines_order+matched_lines_family+matched_lines_genus
		
		if matched_lines!=[]:
			sciNames=table.iloc[matched_lines,9].values.tolist()
			sciNames = list(set(sciNames))
			
			return sciNames,matched_title
		else:
			return [],""
	
	# function for matching a given accession number with the reference table and returning extracted habitat information
	def get_habitat_by_accnumber(self,acc_number):
		table=self.HABITAT_LIBRARY
		
		# search for accession number in table
		matched_lines = table[table[table.columns[0]] == acc_number].index.tolist()
		out_list=[]
	
		# check if habitat is marine
		if table.iloc[matched_lines,1].values.size>0:
			out_list.append("marine")
		
		# check if habitat is brackish
		if table.iloc[matched_lines,2].values.size>0:
			out_list.append("brackish")
		
		# check if habitat is fresh
		if table.iloc[matched_lines,3].values.size>0:
			out_list.append("freshwater")
		
		# check if habitat is terrestrial
		if table.iloc[matched_lines,4].values.size>0:
			out_list.append("terrestrial")
		
		# make the output string
		if out_list!=[]:
			out_string=', '.join(map(str,out_list))
		else:
			out_string=''.join("unknown")
			
		return out_string


# class for searching the GBIF Database
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
			outmap=maps.map(taxonKey=taxkey,source="density",bin="hex",style="purpleYellow.poly")
			map_path=outmap.path
			return map_path
		else:
			return ""



# function for choosing the input method and the input
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
		chooselabel.config(text=f"Input {selector.get()}")
	
	# set radiobuttons and render them into the selection grid
	option_accNumber=tk.Radiobutton(selectorframe,text="Accession Number",variable=selector,value="Accession Number",cursor="circle",command=lambda:clicked())
	option_accNumber.grid(row=1,column=0,padx=20,sticky="nw")
	option_sciName=tk.Radiobutton(selectorframe,text="Scientific Name",variable=selector,value="Scientific Name",cursor="circle",command=lambda:clicked())
	option_sciName.grid(row=2,column=0,padx=20,sticky="nw")
	option_taxGroup=tk.Radiobutton(selectorframe,text="Taxon Group",variable=selector,value="Taxon Group",cursor="circle",command=lambda:clicked())
	option_taxGroup.grid(row=3,column=0,padx=20,sticky="nw")
	
	# functions for binding keyboard shortcuts
	def select_option_accNumber(event=None):
		selector.set("Accession Number")
		clicked()
	def select_option_sciName(event=None):
		selector.set("Scientific Name")
		clicked()
	def select_option3(event=None):
		selector.set("Taxon Group")
		clicked()
	
	# bind keyboard shortcuts for switching between radiobuttons
	selectorframe.bind_all("<Command-Key-1>", select_option_accNumber)
	selectorframe.bind_all("<Command-Key-2>", select_option_sciName)
	selectorframe.bind_all("<Command-Key-3>", select_option3)
	
	return selector


# function for putting search results into the text field
def setText(selection,query,text_field,text_label,gbif_state):
	sciName=""
	sciNames=[]
	search_table=SearchLibrary(query.get(),selection.get())
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
	
	# if GBIF Search is enabled, output search results
	if gbif_state==1:
		gbif_search=SearchGBIF((query.get()))
		gbif_results=gbif_search.getTaxpath()
		gbif_out=f"\nInformation from GBIF backbone:\n{gbif_results}\n"
	elif gbif_state==0:
		gbif_out=""
	
	# check for input of radio buttons
	if selection.get()!="Taxon Group" and query.get()!="":
		#acc_number,acc_list=search_table.sciname_to_accnumber()
		sciName,authority,taxPath,taxGroup,engName,gerName,accList=search_table.get_info_from_table()
		
		habitats=search_table.get_habitat_by_accnumber(accList[0])
		
		if selection.get()=="Accession Number":
			acc_text=""
		elif selection.get()=="Scientific Name" and len(accList)==1:
			acc_text=f"One available Accession Number, {accList[0]}.\n\n"
		elif selection.get()=="Scientific Name" and len(accList)>1:
			acc_text=f"Available Accession Number are {', '.join(accList)}.\n\n"
		
		if sciName!="":
			vern_text=vernacular_text(engName, gerName)
			main_text=[
				f"\n{sciName} {authority} belongs to the {taxGroup}.\n",
				vern_text+"\n",
				f"\nThe Species is known to live in {habitats} habitats.\n\n",
				f"{acc_text}"
				"Taxonomic Path as kingdom > phylum > class > order > family > genus:\n",
				f"{taxPath}\n",
				f"{gbif_out}",
				"\n---------------------------------------------------"+"\n"
				]
		else:
			search=SearchGBIF(query.get())
			taxPath=search.getTaxpath()
			main_text=[
				f"\nScientific Name {query.get()} was not found in Table.\n",
				f"{gbif_out}",
				"\n---------------------------------------------------"+"\n"
				]
	
	elif selection.get()=="Taxon Group" and query.get()!="":
		sciNames,col_title=search_table.get_info_by_taxon_group()
		speciescount=len(sciNames)
		
		if sciNames!=[]:
			main_text=[
				f"\n{speciescount} Species found in table belonging to {col_title} {query.get()}:\n",
				f"{', '.join(sciNames)}\n",
				f"{gbif_out}",
				"\n---------------------------------------------------"+"\n"
				]
		else:
			main_text=[
				f"\nTaxon Group {query.get()} was not found in Table.\n",
				f"{gbif_out}",
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
		text_label.config(text=f"Available information on {query.get()}:")
		text_field.insert(1.0,''.join(main_text))


# function for generating a map png for the current taxon
def generateMap(map_state,selection,query,text_field,map_field,map_image,render_map,map_label):
	if map_state==1 and selection.get()!="Accession Number":
		search_map=SearchGBIF(query.get())
		map_path=search_map.makeMap()
		if map_path!="":
			text_field.config(width=150,height=44)
			map_field.config(width=100,height=44,padx=40,border=2,relief="solid")
			map_label.config(text=f"Occurrence Map for {query.get()}:")
			map_image.config(file=map_path)
			render_map.config(image=map_image)
		else:
			text_field.insert(1.0,"No usage key available, map creation failed.")
	elif map_state==0:
		text_field.config(width=250,height=44)
		map_field.config(width=0,height=0,border=0,relief="flat")
		map_label.config(text="")
		map_image.config(file="")
		render_map.config(image="")
		

#function for the checkbuttons in the Options column
def optionsMenu(selectorframe):
	# title of column
	tk.Label(selectorframe,text="Other Options",font="Arial 14").grid(row=0,column=3,padx=20,sticky="nw")
	
	# checkbox for enabling GBIF search
	gbif_onoff=tk.IntVar()
	enable_gbif=tk.Checkbutton(selectorframe,text='Search GBIF Backbone',variable=gbif_onoff, onvalue=1, offvalue=0)
	enable_gbif.grid(row=1,column=3,padx=20,sticky="nw")
	
	# checkbox for enabling map generation
	map_onoff=tk.IntVar()
	enable_maps=tk.Checkbutton(selectorframe,text="Generate Map (WIP)",variable=map_onoff, onvalue=1, offvalue=0)
	enable_maps.grid(row=2,column=3,padx=20,sticky="nw")
	
	return gbif_onoff,map_onoff


class Buttons():
	# function for initialising the class
	def __init__(self,text_field,text_input,text_label,chooselabel,map_field,map_image,render_map,map_label,gbif_onoff,map_onoff,selector,selection,query):
		self.text_field=text_field
		self.text_input=text_input
		self.text_label=text_label
		self.chooselabel=chooselabel
		self.map_field=map_field
		self.map_image=map_image
		self.render_map=render_map
		self.map_label=map_label
		self.gbif_onoff=gbif_onoff
		self.map_onoff=map_onoff
		self.selector=selector
		self.selection=selection
		self.query=query

	# function for resetting all inputs
	def reset(self):
		self.text_field.config(state="normal")
		self.text_field.delete(1.0,tk.END)
		self.text_field.config(state="disabled")
		self.text_input.delete(0,tk.END)
		self.text_label.config(text="Requested Information will show up below")
		self.gbif_onoff.set(0)
		self.map_onoff.set(0)
		self.selector.set("Accession Number")
		self.chooselabel.config(text="Input Accession Number")
	
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
		map_state=self.map_onoff.get()
		
		self.text_field.config(state="normal")
		setText(self.selection, self.query, self.text_field, self.text_label,gbif_state)
		self.text_field.config(state="disabled")
		
		generateMap(map_state,self.selection,self.query,self.text_field,self.map_field,self.map_image,self.render_map,self.map_label)

# main function and window loop
def main():
	# set name of the program
	program_title="CRYtabia"
	program_version="0.4.5"
	
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
	text_input=tk.Entry(selectorframe,width=30)
	text_input.grid(row=1,column=1)
	
	
	# make the selection und get the data from there
	selector=getInput(selectorframe,chooselabel)
	
	# make empty tkinter variables to later store the selection
	selection=tk.StringVar()
	query=tk.StringVar()
	
	# frame for output
	outputframe=tk.Frame(window)
	outputframe.columnconfigure(0,weight=1)
	outputframe.columnconfigure(1,weight=1)
	outputframe.pack(pady=20,padx=20)
	
	
	# text field
	text_field=tk.Text(outputframe,width=225,height=44,state="disabled",border=2,relief="solid",font="Arial 13",cursor="cross")
	
	# heading for the map
	map_label=tk.Label(outputframe,text="",font="Arial 14")
	# empty text field for the map
	map_field=tk.Text(outputframe,width=0,height=0,state="disabled",cursor="cross")
	# empty PhotoImage to provide an image for the map
	map_image=tk.PhotoImage()
	# empty label to attach the map to
	render_map=tk.Label(map_field)

	# get the output of the checkboxes
	gbif_onoff,map_onoff=optionsMenu(selectorframe)
	
	# heading for the text field
	text_label=tk.Label(outputframe,text="Requested Information will show up below",font="Arial 14")
	
	# prepare class Buttons
	press_button=Buttons(text_field,text_input,text_label,chooselabel,map_field,map_image,render_map,map_label,gbif_onoff,map_onoff,selector,selection,query)
	
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
	render_map.pack(pady=75)

	
	# make it so the input can be cofirmed by pressing return
	window.bind("<Return>",lambda x: press_button.confirm())
	# make it so that the content can be cleared by pressing escape
	window.bind("<Escape>",lambda x: press_button.reset())
	
	# loop the main function while the window is open
	window.mainloop()


# run the main loop
if __name__ == "__main__":
	main()








