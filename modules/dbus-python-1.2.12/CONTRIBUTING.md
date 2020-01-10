# Contributing to dbus-python

## Source code repository and issue tracking

dbus-python is hosted by freedesktop.org. The source code repository,
issue tracking and merge requests are provided by freedesktop.org's
Gitlab installation: <https://gitlab.freedesktop.org/dbus/dbus-python>

## Making changes

If you are making changes that you wish to be incorporated upstream,
please do as small commits to your local git tree that are individually
correct, so there is a good history of your changes.

The first line of the commit message should be a single sentence that
describes the change, optionally with a prefix that identifies the
area of the code that is affected.

The body of the commit message should describe what the patch changes
and why, and also note any particular side effects. This shouldn't be
empty on most of the cases. It shouldn't take a lot of effort to write a
commit message for an obvious change, so an empty commit message body is
only acceptable if the questions "What?" and "Why?" are already answered
on the one-line summary.

The lines of the commit message should have at most 76 characters,
to cope with the way git log presents them.

See [notes on commit messages](https://who-t.blogspot.com/2009/12/on-commit-messages.html),
[A Note About Git Commit Messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
or [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
for recommended reading on writing high-quality commit messages.

Your patches should also include a Signed-off-by line with your name and
email address, indicating that your contribution follows the [Developer's
Certificate of Origin](https://developercertificate.org/). If you're
not the patch's original author, you should also gather S-o-b's by
them (and/or whomever gave the patch to you.) The significance of this
is that it certifies that you created the patch, that it was created
under an appropriate open source license, or provided to you under those
terms. This lets us indicate a chain of responsibility for the copyright
status of the code.

We won't reject patches that lack S-o-b, but it is strongly recommended.

When you consider changes ready for merging to mainline:

* create a personal fork of <https://gitlab.freedesktop.org/dbus/dbus-python>
  on freedesktop.org Gitlab
* push your changes to your personal fork as a branch
* create a merge request at
  <https://gitlab.freedesktop.org/dbus/dbus-python/merge_requests>

## Automated tests

For nontrivial changes please try to extend the test suite to cover it.

Run `make check` to run the test suite.

## Coding style

Please match the existing coding style, which should be approximately
[PEP8](https://www.python.org/dev/peps/pep-0008/) (with 4-space
indentation and no hard tabs) for Python code, and
[PEP7](https://www.python.org/dev/peps/pep-0007/) for C code.
Docstrings etc. are reStructuredText.

(The `dbus-gmain` subproject is maintained separately, and uses the
same GNU/GNOME coding style as libdbus and GLib.)

## Technical notes

### Modules

`dbus`, `dbus.service` and `dbus.mainloop` are core public API.

`dbus.lowlevel` provides a lower-level public API for advanced use.

`dbus.mainloop.glib` is the public API for the GLib main loop integration.

`dbus.types` and `dbus.exceptions` are mainly for backwards
compatibility - use `dbus` instead in new code. Ditto `dbus.glib`.

`dbus._dbus`, `dbus.introspect_parser`, `dbus.proxies` are internal
implementation details.

`_dbus_bindings` is the real implementation of the Python/libdbus
integration, while `_dbus_bindings` is the real implementation of
Python/libdbus-glib integration. Neither is public API, although some
of the classes and functions are exposed as public API in other modules.

### Threading/locking model

All Python functions must be called with the GIL (obviously).

Before calling into any D-Bus function that can block, release the GIL;
as well as the usual "be nice to other threads", D-Bus does its own
locking and we don't want to deadlock with it. Most Connection methods
can block.

## Licensing

Please match the existing licensing. This is the variant of the MIT/X11
license used by the Expat XML library ("MIT" in the SPDX license
vocabulary).

(The `dbus-gmain` subproject is maintained separately, and uses the
same AFL-2.1/GPL-2.0-or-later license as libdbus.)

## Conduct

As a freedesktop.org project, dbus follows the Contributor Covenant,
found at: <https://www.freedesktop.org/wiki/CodeOfConduct>

Please conduct yourself in a respectful and civilised manner when
interacting with community members on mailing lists, IRC, or bug
trackers. The community represents the project as a whole, and abusive
or bullying behaviour is not tolerated by the project.

## Versioning

Version 1.Y.Z, where the micro version *Z* is even (divisible by 2),
is a real release.

Version 1.Y.(Z+1), where *Z* is even (divisible by 2), identifies a
development snapshot leading to version 1.Y.(Z+2). Odd-numbered versions
should never be used as releases.

In the unlikely event that major feature work is done on dbus-python in
future, the minor version *Y* should be set to an odd number (matching
the versioning policy of libdbus) on the development branch, with bug
fixes for the 1.2.x stable series cherry-picked to a `dbus-python-1.2`
branch.

## Contributing to dbus-gmain

The `dbus-gmain` subproject is shared by `dbus-python` and `dbus-glib`,
and has its own contributing guidelines (which are similar to these).
Please see [dbus-gmain/CONTRIBUTING.md](dbus-gmain/CONTRIBUTING.md)
for details.

## Information for maintainers

This section is not directly relevant to infrequent contributors.

### dbus-gmain

dbus-gmain is maintained via `git subtree`. To update, assuming you have
a checkout of the `dbus-gmain` branch of the
[dbus-glib](https://gitlab.freedesktop.org/dbus/dbus-glib) repository in
the `../dbus-gmain` directory:

    git subtree pull -P dbus-gmain ../dbus-gmain HEAD

### Committing other people's patches

If applying a patch from someone else that created them via
"git-format-patch", you can use "git-am -s" to apply.  Otherwise
apply the patch and then use "git commit --author ..."

Nontrivial patches should always go through Gitlab for peer review,
so you should have an issue number or a merge request ID to refer to.

### Making a release

#### Pre-release steps

* Make sure CI (currently Travis-CI and Gitlab) is passing
* Update `NEWS` and the version number in `configure.ac`, and commit them

#### Building and uploading the release

If `${builddir}` is the path to a build directory and `${version}`
is the new version:

```
make -C ${builddir} distcheck
# do any final testing here, e.g. updating the Debian package
git tag -m dbus-python-${version} -s dbus-python-${version}
gpg --detach-sign -a ${builddir}/dbus-python-${version}.tar.gz
make -C ${builddir} maintainer-upload
make -C ${builddir} maintainer-update-website
twine upload ${builddir}/dbus-python-${version}.tar.gz{,.asc}
```

#### Post-release steps

* Announce the new release to the D-Bus mailing list
* Update `NEWS` and the version number in `configure.ac`, and commit them
