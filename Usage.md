# Usage v0.3.000 #


Usage: python ./convertContacts3.py -i`<`filename`[`s`]``>`|-p`<`pathname`>` -o`<`filename`>` -d`<`option`>` -q -v

This program was designed to take the information within a vcard and export
it's contents to a csv file for easy import into other address book clients.

Options
  * -version ..show program version number and exit
  * h --help ..show this help message and exit
  * i --input ..Read data from one or more FILENAMES seperated by a comma (required if no path specified)
  * p --path ..Process all vcards within specified directory (required if no filename specified)
  * o --output ..Name of .csv file to output too (default is addrs.csv)
  * d --delim ..Delimiter to use: comma, semicolon, tab (default is tab)
  * q --quote ..Double quote the output strings (default is off)
  * v --verbose ..Show processing information (default is on)

# Usage v0.2.002 #


python ./convertContacts2.py `[`-i `<`filename`>` | -p `<`pathname`>``]` -o csvFile.csv -d comma -q

## Command line options ##
  * --version - print version and exit
  * -h --help - help/usage
  * -i filename - input a filename
  * -p path - input a path to vcard files (.vcs,.vcf)
  * -o filename - output filename REQUIRED
  * -d [comma|tab|semicolon] - delimiter, tab is default
  * -q - double quote the output values
  * --trace - tons of debugging output

# Usage v0.2.001 #


python ./convertContacts2.py -i `<`filename`>` -o csvFile.csv -d comma -q

## Command line options ##
  * --version - print version and exit
  * -h --help - help/usage
  * -i filename - input a filename(.vcs,.vcf)
  * -o filename - output filename REQUIRED
  * -d [comma|tab|semicolon] - delimiter, tab is default
  * -q - double quote the output values
  * --trace - tons of debugging output