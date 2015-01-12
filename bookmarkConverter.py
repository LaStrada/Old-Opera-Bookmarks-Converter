def removeTabs(str):
	for i, line in enumerate(str):
		line.replace("	", "");

	return str

def removeStuff(str):
	str = str.replace("\t", "")
	str = str.replace("\n", "")
	str = str.replace("\r", "")

	return str

#1089
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
			if debug:
				print "no....."


		elif lines[x].startswith("#FOLDER"):
			x=x+2

			foldername = lines[x][5:]
			foldername = foldername[:-2]

			folders.append({'name': foldername, 'items': []})

			if debug:
				print foldername

			folder = folder+1

		elif lines[x].startswith("#URL"):
			b={'name':'', 'url':'', 'description':''}
			x=x+2

			#NAME=
			b['name'] = lines[x][5:]
			x=x+1

			#URL
			b['url'] = lines[x][4:]
			x=x+1
			
			#CREATED - ignore
			x=x+1

			#VISITED - ignore
			x=x+1

			#DESCRIPTION
			b['description'] = lines[x][11:]
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
	str += '\t<HTML>\n'
	str += '\t<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n'
	str += '\t<Title>Bookmarks</Title>\n'

	
	for x in folders:
		str += '\t<DT><H3 FOLDED>'
		str += removeStuff(x['name'])
		str += '</H3>\n'

		if x['name'] != '' and x['name'] != "N/A":
			str += '\t\t<DL><p>\n'

		for z in x['items']:
			if x['name'] != '' and x['name'] != "N/A":	
				str += '\t\t<DT><A HREF="'
			else:
				str += '\t<DT><A HREF="'
			str += removeStuff(z['url'])
			str += '">'
			str += removeStuff(z['name'])
			str += '</A>\n'

		if x['name'] != '' and x['name'] != "N/A":
			str += '\t</p></DL>\n'

	str += '</HTML>'

	return str


def main():
	filename = raw_input('Read file: ')
	new_file = raw_input('New file: ')
	f=open(filename)
	lines=f.readlines()

	folders = convert(removeTabs(lines), False)

	# print folders

	text_file = open(new_file, "w")
	text_file.write(generateHTML(folders))
	text_file.close()

if __name__ == "__main__":
	main()


'''
folder format

#FOLDER
ID=137
NAME=Opera
CREATED=1358866163
PARTNERID=opera-operafolder
EXPANDED=
UNIQUEID=


#URL
ID=
NAME=
URL=
CREATED=
VISITED=
DESCRIPTION=
'''