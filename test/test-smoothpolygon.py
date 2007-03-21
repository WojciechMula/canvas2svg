from framework import *

n  = 5
k1 = 3
k2 = 15
print "%d polygons with %d-%d vertices (black, 1-pixel width)" % (n, k1, k2)

for i in xrange(n):
	k = randint(k1, k2)
	p = []
	for j in xrange(k):
		p.append(coord())
		p.append(coord())

	item = canv.create_polygon(*p)
	canv.itemconfigure(item, fill="#dddddd", outline="black", smooth="1")

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
