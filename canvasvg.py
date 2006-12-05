import xml.dom as DOM

from warnings    import warn
from Tkconstants import *

unsupported = ["bitmap", "image", "window"]
item_types  = ["line", "oval", "polygon", "rectangle", "text", "arc"]
		
implementation = DOM.getDOMImplementation()

doctype = implementation.createDocumentType(
		"svg",
		"-//W3C//DTD SVG 1.1//EN",
		"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd")

document= implementation.createDocument(None, "svg", doctype)
svg	= document.documentElement
svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')

svg.setAttribute('width',  str(1000))
svg.setAttribute('height', str(1000))

#from test import canvas_get_text as get_text
from Tkconstants import *

from Tkinter import TclError

def canvas_get_text(canvas, text_id):
        tk = canvas.tk
        try:
                result = tk.call(canvas._w, 'itemconfigure', text_id, '-text')
                return tk.splitlist(result)[-1]
        except TclError:
                return ''
get_text = canvas_get_text

def convert(canvas, items=None, ignore_hidden=True, ignore_fun=None):
	tk = canvas.tk

	def color(col):
		r, g, b = canvas.winfo_rgb(col)
		return "#%02x%02x%02x" % (r/256, g/256, b/256)
	
	if items is None:	# default: all items
		items = canvas.find_withtag('all')
	


	for item in items:
		tmp     = canvas.itemconfigure(item)
		options = dict((v0, v4) for v0, v1, v2, v3, v4 in tmp.itervalues())

		# skip hidden items
		if ignore_hidden and options['state'] == 'hidden':
			continue

		# skip unsupported items
		type   = canvas.type(item)
		if type not in item_types:
			warn("Items of type '%s' are not supported." % type)
			continue

		# get coords
		coords = canvas.coords(item)

		# get state of item
		state = options['state']
		if 'current' in options['tags']:
			state = 'active'
		elif state == '':
			state = 'normal'
		else:
			# left state unchanged
			assert state in ['normal', 'disabled']
		
		style = {}

		def get(name):
			if state in ['active', 'disabled']:
				try:
					return options[state+name]
				except KeyError:
					pass

			try:
				return options[name]
			except KeyError:
				return ""

		
		if type == 'line':
			options['outline'] 			= ''
			options['activeoutline'] 	= ''
			options['disabledoutline'] 	= ''
		elif type == 'arc' and options['style'] == ARC:
			options['fill'] 			= ''
			options['activefill'] 		= ''
			options['disabledfill'] 	= ''

		# setup style
		if get('outline') != '':
			style['stroke']		= color(get('outline'))
		else:
			style['stroke']		= 'none'
	
		fill = options['fill']
		if state == 'active' and options['activefill'] != '':
				fill = options['activefill']
		if state == 'disabled' and options['disabledfill'] != '':
				fill = options['disabledfill']

		if fill != '':
			style['fill'] = color(fill)
		else:
			style['fill'] = 'none'

		width = float(options['width'])
		if state == 'active':
			width = max(float(options['activewidth']), width)
		elif state == 'disabled':
			if float(options['disabledwidth']) > 0:
				width = options['disabledwidth']
			
		style['stroke-width']	= width

		if width:
			dash = options['dash']
			if state == 'active' and options['activedash'] != '':
				dash = options['activedash']
			if state == 'disabled' and options['disableddash'] != '':
				dash = options['disableddash']

			if dash != '':
				if type(dash) is str: 
					linewidth = get('width')
					tmp = []
					for char in dash:
						if char == "-":
							tmp.append(4*linewidth)
							tmp.append(2*linewidth)
						else: # "."
							tmp.append(2*linewidth)
							tmp.append(2*linewidth)
				
				style['stroke-dasharray'] = ",".join(definition)
				if get('dashoffset'):
					style['stroke-dashoffset'] = get('dashoffset')


		if type == 'line':
			# setup geometry
			if options['smooth'] in ['1', 'bezier']:
				element = smoothline(coords)
			elif options['smooth'] in ['0']:
				element = line(coords)
			else:
				warn("Unknown smooth type: %s. Falling back to smooth=0" % options['smooth'])
				element = line(coords)

			if get('joinstyle'):
				style['stroke-linejoin'] = get('joinstyle')
			else:
				style['stroke-linejoin'] = 'miter'
			
			if get('capstyle'):
				style['stroke-linecap'] = get('capstyle')
			else:
				style['stroke-linecap'] = 'butt'

			style['stroke'], style['fill'] = style['fill'], style['stroke']
		
			# setup arrows (if any)
			arrow = get('arrow')
			if arrow:
				shape = get('arrowshape')

				if arrow == 'last' or arrow == 'both':
					id = get_marker(shape, 'last', style['stroke'])
					style['marker-end'] = 'url(#%s)' % id

				if arrow == 'first' or arrow == 'both':
					id = get_marker(shape, 'first', style['stroke'])
					style['marker-start'] = 'url(#%s)' % id

		elif type == 'polygon':
			# setup geometry
			if options['smooth'] in ['1', 'bezier']:
				element = smoothpolygon(coords)
			elif options['smooth'] in ['0']:
				element = polygon(coords)
			else:
				warn("Unknown smooth type: %s. Falling back to smooth=0" % options['smooth'])
				element = line(coords)
			
			if get('joinstyle'):
				style['stroke-linejoin'] = get('joinstyle')
			else:
				style['stroke-linejoin'] = 'miter'

		elif type == 'oval':      element = oval(coords)
		elif type == 'rectangle': element = rectangle(coords)
		elif type == 'arc':       element = arc(coords, options['start'], options['extent'], options['style'])
		elif type == 'text':
			# setup geometry
			xmin, ymin, xmax, ymax = canvas.bbox(item)
			text = get_text(canvas, item)
			
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


		# apply style
		tmp = []
		for k, v in style.iteritems():
			if v:
				tmp.append("%s:%s" % (k, v))

		if tmp:
			element.setAttribute('style', ';'.join(tmp))

		svg.appendChild(element)


	if len(first_markers) or len(last_markers):
		defs = tag('defs')
		svg.insertBefore(defs, svg.firstChild)

		for marker in first_markers.itervalues():
			defs.appendChild(marker)
		
		for marker in last_markers.itervalues():
			defs.appendChild(marker)
		
	return document


