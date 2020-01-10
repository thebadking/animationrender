abs_top_srcdir = @abs_top_srcdir@
abs_top_builddir = @abs_top_builddir@
installed_testdir = ${libexecdir}/installed-tests/${PACKAGE_TARNAME}
installed_test_testdir = ${installed_testdir}/test
installed_test_metadir = ${datadir}/installed-tests/${PACKAGE_TARNAME}

ACLOCAL_AMFLAGS = -I m4
SUBDIRS = dbus-gmain .

CLEANFILES = \
	test/test-service.log \
	$(NULL)
EXTRA_DIST = \
	.travis.yml \
	AUTHORS \
	CONTRIBUTING.md \
	COPYING \
	dbus-python.pc.in \
	doc/_static/.gitignore \
	examples/example-async-client.py \
	examples/example-client.py \
	examples/example-service.py \
	examples/example-signal-emitter.py \
	examples/example-signal-recipient.py \
	examples/gconf-proxy-client.py \
	examples/gconf-proxy-service2.py \
	examples/list-system-services.py \
	examples/unix-fd-client.py \
	examples/unix-fd-service.py \
	setup.py \
	test/TestSuitePythonService.service.in \
	test/tmp-session-bus.conf.in \
	tools/check-c-style.sh \
	tools/check-coding-style.mk \
	tools/check-py-style.sh \
	tools/check-whitespace.sh
	tools/ci-build.sh \
	$(NULL)

# === C code ===

AM_CPPFLAGS = \
	-include config.h \
	-I$(top_srcdir)/include \
	$(DBUS_CFLAGS) \
	$(GLIB_CFLAGS) \
	$(PYTHON_CPPFLAGS) \
	$(NULL)
AM_CFLAGS = \
	$(WARN_CFLAGS) \
	$(NULL)
AM_LDFLAGS = \
	$(WARN_LDFLAGS) \
	$(NULL)

pymod_ldflags = \
	-module \
	-avoid-version \
	$(NULL)
pymod_libadd = \
	$(NULL)

if WINDOWS
# Win32 DLLs can't have undefined symbols (so this needs explicit linking
# against the Python DLL), and Python expects extensions to be *.pyd
# instead of *.dll
pymod_ldflags += \
	-no-undefined \
	-shrext ".pyd" \
	$(NULL)
pymod_libadd += \
	$(PYTHON_LIBS) \
	$(NULL)
endif

pyexec_LTLIBRARIES = \
	_dbus_bindings.la \
	_dbus_glib_bindings.la \
	$(NULL)

if ENABLE_INSTALLED_TESTS
nobase_installed_test_LTLIBRARIES = test/dbus_py_test.la
else
noinst_LTLIBRARIES = test/dbus_py_test.la
endif

_dbus_bindings_la_LDFLAGS = \
	$(pymod_ldflags) \
	-export-symbols-regex \(PyInit__\|init_\)dbus_bindings \
	$(AM_LDFLAGS) \
	$(NULL)
_dbus_bindings_la_LIBADD = \
	$(pymod_libadd) \
	$(DBUS_LIBS) \
	$(NULL)
_dbus_bindings_la_SOURCES = \
	dbus_bindings/abstract.c \
	dbus_bindings/bus.c \
	dbus_bindings/bytes.c \
	dbus_bindings/compat-internal.h \
	dbus_bindings/conn.c \
	dbus_bindings/conn-internal.h \
	dbus_bindings/conn-methods.c \
	dbus_bindings/containers.c \
	dbus_bindings/dbus_bindings-internal.h \
	dbus_bindings/debug.c \
	dbus_bindings/exceptions.c \
	dbus_bindings/float.c \
	dbus_bindings/generic.c \
	dbus_bindings/int.c \
	dbus_bindings/unixfd.c \
	dbus_bindings/libdbusconn.c \
	dbus_bindings/mainloop.c \
	dbus_bindings/message-append.c \
	dbus_bindings/message.c \
	dbus_bindings/message-get-args.c \
	dbus_bindings/message-internal.h \
	dbus_bindings/module.c \
	dbus_bindings/pending-call.c \
	dbus_bindings/server.c \
	dbus_bindings/signature.c \
	dbus_bindings/string.c \
	dbus_bindings/types-internal.h \
	dbus_bindings/validation.c \
	$(NULL)

dbus-gmain/libdbus-gmain.la:
	$(MAKE) -C dbus-gmain

