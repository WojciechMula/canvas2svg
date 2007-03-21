# $Revision: 1.2 $
from framework import *

n = 100
print "%d rects" % n

for i in xrange(n):
	rx = randint(5, 50)
	ry = randint(5, 50)
	x  = coord()
	y  = coord()
	canv.create_rectangle(x-rx, y-ry, x+rx, y+ry,
		fill=random_color(), outline=random_color())

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
