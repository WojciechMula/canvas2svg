from Tkinter import TclError
from Tkconstants import *

supported_item_types = \
	set(["line", "oval", "polygon", "rectangle", "text", "arc"])


def canvas_get_text(canvas, text_id):
        tk = canvas.tk
        try:
                result = tk.call(canvas._w, 'itemconfigure', text_id, '-text')
                return tk.splitlist(result)[-1]
        except TclError:
                return ''

def SVGdocument():
	"""
	Create default SVG document
	"""
	import xml.dom.minidom
	implementation = xml.dom.minidom.getDOMImplementation()
	doctype = implementation.createDocumentType(
		"svg", "-//W3C//DTD SVG 1.1//EN",
		"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"
	)
	document= implementation.createDocument(None, "svg", doctype)
	document.documentElement.setAttribute(
		'xmlns', 'http://www.w3.org/2000/svg'
	)
	return document


def convert(document, canvas, items=None):
	"""
	Convert 'items' stored in 'canvas' to SVG 'document'.
	If 'items' is None, then all items are convered.
	"""

	if items is None:	# default: all items
		items = canvas.find_all()
	
	for item in items:
		
		# skip unsupported items
		itemtype = canvas.type(item)
		if itemtype not in supported_item_types:
			warn("Items of type '%s' are not supported." % itemtype)
			continue

		# get item coords
		coords = canvas.coords(item)

		# get item options;
		# options is a dict: opt. name -> opt. actual value
		tmp     = canvas.itemconfigure(item)
		options = dict((v0, v4) for v0, v1, v2, v3, v4 in tmp.itervalues())
		
		# get state of item
		state = options['state']
		if 'current' in options['tags']:
			options['state'] = 'active'
		elif options['state'] == '':
			options['state'] = 'normal'
		else:
			# left state unchanged
			assert options['state'] in ['normal', 'disabled', 'hidden']


		def get(name, default=""):
			if state == 'active' and options.get(state + name):
				return options.get(state + name)
			if state == 'disabled' and options.get(state + name):
				return options.get(state + name)

			if options.get(name):
				return options.get(name)
			else:
				return default
		
		
		if itemtype == 'line':
			options['outline'] 			= ''
			options['activeoutline'] 	= ''
			options['disabledoutline'] 	= ''
		elif itemtype == 'arc' and options['style'] == ARC:
			options['fill'] 			= ''
			options['activefill'] 		= ''
			options['disabledfill'] 	= ''

		style = { # initial default values
			"stroke"		: "none",
			"fill"			: "none",
		}
		
		if get("outline") != "":
			style["stroke"] = HTMLcolor(canvas, get("outline"))

		if get("fill") != "":
			style["fill"] = HTMLcolor(canvas, get("fill"))
		
		
		width = float(options['width'])
		if state == 'active':
			width = max(float(options['activewidth']), width)
		elif state == 'disabled':
			if float(options['disabledwidth']) > 0:
				width = options['disabledwidth']
		
		style['stroke-width'] = width

		if width:
			dash = canvas.itemcget(item, 'dash')
			try:
				dash = tuple(map(int, dash.split()))
			except ValueError:
				pass # int can't parse literal

			if dash != '':
				if type(dash) is str: 
					linewidth = float(get('width'))
					dash = parse_dash(dash, linewidth)
				
				style['stroke-dasharray'] = ",".join(map(str, dash))
				if get('dashoffset'):
					style['stroke-dashoffset'] = get('dashoffset')



		if itemtype == 'line':
			# in this case, outline is set with fill property
			style["fill"], style["stroke"] = style["stroke"], style["fill"]

			if options['smooth'] in ['1', 'bezier']:
				element = smoothline(document, coords)
			elif options['smooth'] in ['0']:
				if len(coords) == 4: # segment
					element = segment(document, coords)
				else:
					element = polyline(document, coords)
			else:
				warn("Unknown smooth type: %s. Falling back to smooth=0" % options['smooth'])
				element = polyline(coords)
		
			style['stroke-linejoin'] = get('joinstyle', "miter")
			style['stroke-linecap'] = capstyle[get('capstyle', "butt")]

		elif itemtype == 'polygon':
			if options['smooth'] in ['1', 'bezier']:
				element = smoothpolygon(document, coords)
			elif options['smooth'] in ['0']:
				element = polygon(document, coords)
			else:
				warn("Unknown smooth type: %s. Falling back to smooth=0" % options['smooth'])
				element = line(coords)
	
			style['fill-rule'] = 'evenodd'
			style['stroke-linejoin'] = get('joinstyle', "miter")
		
		elif itemtype == 'oval':
			element = oval(document, coords)

		elif itemtype == 'rectangle':
			element = rectangle(document, coords)

		elif itemtype == 'arc':
			element = arc(document, coords, options['start'], options['extent'], options['style'])

		elif itemtype == 'text':
			# setup geometry
			xmin, ymin, xmax, ymax = canvas.bbox(item)
			text = canvas.get_text(canvas, item)
			
			x = coords[0]
			element = setattribs(
				tag('text'),
				x = x,
				y = (ymin + font_metrics(tk, options['font'], 'ascent')) # set y at 'dominant-baseline'
			)
			element.appendChild(document.createTextNode(text))

			# 2. Setup style
			opt = font_actual(tk, options['font'])

			# text-anchor
			if options['anchor'] == 'center':
				style['text-anchor'] = 'middle'

			# color
			style['fill'] = color(get('fill'))

			# family
			style['font-family'] = opt['family']

			# size
			size = float(opt['size'])
			if size > 0:
				style['font-size'] = "%spt" % size
			else:
				style['font-size'] = "%spx" % (-size)

			# italic?
			if opt['slant'] == 'italic':
				style['font-style'] = 'italic'

			# bold?
			if opt['weight'] == 'bold':
				style['font-weight'] = 'bold'

			# overstrike/underline
			if opt['overstrike'] and opt['underline']:
				style['text-decoration'] = 'underline line-through'
			elif opt['overstrike']:
				style['text-decoration'] = 'line-through'
			elif opt['underline']:
				style['text-decoration'] = 'underline'


		for attr, value in style.iteritems():
			element.setAttribute(attr, str(value))

		document.documentElement.appendChild(element)


	return document


