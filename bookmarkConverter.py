import getopt
import sys

def removeTabs(str):
	for i, line in enumerate(str):
		line.replace("	", "");

	return str

def removeStuff(str):
	str = str.replace("\t", "")
	str = str.replace("\n", "")
	str = str.replace("\r", "")

	return str

def convert(lines, debug=False):
	numberOfLines = len(lines)
	x=0
	foldername='N/A'

	folders = [{'name': 'N/A', 'items': []}]
	folder = 0

	while 1:
		if x >= numberOfLines:
			break
		elif lines[x] == '' or lines[x] == '-':
			x=x+1

		elif lines[x].startswith("#FOLDER"):
			# Ignore two lines
			x=x+2

			foldername = removeStuff(lines[x][6:])
			folders.append({'name': foldername, 'items': []})

			if debug:
				print foldername

			folder = folder+1

		elif lines[x].startswith("#URL"):
			b={'name':'', 'url':'', 'description':''}

			# Ignore two lines
			x=x+2

			#NAME=
			b['name'] = removeStuff(lines[x])[5:]
			x=x+1

			#URL
			b['url'] = removeStuff(lines[x])[4:]
			x=x+1
			
			#CREATED - ignore
			x=x+1

			#VISITED - ignore
			x=x+1

			#DESCRIPTION
			# b['description'] = lines[x][11:]
			x=x+1

			#UNIQUEID - ignore
			x=x+1
			
			folders[folder]['items'].append(b)
		else:
			x=x+1

	return folders


def generateHTML(folders):
	x=0
	str =  '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n'
	str += '<HTML>\n'
	str += '<HEAD>\n'
	str += '\t<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n'
	str += '\t<Title>Bookmarks</Title>\n'
	str += '</HEAD>\n'
	str += '<BODY>\n'
	str += '\t<H1>Bookmarks</H1>\n'
	str += '\t<DL>\n'

	
	for x in folders:
		if x['name'].lower() == 'papirkurv':
			continue
		# elif x['name'] != '' and x['name'] != "N/A":
		# 	str += '\t\t<DT>\n'
		# 	str += '\t\t\t<H3>'
		# 	str += x['name']
		# 	str += '</H3>\n'
		# 	str += '\t\t\t<DL>\n'
		# 	str += '\t\t\t\t<p> </p>\n'
		# else:
		# 	str += '\t\t<p> </p>\n'
		# 
		for z in x['items']:
		# 	if x['name'] != '' and x['name'] != "N/A":	
		# 		str += '\t\t\t\t<DT><A HREF="'
		# 	else:
		# 		str += '\t\t<DT><A HREF="'

			str += '\t\t<DT><A HREF="'
			str += z['url']
			str += '">'
			str += z['name']
			str += '</A></DT>\n'

		# if x['name'] != '' and x['name'] != "N/A":
		# 	str += '\t\t\t\t<p> </p>\n'
		# 	str += '\t\t\t</DL>\n'
		# 	str += '\t\t</DT>\n'
		#
		# str += '\t\t<p> </p>\n'

	str += '\t\t</DL>\n'
	str += '\t</BODY>\n'
	str += '</HTML>\n'

	return str


def usage():
	print
	print "-h\t--help\t\tShow this."
	print "-i\t--input\t\tInput file"
	print "-o\t--output\tOutput file"

	sys.exit(2)


def main():
	# filename = raw_input('Read file: ')
	# new_file = raw_input('New file: ')

	try:
		opts, args = getopt.getopt(sys.argv[1:], "h?i:o:", ["help", "input=", "output="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	filename = ''
	new_file = ''

	output = None
	verbose = False

	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-?", "-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-i", "--input"):
			filename = a
		elif o in ("-o", "--output"):
			new_file = a
		else:
			assert False, "unhandled option"

	if filename == '':
		print
		print "No input file."
		usage()
		sys.exit(2)
	elif new_file == '':
		print
		print "No output file."
		usage()
		sys.exit(2)

	f=open(filename)
	lines=f.readlines()

	folders = convert(removeTabs(lines), False)

	# print folders

	text_file = open(new_file, "w")
	text_file.write(generateHTML(folders))
	text_file.close()

if __name__ == "__main__":
	main()