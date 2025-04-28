#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 18:24:15 2024

@author: Ronja Rösner

This module extracts data from multiple sources:
	the core database (genotree_master_library.db)
	Wikipedia
	the GBIF backbone
	the NCBI Genome database
"""

# import libraries
import os, requests, sqlite3
from setup import DB_FILE

# class for searching the core database
class SearchDatabase:

	def __init__(self,query: str,selection: str):
		# establishes connection to the database
		db_conn=sqlite3.connect(DB_FILE)
		# creates new cursor object to interact with the database
		self.cursor=db_conn.cursor()

		self.user_query=query.capitalize() if selection!="Accession Number" else query
		self.selection=selection
		
		self.selection_map = {
			"Accession Number": ("ids", ["AccessionNumber"]),
			"Genome Index": ("ids", ["IDX"]),
			"Scientific Name": ("taxonomy", ["ScientificName"]),
			"Taxon Group": ("taxonomy", ["Kingdom", "Phylum", "Class", "taxOrder", "Genus"])
		}

	# function for checking whether the query is available in the database or not
	def inDatabase(self):
		"""
		Check if the user query is available in the database. Returns a boolean.
		"""
		if self.selection in self.selection_map:
			# get the reference table and columns for the user selection
			table, columns = self.selection_map[self.selection]
			# create a string containing all relevant column names for the SQL query
			all_columns = " OR ".join(f"{col}=?" for col in columns)
			# set the SQL query
			db_query = f"SELECT * FROM {table} WHERE {all_columns}"
			# execute the SQL query with the user query as input
			self.cursor.execute(db_query, (self.user_query,) * len(columns))

		if self.cursor.fetchone():
			return True
		else:
			return False

	def getIDX(self):
		"""
		Get the indices for the user query in the database. Returns a list of integers.
		"""
		if self.inDatabase():
			table, columns = self.selection_map[self.selection]
			all_columns = " OR ".join(f"{col}=?" for col in columns)
			db_query = f"SELECT IDX FROM {table} WHERE {all_columns}"
			self.cursor.execute(db_query, (self.user_query,) * len(columns))

			# get the indices from the database and convert them into a simple list
			idx_list=self.cursor.fetchall()
			idx_list=[idx[0] for idx in idx_list]

			return idx_list
		else:
			return None

	def getSpeciesInfo(self):
		"""
		Get Information on the selected species from the database.

		Returns:
		- a tuple of strings containing general information (ScientificName, Authority, Vernacular_Eng, Vernacular_Ger)
		- a list of strings containing all available accession numbers
		- a string containing the taxonomic path
		- a string containing information on the habitats
		- a list of integers containing the indices
		"""

		idx_list=self.getIDX()

		# database accession for getting basic species information
		db_query_a = f"SELECT ScientificName, Authority, Vernacular_Eng, Vernacular_Ger FROM taxonomy WHERE IDX=?"
		self.cursor.execute(db_query_a, (idx_list[0],))
		general_info=self.cursor.fetchone()

		# database accession for getting the accession numbers
		idx_str = " OR ".join(f"IDX={idx}" for idx in idx_list)
		db_query_b = f"SELECT AccessionNumber FROM ids WHERE {idx_str}"
		self.cursor.execute(db_query_b)
		info_b=self.cursor.fetchall()
		acc_list=[acc[0] for acc in info_b]

		# database accession for getting the taxonomic path
		db_query_c = f"SELECT Kingdom, Phylum, Class, 'Order', Family, Genus FROM taxonomy WHERE IDX=?"
		self.cursor.execute(db_query_c, (idx_list[0],))
		info_c=self.cursor.fetchone()
		# convert the taxonomic path into a string
		taxpath_str=" > ".join(info_c)

		# database accession for getting the habitat information
		db_query_d="SELECT isMarine, isBrackish, isFresh, isTerrestrial FROM traits WHERE IDX = ?"
		self.cursor.execute(db_query_d, (idx_list[0],))
		habitat_boolean=self.cursor.fetchone()
		habitat_names = ["marine", "brackish", "freshwater", "terrestrial"]
		habitat_list = [habitat_names[i] for i in range(len(habitat_boolean)) if habitat_boolean[i] == 1]
		if habitat_list!=[]:
			habitat_str=', '.join(map(str,habitat_list))
		else:
			habitat_str=""

		return general_info, acc_list, taxpath_str, habitat_str, idx_list

	def getTaxgroupInfo(self):
		"""
		Get all species belonging to the selected taxon group from the database.

		Returns:
		- a list of strings containing all scientific names
		- a string containing the name of the taxon group
		"""

		if self.inDatabase():
			table, columns = self.selection_map[self.selection]
			all_columns = " OR ".join(f"{col}=?" for col in columns)
			db_query = f"SELECT ScientificName, {', '.join(columns)} FROM {table} WHERE {all_columns}"
			self.cursor.execute(db_query, (self.user_query,) * len(columns))

			results=self.cursor.fetchall()
			sci_names=[name[0] for name in results]

			matched_column = ""
			for col in columns:
				if any(result[columns.index(col) + 1] == self.user_query for result in results):
					matched_column = col
					break

			return sci_names, matched_column
		else:
			return [], ""


# class for searching the GBIF (Global Biodiversity Information Facility, https://gbif.org) Database
class SearchGBIF:
	def __init__(self,query: str,selection: str):
		from pygbif import species as sp
		
		library=SearchDatabase(query,selection)
		if library.inDatabase():
			self.sciName=library.getSpeciesInfo()[0][0]
		else:
			self.sciName=query
		
		self.backbone=sp.name_backbone(self.sciName)
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

		self.selection=selection

		self.library=SearchDatabase(user_input,selection)
		# set the input to the first available accession number if the taxon is in the database
		if self.library.inDatabase():
			self.input=self.library.getSpeciesInfo()[1][0]
		# set the input to the query if the taxon is not in the database
		else:
			self.input=user_input
	
	def getGenomeData(self):
		if self.library.inDatabase():
			dataset_response = requests.get(self.API_URL+self.url_seg_accession+self.input+"/dataset_report")
		else:
			dataset_response = requests.get(self.API_URL+self.url_seg_taxon+self.input+"/dataset_report")
		
		dataset_json = dataset_response.json()
		return dataset_json
	
	def getDatasetAttributes(self):
		dataset_json=self.getGenomeData()
		
		try:
			dataset_organism_info = dataset_json['reports'][0]['organism']
			dataset_biosample_attr = dataset_json['reports'][0]['assembly_info']['biosample']['attributes']
		except KeyError:
			dataset_organism_info = None
			dataset_biosample_attr = None
		return dataset_organism_info,dataset_biosample_attr

# class for getting information from Wikipedia
class SearchWikipedia:
	
	def __init__(self,query: str,selection: str):
		import wikipediaapi as wiki
		self.wiki_en=wiki.Wikipedia('CRYtabia (ronja.roesner@uni-oldenburg.de','en')
		
		library=SearchDatabase(query,selection)
		if library.inDatabase():
			self.sciName=library.getSpeciesInfo()[0][0]
		else:
			self.sciName=query

		
	
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
	search_table=SearchDatabase(query.get(),selection.get())
	
	# function for changing the output sentence on vernaculars depending on which are available
	def vernacular_text(engName,gerName):
		if engName==None and gerName==None:
			text_out="There are no vernaculars available."
		elif engName==None and gerName!=None:
			text_out=f"There is no english vernacular available, but the german vernacular is {gerName}."
		elif engName!=None and gerName==None:
			text_out=f"The english vernacular is {engName}. There is no german vernacular available."
		else:
			text_out=f"The english vernacular is {engName}, the german vernacular is {gerName}."
		
		return text_out
	
	# if GBIF search is enabled and an internet connection is available, output search results
	if gbif_state==1 and internetConnection()==True:
		gbif_search=SearchGBIF((query.get()),selection.get())
		gbif_results=gbif_search.getTaxpath()
		gbif_out=f"\n--- Information from GBIF backbone ---\n{gbif_results}\n"
	elif gbif_state==1 and internetConnection()==False:
		gbif_out="\n!! No internet connection available, GBIF search impossible. !!\n"
	elif gbif_state==0:
		gbif_out=""
	
	# if NCBI search is enabled and an internet connection is available, output search results
	if ncbi_state==1 and internetConnection()==True:
		ncbi_search=SearchNCBI((query.get()),selection.get())
		try:
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
		except AttributeError:
			ncbi_out=f"\nNo NCBI information found for biosample {query.get()}\n"
	elif ncbi_state==1 and internetConnection()==False:
		ncbi_out="\n!! No internet connection available, NCBI search impossible. !!\n"
	elif ncbi_state==0:
		ncbi_out=""
	
	# if Wikipedia search is enabled and an internet connection is available, output page summary
	if wiki_state==1 and internetConnection()==True:
		wiki_search=SearchWikipedia(query.get(),selection.get())
		wiki_summary=wiki_search.getSummary()
		wiki_out=f"\n--- Information from Wikipedia page ---\n{wiki_summary}\n"
	elif wiki_state==1 and internetConnection()==False:
		wiki_out="\n!! No internet connection available, Wikipedia search impossible. !!\n"
	elif wiki_state==0:
		wiki_out=""
	
	# if table search is enabled, output information from library
	if table_state==1:
		if selection.get()!="Taxon Group":
			# run if species is available in reference table
			if search_table.inDatabase():
				# get all information for this species
				info_tuple,accList,taxPath,habitats,indexList=search_table.getSpeciesInfo()
				
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
				vern_text=vernacular_text(info_tuple[2], info_tuple[3])
				
				table_list=[
					"\n--- Information from the core library ---\n",
					f"\nSpecies {info_tuple[0]} {info_tuple[1]} found.\n",
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
	if str(query.get())=="":
		return none_text
	else:
		return main_text


def getSciName(query,selection):
	search_table=SearchDatabase(query.get().capitalize(),selection.get())
	if search_table.inDatabase():
		if selection.get()!="Taxon Group":
			out_str=str(search_table.getSpeciesInfo()[0][0])
		else:
			out_str=str(query.get())
	elif not search_table.inDatabase() and selection.get()=="Scientific Name" or selection.get()=="Taxon Group":
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
	# test the functions
	data=SearchDatabase("GCA_001455555.1","Accession Number")
	print(data.inDatabase())
	print(data.getIDX())
	print(data.getSpeciesInfo())
	#print(data2.getTaxgroupInfo())

	print()