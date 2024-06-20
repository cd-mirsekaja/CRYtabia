#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:45:33 2024

@author: Ronja Roesner
"""

import pandas as pd
from gooey import Gooey, GooeyParser

import os

script_directory = os.path.dirname(os.path.abspath(__file__))
INPUT_TABLE = os.path.join(script_directory, "infolib.xlsx")

TAXO_LIBRARY = pd.read_excel(INPUT_TABLE,usecols="B:F")
HABITAT_LIBRARY = pd.read_excel(INPUT_TABLE,usecols="B,G:J")


def sciname_to_accnumber(table,sciName):
	matched_lines = table[table[table.columns[1]] == sciName].index.tolist()
	acc_values=table.iloc[matched_lines,0].values.tolist()
	acc_out=''.join(map(str, acc_values))
	return acc_out

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


description="Below you can choose whether to input an accession number or scientific name. \nYou will then get some information on the provided query."
@Gooey(disable_stop_button=True,show_restart_button=False,show_success_modal=False,program_name="Find Species Information v1",program_description=description,hide_progress_msg=True)
def main():
	parser = GooeyParser()
	
	parser.add_argument("option",choices=["Accession Number","Scientific Name"],help="Choose where to start.",metavar="Choose Input")
	parser.add_argument("input",action="store",help="Please enter your query.",metavar="Input Query")
	
	args=parser.parse_args()
	
	if args.option=="Accession Number":
		sciName,authority,taxPath,taxGroup=find_taxinfo(TAXO_LIBRARY,args.input)
		habitats=find_habitat(HABITAT_LIBRARY, args.input)
	elif args.option=="Scientific Name":
		acc_number=sciname_to_accnumber(TAXO_LIBRARY, args.input)
		sciName,authority,taxPath,taxGroup=find_taxinfo(TAXO_LIBRARY,acc_number)
		habitats=find_habitat(HABITAT_LIBRARY, acc_number)
	else:
		print("Please enter a valid Option.")
	
	
	
	if sciName!="":
		print("---------------------------------------------------"+"\n")
		print(f"Input: {args.input}"+"\n")
		print(f"{sciName} {authority} - belongs to the {taxGroup}.")
		print(f"The Species is known to live in {habitats} habitats."+"\n")
		print("Taxonomic Information: ")
		print(taxPath+"\n")
	else:
		print(f"{args.option} {args.input} was not found in Table.\nPlease try again.\n")


def select_input(selectorframe,window):
	pass


main()







