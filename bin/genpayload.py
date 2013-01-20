#!/usr/bin/env python
# encoding: utf-8
"""
genpayload.py

Created by Sandro Gauci (sandro@enablesecurity.com) on 2012-05-11.
Copyright (c) 2012 Sandro Gauci. All rights reserved.
"""

import sys
import argparse     
import os
import logging    
import json
from lib import *


help_message = '''
Generates web application exploitation payloads based on existent template
'''                 

def getargs():
	parser = argparse.ArgumentParser(description=help_message)
	parser.add_argument('-p','--payloads', help='name of payload', action="append", default=[])
	parser.add_argument('-o','--output', help='output filename or directory name')
	parser.add_argument('-P','--parameters', action="append", default=[],
						help='set variables in the form variable=value (see the ini files for the useful variable names)')
	parser.add_argument('-t','--payloadtype',help="Type of output, can be js, swf or htmljs",choices=['js','swf','htmljs','html5cors'],default='js')
	parser.add_argument('-H','--payloadhelp', action='store_true', help='Lists parameters for the particular payload and quit')
	parser.add_argument('-L','--listpayloads', action='store_true',help='List available payloads')
	args = parser.parse_args()
	if not (args.payloads or args.listpayloads or args.payloadhelp):
		parser.error('Please specify either -p or -L as option')
	if (args.payloadtype in ['swf','htmljs']) and (not args.output):
		parser.error('Please specify an output location for your swf or htmljs')
	return args

def main(argv=None):
	try:		
		args = getargs()   
		if args.payloadhelp:
			r = listpayloadparams(args)
		elif args.listpayloads:
			r = listpayloads(args)
		elif args.payloads:
			if args.payloadtype == 'js':
				r = generatejspayload(args)
				output(r,args)
			elif args.payloadtype in ['swf','htmljs','html5cors']:
				r = generatehtmlpayload(args)
	except Exception as e:
		if DEBUG:
			raise e
		else:
			print (str(e))
	return(0)

if __name__ == "__main__":
	sys.exit(main())
