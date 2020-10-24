from framework import *

root.title("Rotated text")

for rot in range(0, 360, 45):
	canv.create_text(100, 200,
		text	= "Rotated %s deg" % rot,
		angle	= rot,
		fill	= random_color(),
		font	= ("Helvetica", 8),
		anchor	= W,
	)


for rot in range(0, 360, 45):
	canv.create_text(300, 200,
		text	= "Rotated %s deg" % rot,
		angle	= rot,
		fill	= random_color(),
		font	= ("Helvetica", 8),
		anchor	= E,
	)

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
