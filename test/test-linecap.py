from framework import *
root.title("Line cap style test ($Revision: 1.4 $)")

capstyle = ["butt", "projecting", "round"]

for i, style in enumerate(capstyle):
	canv.create_line(50, 10+50*i, D-50, 10+50*i, width=15, capstyle=style)
	canv.create_line(50, 300+30*i, D/2, 150+30*i, D-50, 300+30*i, width=15, capstyle=style)
	
	canv.create_line(50, 10+50*i, D-50, 10+50*i, width=1.0, fill="white")
	canv.create_line(50, 300+30*i, D/2, 150+30*i, D-50, 300+30*i, width=1.0, fill="white")

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()

