#!/usr/bin/env python3

import getopt
import sys
import prettytable
import yaml
from os.path import expanduser
import requests
import xmltodict
import pprint

# Current version
VERSION=20160814

# Print Usage info and exit
def usage():
  usagestr = ""
  usagestr = usagestr + "\nUsage:\n"
  usagestr = usagestr + "evecli v"+str(VERSION)+" by Sacha Ligthert <sacha@ligthert.net>\n"
  usagestr = usagestr + "-f/--file <configfile>\n"
  usagestr = usagestr + "-k/--key <keyID>\n"
  usagestr = usagestr + "-v/--verification <verificationCodecode>\n"
  usagestr = usagestr + "-c/--character <characterID>\n"
  usagestr = usagestr + "-o/--output [table*,csv]\n"
  usagestr = usagestr + "-w/--write\n"
  usagestr = usagestr + "-q/--query [skillqueue,SkillInTraining]\n"
  print(usagestr)
  sys.exit(2)

# Function responsible for writing away credentials
def file_write( keyID, verificationCode, characterID, filename ):
  stream = open(filename, 'w')
  data = { "keyID":keyID, "verificationCode":verificationCode, "characterID":characterID }
  yaml.dump( data, stream, default_flow_style=False )

def parseXML( resultsXML, multi ):
  results = []
  row = []
  keys = []

  if multi == True:
    columns = resultsXML['@columns']

    for column in columns.rsplit(","):
      row.append(column)

    results.append(row)
    row = []

    for skills in resultsXML['row']:
      for skill in skills:
        row.append(skills[skill])
      results.append(row)
      row = []

  else:
    counter = 0
    for items in resultsXML:
      if counter != 0:
        row.append(items)
      counter = counter + 1
    results.append(row)
    row = []
    counter = 0
    for items in resultsXML:
      if counter != 0:
        row.append(resultsXML[items])
      counter = counter + 1
    results.append(row)
    row = []

  return results

def printTable( results ):
  rowCount = 0
  for row in results:
    if rowCount == 0:
      x = prettytable.PrettyTable(row)
    else:
      x.add_row(row)
    rowCount = rowCount + 1
  print(x)

def printCSV( results ):
  for row in results:
    print(",".join(row))

# The main program
if __name__ == "__main__":

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hf:k:v:c:o:wq:", ["help", "file=", "key=", "verification=", "character=", "output=", "write", "query="])
  except getopt.GetoptError as Err:
    print("Error: " + str(Err))
    usage()

  # Print usage info and exit
  if len(sys.argv[1:]) == 0:
    usage()

  # Set default values
  query = "skillqueue"
  homedir = expanduser("~")
  filename = homedir + "/.evecli"
  output = "table"
  url = "https://api.eveonline.com/char/"
  write = False

  # Parse the commandline parameters, issue errors if needed
  for option, value in opts:
    if option == "-h" or option == "--help":
      usage()
    elif option == "-f" or option == "--file":
      filename = value
    elif option == "-k" or option == "--key":
      keyID = value
    elif option == "-v" or option == "--verification":
      verificationCode = value
    elif option == "-c"  or option == "--character":
      characterID = value
    elif option == "-o" or option == "--output":
      if value != "table" and value != "csv":
        print("Error: Unsupported output method")
        usage()
      output = value
    elif option == "-q" or option == "--query":
      if value.lower() not in ["skillqueue","skillintraining"]:
        print("Error: Unsupported query type: "+ value)
        usage()
      query = value.lower()
    elif option == "-w" or value == "--write":
      write = True

# When a write is issued and the keyID, verificationCode and characterID are there write it away, or else issue an error.
  if write == True:
    file_write( keyID, verificationCode, characterID, filename )

# Open filename, throw error if it doesn't exist. Else open ~/.evecli if exist, throw error otherwise. Check if all the data is in it
  stream = open(filename,"r")
  credentials = yaml.load(stream)
  keyID = credentials['keyID']
  verificationCode = credentials['verificationCode']
  characterID = credentials['characterID']

# Parse the query and create a propper URL
  multi = False
  if query == "skillqueue":
    url = url + "SkillQueue.xml.aspx"
    multi = True
  if query == "skillintraining":
    url = url + "SkillInTraining.xml.aspx"

# Fetch url and parse it. Create an error if XML barfs
  headers = {"keyID": keyID, "vCode":verificationCode, "characterID":characterID}
  r = requests.get(url, headers)
  XML = xmltodict.parse(r.text)

  # Make sure we are not parsing errors
  errorCode = 0
  try:
    if multi == True:
      resultsXML = XML['eveapi']['result']['rowset']
    else:
      resultsXML = XML['eveapi']['result']
  except KeyError:
    errorCode = XML['eveapi']['error']['@code']

  if int(errorCode) > 0:
    print("API ERROR: #"+str(XML['eveapi']['error']['@code'])+" "+XML['eveapi']['error']['#text']+"\n")

  # pprint.pprint(results)
  # Prepare for printing
  resultsFinal = parseXML(resultsXML,multi)


# Send it off to the printers
  if output == "table":
    printTable(resultsFinal)
  elif output == "csv":
    printCSV(resultsFinal)
