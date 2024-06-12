#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:45:33 2024

@author: Ronja Roesner

Program for getting info on a given species from the included reference table.
Comments are always above the commented line.

"""

# import required packages
import pandas as pd
import tkinter as tk
import os


# set script directory
script_directory = os.path.dirname(os.path.abspath(__file__))
# set reference table
INPUT_TABLE = os.path.join(script_directory, "infolib.xlsx")

# get specific columns containing either taxonomic info or habitat info from reference table
TAXO_LIBRARY = pd.read_excel(INPUT_TABLE,usecols="B:O")
HABITAT_LIBRARY = pd.read_excel(INPUT_TABLE,usecols="B,P:S")

# function returns the accession numbers matched to a given scientific name
def sciname_to_accnumber(table,sciName):
	matched_lines = table[table[table.columns[9]] == sciName].index.tolist()
	if matched_lines!=[]:
		acc_values=table.iloc[matched_lines,0].values.tolist()
		acc_out=''.join(map(str, acc_values[0]))
		return acc_out,acc_values
	else:
		return "",""

# function for matching a given accession number with the reference table and returning extracted taxonomic information
def get_info_by_accnumber(table,ac_number):
	# search for accession number in table
	matched_lines = table[table[table.columns[0]] == ac_number].index.tolist()
	
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

# function for matching a given taxon group with the reference table and returning the species belonging to that taxon
def get_info_by_taxon_group(table,taxGroup):
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
def get_habitat_by_accnumber(table,ac_number):
	# search for accession number in table
	matched_lines = table[table[table.columns[0]] == ac_number].index.tolist()
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


class SearchGBIF:
	def __init__(self,sciName,):
		from pygbif import species as sp
		self.sciName=sciName
		self.backbone=sp.name_backbone(sciName)
		self.lookup=sp.name_lookup(sciName,limit=1)
		self.lookup_results=self.lookup['results'][0]
		if 'usageKey' in self.backbone:
			self.taxkey=self.backbone['usageKey']
	
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
	
	def makeMap(self):
		from pygbif import maps
		outmap=maps.map(taxonKey=self.taxkey,source="density",bin="hex",style="purpleYellow.poly",format="@2x.png")
		outmap.response
		outmap.path
		outmap.img
		outmap.plot()



# function for choosing the input method and the input
def getInput(selectorframe):
	
	# input choosing label
	tk.Label(selectorframe,text="Search Library by",font="Arial 14").grid(row=0,column=0,padx=20,sticky="nw")
	
	# set variable for storing the radiobutton selection
	selector=tk.StringVar()
	selector.set("Accession Number")
	
	# set label for above the input box
	chooselabel=tk.Label(selectorframe,text=f"Input {selector.get()}",font="Arial 14")
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
def setText(selection,query,text_field,output_label,gbif_state):
	sciName=""
	sciNames=[]
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
		gbif_search=SearchGBIF(query.get())
		gbif_results=gbif_search.getTaxpath()
		gbif_out=f"\nInformation from GBIF backbone:\n{gbif_results}\n"
	elif gbif_state==0:
		gbif_out=""
	
	# check for input of radio buttons
	if selection.get()=="Accession Number" and query.get()!="":
		sciName,authority,taxPath,taxGroup,engName,gerName=get_info_by_accnumber(TAXO_LIBRARY,query.get())
		habitats=get_habitat_by_accnumber(HABITAT_LIBRARY, query.get())
		
		if sciName!="":
			vern_text=vernacular_text(engName, gerName)
			main_text=[
				f"\n{sciName} {authority} belongs to the {taxGroup}.\n",
				vern_text+"\n",
				f"\nThe Species is known to live in {habitats} habitats."+"\n"+"\n",
				"Taxonomic Path as kingdom > phylum > class > order > family > genus:\n",
				f"{taxPath}\n",
				"\n---------------------------------------------------"+"\n"
				]
		else:
			main_text=[
				f"\nAccession Number {query.get()} was not found in Table.\n",
				"\n---------------------------------------------------"+"\n"
				]
		
	elif selection.get()=="Scientific Name" and query.get()!="":
		acc_number,acc_list=sciname_to_accnumber(TAXO_LIBRARY, query.get())
		sciName,authority,taxPath,taxGroup,engName,gerName=get_info_by_accnumber(TAXO_LIBRARY,acc_number)
		habitats=get_habitat_by_accnumber(HABITAT_LIBRARY, acc_number)
		
		if sciName!="":
			vern_text=vernacular_text(engName, gerName)
			main_text=[
				f"\n{sciName} {authority} belongs to the {taxGroup}.\n",
				vern_text+"\n",
				f"\nThe Species is known to live in {habitats} habitats."+"\n"+"\n",
				f"Available Accession Numbers are {', '.join(acc_list)}\n\n",
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
		sciNames,col_title=get_info_by_taxon_group(TAXO_LIBRARY,query.get())
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
	# set text for when nothing was found

	# set text for when no input was given
	none_text=[
		"\nPlease enter something.\n"
		"\n---------------------------------------------------"+"\n"
		]
	
	# check if an input was given
	if query.get()=="":
		output_label.config(text=f"No {selection.get()} given")
		text_field.insert(1.0,''.join(none_text))
	else:
		output_label.config(text=f"Available information on {query.get()}:")
		text_field.insert(1.0,''.join(main_text))

# function for clearing out the text and input fields
def reset(text_field,text_input,output_label):
	text_field.config(state="normal")
	text_field.delete(1.0,tk.END)
	text_field.config(state="disabled")
	text_input.delete(0,tk.END)
	output_label.config(text="Requested Information will show up below")

def optionsMenu(selectorframe):
	# title of column
	tk.Label(selectorframe,text="Other Options",font="Arial 14").grid(row=0,column=3,padx=20,sticky="nw")
	
	# checkbox for enabling GBIF search
	gbif_onoff=tk.IntVar()
	enable_gbif=tk.Checkbutton(selectorframe,text='Search GBIF Backbone',variable=gbif_onoff, onvalue=1, offvalue=0)
	enable_gbif.grid(row=1,column=3,padx=20,sticky="nw")
	
	# checkbox for enabling map generation
	maps_onoff=tk.IntVar()
	enable_maps=tk.Checkbutton(selectorframe,text="Generate Map (WIP)",variable=maps_onoff, onvalue=1, offvalue=0)
	#enable_maps.grid(row=2,column=3,padx=20,sticky="nw")
	
	return gbif_onoff,maps_onoff
	

# main function
def main():
	# set name of the program
	program_title="Species Information Extractor v3"
	
	# make root window
	window=tk.Tk()
	window.title(program_title)
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
	
	# input field for text
	text_input=tk.Entry(selectorframe)
	text_input.grid(row=1,column=1)
	
	
	# make the selection und get the data from there
	selector=getInput(selectorframe)
	
	# make empty tkinter variables to later store the selection
	selection=tk.StringVar()
	query=tk.StringVar()
	
	# frame for output
	outputframe=tk.Frame(window)
	outputframe.columnconfigure(0,weight=2)
	outputframe.columnconfigure(1,weight=1)
	outputframe.pack(pady=20,padx=20)
	
	# get the output of the checkboxes
	gbif_onoff,maps_onoff=optionsMenu(selectorframe)
	
	# text field
	text_field=tk.Text(outputframe,width=400,height=44,state="disabled",border=2,relief="solid",font="Arial 13",cursor="cross")
	
	# text field label
	output_label=tk.Label(outputframe,text="Requested Information will show up below",font="Arial 14")
	output_label.grid(row=0,column=0,sticky="s")
	
	# confirm button
	tk.Button(selectorframe,text="confirm",command=lambda: confirm()).grid(row=2,column=1,sticky="nw")
	
	# save button
	tk.Button(selectorframe,text="clear",command=lambda: reset(text_field,text_input,output_label)).grid(row=2, column=1,sticky="ne")
	
	# function to get currently entered values and print the search results in the text box
	def confirm():
		text_field.config(state="normal")
		selection.set(selector.get()[:])
		query.set(text_input.get()[:])
		gbif_state=gbif_onoff.get()
		setText(selection, query, text_field, output_label,gbif_state)
		text_field.config(state="disabled")
	
	# render the output field inside the window
	text_field.grid(row=1,column=0)
	
	# make it so the input can be cofirmed by pressing return
	window.bind("<Return>",lambda x: confirm())
	# make it so that the content can be cleared by pressing escape
	window.bind("<Escape>",lambda x: reset(text_field,text_input,output_label))
	
	# loop the main function while the window is open
	window.mainloop()


main()