def setattribs(element, **kwargs):
	for k, v in kwargs.iteritems():
		element.setAttribute(k, str(v))
	return element


def segment(document, coords):
	# segment
	return setattribs(
		document.createElement('line'),
		x1 = coords[0],
		y1 = coords[1],
		x2 = coords[2],
		y2 = coords[3],
	)
	

def polyline(document, coords):
	# polyline
	points = []
	for i in xrange(0, len(coords), 2):
		points.append("%s,%s" % (coords[i], coords[i+1]))
	
	return setattribs(
		document.createElement('polyline'),
		points = ' '.join(points),
	)
#fed

def lerp((xa, ya), (xb, yb), t):
	return (xa + t*(xb-xa), ya + t*(yb-ya))

def smoothline(document, coords):
	element = document.createElement('path')
	path    = []

	points  = [(coords[i], coords[i+1]) for i  in xrange(0, len(coords), 2)]
	def pt(points):
		x0, y0 = points[0]
		x1, y1 = points[1]
		p0     = (2*x0-x1, 2*y0-y1)

		x0, y0 = points[-1]
		x1, y1 = points[-2]
		pn     = (2*x0-x1, 2*y0-y1)

		p = [p0] + points[1:-1] + [pn]

		for i in xrange(1, len(points)-1):
			a = p[i-1]
			b = p[i]
			c = p[i+1]

			yield lerp(a, b, 0.5), b, lerp(b, c, 0.5)
		
	for i, (A, B, C) in enumerate(pt(points)):
		if i == 0:
			path.append("M%s,%s Q%s,%s %s,%s" % (A[0], A[1], B[0], B[1], C[0], C[1]))
		else:
			path.append("T%s,%s" % (C[0], C[1]))

	element.setAttribute('d', ' '.join(path))
	return element


def rectangle(document, coords):
	element = document.createElement('rect')
	return setattribs(element,
		x = coords[0],
		y = coords[1],
		width  = coords[2]-coords[0],
		height = coords[3]-coords[1],
	)


def polygon(document, coords):
	points = []
	for i in xrange(0, len(coords), 2):
		points.append("%s,%s" % (coords[i], coords[i+1]))

	return setattribs(document.createElement('polygon'),
		points = ' '.join(points)
	)


def smoothpolygon(document, coords):
	element = document.createElement('path')
	path    = []

	points  = [(coords[i], coords[i+1]) for i  in xrange(0, len(coords), 2)]
	def pt(points):
		p = points
		n = len(points)
		for i in xrange(0, len(points)):
			a = p[(i-1) % n]
			b = p[i]
			c = p[(i+1) % n]

			yield lerp(a, b, 0.5), b, lerp(b, c, 0.5)
		
	for i, (A, B, C) in enumerate(pt(points)):
		if i == 0:
			path.append("M%s,%s Q%s,%s %s,%s" % (A[0], A[1], B[0], B[1], C[0], C[1]))
		else:
			path.append("T%s,%s" % (C[0], C[1]))
	
	path.append("z")

	element.setAttribute('d', ' '.join(path))
	return element

def oval(document, coords):
	x1, y1, x2, y2 = coords

	# circle
	if x2-x1 == y2-y1:
		return setattribs(document.createElement('circle'),
			cx = (x1+x2)/2,
			cy = (y1+y2)/2,
			r  = abs(x2-x1)/2,
		)
	
	# ellipse
	else:
		return setattribs(document.createElement('ellipse'),
			cx = (x1+x2)/2,
			cy = (y1+y2)/2,
			rx = abs(x2-x1)/2,
			ry = abs(y2-y1)/2,
		)
	
	return element


