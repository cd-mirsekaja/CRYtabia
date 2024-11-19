#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 14:33:49 2024

@author: Ronja Rösner
@source: https://medium.com/@linuxadminhacks/creating-a-gui-autocomplete-app-with-tkinter-and-trie-tree-a066936aa17e
"""

from collections import defaultdict
import pandas as pd


class TrieNode:
	def __init__(self):
		self.children = defaultdict(TrieNode)
		self.is_word = False


class Trie:
	def __init__(self):
		self.root = TrieNode()

	def insert(self, word):
		node = self.root
		try:
			for char in word:
				node = node.children[char]
			node.is_word = True
		except TypeError:
			pass

	def search(self, prefix):
		node = self.root
		suggestions = []
		for char in prefix:
			if char not in node.children:
				return suggestions
			node = node.children[char]
		self._find_suggestions(node, prefix, suggestions)
		return suggestions

	def _find_suggestions(self, node, prefix, suggestions):
		if node.is_word:
			suggestions.append(prefix)
		for char, child in node.children.items():
			self._find_suggestions(child, prefix + char, suggestions)


def load_words(filename):
	table=pd.read_excel(filename,usecols='A:O')
	taxgroup_table=pd.read_excel(filename,usecols='C:H, O')
	
	acc_numbers=set(table['AccessionNumber'])
	
	genome_ids=set(table['Index'])
	genome_ids_str=set()
	for item in genome_ids:
		genome_ids_str.add(str(item))
	
	sci_names=set(table['ScientificName'])
	
	taxon_groups=set()
	for column_name,column in taxgroup_table.items():
		taxon_groups.update(taxgroup_table[column_name])
	
	return acc_numbers, genome_ids_str, sci_names, taxon_groups


def getSuggestions(selection):
	acc_numbers, genome_ids, sci_names, taxon_groups = load_words("infolib.xlsx")
	trie = Trie()
	
	if selection=="Accession Number":
		words=acc_numbers
	elif selection=="Genome Index":
		words=genome_ids
	elif selection=="Scientific Name":
		words=sci_names
	elif selection=="Taxon Group":
		words=taxon_groups
	
	for word in words:
		trie.insert(word)
	
	return trie



if __name__=='__main__':
	table=table=pd.read_excel('infolib.xlsx',usecols='A:O')
	
	sci_names=set(table['ScientificName'])
	
	genome_ids=set(table['Index'])
	genome_ids_str=set()
	for item in genome_ids:
		genome_ids_str.add(str(item))
	
	indices=set(table['Index'])
	indices_str=set()
	for item in indices:
		indices_str.add(str(item))
	
	print(indices_str)
