#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 14:33:49 2024

@author: Ronja Rösner
@source: https://medium.com/@linuxadminhacks/creating-a-gui-autocomplete-app-with-tkinter-and-trie-tree-a066936aa17e
"""

from collections import defaultdict
import os, sqlite3

from setup import DB_FILE

# establishes connection to the database
db_conn=sqlite3.connect(DB_FILE)
# creates new cursor object to interact with the database
cursor=db_conn.cursor()

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


def load_words():

	try:
		acc_numbers=cursor.execute("SELECT AccessionNumber FROM ids").fetchall()
		acc_numbers=set([acc[0] for acc in acc_numbers])
		
		genome_ids=cursor.execute("SELECT IDX FROM ids").fetchall()
		genome_ids=set([str(idx[0]) for idx in genome_ids])
		
		sci_names=cursor.execute("SELECT ScientificName FROM taxonomy").fetchall()
		sci_names=set([name[0] for name in sci_names])
		
		taxon_groups=cursor.execute("SELECT Kingdom, Phylum, Class, taxOrder, Family, Genus FROM taxonomy").fetchall()
		taxon_groups=set([group for group_tup in taxon_groups for group in group_tup])

		return acc_numbers, genome_ids, sci_names, taxon_groups
	except:
		return "", "", "", ""


def getSuggestions(selection):
	acc_numbers, genome_ids, sci_names, taxon_groups = load_words()
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
	print(getSuggestions("Accession Number"))
