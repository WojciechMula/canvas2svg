from framework import *
root.title("Arrows test 2 ($Revision: 1.2 $)")

k = 7
for i in xrange(30):
	d1 = randint(-10, 20)
	d2 = randint(-10, 20)
	d3 = randint(1, 20)
	color = random_color()

	points = [coord() for i in xrange(3*2, k*2)]
	item = canv.create_line(*points)
	canv.itemconfigure(item, 
		fill		= random_color(),
		arrow		= choice([LAST, BOTH, FIRST]),
		arrowshape	= (d1, d2, d3))

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
