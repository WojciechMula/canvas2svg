from framework import *
root.title("Polyline test ($Revision: 1.3 $)")

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
	canv.itemconfigure(item, fill=random_color())

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()

