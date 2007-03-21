from framework import *
root.title("Line join style test ($Revision: 1.3 $)")

d = 50
paths = [
	(0, 0, d, 0, 2.0*d, d/2),
	(0, 0, d, 0, 2.0*d, d),
	(0, 0, d, 0, 1.5*d, d),
	(0, 0, d, 0, 1.0*d, d),
	(0, 0, d, 0, 0.5*d, d),
	(0, 0, d, 0, 0.0*d, d),
	(0, 0, d, 0, 0.0*d, d/2),
]

joinstyles = ["bevel", "miter", "round"]

for x, joinstyle in enumerate(joinstyles):
	for y, path in enumerate(paths):
		item = canv.create_line(*path)
		canv.itemconfigure(item, joinstyle=joinstyle, width=10)
		canv.move(item, 10 + x*(2*d+10), 10 + y*(d+10))

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
