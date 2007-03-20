from framework import *

n = 50
k = 10
print "%d ellipses, %d circles" % (n, k)

for i in xrange(n):
	rx = randint(5, 50)
	ry = randint(5, 50)
	x  = coord()
	y  = coord()
	canv.create_oval(x-rx, y-ry, x+rx, y+ry, fill="#dddddd", outline="#000")

for i in xrange(k):
	r = randint(5, 50)
	x  = coord()
	y  = coord()
	canv.create_oval(x-r, y-r, x+r, y+r, fill="#ddddff", outline="#000")


thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
