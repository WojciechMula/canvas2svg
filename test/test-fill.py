from framework import *
root.title("Fill test ($Revision: 1.4 $)")

n  = 10
k1 = 3
k2 = 15

for i in xrange(n):
	k = randint(k1, k2)
	p = []
	for j in xrange(k):
		p.append(coord())
		p.append(coord())
	item = canv.create_polygon(*p)
	
	color = random_color()
	if randint(0, 1000) > 200:
		canv.itemconfigure(item, fill=color, outline="black")
	else:
		canv.itemconfigure(item, fill=color, outline="black",
			disabledfill="black", state=DISABLED)
			

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
