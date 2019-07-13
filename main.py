from math import log
from collections import Counter, defaultdict
from glob import glob
import os.path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from random import randint, random
import os

dct = defaultdict(list)

def getSize(filename):
    st = os.stat(filename)
    return st.st_size

home = os.path.expanduser("~")
files = glob(home+"/**/*")

try:
	for filepath in files:

		if not os.path.isfile(filepath):
			continue
		
		size = getSize(filepath)
		print(size)
		
		if size > 1_000_000:
			continue

		try:
			filename = filepath.rsplit("/",1)[-1]
			if "." not in filename:
				continue
			ext = filename.rsplit(".",1)[-1]
		except IndexError:
			continue
		
		if len(dct[ext]) > 1000:
			continue
			
		with open(filepath, "rb") as f:
			bytes = f.read()
			
		c = Counter(bytes)

		#print(len(c))

		for k in c:
			c[k] /= len(bytes)

		H = - sum([c[i]*log(c[i],2) for i in range(256) if c[i]>0])
		
		dct[ext].append((H, size))

		#print(H)
except KeyboardInterrupt:
	pass

print(dct)


x = []
y = []
s = []
c = []
alpha = 0.5

def randcolor():
	return [random() for i in range(3)]
	
colors = defaultdict(randcolor)

for ext in dct:
	for f in dct[ext]:
		x.append(f[0])
		y.append(f[1])
		s.append(10)
		c.append(colors[ext])



plt.scatter(x,y,s=s,c=c,alpha=alpha)

for ext in dct:
	for f in dct[ext]:
		plt.annotate(ext, (f[0], f[1]))

#patches = [mpatches.Patch(color=v, label="."+k) for k,v in colors.items()]
#plt.legend(handles=patches)

plt.show()
