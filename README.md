# Webapp Exploit Payloads

A collection of payloads for common webapps and a tool to help
generate them.


## Usage:

To list the available payloads:

	$ ./genpayload.py -L 

To generate one big JavaScript file called `out.js`:

	$ ./genpayload.py -p wordpress/newadmin -o out.js

To list valid parameters:

	$ ./genpayload.py -p wordpress/newadmin -H

To pass the parameters through command line:

	$ ./genpayload.py -p wordpress/newadmin -P usernewpage=http://victimsite/blog/wp-admin/user-new.php

To generate payload for crossdomain.xml exploitation:

	$ ./genpayload.py -p wordpress/newadmin -t swf -P usernewpage=http://victimsite/blog/wp-admin/user-new.php

To generate payload with an html file:

	$ ./genpayload.py -p wordpress/newadmin -t htmljs -P usernewpage=http://victimsite/blog/wp-admin/user-new.php

## Payload types

### JS

Outputs a single JavaScript file that contains all the necessary libraries, such as 
jQuery. This can then be included in your XSS. Can also be compressed if need be. 

### HTMLJS

Creates a directory containing `index.html` and the included libraries. The html
file contains the payload JavaScript. 

### SWF

Creates a directory containing `index.html` and all libraries, including the
files needed for flXHR.

### HTML5CORS

Similar to HTMLJS but makes the code work cross-domain thanks to HTML5 
cross origin resource sharing. The victim server needs to trust the attacker server
through the `Access-Control-Allow-Origin: http://attackersite` header and also the header
`Access-Control-Allow-Credentials: true` needs to be set.

## Directory structure

### /bin

This is where `genpayload.py` resides.

### /src

This is where all the code is generated from. 

#### /src/config

A directory containing general configuration files. The file
`settings.ini` is used to store one `statusurl` for all.  

#### /src/includes

A directory containing files that are included by the payloads. For example,
jquery and its plugins are stored here. There is also a common.js which 
contains functions that are commonly used across most payloads. 

#### /src/payloads

This directory contains all the payloads. The subdirectories under this one
are named after the product that they exploit, for example, wordpress. 
There is one directory called generic where generic payloads are stored. 

Each payload has to contain a `config.ini` file that specifies the filename
of the payload, other dependencies and default variable values. 

## Configuration files

Each `config.ini` has the following sections:

- `[config]` where all variables that do not fit anywhere else and their values are stored 
- `[locations]` where all URLs are stored .. these URLs become variables within the payload 
- `[dependencies]` which contains the following options:
	- `script` which is the filename of the payload
	- `jquery` which is the filename of the jquery script
	- `include` which is any other JavaScript files to be included in the final payload
- `[about]` which contains information about the script including:
	- `description` which is a summary of what the payload does
- `[includes]` which contains variable names whose values include filenames for files 
  that are read by the payload generator and then their contents end up a JavaScript 
  string in the payload. Useful for placing that backdoor php code