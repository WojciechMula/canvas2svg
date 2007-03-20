from framework import *

print "different line join style"

d = 50
canv.move(canv.create_line(0, 0, d, 0, 2.0*d, d/2, joinstyle='bevel'), 10, 10+0*d)
canv.move(canv.create_line(0, 0, d, 0, 2.0*d, d  , joinstyle='bevel'), 10, 20+1*d)
canv.move(canv.create_line(0, 0, d, 0, 1.5*d, d  , joinstyle='bevel'), 10, 30+2*d)
canv.move(canv.create_line(0, 0, d, 0, 1.0*d, d  , joinstyle='bevel'), 10, 40+3*d)
canv.move(canv.create_line(0, 0, d, 0, 0.5*d, d  , joinstyle='bevel'), 10, 50+4*d)
canv.move(canv.create_line(0, 0, d, 0, 0.0*d, d  , joinstyle='bevel'), 10, 60+5*d)
canv.move(canv.create_line(0, 0, d, 0, 0.0*d, d/2, joinstyle='bevel'), 10, 70+6*d)

canv.move(canv.create_line(0, 0, d, 0, 2.0*d, d/2, joinstyle='miter'), 20+2*d, 10+0*d)
canv.move(canv.create_line(0, 0, d, 0, 2.0*d, d  , joinstyle='miter'), 20+2*d, 20+1*d)
canv.move(canv.create_line(0, 0, d, 0, 1.5*d, d  , joinstyle='miter'), 20+2*d, 30+2*d)
canv.move(canv.create_line(0, 0, d, 0, 1.0*d, d  , joinstyle='miter'), 20+2*d, 40+3*d)
canv.move(canv.create_line(0, 0, d, 0, 0.5*d, d  , joinstyle='miter'), 20+2*d, 50+4*d)
canv.move(canv.create_line(0, 0, d, 0, 0.0*d, d  , joinstyle='miter'), 20+2*d, 60+5*d)
canv.move(canv.create_line(0, 0, d, 0, 0.0*d, d/2, joinstyle='miter'), 20+2*d, 70+6*d)

canv.move(canv.create_line(0, 0, d, 0, 2.0*d, d/2, joinstyle='round'), 30+4*d, 10+0*d)
canv.move(canv.create_line(0, 0, d, 0, 2.0*d, d  , joinstyle='round'), 30+4*d, 20+1*d)
canv.move(canv.create_line(0, 0, d, 0, 1.5*d, d  , joinstyle='round'), 30+4*d, 30+2*d)
canv.move(canv.create_line(0, 0, d, 0, 1.0*d, d  , joinstyle='round'), 30+4*d, 40+3*d)
canv.move(canv.create_line(0, 0, d, 0, 0.5*d, d  , joinstyle='round'), 30+4*d, 50+4*d)
canv.move(canv.create_line(0, 0, d, 0, 0.0*d, d  , joinstyle='round'), 30+4*d, 60+5*d)
canv.move(canv.create_line(0, 0, d, 0, 0.0*d, d/2, joinstyle='round'), 30+4*d, 70+6*d)
canv.itemconfigure('all', width=10)

thread.start_new_thread(test, (canv, __file__, True))
root.mainloop()
