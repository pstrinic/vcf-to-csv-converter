#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
"""
	VcfToCsvConverter v0.2 - Converts VCF/VCARD files into CSV
	Copyright (C) 2009 Petar Strinic (http://petarstrinic.com)
	Contributor -- Dave Dartt

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.	If not, see <http://www.gnu.org/licenses/>.

"""
#modified 11-23-09
#added glob, os
import os
import re
import sys
import glob
import codecs
import getopt

class VcfToCsvConverter:
	def __outputQuote(self):
		if self.quote == True:
			self.output += '"'

	def __output(self, text):
		self.__outputQuote();
		self.output += text
		self.__outputQuote();
		self.output += self.delimiter

	def __trace(self, text):
		if self.trace == True:
			print text

	def __resetRow(self):
		self.addressCount = { 'HOME' : 1, 'WORK' : 1 }
		self.telephoneCount = { 'HOME PHONE' : 1, 'WORK PHONE' : 1, 'MOBILE PHONE' : 1, 'HOME FAX' : 1, 'WORK FAX' : 1 }
		self.emailCount = { 'HOME' : 1, 'WORK' : 1 }
		array = {}
		for k in self.columns:
			array[ k ] = '';
		return array

	def __setitem__(self, k, v):
		self.data[ k ] = v

	def __getitem__(self, k):
		return self.data[ k ]

	def __endLine(self):
		for k in self.columns:
			try:
				self.__output(self.data[ k ])
			except KeyError:
				self.output += self.delimiter
		self.output += "\r\n"
		self.data = self.__resetRow()

	#added 11-23-09 
	#retrieve the list of vcard file names within the directory specified
	def __getfilenames(self):
		try:
			if os.path.isdir(self.inputPath):
				self.inputFileArray = glob.glob(os.path.join(self.inputPath, '*.vc[sf]') )
			else:
				print "Invalid path please try again"
				usage()
				sys.exit(2)
		except IOError:
			print "Directory is empty or does not contain any vcard format files."
			sys.exit(2)

	#modified 11-23-09
	#if -i option used execute on one filename 
	#if -p option used execute parser per filename found
	def __parseFile(self):
		if self.inputPath == None and self.inputFile != None:
			try:
				print "Processing .... %s" % (self.inputFile)
				inFile = codecs.open(self.inputFile, 'r', 'utf-8', 'ignore')
				theLine = inFile.readline()
				for theLine in inFile:
					self.__parseLine(theLine)
				inFile.close()
			except IOError:
				print "error opening file during read operation: %s" % (self.inputFile)
				sys.exit(2)
			outFile = codecs.open(self.outputFile, 'w', 'utf-8', 'ignore')
			outFile.write(self.output)
			outFile.close()
		elif self.inputFile == None:
			self.__getfilenames()
			outFile = codecs.open(self.outputFile, 'w', 'utf-8', 'ignore')
			for NewFileName in self.inputFileArray:
				try:
					print "Processing .... %s\n" % (NewFileName)
					inFile = codecs.open(NewFileName, 'r', 'utf-8', 'ignore')
					theLine = inFile.readline()
					for theLine in inFile:
						self.__parseLine(theLine)
					inFile.close()
				except IOError:
					print "error opening file during read operation via path: %s\n" % (NewFileName)
					sys.exit(2)
			outFile.write(self.output)
			outFile.close()

	def __parseLine(self, theLine):
		theLine = theLine.strip()
		if len(theLine) < 1:
			pass
		elif re.match('^BEGIN:VCARD', theLine):
			pass
		elif re.match('^END:VCARD', theLine):
			self.__endLine()
		else:
			self.__processLine(theLine.split(":"))

	def __processLine(self, pieces):
		self.__trace("pieces: %s " % pieces)
		pre = pieces[0].split(";")
		self.__trace("pieces pre: %s " % pre)
		self.__trace("item pieces pre0: %s " % pre[0])

		self.__trace("item match: %s " % re.match('item.*', pre[0].split(".")[0], re.I))
		if re.match('item.*', pre[0].split(".")[0], re.I) != None:
			try:
				self.__trace("item pieces pre: %s " % pre[0].split("."))
				self.__trace("item pieces pre0: %s " % pre[0].split(".")[1])
				pre[0] = pre[0].split(".")[1]
			except IndexError:
				self.__trace("item pre0 split: %s " % pre[0].split("."));

		"""
		1x N  Name  a structured representation of the name of the person, place or thing associated with the vCard object.
		1x FN  Formatted Name the formatted name string associated with the vCard object
		LS PHOTO  Photograph an image or photograph of the individual associated with the vCard
		1x BDAY   Birthday  date of birth of the individual associated with the vCard
		6x ADR Delivery Address  a structured representation of the physical delivery address for the vCard object
		NS LABEL  Label Address  addressing label for physical delivery to the person/object associated with the vCard
		15x TEL   Telephone  the canonical number string for a telephone number for telephony communication with the vCard object
		6x EMAIL  Email  the address for electronic mail communication with the vCard object
		1x MAILER  Email Program (Optional)  Type of email program used
		1x TZ  Time Zone  information related to the standard time zone of the vCard object
		1x GEO Global Positioning The property specifies a latitude and longitude
		1x TITLE  Title  specifies the job title, functional position or function of the individual associated with the vCard object within an organization (V. P. Research and Development)
		1x ROLE   Role or occupation the role, occupation, or business category of the vCard object within an organization (eg. Executive)
		LS LOGO   Logo  an image or graphic of the logo of the organization that is associated with the individual to which the vCard belongs
		1x AGENT  Agent  information about another person who will act on behalf of the vCard object. Typically this would be an area administrator, assistant, or secretary for the individual
		1x ORG Organization Name or Organizational unit  the name and optionally the unit(s) of the organization associated with the vCard object. This property is based on the X.520 Organization Name attribute and the X.520 Organization Unit attribute
		1x NOTE   Note  specifies supplemental information or a comment that is associated with the vCard
		1x REV Last Revision  combination of the calendar date and time of day of the last update to the vCard object
		NS SOUND  Sound  By default, if this property is not grouped with other properties it specifies the pronunciation of the Formatted Name property of the vCard object.
		1x URL URL   An URL is a representation of an Internet location that can be used to obtain real-time information about the vCard object
		1x UID Unique Identifier  specifies a value that represents a persistent, globally unique identifier associated with the object
		NA VERSION Version   Version of the vCard Specification
		NS KEY Public Key the public encryption key associated with the vCard object
		X-ABUID property  string Apple Address Book UUID for that entry
		X-ANNIVERSARY  property  YYYY-MM-DD arbitrary anniversary, in addition to BDAY = birthday
		X-ASSISTANT property  string assistant name (instead of Agent)
		X-MANAGER  property  string manager name
		X-SPOUSE   property  string spouse name
		1x X-AIM  property  string Instant Messaging (IM) contact information; TYPE parameter as for TEL (I.e. WORK/HOME/OTHER)
		1x X-ICQ  property  string "
		1x X-JABBER   property  string "
		1x X-MSN  property  string "
		1x X-YAHOO property  string "
		1x X-SKYPE-USERNAME   property  string "
		1x X-GADUGADU  property  string "
		1x X-GROUPWISE property  string "
		X-MS-IMADDRESS  property  string " (IM address in VCF attachment from Outlook (right click Contact, Send Full Contact, Internet Format.)
		X-MS-CARDPICTURE   property  string Works as PHOTO or LOGO. Contains an image of the Card in Outlook.
		X-PHONETIC-FIRST-NAME, X-PHONETIC-LAST-NAME property  string alternative spelling of name, used for Japanese names by Android and iPhone introduced and used by Mozilla, also used by Evolution (software)
		X-MOZILLA-HTML  property  TRUE/FALSE mail recipient wants HTML email introduced and used by Evolution (software)
		X-EVOLUTION-ANNIVERSARY property  YYYY-MM-DD arbitrary anniversary, in addition to BDAY = birthday
		X-EVOLUTION-ASSISTANT  property  string assistant name (instead of Agent)
		X-EVOLUTION-BLOG-URL   property  string/URL blog URL
		X-EVOLUTION-FILE-AS property  string file under different name (in addition to N = name components and FN = full name
		X-EVOLUTION-MANAGER property  string manager name
		X-EVOLUTION-SPOUSE  property  string spouse name
		X-EVOLUTION-VIDEO-URL  property  string/URL video chat address
		X-EVOLUTION-CALLBACK   TEL TYPE parameter value  -  callback phone number
		X-EVOLUTION-RADIO  TEL TYPE parameter value  -  radio contact information
		X-EVOLUTION-TELEX  TEL TYPE parameter value  -  Telex contact information
		X-EVOLUTION-TTYTDD  TEL TYPE parameter value  -  TTY TDD contact information
		"""
		if pre[0] == 'VERSION':
			self.__trace("version: %s " % pieces[1])
			if pieces[1] != '3.0':
				self.data['WARNING'] = "Unexpected VCARD version: %s. " % pieces[1]
				self.__trace("Unexpected VCARD version: %s. " % pieces[1])
		elif pre[0] == 'N':
			self.__processName(pre, pieces[1])
		elif pre[0] == 'FN':
			self.__processSingleValue('FORMATTED NAME', pre, pieces[1])
		elif pre[0] == 'NICKNAME':
			self.__processSingleValue('NICKNAME', pre, pieces[1])
		elif pre[0] == 'TITLE':
			self.__processSingleValue('TITLE', pre, pieces[1])
		elif pre[0] == 'BDAY':
			self.__processSingleValue('BIRTHDAY', pre, pieces[1])
		elif pre[0] == 'ORG':
			self.__processSingleValue('ORGANIZATION', pre, pieces[1])
		elif pre[0] == 'ROLE':
			self.__processSingleValue('ROLE', pre, pieces[1])
		elif pre[0] == 'GEO':
			self.__processSingleValue('GEOCODE', pre, pieces[1])
		elif pre[0] == 'MAILER':
			self.__processSingleValue('MAILER', pre, pieces[1])
		elif pre[0] == 'TZ':
			self.__processTimeZone(pieces[1:])
		elif pre[0] == 'ADR':
			self.__processAddress(pre, pieces[1])
		elif pre[0] == 'LOGO':
			self.__processImageUrl('LOGO URL', pre, pieces[1:])
		elif pre[0] == 'PHOTO':
			self.__processImageUrl('PHOTO', pre, pieces[1:])
		elif pre[0] == 'TEL':
			self.__processTelephone(pre, pieces[1:])
		elif pre[0] == 'EMAIL':
			self.__processEmail(pre, pieces[1:])
		elif pre[0] == 'AGENT':
			self.__processAgent(pre, pieces[1:])
		elif pre[0] == 'NOTE':
			self.__processSingleValue('NOTE', pre, pieces[1])
		elif pre[0] == 'REV':
			self.__processSingleValue('REV', pre, pieces[1])
		elif pre[0] == 'URL':
			self.__processSingleValue('URL', pre, ":".join(pieces[1:]))
		elif pre[0] == 'UID':
			self.__processSingleValue('UID', pre, pieces[1])
		elif pre[0] == 'X-AIM':
			self.__processSingleValue('AIM', pre, pieces[1])
		elif pre[0] == 'X-ICQ':
			self.__processSingleValue('ICQ', pre, pieces[1])
		elif pre[0] == 'X-JABBER':
			self.__processSingleValue('JABBER', pre, pieces[1])
		elif pre[0] == 'X-MSN':
			self.__processSingleValue('MSN', pre, pieces[1])
		elif pre[0] == 'X-YAHOO':
			self.__processSingleValue('YAHOO', pre, pieces[1])
		elif pre[0] == 'X-SKYPE-USERNAME':
			self.__processSingleValue('SKYPE', pre, pieces[1])
		elif pre[0] == 'X-GADUGADU':
			self.__processSingleValue('GADUGADU', pre, pieces[1])
		elif pre[0] == 'X-GROUPWISE':
			self.__processSingleValue('GROUPWISE', pre, pieces[1])

	def __processEmail(self, pre, p):
		self.__trace("__processEmail: %s %s" % (pre, p))
		hwm = "HOME"
		if re.search('work',(",").join(pre[1:]), re.I) != None:
			hwm = "WORK"
		self.__trace("__email type: %s" % hwm)
		if self.emailCount[hwm] <= self.maxEmails:
			self.data["%s EMAIL %s" % (hwm, self.emailCount[hwm])] = p[0]
			self.__trace("__email %s %s: %s" % (hwm, self.emailCount[hwm], p[0]))
			self.emailCount[hwm] += 1
		else:
			self.data['WARNING'] += ("Maximum number of %s emails reached, discarded: %s. " % (hwm, p[0]))

	def __processTelephone(self, pre, p):
		self.__trace("__processTelephone: %s %s" % (pre, p))
		telephoneType = "PHONE"
		hwm = "HOME"
		if re.search('work',(",").join(pre[1:]), re.I) != None:
			hwm = "WORK"
		elif re.search('cell',(",").join(pre[1:]), re.I) != None:
			hwm = "MOBILE"

		if re.search('fax',(",").join(pre[1:]), re.I) != None:
			telephoneType = "FAX"

		self.__trace("_telephone number = %s" % p[0])
		self.__trace("_telephone type: %s" % "%s %s %s" % (hwm, telephoneType, self.telephoneCount["%s %s" % (hwm, telephoneType)]))

		if self.telephoneCount[("%s PHONE" % hwm)] <= self.maxTelephones:
			self.data["%s %s %s" % (hwm, telephoneType, self.telephoneCount["%s %s" % (hwm, telephoneType)])] = p[0]
			self.telephoneCount["%s %s" % (hwm, telephoneType)] += 1
		else:
			self.data['WARNING'] += ("Maximum number of %s telephones reached, discarded: %s. " % (hwm, p[0]))

	def __processAgent(self, pre, p):
		self.__trace("__processAgent: %s %s" % (pre, p))
		self.data["AGENT"] = ":".join(p)
		self.__trace("_agent: %s" % (self.data["AGENT"]))

	def __processImageUrl(self, imageType, pre, p):
		self.__trace("__processImageUrl: %s %s" % (pre, p))
		try:
			if pre[1].lower() == 'value=uri'.lower():
				self.data[imageType] = ":".join(p)
			else:
				self.__trace("_imageUrl: Not a URL. skipping")
		except ValueError:
			self.__trace("_imageUrl: Not a URL. skipping")
		self.__trace("_Url: %s" % (self.data[imageType]))


	def __processAddress(self, pre, p):
		self.__trace("__processAddress: %s %s" % (pre, p))
		self.__trace("_ADDRESS: %s" % (p))
		try:
			(a, b, address, city, state, zip, country ) = p.split(";")
		except ValueError:
			(a, b, address, city, state, zip ) = p.split(";")
			country = '';

		addressType = "HOME"
		try:
			(a,addressTypes) = pre[1].split("=");
			self.__trace("_addressTypes: %s " % addressTypes)
			if "work" in (addressTypes.lower()).split(","):
				self.__trace("_work address");
				addressType = "WORK"
		except ValueError:
			self.__trace("_home address")

		self.__trace(self.addressCount);
		self.__trace(self.addressCount[addressType]);

		if self.addressCount[addressType] <= self.maxAddresses:
			self.data["%s ADDRESS %s" % (addressType, self.addressCount[addressType])] = address
			self.data["%s CITY %s" % (addressType, self.addressCount[addressType])] = city
			self.data["%s STATE %s" % (addressType, self.addressCount[addressType])] = state
			self.data["%s ZIP %s" % (addressType, self.addressCount[addressType])] = zip
			self.data["%s COUNTRY %s" % (addressType, self.addressCount[addressType])] = country
			self.addressCount[addressType] += 1
		else:
			self.data['WARNING'] += ("Maximum number of %s addresses reached, discarded: %s. " % (addressType, p))

	def __processTimeZone(self, p):
		self.__trace("__processTimeZone: %s" % (p))
		self.__trace("_TIMEZONE: %s:%s" % (p[0],";".join(p[1:])))
		self.data['TIMEZONE'] = ("%s:%s" % (p[0],";".join(p[1:])))

	def __processValueList(self, valueType, pre, p, delimiter):
		self.__trace("__processValueList: %s %s %s %s" % (valueType, pre, p, delimiter))
		self.__trace("_%s: %s" % (valueType,p))
		self.data[valueType] = delimiter.join(p);

	def __processSingleValue(self, valueType, pre, p):
		self.__trace("__processSingleValue: %s %s %s" % (valueType, pre, p))
		self.__trace("_%s: %s" % (valueType,p))
		self.data[valueType] = p

	def __processName(self, pre, p):
		self.__trace("__processName: %s %s" % (pre, p))
		try:
			( ln, fn, mi, pr, po ) = p.split(";")
			self.__trace("_name: %s %s %s %s %s" % (pr, fn, mi, ln, po))
			self.data['NAME PREFIX'] = pr
			self.data['NAME FIRST'] = fn
			self.data['NAME MIDDLE'] = mi
			self.data['NAME LAST'] = ln
			self.data['NAME POSTFIX'] = po
		except ValueError:
			if self.data['FORMATTED NAME'] == None:
				self.data['FORMATTED NAME'] = p
				self.data['WARNING'] += "Invalid format for N tag, using as FN instead. "
				self.__trace("_name: Invalid format for N tag, using as FN instead. %s" % p)

	#modified 11-23-09
	#added inputFilePath variable and initialize into class
	#added initialize of inputFileArray variable into class 
	def __init__(self, inputFileName, inputFilePath, outputFileName, delimiter, quote, trace):
		self.trace = trace
		self.addressCount = { 'HOME' : 1, 'WORK' : 1 }
		self.telephoneCount = { 'HOME PHONE' : 1, 'WORK PHONE' : 1, 'MOBILE PHONE' : 1, 'HOME FAX' : 1, 'WORK FAX' : 1 }
		self.emailCount = { 'HOME' : 1, 'WORK' : 1 }
		self.data = {}
		self.quote = quote
		self.delimiter = delimiter
		self.output = ''
		self.inputFile = inputFileName
		self.inputPath = inputFilePath
		self.inputFileArray = None
		self.outputFile = outputFileName
		self.maxAddresses = 3
		self.maxTelephones = 3
		self.maxEmails = 3
		self.columns = (
			'WARNING',
			'FORMATTED NAME', 'NAME PREFIX', 'NAME FIRST', 'NAME MIDDLE', 'NAME LAST',
				'NAME POSTFIX', 'NICKNAME', 'BIRTHDAY', 'PHOTO',
			'ORGANIZATION', 'TITLE', 'ROLE', 'LOGO URL',
			'MAILER',
			'HOME ADDRESS 1', 'HOME CITY 1', 'HOME STATE 1', 'HOME ZIP 1',
			'HOME ADDRESS 2', 'HOME CITY 2', 'HOME STATE 2', 'HOME ZIP 2',
			'HOME ADDRESS 3', 'HOME CITY 3', 'HOME STATE 3', 'HOME ZIP 3',
			'WORK ADDRESS 1', 'WORK CITY 1', 'WORK STATE 1', 'WORK ZIP 1',
			'WORK ADDRESS 2', 'WORK CITY 2', 'WORK STATE 2', 'WORK ZIP 2',
			'WORK ADDRESS 3', 'WORK CITY 3', 'WORK STATE 3', 'WORK ZIP 3',
			'HOME PHONE 1', 'HOME PHONE 2', 'HOME PHONE 3',
			'WORK PHONE 1', 'WORK PHONE 2', 'WORK PHONE 3',
			'HOME FAX 1', 'HOME FAX 2', 'HOME FAX 3',
			'WORK FAX 1', 'WORK FAX 2', 'WORK FAX 3',
			'MOBILE PHONE 1', 'MOBILE PHONE 2', 'MOBILE PHONE 3',
			'HOME EMAIL 1', 'HOME EMAIL 2', 'HOME EMAIL 3',
			'WORK EMAIL 1', 'WORK EMAIL 2', 'WORK EMAIL 3',
			'GEOCODE', 'TIMEZONE', 'AGENT', 'NOTE', 'REV', 'URL', 'UID'
			'AIM', 'ICQ', 'MSN', 'YAHOO', 'JABBER',
			'SKYPE', 'GADUGADU', 'GROUPWISE')
		self.data = self.__resetRow()
		for k in self.columns:
			self.__output( k )
		self.output += "\r\n"
		self.__parseFile()

		self.__trace(self.output)

