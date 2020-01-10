# Contributing to dbus-gmain

dbus-gmain is hosted by freedesktop.org. The source code repository,
issue tracking and merge requests are provided by freedesktop.org's
Gitlab installation, as a branch in the dbus-glib project:
<https://gitlab.freedesktop.org/dbus/dbus-glib/tree/dbus-gmain>

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

* create a personal fork of <https://gitlab.freedesktop.org/dbus/dbus-glib>
  on freedesktop.org Gitlab
* push your changes to your personal fork as a branch
* create a merge request at
  <https://gitlab.freedesktop.org/dbus/dbus-glib/merge_requests>,
  and remember to specify `dbus-gmain` as the target branch

## Automated tests

For nontrivial changes please try to extend the test suite to cover it.
dbus-gmain uses GLib's test framework; tests are in the `tests/`
directory.

Run `make check` to run the test suite.

## Coding style

Please match the existing code style (Emacs: "gnu").

## Licensing

Please match the existing licensing (a dual-license: AFL-2.1 or GPL-2+,
recipient's choice). Entirely new modules can be placed under a more
permissive license: to avoid license proliferation, our preferred
permissive license is the variant of the MIT/X11 license used by the
Expat XML library (for example see the top of tools/ci-build.sh).

## Conduct

As a freedesktop.org project, dbus follows the Contributor Covenant,
found at: <https://www.freedesktop.org/wiki/CodeOfConduct>

Please conduct yourself in a respectful and civilised manner when
interacting with community members on mailing lists, IRC, or bug
trackers. The community represents the project as a whole, and abusive
or bullying behaviour is not tolerated by the project.

## (Lack of) versioning and releases

dbus-gmain is currently set up to be a git subtree or git submodule,
so it does not have releases in its own right. It gets merged or
otherwise included in larger projects like dbus-glib and dbus-python
instead.

## Information for maintainers

This section is not directly relevant to infrequent contributors.

### Updating the copies of dbus-gmain in dbus-glib and dbus-python

dbus-gmain is maintained via `git subtree`. To update one of the dependent
projects, assuming you have a checkout of the dbus-gmain branch of the
dbus-glib repository in ../dbus-gmain:

    git subtree pull -P dbus-gmain ../dbus-gmain HEAD

### Committing other people's patches

If applying a patch from someone else that created them via
"git-format-patch", you can use "git-am -s" to apply.  Otherwise
apply the patch and then use "git commit --author ..."

Nontrivial patches should always go through Gitlab for peer review,
so you should have an issue number or a merge request ID to refer to.
