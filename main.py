#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 18:20:52 2024

@author: Ronja Rösner

Main script for CRYtabia.
"""

import sqlite3
# import custom functions for constructing interface
from mainInterface import MainInterface

# import the program name and version from the setup file
from setup import NAME, VERSION, DB_FILE

# import function for creating an empty database if nessecary
from GeDaMa.src.createDatabase import createNewDatabase

# turn the imported program info into strings
program_name=str(NAME[0])
program_version=str(VERSION[0])

# function for constructing the application
def main():
	createNewDatabase(DB_FILE)
	
	main_window=MainInterface(
		program_name,
		program_version
		)
	
	main_window.focus_set()
	main_window.mainloop()


if __name__ == "__main__":
	main()