_dbus_glib_bindings_la_LDFLAGS = \
	$(pymod_ldflags) \
	-export-symbols-regex \(PyInit__\|init_\)dbus_glib_bindings \
	$(AM_LDFLAGS) \
	$(NULL)
_dbus_glib_bindings_la_LIBADD = \
	dbus-gmain/libdbus-gmain.la \
	$(pymod_libadd) \
	$(DBUS_LIBS) \
	$(NULL)
_dbus_glib_bindings_la_SOURCES = \
	dbus_glib_bindings/module.c \
	$(NULL)

# unconditionally add an -rpath to force Libtool to build a shared library
test_dbus_py_test_la_LDFLAGS = \
	$(pymod_ldflags) \
	$(AM_LDFLAGS) \
	-rpath $(installed_testdir) \
	$(NULL)
test_dbus_py_test_la_LIBADD = $(DBUS_LIBS)
test_dbus_py_test_la_SOURCES = \
	include/dbus/dbus-python.h \
	test/dbus_py_test.c \
	$(NULL)

# === dbus package ===

nobase_python_PYTHON = \
    dbus/bus.py \
    dbus/connection.py \
    dbus/_compat.py \
    dbus/_dbus.py \
    dbus/decorators.py \
    dbus/exceptions.py \
    dbus/_expat_introspect_parser.py \
    dbus/gi_service.py \
    dbus/glib.py \
    dbus/__init__.py \
    dbus/lowlevel.py \
    dbus/mainloop/__init__.py \
    dbus/mainloop/glib.py \
    dbus/proxies.py \
    dbus/server.py \
    dbus/service.py \
    dbus/types.py

if !HAVE_PYTHON_3
nobase_python_PYTHON += \
    dbus/gobject_service.py \
    $(NULL)
endif

check_py_sources = $(nobase_python_PYTHON)
include $(top_srcdir)/tools/check-coding-style.mk

# === Devel stuff ===

pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = dbus-python.pc

dbusincludedir = $(includedir)/dbus-1.0/dbus
dbusinclude_HEADERS = include/dbus/dbus-python.h

# === Tests ===

cross-test-compile: all

cross-test-server:
	$(AM_TESTS_ENVIRONMENT) $(PYTHON) $(top_srcdir)/test/cross-test-server.py
cross-test-client:
	$(AM_TESTS_ENVIRONMENT) $(PYTHON) $(top_srcdir)/test/cross-test-client.py

AM_TESTS_ENVIRONMENT = \
	export DBUS_TOP_SRCDIR="$(abs_top_srcdir)"; \
	export DBUS_TOP_BUILDDIR="$(abs_top_builddir)"; \
	export DBUS_TEST_TMPDIR="$(abs_top_builddir)/test"; \
	export DBUS_TEST_UNINSTALLED=1; \
	export DBUS_PYTHON_VERSION='$(PACKAGE_VERSION)'; \
	export PYTHONPATH="$(abs_top_srcdir):$(abs_top_srcdir)/test:$(abs_top_builddir)/.libs:$(abs_top_builddir)/test/.libs"; \
	export PYTHON='$(PYTHON)'; \
	export DBUS_FATAL_WARNINGS=1; \
	$(NULL)

TEST_EXTENSIONS = .sh .py

LOG_DRIVER = env AM_TAP_AWK='$(AWK)' $(SHELL) $(top_srcdir)/build-aux/tap-driver.sh
SH_LOG_DRIVER = $(LOG_DRIVER)
PY_LOG_DRIVER = $(LOG_DRIVER)

LOG_COMPILER = $(DBUS_RUN_SESSION) \
	--config-file=$(top_builddir)/test/tmp-session-bus.conf \
	--
installed_log_compiler = $(DBUS_RUN_SESSION) \
	--config-file=$(installed_testdir)/test/tmp-session-bus.conf \
	--

installed_log_compiler += \
	env \
	PYTHON=$(PYTHON) \
	DBUS_TOP_SRCDIR=$(installed_testdir) \
	DBUS_TOP_BUILDDIR=$(installed_testdir) \
	$(NULL)

SH_LOG_COMPILER = $(LOG_COMPILER) $(SHELL)
PY_LOG_COMPILER = $(LOG_COMPILER) $(PYTHON)

dist_test_sh = \
	test/run-test.sh \
	$(NULL)

dist_test_py = \
	test/test-client.py \
	test/test-p2p.py \
	test/test-signals.py \
	test/test-standalone.py \
	test/test-unusable-main-loop.py \
	$(NULL)

