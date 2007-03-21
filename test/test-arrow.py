from framework import *
root.title("Arrows test ($Revision: 1.3 $)")

for i in xrange(50):
	d1 = randint(-10, 20)
	d2 = randint(-10, 20)
	d3 = randint(1, 20)
	color = random_color()
	canv.create_line(coord(), coord(), coord(), coord(),
		fill		= random_color(),
		arrow		= choice([LAST, BOTH, FIRST]),
		arrowshape	= (d1, d2, d3))

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
