from framework import *
root.title("Normal/disabled outline width ($Revision: 1.3 $)")

for i in xrange(1, D//20+1):
	y = i*20
	canv.create_line(10, y, 10+150, y, width=i/4.0)
	canv.create_line(20+150, y, 20+300, y,
		width=5, disabledwidth=i/4.0, state='disabled')

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
