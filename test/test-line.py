from framework import *

n = 50
print n, "lines (black, 1-pixel width)"

for i in xrange(n):
	canv.create_line(coord(), coord(), coord(), coord())


thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
