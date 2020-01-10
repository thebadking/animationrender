/* Regression test for https://bugs.freedesktop.org/show_bug.cgi?id=23831 */
/* SPDX-License-Identifier: MIT */

#include <stdio.h>

#include <Python.h>

int main(void)
{
    int i;

    puts("1..1");

    for (i = 0; i < 100; ++i) {
        Py_Initialize();
        if (PyRun_SimpleString("import dbus\n") != 0) {
            puts("not ok 1 - there was an exception");
            return 1;
        }
        Py_Finalize();
    }

    puts("ok 1 - was able to import dbus 100 times");

    return 0;
}
