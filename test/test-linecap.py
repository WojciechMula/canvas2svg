from framework import *

print "line cap"

capstyle = ["butt", "projecting", "round"]

for i, style in enumerate(capstyle):
	canv.create_line(50, 10+50*i, D-50, 10+50*i, width=10, capstyle=style)

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()

