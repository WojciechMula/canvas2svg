from framework import *
root.title("Normal/disabled outline color ($Revision: 1.3 $)")

n = 200
for i in xrange(n):
	color = "blue"
	if randint(0, 1000) > 200:
		canv.create_line(coord(), coord(), coord(), coord(), 
			fill=color)
	else:
		canv.create_line(coord(), coord(), coord(), coord(), 
			fill=color, disabledfill="red", state=DISABLED)

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