dist_test_extra_python = \
	test/crosstest.py \
	$(NULL)

dist_test_extra_scripts = \
	test/cross-test-client.py \
	test/cross-test-server.py \
	test/test-service.py \
	test/wait-for-name.py \
	$(NULL)

if HAVE_PYTHON_3
dist_test_py += test/test-exception-py3.py
else
dist_test_py += test/test-exception-py2.py
endif

test_programs = \
	test/test-import-repeatedly \
	$(NULL)

test_test_import_repeatedly_SOURCES = test/import-repeatedly.c
test_test_import_repeatedly_CPPFLAGS = $(PYTHON_CPPFLAGS)
test_test_import_repeatedly_LDADD = $(PYTHON_LIBS) $(PYTHON_EXTRA_LIBS)
test_test_import_repeatedly_LDFLAGS = $(PYTHON_EXTRA_LDFLAGS)

TESTS = \
	$(dist_test_py) \
	$(dist_test_sh) \
	$(test_programs) \
	$(NULL)

noinst_DATA = \
	test/TestSuitePythonService.service \
	test/tmp-session-bus.conf \
	$(NULL)
CLEANFILES += $(noinst_DATA)

installed_test_test_data = \
	test/installable/TestSuitePythonService.service \
	test/installable/tmp-session-bus.conf \
	$(NULL)
CLEANFILES += $(installed_test_test_data)

$(noinst_DATA): test/%: test/%.in
	@$(MKDIR_P) $(dir $@)
	$(AM_V_GEN)$(SED) \
		-e 's|[@]PYTHON[@]|$(PYTHON)|g' \
		-e 's|[@]G_TEST_SRCDIR[@]|$(abs_top_srcdir)|g' \
		-e 's|[@]G_TEST_BUILDDIR[@]|$(abs_top_builddir)|g' \
		$< > $@

$(installed_test_test_data): test/installable/%: test/%.in
	@$(MKDIR_P) $(dir $@)
	$(AM_V_GEN)$(SED) \
		-e 's|[@]PYTHON[@]|$(PYTHON)|g' \
		-e 's|[@]G_TEST_SRCDIR[@]|$(installed_testdir)|g' \
		-e 's|[@]G_TEST_BUILDDIR[@]|$(installed_testdir)|g' \
		$< > $@

if ENABLE_INSTALLED_TESTS
nobase_installed_test_PROGRAMS = $(test_programs)
nobase_dist_installed_test_SCRIPTS = \
	$(dist_test_py) \
	$(dist_test_sh) \
	$(dist_test_extra_scripts) \
	$(NULL)
nobase_dist_installed_test_PYTHON = \
	$(dist_test_extra_python) \
	$(NULL)
installed_test_test_DATA = $(installed_test_test_data)
installed_test_meta_DATA = $(installed_test_metadata)
else
noinst_PROGRAMS = $(test_programs)
dist_noinst_SCRIPTS = \
	$(dist_test_py) \
	$(dist_test_sh) \
	$(dist_test_extra_scripts) \
	$(NULL)
endif

installed_test_metadata = \
	$(patsubst %,%.test,$(dist_test_py)) \
	$(patsubst %,%.test,$(dist_test_sh)) \
	$(patsubst %,%.test,$(test_programs)) \
	$(NULL)
CLEANFILES += $(installed_test_metadata)

$(patsubst %,%.test,$(dist_test_py)): %.test: Makefile
	@$(MKDIR_P) $(dir $@)
	$(AM_V_GEN) (echo '[Test]' > $@.tmp; \
	echo 'Type=session' >> $@.tmp; \
	echo 'Exec=$(installed_log_compiler) $(PYTHON) $(installed_testdir)/$*' >> $@.tmp; \
	mv $@.tmp $@)

$(patsubst %,%.test,$(dist_test_sh)): %.test: Makefile
	@$(MKDIR_P) $(dir $@)
	$(AM_V_GEN) (echo '[Test]' > $@.tmp; \
	echo 'Type=session' >> $@.tmp; \
	echo 'Exec=$(installed_log_compiler) $(installed_testdir)/$*' >> $@.tmp; \
	mv $@.tmp $@)

$(patsubst %,%.test,$(test_programs)): %.test: Makefile
	@$(MKDIR_P) $(dir $@)
	$(AM_V_GEN) (echo '[Test]' > $@.tmp; \
	echo 'Type=session' >> $@.tmp; \
	echo 'Exec=$(installed_log_compiler) $(installed_testdir)/$*$(EXEEXT)' >> $@.tmp; \
	mv $@.tmp $@)

