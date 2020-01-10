-*- mode: m4 -*-
AC_PREREQ(2.59c)

dnl The dbus-python version number
m4_define(dbus_python_major_version, 1)
m4_define(dbus_python_minor_version, 2)
dnl Micro version is odd for non-releases
m4_define(dbus_python_micro_version, 12)

AC_INIT([dbus-python],
  dbus_python_major_version.dbus_python_minor_version.dbus_python_micro_version,
  [http://bugs.freedesktop.org/enter_bug.cgi?product=dbus&component=python])
AC_CONFIG_MACRO_DIR([m4])
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES])
AC_CONFIG_AUX_DIR([build-aux])

m4_pattern_forbid([^AX_],
  [Unexpanded AX_ macro found. Please install GNU autoconf-archive])

# By default, rebuild autotools files on demand; only use ./missing if the
# user says --disable-maintainer-mode (in particular this is useful when
# running under pip, which does not preserve timestamps)
AM_MAINTAINER_MODE([enable])

AX_IS_RELEASE([micro-version])
AC_DEFINE(DBUS_PYTHON_MAJOR_VERSION, dbus_python_major_version, [dbus-python major version])
AC_SUBST(DBUS_PYTHON_MAJOR_VERSION, dbus_python_major_version)
AC_DEFINE(DBUS_PYTHON_MINOR_VERSION, dbus_python_minor_version, [dbus-python minor version])
AC_SUBST(DBUS_PYTHON_MINOR_VERSION, dbus_python_minor_version)
AC_DEFINE(DBUS_PYTHON_MICRO_VERSION, dbus_python_micro_version, [dbus-python micro version])
AC_SUBST(DBUS_PYTHON_MICRO_VERSION, dbus_python_micro_version)

AC_CONFIG_SRCDIR([dbus_bindings/module.c])
AC_CONFIG_HEADERS(config.h)
AC_USE_SYSTEM_EXTENSIONS

AM_INIT_AUTOMAKE([1.13 -Wno-portability foreign subdir-objects tar-ustar])

AC_CANONICAL_BUILD
AC_CANONICAL_HOST

# mingw32, mingw-w64 are native Windows; for our purposes, Cygwin isn't
AC_MSG_CHECKING([for native Windows host])
AS_CASE(["$host"],
  [*-*-mingw*],
    [windows=yes],
  [*],
    [windows=no])
AC_MSG_RESULT([$windows])
AM_CONDITIONAL([WINDOWS], [test "x$windows" = xyes])

AC_DISABLE_STATIC

dnl XXXX hack to kill off all the libtool tags ...
dnl it isn't like we are using C++ or Fortran.
dnl (copied from libglade/configure.in)
m4_define([_LT_AC_TAGCONFIG],[])

AC_PROG_LIBTOOL
AM_PROG_CC_C_O
AC_C_INLINE
AC_PROG_MKDIR_P

AC_PROG_AWK
AC_REQUIRE_AUX_FILE([tap-driver.sh])

AC_ARG_VAR([PYTHON_CPPFLAGS],
  [compiler flags to find Python headers [default: auto-detect] [typical value: -I/opt/mypython/include]])
AC_ARG_VAR([PYTHON_LIBS],
  [libraries to link into Python extensions [default: auto-detect] [typical value: -L/opt/mypython/lib -lpython2.7]])
AC_ARG_VAR([PYTHON_EXTRA_LIBS],
  [libraries to link when embedding a Python interpreter [default: auto-detect]])
AC_ARG_VAR([PYTHON_EXTRA_LDFLAGS],
  [compiler flags to link when embedding a Python interpreter [default: auto-detect]])

AC_ARG_VAR([PYTHON_INCLUDES], [deprecated form of PYTHON_CPPFLAGS])
AS_IF([test -n "$PYTHON_INCLUDES"],
  [PYTHON_CPPFLAGS="$PYTHON_CPPFLAGS $PYTHON_INCLUDES"])

AX_PYTHON_DEVEL([>= '2.7'])
AM_PATH_PYTHON

# This command exits 0 (success) if sys.version >= "3", or 1 (failure)
# if sys.version < "3" (i.e. starts with "2").
AM_CONDITIONAL([HAVE_PYTHON_3],
  [$PYTHON -c "import sys; sys.exit(sys.version < '3')"])

PLATFORM=`$PYTHON -c "from __future__ import print_function; from distutils import util; print(util.get_platform())"`
AC_SUBST(PLATFORM)

AC_ARG_ENABLE([installed-tests],
  [AC_HELP_STRING([--enable-installed tests],
    [install test programs and helpers for as-installed testing])],
  [],
  [enable_installed_tests=no])
AM_CONDITIONAL([ENABLE_INSTALLED_TESTS], [test "_$enable_installed_tests" = _yes])

dnl Building documentation

AC_ARG_ENABLE([documentation],
  [AC_HELP_STRING([--enable-documentation],
    [Enable documentation building (requires sphinx and sphinx_rtd_theme)])],
  [:],
  [enable_documentation=auto])
AX_PYTHON_MODULE([sphinx])
AS_IF([test "x$HAVE_PYMOD_SPHINX" = xno],
  [
  AS_IF([test "$enable_documentation" = yes],
    [AC_MSG_ERROR([cannot build documentation without sphinx Python module])],
    [enable_documentation=no])
  ])
AX_PYTHON_MODULE([sphinx_rtd_theme])
AS_IF([test "x$HAVE_PYMOD_SPHINX_RTD_THEME" = xno],
  [
  AS_IF([test "$enable_documentation" = yes],
    [AC_MSG_ERROR([cannot build documentation without sphinx_rtd_theme Python module])],
    [enable_documentation=no])
  ])

AC_ARG_VAR([DBUS_RUN_SESSION],
  [The dbus-run-session tool from dbus 1.8 or later])
AC_PATH_PROG([DBUS_RUN_SESSION], [dbus-run-session], [dbus-run-session])

AM_CONDITIONAL([ENABLE_DOCUMENTATION], [test "$enable_documentation" != no])

PKG_CHECK_MODULES(DBUS, [dbus-1 >= 1.8])
PKG_CHECK_MODULES([GLIB], [glib-2.0 >= 2.40])

AX_COMPILER_FLAGS([WARN_CFLAGS],
  [WARN_LDFLAGS], [],
  dnl unfortunately the Python headers fail various checks included in
  dnl AX_COMPILER_FLAGS, and are not const-correct for strings
  [ \
   -Wdeprecated-declarations \
   -Wno-duplicated-branches \
   -Wno-redundant-decls \
   -Wno-switch-default \
   -Wno-write-strings \
  ])
dnl AX_COMPILER_FLAGS doesn't order the compiler flags correctly to be able
dnl to disable flags that it would normally enable
WARN_CFLAGS="$(echo "${WARN_CFLAGS}" | ${SED} \
  -e s/-Wduplicated-branches// \
  -e s/-Wredundant-decls// \
  -e s/-Wswitch-default// \
  -e s/-Wwrite-strings// \
  )"

AC_ARG_ENABLE([coding-style-checks],
  [AC_HELP_STRING([--enable-coding-style-checks],
                 [check coding style using grep])],
  [ENABLE_CODING_STYLE_CHECKS=$enableval],
  [ENABLE_CODING_STYLE_CHECKS=$ax_is_release])

# Make dbus-gmain submodule part of dbus-python's namespace
AH_BOTTOM([
#define DBUS_GMAIN_FUNCTION_NAME(name) _dbus_py_glib_ ## name
])

AC_CONFIG_FILES([
  Makefile
  dbus-gmain/Makefile
  dbus-python.pc
])
AC_OUTPUT
