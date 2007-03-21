# $Revision: 1.3 $
from framework import *

print "different dashes"

def line(y, dash, width=1):
	canv.create_line(20, y, D-20, y, width=width, dash=dash)

# dash pattern defined by list of length
line(10, (5))
line(20, (5, 10))
line(30, (5, 10, 5))
line(40, (5, 10, 5, 20))
line(50, (5, 10, 5, 20, 5))
line(50, (5, 10, 5, 20, 5, 30))

# dash pattern defined by string
line(70,  "-. _,  -")
line(80,  "-. _,  -", width=2)
line(90,  "-. _,  -", width=3)
line(110, "-. _,  -", width=4)
line(120, "_.", width=2)
line(130, "-.", width=3)
line(140, "- - ", width=4)

# space
line(150, ".", width=4)
line(160, ". ", width=4)
line(170, ".  ", width=4)
line(180, ".   ", width=4)
line(190, ".    ", width=4)

# disableddash
def line2(y, dash, width=1):
	canv.create_line(20, y, D-20, y, width=width, state=DISABLED,
		dash=(5,5), disableddash=dash)

line2(210, (5))
line2(220, (5, 10))
line2(230, (5, 10, 5))
line2(240, (5, 10, 5, 20))
line2(250, (5, 10, 5, 20, 5))
line2(250, (5, 10, 5, 20, 5, 30))

# dashoffset
def line3(y, offset):
	canv.create_line(20, y, D-20, y, dash=(4,6), dashoffset=offset)

line3(300, 0)
line3(310, 1)
line3(320, 2)
line3(330, 3)
line3(340, 4)
line3(350, 5)
line3(360, 6)
line3(370, 7)
line3(380, 8)
line3(390, 9)

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
