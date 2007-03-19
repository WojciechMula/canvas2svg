from Tkconstants import *
from random      import randint, seed, choice
import Tkinter
import canvasvg

D = 400
def coord():
	return randint(0, D)

def dump(canv, name, pretty=False):
	doc = canvasvg.SVGdocument()
	canvasvg.convert(doc, canv)

	x1, y1, x2, y2 = canv.bbox('all')
	doc.documentElement.setAttribute('width',  str(x2))
	doc.documentElement.setAttribute('height', str(y2))

	f = open(name + '.svg', 'w')
	f.write(doc.toprettyxml())
	f.close()

root = Tkinter.Tk()
canv = Tkinter.Canvas(width=D, height=D, bg="#ffffff")
canv.pack()

seed(100)
