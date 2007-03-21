from framework import *
root.title("Rectangle test ($Revision: 1.3 $)")

n = 100
for i in xrange(n):
	rx = randint(5, 50)
	ry = randint(5, 50)
	x  = coord()
	y  = coord()
	canv.create_rectangle(x-rx, y-ry, x+rx, y+ry,
		fill=random_fill(), outline=random_color())

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
