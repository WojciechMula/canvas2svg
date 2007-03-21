from framework import *
root.title("Dash patterns test ($Revision: 1.4 $)")

# dash pattern defined by list of length
patterns1 = [
	(5),
	(5, 10),
	(5, 10, 5),
	(5, 10, 5, 20),
	(5, 10, 5, 20, 5),
	(5, 10, 5, 20, 5, 30),
]

top = 1
for i, pattern in enumerate(patterns1):
	y = (top + i)*10
	canv.create_line(20, y, D-20, y, dash=pattern)

# dash pattern defined by string
patterns2 = [
	("-. _,  -",	1),
	("-. _,  -",	2),
	("-. _,  -",	3),
	("-. _,  -",	4),
	("_.",		2),
	("-.",		3),
	("- - ",	4),
]

top += len(patterns1)
for i, (pattern, width) in enumerate(patterns2):
	y = (top + i)*10
	canv.create_line(20, y, D-20, y, dash=pattern, width=width)


# space
patterns3 = [
	".",
	". ",
	".  ",
	".   ",
	".    ",
]

top += len(patterns2)
for i, pattern in enumerate(patterns1):
	y = (top + i)*10
	canv.create_line(20, y, D-20, y, dash=pattern)


# disableddash
top += len(patterns3)
for i, pattern in enumerate(patterns1):
	y = (top + i)*10
	canv.create_line(20, y, D-20, y, width=2, state=DISABLED,
		dash=(5,5), disableddash=pattern)

# dashoffset
top += len(patterns1)
for i in xrange(11):
	y = (top + i)*10
	canv.create_line(20, y, D-20, y, dash=(4,6), dashoffset=i)

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