# === Documentation ===

dist-hook:
	echo $(VERSION) > $(distdir)/.version
	touch $(distdir)/MANIFEST
	touch $(distdir)/MANIFEST.in
	( cd $(distdir) && $(PYTHON) setup.py egg_info )
	cp $(distdir)/dbus_python.egg-info/PKG-INFO $(distdir)
	( cd $(distdir) && find -type d -o -print ) | \
		LC_ALL=C sort | \
		$(SED) -e 's|^\./||' \
		> $(distdir)/MANIFEST
	sed -e 's/.*/include &/' < $(distdir)/MANIFEST > $(distdir)/MANIFEST.in
	cp $(distdir)/MANIFEST $(distdir)/dbus_python.egg-info/SOURCES.txt

maintainer-upload:
	rsync -tvpP --chmod=ugo=r $(DIST_ARCHIVES) $(DIST_ARCHIVES:%=%.asc) \
	dbus.freedesktop.org:/srv/dbus.freedesktop.org/www/releases/dbus-python/

sphinx_sources = \
	doc/API_CHANGES.txt \
	doc/conf.py \
	doc/dbus.bus.rst \
	doc/dbus.connection.rst \
	doc/dbus.decorators.rst \
	doc/dbus.exceptions.rst \
	doc/dbus.gi_service.rst \
	doc/dbus.glib.rst \
	doc/dbus.gobject_service.rst \
	doc/dbus.lowlevel.rst \
	doc/dbus.mainloop.rst \
	doc/dbus.proxies.rst \
	doc/dbus.rst \
	doc/dbus.server.rst \
	doc/dbus.service.rst \
	doc/dbus.types.rst \
	doc/index.rst \
	doc/news.rst \
	doc/PY3PORT.txt \
	doc/tutorial.txt \
	NEWS \
	README \
	$(NULL)
EXTRA_DIST += $(sphinx_sources)

# A hack used for the HTML documentation on dbus.freedesktop.org
EXTRA_DIST += \
	doc/redirects \
	doc/redirects.py \
	$(NULL)

install-data-local: install-data-local-sphinx
uninstall-local: uninstall-local-pycache
uninstall-local: uninstall-local-sphinx

uninstall-local-pycache:
	rm -fr $(DESTDIR)$(pythondir)/dbus/__pycache__
	rm -fr $(DESTDIR)$(pythondir)/dbus/mainloop/__pycache__

if ENABLE_DOCUMENTATION
all: doc/_build/.stamp

doc/_build/.stamp: $(nobase_python_PYTHON) \
			_dbus_bindings.la \
			_dbus_glib_bindings.la \
			$(sphinx_sources) \
			Makefile \
			$(NULL)
	rm -rf doc/_build
	$(MKDIR_P) doc/_build
	abs_top_srcdir='$(abs_top_srcdir)' \
	abs_top_builddir='$(abs_top_builddir)' \
	DBUS_PYTHON_NO_DEPRECATED=1 \
	$(PYTHON) -m sphinx -b html $(abs_top_srcdir)/doc doc/_build
	touch $@

maintainer-update-website: doc/_build/.stamp
	DBUS_TOP_SRCDIR="$(abs_top_srcdir)" \
	$(PYTHON) $(srcdir)/doc/redirects.py
	rsync -rtvzPp --chmod=Dg+s,ug+rwX,o=rX doc/_build/ \
	dbus.freedesktop.org:/srv/dbus.freedesktop.org/www/doc/dbus-python/

install-data-local-sphinx: doc/_build/.stamp
	$(mkinstalldirs) $(DESTDIR)$(htmldir)
	cp -R doc/_build/* $(DESTDIR)$(htmldir)

uninstall-local-sphinx:
	rm -fr $(DESTDIR)$(htmldir)
else
maintainer-update-website:
	@echo "*** Not updating the API docs on the website - install sphinx"
	@echo "*** and configure with --enable-api-docs"
install-data-local-sphinx:
	@:
uninstall-local-sphinx:
	@:
endif

clean-local:
	rm -rf doc/_build

check_c_sources = \
	$(_dbus_bindings_la_SOURCES) \
	$(_dbus_glib_bindings_la_SOURCES) \
	$(NULL)

include $(top_srcdir)/tools/check-coding-style.mk

.PHONY: cross-test-compile cross-test-server cross-test-client \
	always-rebuild maintainer-update-website \
	maintainer-upload
