from Tkconstants import *
from random      import randint, seed, choice
import Tkinter, os
import canvasvg
import thread

D = 400
def coord():
	return randint(0, D)

def test(canv, name, pretty=False):
	doc = canvasvg.SVGdocument()
	canvasvg.convert(doc, canv)

	doc.documentElement.setAttribute('width',  str(D))
	doc.documentElement.setAttribute('height', str(D))

	f = open(name + '.svg', 'w')
	if pretty:
		f.write(doc.toprettyxml())
	else:
		f.write(doc.toxml())
	f.close()
	os.system("inkview %s.svg" % name)
	raise SystemExit


root = Tkinter.Tk()
canv = Tkinter.Canvas(width=D, height=D, bg="#ffffff")
canv.pack()

seed(100)
