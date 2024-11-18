#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 18:24:15 2024

@author: Ronja Rösner

This module extracts data from multiple sources:
	- the companion database
	- Wikipedia
	- the GBIF backbone
"""

# import library for accessing the os
import os
# import library for internet connections
import requests


# get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# class for searching the input table
class SearchLibrary:
	
	def __init__(self,query: str,selection: str):
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
			# search for accession number in table. Input needs to get transformed to upper case.
			matched_lines = table[table[table.columns[1]] == self.query.upper()].index.tolist()
			
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
	
	def getSciName(self):
		table=self.TAXO_LIBRARY
		
		if self.selection=="Accession Number":
			# search for accession number in table. Input needs to get transformed to upper case.
			matched_lines = table[table[table.columns[1]] == self.query.upper()].index.tolist()
		
		elif self.selection=="Genome Index":
			# search for Genome Index in table. Data type set to int, important!
			matched_lines = table[table[table.columns[0]] == int(self.query)].index.tolist()
		
		elif self.selection=="Scientific Name":
			# search for the scientific name in the table
			matched_lines = table[table[table.columns[10]] == self.query].index.tolist()
		
		name_values = table.iloc[matched_lines,10].values
		name_str = ''.join(map(str, name_values[0]))
		
		return name_str
	
	# function for retrieving taxonomic information for one species from the table
	def getSpeciesInfo(self):
		table=self.TAXO_LIBRARY
		
		if self.selection=="Accession Number":
			# search for accession number in table. Input needs to get transformed to upper case.
			matched_lines = table[table[table.columns[1]] == self.query.upper()].index.tolist()
		
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
		index_values = table.iloc[matched_lines,0].values.tolist()
		
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

		return species_str,authority_str,taxpath_str,taxgroup_str,engName_str,gerName_str,acc_values,index_values
	
	# function for matching a given accession number with the reference table and returning extracted habitat information
	def getHabitat(self):
		table=self.HABITAT_LIBRARY
		out_list=[]
		
		if self.selection=="Accession Number":
			# search for accession number in table. Input needs to get transformed to upper case.
			matched_lines = table[table[table.columns[1]] == self.query.upper()].index.tolist()
		
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
	def makeMap(self,source="density",bin="hex",style="purpleYellow-noborder.poly",year=None):
		from pygbif import maps
		if 'usageKey' in self.backbone:
			taxkey=self.backbone['usageKey']
			outmap=maps.map(taxonKey=taxkey,source=source,style=style,bin=bin,year=year, hexPerTile="200",format="@1x.png",srs="EPSG:3857",x=0,y=0)
			map_path=outmap.path
			return map_path
		else:
			return ""

# class for getting information from the NCBI database
class SearchNCBI:
	
	def __init__(self,user_input,selection):
		self.API_URL = "https://api.ncbi.nlm.nih.gov/datasets/v2/"
		self.url_seg_accession = "genome/accession/"
		self.url_seg_taxon = "genome/taxon/"
		
		self.user_input=user_input
		self.selection=selection
	
	def getGenomeData(self):
		if self.selection=="Genome Index":
			dataset_response=None
		elif self.selection=="Accession Number":
			dataset_response = requests.get(self.API_URL+self.url_seg_accession+self.user_input+"/dataset_report")
		else:
			dataset_response = requests.get(self.API_URL+self.url_seg_taxon+self.user_input+"/dataset_report")
		
		dataset_json = dataset_response.json()
		return dataset_json
	
	def getDatasetAttributes(self):
		dataset_json=self.getGenomeData()
		
		dataset_organism_info = dataset_json['reports'][0]['organism']
		dataset_biosample_attr = dataset_json['reports'][0]['assembly_info']['biosample']['attributes']
		return dataset_organism_info,dataset_biosample_attr

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

# function for preparing the search results for the text field
def getText(selection,query,gbif_state,ncbi_state,wiki_state,table_state):
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
			gbif_out=f"\n--- Information from GBIF backbone ---\n{gbif_results}\n"
		elif selection.get()=="Accession Number" or selection.get()=="Genome Index":
			gbif_out=f"\n!! No GBIF information available for {selection.get()}s. !!\n"
	elif gbif_state==1 and internetConnection()==False:
		gbif_out="\n!! No internet connection available, GBIF search impossible. !!\n"
	elif gbif_state==0:
		gbif_out=""
	
	# if NCBI search is enabled and an internet connection is available, output search results
	if ncbi_state==1 and internetConnection()==True:
		if selection.get()=="Accession Number":
			ncbi_search=SearchNCBI((query.get()),selection.get())
			organism_info,biosample_attributes=ncbi_search.getDatasetAttributes()
			
			ncbi_text=[]
			
			ncbi_text.append("--- NCBI Organism Report ---\n")
			for key, item in organism_info.items():
				ncbi_text.append(f"{key.capitalize()}: {item}\n")
			
			ncbi_text.append("\n--- Available information on NCBI for this biosample ---\n")
			for list_obj in biosample_attributes:
				for key, item in list_obj.items():
					if key=="name":
						ncbi_text.append(f"{item.capitalize()}: ")
					elif key=="value":
						ncbi_text.append(f"{item}\n")
			
			ncbi_out=f"\n{''.join(ncbi_text)}\n"
		elif selection.get()=="Scientific Name" or selection.get()=="Taxon":
			try:
				ncbi_search=SearchNCBI((query.get()),selection.get())
				organism_info,biosample_attributes=ncbi_search.getDatasetAttributes()
				
				ncbi_text=[]
				
				ncbi_text.append("--- NCBI Organism Report ---\n")
				for key, item in organism_info.items():
					ncbi_text.append(f"{key.capitalize()}: {item}\n")
				
				ncbi_text.append("\n--- Available information on NCBI for this taxon ---\n")
				for list_obj in biosample_attributes:
					for key, item in list_obj.items():
						if key=="name":
							ncbi_text.append(f"{item.capitalize()}: ")
						elif key=="value":
							ncbi_text.append(f"{item}\n")
				
				ncbi_out=f"\n{''.join(ncbi_text)}\n"
			except KeyError:
				ncbi_out=f"\n!! NCBI Information not found for {selection.get()} {query.get()} !!\n"
		else:
			ncbi_out=f"\nCurrently no NCBI information available for {selection.get()}s.\n"
	elif ncbi_state==1 and internetConnection()==False:
		ncbi_out="\n!! No internet connection available, NCBI search impossible. !!\n"
	elif ncbi_state==0:
		ncbi_out=""
	
	# if Wikipedia search is enabled and an internet connection is available, output page summary
	if wiki_state==1 and internetConnection()==True:
		if selection.get()!="Accession Number" and selection.get()!="Genome Index":
			wiki_search=SearchWikipedia(query.get())
			wiki_summary=wiki_search.getSummary()
			wiki_out=f"\n--- Information from Wikipedia page ---\n{wiki_summary}\n"
		elif selection.get()=="Accession Number" or selection.get()=="Genome Index":
			wiki_out=f"\n!! No Wikipedia information for {selection.get()}s. !!\n"
	elif wiki_state==1 and internetConnection()==False:
		wiki_out="\n!! No internet connection available, Wikipedia search impossible. !!\n"
	elif wiki_state==0:
		wiki_out=""
	
	# if table search is enabled, output information from library
	if table_state==1:
		if selection.get()!="Taxon Group":
			# check if species is available in reference table
			is_in_table=search_table.inTable()
			
			if is_in_table:
				# get taxonomic information
				sciName,authority,taxPath,taxGroup,engName,gerName,accList,indexList=search_table.getSpeciesInfo()
				# get habitats the species lives in
				habitats=search_table.getHabitat()
				
				# combine available accession numbers into string
				if selection.get()=="Accession Number":
					acc_text=""
				elif selection.get()=="Genome Index":
					acc_text=f"Accession Number for this index is {accList[0]}\n\n"
				elif selection.get()!="Accession Number" and len(accList)==1:
					acc_text=f"One available Accession Number, {accList[0]} with Index {indexList[0]}\n\n"
				elif selection.get()!="Accession Number" and len(accList)>1:
					acc_text=f"Available Accession Number are {', '.join(accList)}\nAvailable Indices are {indexList}\n"
				
				# get vernacular name string
				vern_text=vernacular_text(engName, gerName)
				
				table_list=[
					"\n--- Information from the core library ---\n",
					f"\n{sciName} {authority} belongs to the {taxGroup}.\n",
					vern_text+"\n",
					f"\nThe Species is known to live in {habitats} habitats.\n\n",
					f"{acc_text}"
					"Taxonomic Path as kingdom > phylum > class > order > family > genus:\n",
					f"{taxPath}\n",
					]
				table_out=''.join(table_list)
			else:
				table_out=f"\nNo information on {selection.get().lower()} {query.get()} available from reference table.\n"
		elif selection.get()=="Taxon Group":
			# get scientific names and name of taxon group
			sciNames,col_title=search_table.getTaxgroupInfo()
			# get the number of species belonging to the taxon
			speciescount=len(sciNames)
			
			if speciescount>0:
				table_out=f"\n{speciescount} species found in table belonging to {col_title.lower()} {query.get().capitalize()}:\n{', '.join(sciNames)}\n"
			else:
				table_out=f"\nNo information on taxon group {query.get()} available from reference table.\n"
			
	else:
		table_out=""
	

	# set main output text
	main_text=[
		f"\n=== Info for {selection.get().lower()} {query.get()} ===\n",
		f"{table_out}",
		f"{gbif_out}",
		f"{wiki_out}",
		f"{ncbi_out}",
		"\n-------------------------------------------------------------"+"\n"
		]
	
	# set text for when no input was given
	none_text=[
		"\nPlease enter something.\n"
		"\n-------------------------------------------------------------"+"\n"
		]
	
	# check if an input was given and modifify text field accordingly
	if query.get()=="":
		return none_text
	else:
		return main_text


def getSciName(query,selection):
	search_table=SearchLibrary(query.get().capitalize(),selection.get())
	if search_table.inTable():
		if selection.get()!="Taxon Group":
			out_str=str(search_table.getSpeciesInfo()[0])
		else:
			out_str=str(query.get())
	elif not search_table.inTable() and selection.get()=="Scientific Name" or selection.get()=="Taxon Group":
		out_str=query.get()
	else:
		out_str=""
	
	return out_str
	

# function for checking if the user is connected to the internet
def internetConnection():
	try:
		requests.get("https://api.gbif.org/", timeout=5)
		return True
	except requests.ConnectionError:
		return False


if __name__ == "__main__":
	data=SearchLibrary()

