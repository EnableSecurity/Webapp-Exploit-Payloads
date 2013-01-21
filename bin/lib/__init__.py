#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Sandro Gauci on 2013-01-13.
Copyright (c) 2013 EnableSecurity. All rights reserved.
"""

import sys
import argparse     
import os
import logging    
import json
import shutil


DEBUG = True

major_version = sys.version_info[0]
if major_version == 2:
	from ConfigParser import ConfigParser, NoSectionError, ParsingError
	import urlparse
elif major_version == 3:
	from configparser import ConfigParser, NoSectionError, ParsingError
	from urllib.parse import urlparse
else:
	print('python version needs to be 2 or 3')
	sys.exit(-1)


def getinclude(path,include):
	includespath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'..','src','includes'))
	fn = os.path.join(includespath,include)
	fn2 = os.path.join(path,include)	
	if os.path.exists(fn):
		f=open(fn,'rb')
		buff = f.read().decode('utf-8')
		f.close()
	else:
		f=open(fn2,'rb')
		buff = f.read().decode('utf-8')
		f.close()
	return buff + "\r\n\r\n"
   

def output(payload,args):
	if args.output:
		f = open(args.output,'wb')
	else:
		f = sys.stdout
	f.write(payload.encode('utf-8'))
	f.close()




def getparameters(args):	
	conf = dict()	
	jsvarsdict = dict()
	jsvars = str()
	locationsdict = dict()
	includes = str()
	statusurl = str()
	payloadfiles = set()
	includesfn = set()
	jqueryadded = False
	jqueryinclude = str()
	jqueryfn = str()
	
	basepath = os.path.dirname(os.path.abspath(sys.argv[0]))
	
	defaultsettingsfn = os.path.abspath(os.path.join(basepath,'..','src','config','settings.ini'))
	defaultsettings = ConfigParser()
	if not os.path.exists(defaultsettingsfn):
		raise Exception('settings.ini not found')
	defaultsettings.read(defaultsettingsfn)
	try:
		statusurl = defaultsettings.get('status','url')
	except (NoSectionError,ParsingError) as e:
		raise Exception('Invalid settings.ini')

	
	
	for payload in args.payloads:
		path = os.path.abspath(os.path.join(basepath,'..','src','payloads',payload))
		configfn = os.path.join(path,'config.ini')
		config = ConfigParser()
		config.read(configfn)

		mainconfig = config.items('config')	
		for kv in mainconfig:
			k,v = kv
			jsvarsdict[k] = v

		locationsconfig = config.items('locations')
		for kv in locationsconfig:
			k,v = kv
			jsvarsdict[k] = v
			locationsdict[k]=v

		if not jqueryadded:
			if config.has_option('dependencies','jquery'):
				jqueryfn = config.get('dependencies','jquery')
				jqueryinclude = getinclude(path,jqueryfn)
				jqueryadded = True
				jqueryfn=jqueryfn

		for include in config.get('dependencies','include').split():
			includesfn.add(include)
		
		## this allows files to be included as javascript variables
		if config.has_section('includes'):
			for includevar in config.options('includes'):
				includefn = config.get('includes',includevar)
				jsvarsdict[includevar] = getinclude(path,includefn).strip()

		payloadfiles.add(os.path.join(path,config.get('dependencies','script')))
		
		if 'status' in config.sections():
			if config.has_option('status','url'):
				statusurl = config.get('status','url')

	for param in args.parameters:
		k,v = param.split('=',1)
		jsvarsdict[k] = v
		if k in locationsdict:
			locationsdict[k] = v

	for k,v in jsvarsdict.items():
		jsvars += '%s = %s;\r\n' % (k,json.dumps(v))


	for includefn in includesfn:
		includes += getinclude(path,includefn)		

	jsvarsdict['statusurl'] = statusurl

	conf['jsvarsdict'] = jsvarsdict
	conf['jsvars'] = jsvars
	conf['includes'] = includes
	conf['statusurl'] = statusurl	
	conf['payloadfiles'] = payloadfiles
	conf['locationsdict'] = locationsdict
	conf['includesfn'] = includesfn
	conf['jqueryinclude'] = jqueryinclude
	conf['jqueryfn'] = jqueryfn
	
	return conf
	

def generateswfpayload(args):
	conf = getparameters(args)
	firsturl = conf['locationsdict'].values()[0]
	payload = str()
	urlsplit = urlparse.urlsplit(firsturl)
	if len(urlsplit.scheme) == 0:
		raise Exception('Please pass a full URL rather than a relative path for the SWF output')
		
	baseurl = urlsplit.scheme + '://' + urlsplit.netloc
	for payloadfile in conf['payloadfiles']:
		f = open(payloadfile,'rb')
		payload += f.read().decode('utf-8') + '\r\n\r\n'
		f.close()
	
	codeToAdd = "jQuery.flXHRproxy.registerOptions(%s,{noCacheHeader: false,xmlResponseText:false});\r\njQuery.ajaxSetup({transport:'flXHRproxy'});" % (json.dumps(baseurl))
	payloadstr = '\r\n\r\n'.join([conf['jsvars'],codeToAdd,payload])
	return(payloadstr)
	

def generatejspayload(args):	
	conf = getparameters(args)
	payload = str()
	for payloadfile in conf['payloadfiles']:
		f = open(payloadfile,'rb')
		payload += f.read().decode('utf-8') + '\r\n\r\n'
		f.close()
	if args.payloadtype == 'htmljs':
		payloadstr = '\r\n\r\n'.join([conf['jsvars'],payload])	
	else:
		payloadstr = '\r\n\r\n'.join([conf['jsvars'],conf['jqueryinclude'],conf['includes'],payload])	
	return(payloadstr)

def generatehtmlpayload(args):
	conf = getparameters(args)	
	filestocopy = list()
	if args.payloadtype == 'swf':
		filestocopy = ['swf/checkplayer.js','swf/flXHR.js', 'jquery.js','common.js',
						'swf/flXHR.swf','swf/flensed.js','swf/jquery.flXHRproxy.js',
						'swf/swfobject.js','swf/updateplayer.swf','swf/flCookie.js',
						'swf/flCookie.swf']
		filestoinclude = ['flXHR.js','jquery.js','jquery.flXHRproxy.js','common.js']
		payloadstr = generateswfpayload(args)
	elif args.payloadtype in ['html5cors','htmljs']:
		filestocopy = [conf['jqueryfn']]
		filestocopy.extend(conf['includesfn'])		
		filestoinclude = map(lambda ctx: os.path.split(ctx)[1],filestocopy)
		if args.payloadtype == 'html5cors':
			payloadstr = generatehtmlwithcredspayload(args)		
		elif args.payloadtype == 'htmljs':
			payloadstr = generatejspayload(args)
	else:
		raise Exception('Should not be here') 

	htmloutput = '<html>\r\n'
	for jsfn in filestoinclude:
		htmloutput += '<script src="%s"></script>\r\n'%jsfn

	if not os.path.exists(args.output):
		os.makedirs(args.output)

	includespath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'..','src','includes'))
	for fn in filestocopy:
		shutil.copy(os.path.join(includespath,fn),args.output)

	htmloutput += '<script src="payload.js"></script>\r\n</html>'
	outfile=open(os.path.join(args.output,'index.html'),'w')
	outfile.write(htmloutput.encode('utf-8'))
	outfile.close()
	outfile2=open(os.path.join(args.output,'payload.js'),'w')
	outfile2.write(payloadstr.encode('utf-8'))
	outfile2.close()

def generatehtmlwithcredspayload(args):
	conf = getparameters(args)
	payload = str()
	for payloadfile in conf['payloadfiles']:
		f = open(payloadfile,'rb')
		payload += f.read().decode('utf-8') + '\r\n\r\n'
		f.close()
	codeToAdd = '$.ajaxSetup({\n    xhrFields: {\n       withCredentials: true\n    },\n    crossDomain: true\n});'
	payloadstr = '\r\n\r\n'.join([conf['jsvars'],codeToAdd,payload])
	return(payloadstr)
	

def listpayloads(args):
	payloadsdir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'..','src','payloads'))
	for root, dirs, files in os.walk(payloadsdir):
		if 'config.ini' in files:
			configfn = os.path.join(root,'config.ini')
			config = ConfigParser()
			try:
				config.read(configfn)
				mainconfig = config.items('about')	
			except NoSectionError as e:
				raise Exception('Invalid config.ini. Missing [about] section')
			tmpgroupdir,payloadname = os.path.split(root)
			groupname = os.path.split(tmpgroupdir)[1]
			print("Payload: %s/%s" % (groupname,payloadname))
			for kv in mainconfig:
				print("\t%s:\t%s" % kv)
			print("\r\n")





def listpayloadparams(args):	
	for payload in args.payloads:		
		path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'..','src','payloads',payload))
		configfn = os.path.join(path,'config.ini')
		if not os.path.exists(configfn):
			raise Exception('Invalid payload directory: %s' % path)
		config = ConfigParser()
		try:
			config.read(configfn)
			mainconfig = config.items('config')	
			locationsconfig = config.items('locations')	
		except NoSectionError as e:
			raise Exception('Invalid config.ini. Missing [config] or [locations] section')
		print("Default parameters for %s:\r\n" % payload)
		for kv in mainconfig:
			print("\tparameter: %s\tdefault: %s" % kv)
		for kv in locationsconfig:
			print("\tparameter: %s\tdefault: %s" % kv)
		print('\r\n')