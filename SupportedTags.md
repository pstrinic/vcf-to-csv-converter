# Supported Tags v0.2 #

## Introduction ##

The following VCARD 3.0 fields are supported, based on vCard MIME Directory Profile (http://tools.ietf.org/html/rfc2426). For the list of output fields, and mapping information, see [Output Fields and Mapping](OutputFields_and_Mapping.md).

### FULL SUPPORT ###
  * N 	Name 	a structured representation of the name of the person, place or thing associated with the vCard object.
  * FN 	Formatted Name 	the formatted name string associated with the vCard object
  * BDAY 	Birthday 	date of birth of the individual associated with the vCard
  * ADR 	Delivery Address 	a structured representation of the physical delivery address for the vCard object
  * TEL 	Telephone 	the canonical number string for a telephone number for telephony communication with the vCard object
  * EMAIL 	Email 	the address for electronic mail communication with the vCard object
  * MAILER 	Email Program (Optional) 	Type of email program used
  * TZ 	Time Zone 	information related to the standard time zone of the vCard object
  * GEO 	Global Positioning 	The property specifies a latitude and longitude
  * TITLE 	Title 	specifies the job title, functional position or function of the individual associated with the vCard object within an organization (V. P. Research and Development)
  * ROLE 	Role or occupation 	the role, occupation, or business category of the vCard object within an organization (eg. Executive)
  * AGENT 	Agent 	information about another person who will act on behalf of the vCard object. Typically this would be an area administrator, assistant, or secretary for the individual
  * ORG 	Organization Name or Organizational unit 	the name and optionally the unit(s) of the organization associated with the vCard object. This property is based on the X.520 Organization Name attribute and the X.520 Organization Unit attribute
  * NOTE 	Note 	specifies supplemental information or a comment that is associated with the vCard
  * REV 	Last Revision 	combination of the calendar date and time of day of the last update to the vCard object
  * URL 	URL 	An URL is a representation of an Internet location that can be used to obtain real-time information about the vCard object
  * UID 	Unique Identifier 	specifies a value that represents a persistent, globally unique identifier associated with the object
  * X-AIM 	property
  * X-ICQ 	property
  * X-JABBER 	property
  * X-MSN 	property
  * X-YAHOO 	property
  * X-SKYPE-USERNAME 	property
  * X-GADUGADU 	property
  * X-GROUPWISE 	property

### LIMITED SUPPORT ###
  * LS PHOTO 	Photograph 	an image or photograph of the individual associated with the vCard (URL only)
  * LS LOGO 	Logo 	an image or graphic of the logo of the organization that is associated with the individual to which the vCard belongs (URL only)

### NO SUPPORT ###
  * LABEL 	Label Address 	addressing label for physical delivery to the person/object associated with the vCard
  * SOUND 	Sound 	By default, if this property is not grouped with other properties it specifies the pronunciation of the Formatted Name property of the vCard object.
  * VERSION 	Version 	Version of the vCard Specification
  * KEY 	Public Key 	the public encryption key associated with the vCard object
  * X-ABUID 	property 	string 	Apple Address Book UUID for that entry
  * X-ANNIVERSARY 	property 	YYYY-MM-DD 	arbitrary anniversary, in addition to BDAY = birthday
  * X-ASSISTANT 	property 	string 	assistant name (instead of Agent)
  * X-MANAGER 	property 	string 	manager name
  * X-SPOUSE 	property 	string 	spouse name
  * X-MS-IMADDRESS 	property 	string 	" (IM address in VCF attachment from Outlook (right click Contact, Send Full Contact, Internet Format.)
  * X-MS-CARDPICTURE 	property 	string 	Works as PHOTO or LOGO. Contains an image of the Card in Outlook.
  * X-PHONETIC-FIRST-NAME, X-PHONETIC-LAST-NAME 	property 	string 	alternative spelling of name, used for Japanese names by Android and iPhone introduced and used by Mozilla, also used by Evolution (software)
  * X-MOZILLA-HTML 	property 	TRUE/FALSE 	mail recipient wants HTML email introduced and used by Evolution (software)
  * X-EVOLUTION-ANNIVERSARY 	property 	YYYY-MM-DD 	arbitrary anniversary, in addition to BDAY = birthday
  * X-EVOLUTION-ASSISTANT 	property 	string 	assistant name (instead of Agent)
  * X-EVOLUTION-BLOG-URL 	property 	string/URL 	blog URL
  * X-EVOLUTION-FILE-AS 	property 	string 	file under different name (in addition to N = name components and FN = full name
  * X-EVOLUTION-MANAGER 	property 	string 	manager name
  * X-EVOLUTION-SPOUSE 	property 	string 	spouse name
  * X-EVOLUTION-VIDEO-URL 	property 	string/URL 	video chat address
  * X-EVOLUTION-CALLBACK 	TEL TYPE parameter value 	- 	callback phone number
  * X-EVOLUTION-RADIO 	TEL TYPE parameter value 	- 	radio contact information
  * X-EVOLUTION-TELEX 	TEL TYPE parameter value 	- 	Telex contact information
  * X-EVOLUTION-TTYTDD 	TEL TYPE parameter value 	- 	TTY TDD contact information