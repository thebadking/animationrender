dbus-gmain - GLib main loop integration for libdbus
===================================================

This directory contains GLib main loop integration for libdbus, salvaged
from dbus-glib. At the moment it is designed to be bundled in other
projects using the `git subtree` or `git submodule` commands.

Please do not use this module unless you really need it. The majority
of GLib-based D-Bus users would be better off using GDBus, part of GLib,
instead of the low-level APIs provided by libdbus. In particular, the
combination of dbus-gmain and libdbus is known to have thread-safety
issues.

However, using this module is still better than using dbus-glib; the
rest of dbus-glib mostly consists of design flaws.

Integrating dbus-gmain in a larger project
------------------------------------------

dbus-gmain requires libdbus >= 1.8. This can be reduced to some ancient
version if you don't build the tests.

dbus-gmain requires GLib >= 2.40. This can be reduced to 2.32, or
probably older, if you don't build the tests.

If you use the included Makefile.am (which requires building the tests),
you must check for libdbus via pkg-config using the prefix `DBUS`, check
for GLib (and optionally gobject and gio) via pkg-config using the prefix
`GLIB`, and check for `DBUS_RUN_SESSION` for the tests:

```
PKG_CHECK_MODULES([DBUS], [dbus-1 >= 1.8])
PKG_CHECK_MODULES([GLIB], [glib-2.0 >= 2.40])
AC_ARG_VAR([DBUS_RUN_SESSION],
  [The dbus-run-session tool from dbus 1.8 or later])
AC_PATH_PROG([DBUS_RUN_SESSION], [dbus-run-session], [dbus-run-session])
```

Alternatively, you can include dbus-gmain.[ch] among the source files for
some executable or library.

By default, dbus-gmain declares its functions in the `dbus_gmain_`\*
namespace. To change this, define `DBUS_GMAIN_FUNCTION_NAME(name)` to
a suitably prefixed or suffixed version of name. The default is
`dbus_gmain_ ## name`.

By default, dbus-gmain declares its functions `G_GNUC_INTERNAL`, so they
will not be part of your library's ABI on supported compilers. To change
this (not recommended), define `DBUS_GMAIN_FUNCTION(ret, name, ...)` to
a form that includes suitable decorators. The default is
`G_GNUC_INTERNAL ret DBUS_GMAIN_FUNCTION_NAME (name) (__VA_ARGS__)`.
