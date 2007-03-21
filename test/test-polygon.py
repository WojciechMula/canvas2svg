from framework import *
root.title("Polygons tests ($Revision: 1.4 $)")

n  = 30
k1 = 3
k2 = 15

for i in xrange(n):
	k = randint(k1, k2)
	p = []
	for j in xrange(k):
		p.append(coord())
		p.append(coord())

	item = canv.create_polygon(*p)
	canv.itemconfigure(item,
		fill	= random_fill(),
		outline	= random_color())

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()

