from framework import *

n = 7
print "%d arcs" % n 

arcstyle = [PIESLICE, CHORD, ARC]

for j, style in enumerate(arcstyle):
	for i in xrange(n):
		rx = 50
		ry = 20
		y  = i*2*(ry+5) + 10 + ry
		x  = j*2*(rx+5) + 10 + rx

		k  = i+1
		canv.create_arc(x-rx, y-ry, x+rx, y+ry,
			start=k*5, extent=k*45, style=style,
			fill="#dddddd"
		)


thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
