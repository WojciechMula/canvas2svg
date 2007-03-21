from framework import *
root.title("Segments test ($Revision: 1.3 $)")

n = 100
for i in xrange(n):
	item = canv.create_line(coord(), coord(), coord(), coord())
	canv.itemconfigure(item, fill=random_color())

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
