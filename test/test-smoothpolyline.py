from framework import *
root.title("Smoothed polyline test ($Revision: 1.4 $)")

n  = 50
k1 = 3
k2 = 10

for i in xrange(n):
	k = randint(k1, k2)
	p = []
	for j in xrange(k):
		p.append(coord())
		p.append(coord())

	item = canv.create_line(*p)
	canv.itemconfigure(item, smooth="1",
		fill=random_color(),
		width=randint(1,3))

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
