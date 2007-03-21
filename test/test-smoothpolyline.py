from framework import *

n  = 50
k1 = 3
k2 = 10
print "%d smoothed polylines with %d-%d vertices (black, 1-pixel width)" % (n, k1, k2)

for i in xrange(n):
	k = randint(k1, k2)
	p = []
	for j in xrange(k):
		p.append(coord())
		p.append(coord())

	item = canv.create_line(*p)
	canv.itemconfigure(item, fill=random_color(), width=randint(1,3), smooth="1")

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
