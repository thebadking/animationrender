/* Regression test utilities
 *
 * Copyright © 2009-2018 Collabora Ltd. <http://www.collabora.co.uk/>
 * Copyright © 2009-2011 Nokia Corporation
 *
 * SPDX-License-Identifier: AFL-2.1 OR GPL-2.0-or-later
 *
 * Licensed under the Academic Free License version 2.1
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
 * 02110-1301  USA
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "util.h"

void
test_run_until_disconnected (DBusConnection *connection,
                             GMainContext *context)
{
  g_printerr ("Disconnecting... ");

  dbus_connection_set_exit_on_disconnect (connection, FALSE);
  dbus_connection_close (connection);

  while (dbus_connection_get_is_connected (connection))
    {
      g_printerr (".");
      g_main_context_iteration (context, TRUE);
    }

  g_printerr (" disconnected\n");
}
