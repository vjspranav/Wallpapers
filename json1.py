#!/usr/bin/python3

from PIL import Image
import math
import os
import json

d = {}

def createAuthor(fname):
	with open(fname, "r") as f:
		for line in f:
			(key, val, val1) = line.split(":")
			key = key[:-1]
			key=key.replace(' ', '_')
			if (val[0]!='"' and val[1]!='"'):
				val='"'+val+'"' 
			d[key] = val
			if val1[-1]=="\n":
				(val1, _)=val1.split("\n")
			key = key+"_copyright"
			if (val1[0]!='"' or val1[1]!='"'):
				val1='"'+val1+'"'
			d[key] = val1

def compressimg(x1, y1):
	foo = Image.open(x1)
	x, y = foo.size
	x2, y2 = math.floor(x-50), math.floor(y-20)
	foo = foo.resize((x2,y2),Image.LANCZOS)
	foo.save('thumbs/'+y1,optimize=True,quality=20)

folist=os.listdir('.')
if 'json1.py' in folist: folist.remove('json1.py')
if 'walls.json' in folist: folist.remove('walls.json')
if 'README.txt' in folist: folist.remove('README.txt')
folist.remove('thumbs')
folist.remove('.git')
data = []
count=0
no=0

for j in folist:
	print("Creating authors in " + j)
	createAuthor(j+"/Authors.txt")  
	list=[f for f in os.listdir(j) if os.path.isfile(j+'/'+f)]
	count = count+len(list)

for j in folist:
	list=[f for f in os.listdir(j) if os.path.isfile(j+'/'+f)]
	list.remove("Authors.txt")
	for i in list:
		no=no+1
		fname=j+'/'+i
		print('(', no, '/' ,count, ') Compressing ' + i, end='\r')
		compressimg(fname, i)
		s=os.stat(fname).st_size
		cpr = d[i + "_copyright"]
		auth = d[i]
		str='''
	        {
	                "name": "%s",
	                "author": %s,
	                "url": "https://github.com/vjspranav/Wallpapers/raw/sx/%s/%s",
	                "thumbnail": "https://github.com/vjspranav/Wallpapers/raw/sx/thumbs/%s",
	                "collections": "%s",
	                "downloadable": true,
	                "size": %s,
        	        "copyright": %s 
        	}''' % ( i, auth, j, i, i, j, s, cpr)
		data.append(str)

with open('walls.json', 'w') as outfile:
	outfile.write('[')
	for ele in data[:-1]:
		outfile.write(ele+',')
	outfile.write(data[-1] +'\n]')

os.system("git add .")
os.system('git commit -m "Add some more new Walls"')
os.system("git push origin HEAD:sx")

print('Json Generated and pushed successfully')

