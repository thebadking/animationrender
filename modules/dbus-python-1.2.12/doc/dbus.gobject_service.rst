.. This is not done via automodule because it cannot be imported in
.. Python 3.

dbus.gobject\_service module
----------------------------

.. py:module:: gobject_service

This module is only available when using Python 2, and is deprecated.

.. py:class:: ExportedGObjectType(cls, name, bases, dct)

    A metaclass which inherits from both GObjectMeta and
    `dbus.service.InterfaceType`. Used as the metaclass for
    `ExportedGObject`.

.. py:class:: ExportedGObject(self, conn=None, object_path=None, **kwargs)

    A GObject which is exported on the D-Bus.

    Because GObject and `dbus.service.Object` both have custom metaclasses,
    the naive approach using simple multiple inheritance won't work. This
    class has `ExportedGObjectType` as its metaclass, which is sufficient
    to make it work correctly.

    :param dbus.connection.Connection conn:
         The D-Bus connection or bus
    :param str object_path:
         The object path at which to register this object.
    :keyword dbus.service.BusName bus_name:
         A bus name to be held on behalf of this object, or None.
    :keyword dict gobject_properties:
         GObject properties to be set on the constructed object.

         Any unrecognised keyword arguments will also be interpreted
         as GObject properties.
