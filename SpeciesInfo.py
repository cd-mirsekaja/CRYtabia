#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:45:33 2024

@author: Ronja Roesner

Program for getting info on a given species from the included reference table.
Comments are always above the commented line.

"""

import pandas as pd
import tkinter as tk
import os


script_directory = os.path.dirname(os.path.abspath(__file__))
INPUT_TABLE = os.path.join(script_directory, "infolib.xlsx")

# get specific columns containing either taxonomic info or habitat info from reference table
TAXO_LIBRARY = pd.read_excel(INPUT_TABLE,usecols="B:N")
HABITAT_LIBRARY = pd.read_excel(INPUT_TABLE,usecols="B,I:L")

# function returns the accession numbers matched to a given scientific name
def sciname_to_accnumber(table,sciName):
	matched_lines = table[table[table.columns[1]] == sciName].index.tolist()
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
		species_values = table.iloc[matched_lines,1].values
		authority_values = table.iloc[matched_lines,2].values
		taxgroup_values = table.iloc[matched_lines,3].values
		engName_values = table.iloc[matched_lines,4].values
		gerName_values = table.iloc[matched_lines,5].values
		taxpath_values = table.iloc[matched_lines,6:12].values
		
		# join the individual list elements into strings
		species_str = ''.join(map(str, species_values))
		authority_str = ''.join(map(str, authority_values))
		taxgroup_str = ''.join(map(str, taxgroup_values))
		taxpath_str = ' > '.join(map(str, taxpath_values.flatten()))
		
		engName_str = ''.join(map(str, engName_values))
		gerName_str = ''.join(map(str, gerName_values))
		
		return species_str,authority_str,taxpath_str,taxgroup_str,engName_str,gerName_str
	else:
		return "","","",""

def get_info_by_taxon_group(table,taxGroup):
	matched_lines=table[table[table.columns[3]] == taxGroup].index.tolist()
	
	if matched_lines!=[]:
		sciNames=table.iloc[matched_lines,1].values.tolist()
		
		return sciNames
	else:
		return ""

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


# function for choosing the input method and the input
def choose_input(selectorframe):
	
	# input choosing label
	tk.Label(selectorframe,text="Search Library by",font="Arial 14").grid(row=0,column=0,padx=20,sticky="nw")
	
	# radiobuttons
	selector=tk.StringVar()
	selector.set("Accession Number")
	
	chooselabel=tk.Label(selectorframe,text=f"Input {selector.get()}",font="Arial 14")
	chooselabel.grid(row=0,column=1,sticky="nw")
	
	def clicked():
		chooselabel.config(text=f"Input {selector.get()}")
	
	option1=tk.Radiobutton(selectorframe,text="Accession Number",variable=selector,value="Accession Number",command=lambda:clicked())
	option1.grid(row=1,column=0,padx=20,sticky="nw")
	option2=tk.Radiobutton(selectorframe,text="Scientific Name",variable=selector,value="Scientific Name",command=lambda:clicked())
	option2.grid(row=2,column=0,padx=20,sticky="nw")
	option3=tk.Radiobutton(selectorframe,text="Taxon Group",variable=selector,value="Taxon Group",command=lambda:clicked())
	option3.grid(row=3,column=0,padx=20,sticky="nw")
	
	return selector


# function for putting search results into the text field
def text_box(selection,query,output_field,output_label):
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
	
	# check for input of radio buttons
	if selection.get()=="Accession Number":
		sciName,authority,taxPath,taxGroup,engName,gerName=get_info_by_accnumber(TAXO_LIBRARY,query.get())
		habitats=get_habitat_by_accnumber(HABITAT_LIBRARY, query.get())
		
		vern_text=vernacular_text(engName, gerName)
		success_text=[
			f"\n{sciName} {authority} belongs to the {taxGroup}.",
			vern_text+"\n",
			f"\nThe Species is known to live in {habitats} habitats."+"\n"+"\n",
			f"Taxonomic Path: {taxPath}\n",
			"\n---------------------------------------------------"+"\n"
			]
		
	elif selection.get()=="Scientific Name":
		acc_number,acc_list=sciname_to_accnumber(TAXO_LIBRARY, query.get())
		sciName,authority,taxPath,taxGroup,engName,gerName=get_info_by_accnumber(TAXO_LIBRARY,acc_number)
		habitats=get_habitat_by_accnumber(HABITAT_LIBRARY, acc_number)
		
		vern_text=vernacular_text(engName, gerName)
		success_text=[
			f"\n{sciName} {authority} belongs to the {taxGroup}.\n",
			vern_text+"\n",
			f"\nThe Species is known to live in {habitats} habitats.\n\n",
			f"Available Accession Numbers are {', '.join(acc_list)}\n\n",
			f"Taxonomic Path: {taxPath}\n",
			"\n---------------------------------------------------"+"\n"
			]
	
	elif selection.get()=="Taxon Group":
		sciName=get_info_by_taxon_group(TAXO_LIBRARY,query.get())
		speciescount=len(sciName)
		success_text=[
			f"{speciescount} Species belonging to taxon group {query.get()}:\n",
			f"{', '.join(sciName)}\n",
			"\n---------------------------------------------------"+"\n"
			]
	
	fail_text=[
		f"\n{selection.get()} {query.get()} was not found in Table.\nPlease enter something else.\n",
		"\n---------------------------------------------------"+"\n"
		]
	
	none_text=[
		"\nPlease enter something.\n"
		"\n---------------------------------------------------"+"\n"
		]
	
	# check if an input was given
	if query.get()=="":
		output_field.insert(1.0,''.join(none_text))
	# check if something was found in the table
	elif sciName!="":
		output_label.config(text=f"Available information on {query.get()}:")
		output_field.insert(1.0,''.join(success_text))
	# check if nothing was found in the table
	elif sciName=="":
		output_label.config(text=f"No information available for {query.get()}")
		output_field.insert(1.0,''.join(fail_text))


# function for clearing out the text and input fields
def reset(output_field,text_input,output_label):
	output_field.config(state="normal")
	output_field.delete(1.0,tk.END)
	output_field.config(state="disabled")
	text_input.delete(0,tk.END)
	output_label.config(text="Requested Information will show up below.")

# main function
def main():
	# make root window
	window=tk.Tk()
	window.title("Species Information Extractor v2")
	window.geometry("1280x720")
	
	# lable for title
	title_label=tk.Label(window,text="Species Information Extractor v2",font="Arial 18 bold")
	title_label.pack(padx=20,pady=20)
	
	# frame for selection and input
	selectorframe=tk.Frame(window)
	selectorframe.columnconfigure(0,weight=1)
	selectorframe.columnconfigure(1,weight=1)
	
	# render the frame inside the main window
	selectorframe.pack()
	
	# input field for text
	text_input=tk.Entry(selectorframe)
	text_input.grid(row=1,column=1)
	
	# make the selection und get the data from there
	selector=choose_input(selectorframe)
	
	# make empty tkinter variables to later store the selection
	selection=tk.StringVar()
	query=tk.StringVar()
	
	# frame for output
	outputframe=tk.Frame(window,borderwidth=10)
	outputframe.columnconfigure(0,weight=1)
	outputframe.pack(pady=20,padx=20)
	
	# text field
	output_field=tk.Text(outputframe,width=400,height=40,state="disabled")
	
	# text field label
	output_label=tk.Label(outputframe,text="Requested Information will show up below.",font="Arial 14")
	output_label.grid(row=0,column=0,sticky="s")
	
	# confirm button
	tk.Button(selectorframe,text="confirm",command=lambda: confirm()).grid(row=2,column=1,sticky="nw")
	
	# save button
	tk.Button(selectorframe,text="clear",command=lambda: reset(output_field,text_input,output_label)).grid(row=2, column=1,sticky="ne")
	
	# function to get currently entered values and print the search results in the text box
	def confirm():
		output_field.config(state="normal")
		selection.set(selector.get()[:])
		query.set(text_input.get()[:])
		text_box(selection, query, output_field, output_label)
		output_field.config(state="disabled")
	
	# render the output field inside the window
	output_field.grid(row=1,column=0)
	
	# make it so the input can be cofirmed by pressing return
	window.bind("<Return>",lambda x: confirm())
	window.bind("<Escape>",lambda x: reset(output_field,text_input,output_label))
	
	# loop the program while the window is open
	window.mainloop()


main()







