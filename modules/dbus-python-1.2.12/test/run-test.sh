#! /bin/bash

# Copyright (C) 2006 Red Hat Inc. <http://www.redhat.com/>
# Copyright (C) 2006-2007 Collabora Ltd. <http://www.collabora.co.uk/>
#
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

set -e

failed=
test_num=0

echo "# DBUS_TOP_SRCDIR=$DBUS_TOP_SRCDIR"
echo "# DBUS_TOP_BUILDDIR=$DBUS_TOP_BUILDDIR"
echo "# PYTHONPATH=$PYTHONPATH"
echo "# PYTHON=${PYTHON:=python}"

if ! [ -d "$DBUS_TEST_TMPDIR" ]; then
  DBUS_TEST_TMPDIR="$(mktemp -d)"
  if ! [ -d "$DBUS_TEST_TMPDIR" ]; then
    echo "Bail out! Failed to create temporary directory (install mktemp?)"
    exit 1
  fi
fi

if ! "$PYTHON" -c 'from gi.repository import GLib'; then
  echo "1..0 # SKIP could not import python-gi"
  exit 0
fi

ok () {
  test_num=$(( $test_num + 1 ))
  echo "ok $test_num - $*"
}

not_ok () {
  test_num=$(( $test_num + 1 ))
  echo "not ok $test_num - $*"
}

skip () {
  test_num=$(( $test_num + 1 ))
  echo "ok $test_num # SKIP - $*"
}

dbus-monitor > "$DBUS_TEST_TMPDIR"/monitor.log &

#echo "running the examples"

#$PYTHON "$DBUS_TOP_SRCDIR"/examples/example-service.py &
#$PYTHON "$DBUS_TOP_SRCDIR"/examples/example-signal-emitter.py &
#$PYTHON "$DBUS_TOP_SRCDIR"/examples/list-system-services.py --session ||
#  die "list-system-services.py --session failed!"
#$PYTHON "$DBUS_TOP_SRCDIR"/examples/example-async-client.py ||
#  die "example-async-client failed!"
#$PYTHON "$DBUS_TOP_SRCDIR"/examples/example-client.py --exit-service ||
#  die "example-client failed!"
#$PYTHON "$DBUS_TOP_SRCDIR"/examples/example-signal-recipient.py --exit-service ||
#  die "example-signal-recipient failed!"

echo "# running cross-test (for better diagnostics use mjj29's dbus-test)"

$PYTHON "$DBUS_TOP_SRCDIR"/test/cross-test-server.py > "$DBUS_TEST_TMPDIR"/cross-server.log &
cross_test_server_pid="$!"

$PYTHON "$DBUS_TOP_SRCDIR"/test/wait-for-name.py org.freedesktop.DBus.Binding.TestServer >&2

e=0
$PYTHON "$DBUS_TOP_SRCDIR"/test/cross-test-client.py > "$DBUS_TEST_TMPDIR"/cross-client.log || e=$?
echo "# test-client exit status: $e"

if test "$e" = 77; then
  skip "cross-test-client exited $e, marking as skipped"
elif grep . "$DBUS_TEST_TMPDIR"/cross-client.log >/dev/null; then
  ok "cross-test-client produced some output"
else
  not_ok "cross-test-client produced no output"
fi

if test "$e" = 77; then
  skip "test-client exited $e, marking as skipped"
elif grep . "$DBUS_TEST_TMPDIR"/cross-server.log >/dev/null; then
  ok "cross-test-server produced some output"
else
  not_ok "cross-test-server produced no output"
fi

if grep fail "$DBUS_TEST_TMPDIR"/cross-client.log >&2; then
  not_ok "cross-client reported failures"
else
  ok "cross-test client reported no failures"
fi

if grep untested "$DBUS_TEST_TMPDIR"/cross-server.log; then
  not_ok "cross-server reported untested functions"
else
  ok "cross-test server reported no untested functions"
fi

echo "# waiting for cross-test server to exit"
if wait "$cross_test_server_pid"; then
  ok "cross-test server: exit status 0"
else
  not_ok "cross-test server: exit status $?"
fi

echo "# ==== client log ===="
cat "$DBUS_TEST_TMPDIR"/cross-client.log | sed -e 's/^/#    /'
echo "# ==== end ===="

echo "# ==== server log ===="
cat "$DBUS_TEST_TMPDIR"/cross-server.log | sed -e 's/^/#    /'
echo "# ==== end ===="

rm -f "$DBUS_TEST_TMPDIR"/test-service.log
rm -f "$DBUS_TEST_TMPDIR"/cross-client.log
rm -f "$DBUS_TEST_TMPDIR"/cross-server.log
rm -f "$DBUS_TEST_TMPDIR"/monitor.log

echo "1..$test_num"

if test -n "$failed"; then
  exit 1
fi
exit 0
