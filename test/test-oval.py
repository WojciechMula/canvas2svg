from framework import *
root.title("Ovals, i.e. circles & ellipses test ($Revision: 1.3 $)")

n = 100
k = 40

for i in xrange(n):
	rx = randint(5, 50)
	ry = randint(5, 50)
	x  = coord()
	y  = coord()
	canv.create_oval(x-rx, y-ry, x+rx, y+ry,
		fill	= random_fill(),
		outline	= random_color())

for i in xrange(k):
	r = randint(5, 50)
	x  = coord()
	y  = coord()
	canv.create_oval(x-r, y-r, x+r, y+r,
		fill	= random_fill(),
		outline	= random_color())

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
