from framework import *
root.title("Disabled text")

canv.create_text(200, 200,
	text = "Test disabled text",
	font = ("Times", 20),
	state = DISABLED
)

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