import math

def arc(document, (x1, y1, x2, y2), start, extent, style):

	cx = (x1 + x2)/2.0
	cy = (y1 + y2)/2.0

	rx = (x2 - x1)/2.0
	ry = (y2 - y1)/2.0
	
	start  = math.radians(float(start))
	extent = math.radians(float(extent))

	# from SVG spec
	x1 =  rx * math.cos(start) + cx
	y1 = -ry * math.sin(start) + cy # XXX: ry is negated here

	x2 =  rx * math.cos(start + extent) + cx
	y2 = -ry * math.sin(start + extent) + cy # XXX: ry is negated here

	if abs(extent) > math.pi:
		fa = 1
	else:
		fa = 0

	if extent > 0.0:
		fs = 0
	else:
		fs = 1
	

	path = []
	if style == ARC:
		path.append('M%s,%s' % (x1, y1))
		path.append('A%s,%s 0 %d %d %s,%s' % (rx, ry, fa, fs, x2, y2))
	
	elif style == CHORD:
		path.append('M%s,%s' % (x1, y1))
		path.append('A%s,%s 0 %d %d %s,%s' % (rx, ry, fa, fs, x2, y2))
		path.append('z')

	else: # default: pieslice
		path.append('M%s,%s' % (cx, cy))
		path.append('L%s,%s' % (x1, y1))
		path.append('A%s,%s 0 %d %d %s,%s' % (rx, ry, fa, fs, x2, y2))
		path.append('z')

	return setattribs(document.createElement('path'), d = ''.join(path))


def arrow_head(document, x1, y1, x2, y2, d1, d2, d3):
	dx = x2 - x1
	dy = y2 - y1

	d = math.sqrt(dx*dx + dy*dy)
	t = (d1 + d2)/d
	pass


def font_actual(tkapp, font):
		tmp = tkapp.call('font', 'actual', font)
		return dict(
			(tmp[i][1:], tmp[i+1]) for i in xrange(0, len(tmp), 2)
		)
	
def font_metrics(tkapp, font, property=None):
	if property is None:
		tmp = tkapp.call('font', 'metrics', font)
		return dict(
			(tmp[i][1:], int(tmp[i+1])) for i in xrange(0, len(tmp), 2)
		)
	else:
		return int(tkapp.call('font', 'metrics', font, '-' + property))


def HTMLcolor(canvas, color):
	r, g, b = canvas.winfo_rgb(color)
	return "#%02x%02x%02x" % (r/256, g/256, b/256)


def parse_dash(string, width):
	# DashConvert from tkCanvUtil.c
	w = int(width + 0.5)
	if w < 1: w = 1

	n = len(string)
	result = []
	for i, c in enumerate(string):
		if c == " " and len(result):
			result[-1] += w + 1
		elif c == "_":
			result.append(8*w)
			result.append(4*w)
		elif c == "-":
			result.append(6*w)
			result.append(4*w)
		elif c == ",":
			result.append(4*w)
			result.append(4*w)
		elif c == ".":
			result.append(2*w)
			result.append(4*w)
	return result


capstyle = {"butt": "butt", "round": "round", "projecting": "square"}


if __name__ == '__main__':
	import Tkinter
	import random
	from random import randint, seed, choice

	D = 400

	root = Tkinter.Tk()
	canv = Tkinter.Canvas(bg="white", width=D, height=D)
	canv.pack()

	seed(100)

	def rand_color():
		return "#" + "".join(("%02x" % randint(0,255)) for i in xrange(6))
	

	def create_lines(n):
		for i in xrange(n):
			x1 = randint(0, D)
			y1 = randint(0, D)
			x2 = randint(0, D)
			y2 = randint(0, D)
			canv.create_line(
				x1, y1, x2, y2,
				fill  = rand_color(),
				width = randint(0, 20)/2.0,
			)

	def random_joinstyle():
		return choice(['bevel', 'miter', 'round'])
	
	
	def random_capstyle():
		return choice(['butt', 'projecting', 'round'])
	
	
	def create_polylines(n, k):
		for i in xrange(n):
			points = []
			for j in xrange(k):
				points.append(randint(0, D))
				points.append(randint(0, D))

			item = canv.create_line(*points)
			canv.itemconfigure(item, 
				fill  = rand_color(),
				width = 5,
				#joinstyle = random_joinstyle(),
				#capstyle  = random_capstyle(),
				dash = (5, 10, 15),
				#dash = "- . -",

			)
	
	#create_lines(10)
	create_polylines(5, 7)

	doc = SVGdocument()
	convert(doc, canv)
	x1, y1, x2, y2 = canv.bbox('all')
	doc.documentElement.setAttribute('width',  str(x2))
	doc.documentElement.setAttribute('height', str(y2))
	open('test.svg', 'w').write(doc.toprettyxml())

	root.mainloop()


# vim: ts=4 sw=4 nowrap noexpandtab
