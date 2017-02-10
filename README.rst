Tkinter canvas to SVG exporter
========================================================================

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


``warnings(mode)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Module might emit warnings. By default it use custom function which
prints message on the standard error. You can change this by calling
method ``canvasvg.warnings(mode)`` with three possible values:

* ``canvasvg.PYTHON`` --- use ``warn`` from the standard module
  ``warnings``;
* ``canvasvg.MODULE`` --- use the custom function;
* ``canvasvg.NONE``   --- do not print any message.


``configure(*flags)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Module might use either ``<path>`` or ``<line>`` tag for segment
representation. By default it uses ``<line>``. The behaviour could be changed
globally by calling ``canvasvg.configure(*flags)`` with one of consequent
values:

* ``canvasvg.SEGMENT_TO_LINE`` --- use ``<line>`` tag;
* ``canvasvg.SEGMENT_TO_PATH`` --- use ``<path>`` tag.


Changelog
------------------------------------------------------------------------

Below are major changes made before moving on Github__.

* 2013-07-23 --- support for "raw" smoothed lines (contributed by Marc Culler, author of plink__)
* 2011-02-20 --- python3 compatibility
* 2011-01-25 --- update ``saveall``: use list of items to export
* 2008-11-08 --- added ``tounicode``, optional argument
* 2006-12-01 --- initial release

__ https://github.com/WojciechMula/canvas2svg
__ http://www.math.uic.edu/t3m/plink/doc/
