#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:45:33 2024

@author: Ronja Roesner
"""

import pandas as pd
import tkinter as tk
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
INPUT_TABLE = os.path.join(script_directory, "infolib.xlsx")

TAXO_LIBRARY = pd.read_excel(INPUT_TABLE,usecols="B:F")
HABITAT_LIBRARY = pd.read_excel(INPUT_TABLE,usecols="B,G:J")


def sciname_to_accnumber(table,sciName):
	matched_lines = table[table[table.columns[1]] == sciName].index.tolist()
	if matched_lines!=[]:
		acc_values=table.iloc[matched_lines,0].values.tolist()
		acc_out=''.join(map(str, acc_values[0]))
		return acc_out,acc_values
	else:
		return "",""

def find_taxinfo(table,ac_number):
# Search for the accession number in the table
	matched_lines = table[table[table.columns[0]] == ac_number].index.tolist()
	
	if matched_lines!=[]:
		# output the species and taxon group
		species_values = table.iloc[matched_lines,1].values.tolist()
		authority_values = table.iloc[matched_lines,2].values.tolist()
		taxgroup_values = table.iloc[matched_lines,3].values.tolist()
		taxpath_values = table.iloc[matched_lines,4].values.tolist()
		
		# Join the list elements into strings
		species_str = ''.join(map(str, species_values))
		authority_str = ''.join(map(str, authority_values))
		taxgroup_str = ''.join(map(str, taxgroup_values))
		taxpath_str = ''.join(map(str, taxpath_values))
		
		return species_str,authority_str,taxpath_str,taxgroup_str
	else:
		return "","","",""


def find_habitat(table,ac_number):
	matched_lines = table[table[table.columns[0]] == ac_number].index.tolist()
	out_list=[]
	
	if table.iloc[matched_lines,1].values.size>0:
		out_list.append("marine")
		
	if table.iloc[matched_lines,2].values.size>0:
		out_list.append("brackish")
		
	if table.iloc[matched_lines,3].values.size>0:
		out_list.append("freshwater")
		
	if table.iloc[matched_lines,4].values.size>0:
		out_list.append("terrestrial")
		
	if out_list!=[]:
		out_string=', '.join(map(str,out_list))
	else:
		out_string=''.join("unknown")
		
	return out_string


# function for choosing the input method and the input
def choose_input(selectorframe):
	
	# input choosing label
	tk.Label(selectorframe,text="Choose Input Method",font="Arial 14").grid(row=0,column=0)
	
	# radiobuttons
	selector=tk.StringVar()
	selector.set("Accession Number")
	#selection="Accession Number"
	
	chooselabel=tk.Label(selectorframe,text=f"Input {selector.get()}",font="Arial 14")
	chooselabel.grid(row=0,column=1,sticky="nw")
	
	def clicked():
		chooselabel.config(text=f"Input {selector.get()}")
	
	option1=tk.Radiobutton(selectorframe,text="Accession Number",variable=selector,value="Accession Number",command=lambda:clicked())
	option1.grid(row=1,column=0,padx=20,sticky="nw")
	option2=tk.Radiobutton(selectorframe,text="Scientific Name",variable=selector,value="Scientific Name",command=lambda:clicked())
	option2.grid(row=2,column=0,padx=20,sticky="nw")
	
	
	
	
	return selector#,input_field


# function for putting search results into the text field
def text_box(selection,query,output_field,output_label):
	if selection.get()=="Accession Number":
		sciName,authority,taxPath,taxGroup=find_taxinfo(TAXO_LIBRARY,query.get())
		habitats=find_habitat(HABITAT_LIBRARY, query.get())
		success_text=[
			"---------------------------------------------------"+"\n",
			f"{sciName} {authority} - belongs to the {taxGroup}.\n",
			f"The Species is known to live in {habitats} habitats."+"\n"+"\n",
			"Taxonomic Information: ",
			taxPath+"\n",
			"---------------------------------------------------"+"\n"
			]
	elif selection.get()=="Scientific Name":
		acc_number,acc_list=sciname_to_accnumber(TAXO_LIBRARY, query.get())
		sciName,authority,taxPath,taxGroup=find_taxinfo(TAXO_LIBRARY,acc_number)
		habitats=find_habitat(HABITAT_LIBRARY, acc_number)
		success_text=[
			"---------------------------------------------------"+"\n",
			f"{sciName} {authority} - belongs to the {taxGroup}.\n",
			f"The Species is known to live in {habitats} habitats.\n\n",
			f"Available Accession Numbers are {', '.join(acc_list)}\n\n",
			"Taxonomic Information: ",
			taxPath+"\n",
			"---------------------------------------------------"+"\n"
			]
	
	fail_text=f"\n{selection.get()} {query.get()} was not found in Table.\nPlease enter something else.\n"
		
	
	if query.get()=="":
		output_field.insert(tk.END,"\nPlease enter something.\n")
	elif sciName!="":
		output_label.config(text=f"Available information on {query.get()}")
		output_field.delete(1.0,tk.END)
		output_field.insert(tk.END,''.join(success_text))
	elif sciName=="":
		output_label.config(text=f"No information available for {query.get()}")
		output_field.insert(tk.END,fail_text)

def reset(output_field,text_input,output_label):
	output_field.config(state="normal")
	output_field.delete(1.0,tk.END)
	output_field.config(state="disabled")
	text_input.delete(0,tk.END)
	output_label.config(text="Requested Information will show up below.")

# main function
def main():
	
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
	
	# text field creation
	outputframe=tk.Frame(window,borderwidth=10)
	outputframe.columnconfigure(0,weight=1)
	outputframe.pack(pady=20,padx=20)
	
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
	
	# loop the program while the window is open
	window.mainloop()



main()







