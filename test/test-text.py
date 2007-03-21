from framework import *
root.title("Font family, size, slant & weight test ($Revision: 1.3 $)")

texts = "Python Tkinter foo bar spam".split()

for i in xrange(200):
	x = coord()
	y = coord()

	def rand_weight():
		if randint(0, 1000) > 500:
			return "bold"
		else:
			return "normal"
	
	def rand_slant():
		if randint(0, 1000) > 500:
			return "italic"
		else:
			return "roman"

	canv.create_text(x, y,
		text = choice(texts),
		fill = random_color(),
		font = (choice(["Helvetica", "Times"]),
			randint(10,30),
			rand_weight(),
			rand_slant()),
	)

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
