#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 18:20:52 2024

@author: Ronja Rösner

Main script for CRYtabia.
"""



#from setup import VERSION,NAME

# import custom functions for constructing interface
import makeInterface

# function for constructing the application
def main():
	main_window=makeInterface.MainInterface('CRYtabia','0.7.0')
	main_window.focus_set()
	main_window.mainloop()


if __name__ == "__main__":
	main()

