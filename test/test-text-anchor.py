from framework import *
root.title("Text anchor test ($Revision: 1.2 $)")

anchors = [NW, N, NE, W, CENTER, E, SW, S, SE]

for i, anchor in enumerate(anchors):
	x = D/2 - ((i % 3)-1)*100
	y = D/2 - ((i // 3)-1)*100

	canv.create_oval(x-3, y-3, x+3, y+3, fill="black")
	canv.create_text(x, y,
		text	= anchor.upper(),
		fill	= random_color(),
		font	= ("Helvetica", -30),
		anchor	= anchor,
	)

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
