try:
	# python3
	import tkinter as Tkinter
	from tkinter.constants import *
except ImportError:
	# python2
	import Tkinter
	from Tkconstants import *

from random import randint, seed, choice
import os
import canvasvg

try:
	import thread
except ImportError:
	import _thread as thread

try:
	xrange
except NameError:
	xrange = range

D = 400
def coord():
	return randint(0, D)

def random_color():
	r = randint(0, 255)
	g = randint(0, 255)
	b = randint(0, 255)
	return "#%02x%02x%02x" % (r, g, b)

def random_fill():
	if randint(0, 1000) > 500:
		return random_color()
	else:
		return ""


def test(canv, name, pretty=False, tounicode=None):
	doc = canvasvg.SVGdocument()
	for element in canvasvg.convert(doc, canv, tounicode=tounicode):
		doc.documentElement.appendChild(element)

	doc.documentElement.setAttribute('width',  str(D))
	doc.documentElement.setAttribute('height', str(D))

	f = open(name + '.svg', 'w')
	if pretty:
		f.write(doc.toprettyxml())
	else:
		f.write(doc.toxml())
	f.close()
	os.system("inkview %s.svg" % name)
	root.destroy()


root = Tkinter.Tk()
canv = Tkinter.Canvas(width=D, height=D, bg="#ffffff")
canv.pack()

seed(100)