#modified 11-23-09 
#modified to reflect current options available
def usage():
	print "options \n-h| --help this menu\n-i input file (VCS,VCF) *required if no path specified\n-p path of input files (VCS,VCF) *required if no input file specified\n-o output file (TAB) *required\n-d [comma|tab|semicolon] delimiter (tab is default)\n-q double quote values"

#modified 11-23-09
#modified to include dave dartt as a contributer
def version():
	print "convertContacts.py v0.2.002 2009-11-23 - by Petar Strinic http://petarstrinic.com\nMultifile input contribution by Dave Dartt"

#modified 11-23-09
#modified to accept -p option and process option accordingly
#modified verbose statement to show processing according to options used
#during calling of script.
def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ho:i:p:d:q", ["help","trace", "version"])
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)
	input_file = None
	input_path = None
	output_file = None
	quote = False
	trace = False
	delimiter = "\t"
	delimiter_string = "tab"
	for option, value in opts:
		if option == "--version":
			version()
			sys.exit(0)
		elif option == "-i":
			input_file = value
		elif option == "-p":
			input_path = value
		elif option == "-o":
			output_file = value
		elif option == "-q":
			quote = True
		elif option == "--trace":
			print "Trace On"
			trace = True
		elif option == "-d":
			if value == "comma":
				delimiter = ","
				delimiter_string = "comma"
			elif value == "semicolon":
				delimiter = ";"
				delimiter_string = "semicolon"
			elif value == "newline":
				delimiter = "\r\n"
				delimiter_string = "newline"
			else:
				delimiter = "\t"
				delimiter_string = "tab"
		elif option in ("-h", "--help"):
			usage()
			sys.exit(2)
		else:
			print "unhandled option %s" % option
			sys.exit(2)
	if (input_file == None and input_path == None) or output_file == None:
		print "missing required parameters"
		usage()
		sys.exit(2)
	if input_file != None and input_path == None:
		print "converting %s > %s (%s delimited)" % (input_file, output_file, delimiter_string)
		VcfToCsvConverter(input_file, input_path, output_file, delimiter, quote, trace)
		sys.exit(0)
	elif input_file == None and input_path != None:
		print "converting files within path: %s > %s (%s delimited)" % (input_path, output_file, delimiter_string)
		VcfToCsvConverter(input_file, input_path, output_file, delimiter, quote, trace)
		sys.exit(0)
	else:
		print "Invalid filename or path"
		usage()
		sys.exit(0)

if __name__ == "__main__":
	main()
