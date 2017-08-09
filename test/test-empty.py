from framework import *

# This test reproduces `TypeError: 'NoneType' object is not iterable` raised on
# empty canvas conversion attempt.

canvasvg.saveall(__file__ + '.svg', canv)

os.system("inkview %s.svg" % __file__)