def tag(name):
	return document.createElement(name)

def setattribs(element, **kwargs):
	for k, v in kwargs.iteritems():
		element.setAttribute(k, str(v))
	return element

def line(coords):
	# segment
	if len(coords) == 4:
		return setattribs(
			tag('line'),
			x1 = coords[0],
			y1 = coords[1],
			x2 = coords[2],
			y2 = coords[3],
		)
	# polyline
	else: 
		points = []
		for i in xrange(0, len(coords), 2):
			points.append("%s,%s" % (coords[i], coords[i+1]))
	
		return setattribs(
			tag('polyline'),
			points = ' '.join(points),
		)
#fed

def lerp((xa, ya), (xb, yb), t):
	return (xa + t*(xb-xa), ya + t*(yb-ya))

def smoothline(coords):
	element = tag('path')
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

def rectangle(coords):
	element = tag('rect')
	return setattribs(element,
		x = coords[0],
		y = coords[1],
		width  = coords[2]-coords[0],
		height = coords[3]-coords[1],
	)


def polygon(coords):
	points = []
	for i in xrange(0, len(coords), 2):
		points.append("%s,%s" % (coords[i], coords[i+1]))

	return setattribs(tag('polygon'),
		points = ' '.join(points)
	)


def smoothpolygon(coords):
	element = tag('path')
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

def oval(coords):
	x1, y1, x2, y2 = coords

	# circle
	if x2-x1 == y2-y1:
		return setattribs(tag('circle'),
			cx = (x1+x2)/2,
			cy = (y1+y2)/2,
			r  = abs(x2-x1)/2,
		)
	
	# ellipse
	else:
		return setattribs(tag('ellipse'),
			cx = (x1+x2)/2,
			cy = (y1+y2)/2,
			rx = abs(x2-x1)/2,
			ry = abs(y2-y1)/2,
		)
	
	return element


from math import sin, cos, radians, pi

def arc((x1, y1, x2, y2), start, extent, style):

	cx = (x1 + x2)/2.0
	cy = (y1 + y2)/2.0

	rx = (x2 - x1)/2.0
	ry = (y1 - y2)/2.0	# note: negative ry!
	
	start  = radians(float(start))
	extent = radians(float(extent))

	# from SVG spec
	x1 = rx * cos(start) + cx
	y1 = ry * sin(start) + cy

	x2 = rx * cos(start + extent) + cx
	y2 = ry * sin(start + extent) + cy

	if abs(extent) > pi:
		fa = 1
	else:
		fa = 0

	if extent > 0.0:
		fs = 1
	else:
		fs = 0
	

	path = []
	if style == 'arc':
		path.append('M%s,%s ' % (x1, y1))
		path.append('A%s,%s 0 %d %d %s,%s' % (rx, ry, fa, fs, x2, y2))
	
	elif style == 'chord':
		path.append('M%s,%s ' % (x1, y1))
		path.append('A%s,%s 0 %d %d %s,%s' % (rx, ry, fa, fs, x2, y2))
		path.append('z')

	else: # default: pieslice
		path.append('M%s,%s' % (cx, cy))
		path.append('L%s,%s' % (x1, y1))
		path.append('A%s,%s 0 %d %d %s,%s' % (rx, ry, fa, fs, x2, y2))
		path.append('z')

	return setattribs(tag('path'), d = ''.join(path))


#######################################################################
# markers support

first_markers = {}
last_markers  = {}

def get_marker(arrowshape, where, color):
	global first_markers, last_markers

	if where == 'first':
		markers = first_markers
	elif where == 'last':
		markers = last_markers

	try:
		return markers[arrowshape, color].getAttribute('id')
	except KeyError:
		pass

	(d2, d1, d3) = map(float, arrowshape)
	if where == 'last':
		points  = "%r,%r %r,%r %r,%r %r,%r" % (0.0, 0.0, -d1, -d3, -d2, 0.0, -d1, d3)
		minx = min(-d1, -d2, 0.0)
		maxx = max(-d1, -d2, 0.0)
		w    = maxx-minx
		refX = -minx
	else:
		points  = "%r,%r %r,%r %r,%r %r,%r" % (0.0, 0.0, d1, -d3, d2, 0.0, d1, d3)
		minx = min(d1, d2, 0.0)
		maxx = max(d1, d2, 0.0)
		w    = maxx-minx
		refX = -minx

	polygon = tag('polygon')
	polygon.setAttribute('points', points)
	polygon.setAttribute('style', 'fill:%s' % color)

	marker = tag('marker')
	marker.appendChild(polygon)

	setattribs(marker,
		id           = '%s%d' % (where[0], len(markers)),
		orient       = 'auto',
		markerUnits  = 'userSpaceOnUse',
		markerWidth  = w,
		markerHeight = 2*d3,
		viewBox      = '%r %r %r %r' % (minx, -d3, maxx-minx, 2*d3),
		refX         = '%r' % refX,
		refY         = '%r' % d3,
	)

	markers[arrowshape, color] = marker
	return marker.getAttribute('id')

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

# vim: ts=4 sw=4 nowrap noexpandtab
