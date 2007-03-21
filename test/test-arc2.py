from framework import *
root.title("Arc test ($Revision: 1.1 $)")

n = 200
arcstyle = [PIESLICE, CHORD, ARC]

for i in xrange(n):
	rx = randint(5, 50)
	ry = randint(5, 50)
	y  = coord()
	x  = coord()

	canv.create_arc(x-rx, y-ry, x+rx, y+ry,
		start	= randint(0, 360),
		extent	= randint(0, 360),
		style	= choice(arcstyle),
		fill	= random_fill(),
		outline	= random_color(),
	)

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
