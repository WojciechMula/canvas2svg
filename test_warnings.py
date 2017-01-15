import canvasvg
from canvasvg import saveall

import turtle
turtle.forward(100)

for mode in [canvasvg.PYTHON, canvasvg.MODULE, canvasvg.NONE]:
    print("warning mode = %d\n" % mode)
    canvasvg.warnings(mode)
    saveall('turtlepower.svg', turtle.getscreen().getcanvas())
