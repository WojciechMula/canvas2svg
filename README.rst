Tkinter canvas to SVG exporter
========================================================================

:Added on: 1.12.2006
:Update: 2013-07-23 --- support for "raw" smoothed lines (contributed by Marc Culler, author of plink_)
:Update: 2011-02-20 --- python3 compatibility
:Update: 2011-01-25 --- update ``saveall``: use list of items to export
:Update: 2008-11-08 --- added ``tounicode``, optional argument

This module provides function ``convert`` that convert all or selected
items placed on given canvas object.

Supported items:

* lines
* lines with arrows
* polygons
* smoothed lines and polygons
* ovals (i.e. circle & ellipse)
* arcs (all kind, i.e. ARC, CHORD, PIESLICE)
* rectangles
* text (**unwrapped** only i.e. attribute ``width = 0``)

Unsupported items:

* images
* bitmaps
* windows

Stipples are not applied.


Public functions
------------------------------------------------------------------------

``convert(document, canvas, items=None, tounicode=None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``document`` --- SVG document, object that support DOM, i.e. provides
  ``createElement`` method etc. (function ``SVGdocument`` can be used
  to get such object)
* ``canvas`` --- Tkinter.Canvas object
* ``items`` --- list of objects to convert; if ``None`` then all items
  are converted
* ``tounicode`` --- user function that should return proper unicode
  string if Tkinter app use other then ASCII encoding. By default
  ``tounicode = lambda text: unicode(text).encode('utf-8')``.
  Thanks to **Jan Böcker** who provided solution.


``SVGdocument``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Takes no arguments, returns SVG document;  class provided in standard
``xml.dom.minidom`` module is used.


``saveall(filename, canvas, items=None, margin=10, tounicode=None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Helper function: saves whole canvas or selected items in SVG file,
sets proper  dimensions, and viewport;  additional ``margin`` can
be set.

License & Author
------------------------------------------------------------------------

* License: BSD
* Author: Wojciech Muła, e-mail: wojciech_mula@poczta.onet.pl

.. _plink: http://www.math.uic.edu/t3m/plink/doc/
