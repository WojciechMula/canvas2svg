# $Revision: 1.2 $
from framework import *

print "different dashes"

def line(y, dash, width=1):
	canv.create_line(20, y, D-20, y, width=width, dash=dash)

line(10, (5))
line(20, (5, 10))
line(30, (5, 10, 5))
line(40, (5, 10, 5, 20))
line(50, (5, 10, 5, 20, 5))
line(50, (5, 10, 5, 20, 5, 30))

line(70,  "-. _,  -")
line(80,  "-. _,  -", width=2)
line(90,  "-. _,  -", width=3)
line(110, "-. _,  -", width=4)
line(120, "_.", width=2)
line(130, "-.", width=3)
line(140, "- - ", width=4)
line(150, ".", width=4)
line(160, ". ", width=4)
line(170, ".  ", width=4)
line(180, ".   ", width=4)
line(190, ".    ", width=4)

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
