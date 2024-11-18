#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 00:11:50 2024

@author: privatstudium

api endpoint infos at https://www.ncbi.nlm.nih.gov/datasets/docs/v2/api/rest-api/
"""
import requests

acc_numbers = [
	"GCF_905163445.1",
	"GCF_010993605.1",
	"GCA_903684865.1",
	"GCA_903684855.2"
	]

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




if __name__ == '__main__':
	ncbi_search = SearchNCBI(acc_numbers[0],"Accession Number")
	#dataset_json = ncbi_search.getGenomeData()
	"""
	print(dataset_json['reports'][0].keys())
	print("\n\n")
	
	print(dataset_json['reports'][0]['assembly_info']['biosample'].keys())
	try:
		print(dataset_json['reports'][0]['assembly_info']['biosample']['geo_loc_name'])
	except KeyError:
		pass
	
	print("\n\n")
	"""
	
	organism_info,biosample_attributes=ncbi_search.getDatasetAttributes()
	
	print("\nOrganism Report:")
	for key, item in organism_info.items():
		print(f"{key.capitalize()}: {item}")
	
	print("\nAvailable information for this biosample:")
	for list_obj in biosample_attributes:
		for key, item in list_obj.items():
			if key=="name":
				print(item,end=" -> ")
			elif key=="value":
				print(f"{item}")









