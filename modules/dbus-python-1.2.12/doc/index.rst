=======================================
dbus-python_: Python bindings for D-Bus
=======================================

.. _dbus-python: http://www.freedesktop.org/wiki/Software/DBusBindings#python

dbus-python is a Python binding for ``dbus``, the reference implementation
of the D-Bus protocol.

Problems and alternatives
=========================

dbus-python might not be the best D-Bus binding for you to use. dbus-python
does not follow the principle of "In the face of ambiguity, refuse the
temptation to guess", and can't be changed to not do so without seriously
breaking compatibility.

In addition, it uses libdbus (which has known problems with multi-threaded
use) and attempts to be main-loop-agnostic (which means you have to select
a suitable main loop for your application).

Alternative ways to get your Python code onto D-Bus include:

* GDBus, part of the GIO module of `GLib`_, via GObject-Introspection and
  `PyGI`_ (uses the GLib main loop and object model)

* QtDBus, part of `Qt`_, via `PyQt`_ (uses the Qt main loop and object model)

.. _GLib: http://developer.gnome.org/glib/
.. _PyGI: https://live.gnome.org/PyGObject
.. _Qt: https://qt.nokia.com/
.. _PyQT: http://www.riverbankcomputing.co.uk/software/pyqt/intro

Documentation
=============

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    tutorial
    dbus
    PY3PORT
    news
    API_CHANGES

Contributing to dbus-python
===========================

Please see `the Gitlab project`_.

.. _the Gitlab project: https://gitlab.freedesktop.org/dbus/dbus-python/blob/master/CONTRIBUTING.md

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
