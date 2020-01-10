#!/usr/bin/python

# SPDX-License-Identifier: MIT

import os

SRCDIR = os.environ.get('DBUS_TOP_SRCDIR', '.')

if __name__ == '__main__':
    with open(os.path.join(SRCDIR, 'doc', 'redirects'), 'r') as reader:
        for line in reader:
            line = line.strip()

            if not line:
                continue

            if line.startswith('#'):
                continue

            page, dest = line.split(None, 1)

            try:
                os.makedirs(os.path.join('doc', '_build', os.path.dirname(page)))
            except OSError:
                pass

            assert not os.path.exists(os.path.join('doc', '_build', page))

            if dest.startswith('"'):
                assert page.endswith('.txt')
                text = dest.strip('"')

                with open(os.path.join('doc', '_build', page), 'w') as writer:
                    writer.write(text)
                    writer.write('\n')
            else:
                assert page.endswith('.html')

                with open(os.path.join('doc', '_build', page), 'w') as writer:
                    writer.write(
                        '<meta http-equiv="refresh" content="0; url={}" />\n'.format(
                            dest))
                    writer.write(
                        'See <a href="{}">{}</a>\n'.format(
                            dest, dest))
