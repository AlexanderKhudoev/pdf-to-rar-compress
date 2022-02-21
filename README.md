## Problem

Storing large PDFs (over 2GB) wastes server space and causes problems when downloading with Google Chrome.

## Solution

The most efficient way to save server space is to compress `PDF` to `RAR`.

RAR compression provides nearly 20x PDF compression and is currently the best compression algorithm for `pdf`
and can reduce file size tenfold
(comparison chart - zip, 7z, rar)

On a Linux server, this can be done by creating a watchdog script in [Python 3](https://www.python.org/downloads/)
and the [patool package](https://pypi.org/project/patool/).

### General idea of the script

1. When the `pdf` file appears and ready to work, archiving in `rar` will start.

**_Pay attention_** to the phrase `"the file is ready to work"`: _a file that is still in the process of being written
to disk cannot be called "ready to work". You need to wait, the file will be completely written to the disk, and only then you can work with it (otherwise the broken file will be archived, which then cannot be read)_.

2. After the successful creation of the `rar archive`, a `text file` will be created, which will be a kind of `marker`
3. signaling to any `external system` that the archive is `successfully ready`.

For example, if the external system is `Oracle`, and you want to write the `RAR file` into `database field`.
Here it is important to track the moment when the file is `completely ready` and formed for further actions.
For example, it may turn out that the file is not yet fully copied to the directory.
To do this, Linux has several file-specific events.

We need the following `Linux file system events`:
- IN_CREATE
- CLOSE_WRITE
- MOVED_TO
- MOVED_FROM
- IN_DELETE
- IN_DELETE_SELF

## Requirements ##
- Python 3.6 or higher
- [pyinotify](https://github.com/seb-m/pyinotify/wiki)

Pyinotify is a Python module for monitoring filesystems changes.
Pyinotify relies on a Linux Kernel feature (merged in kernel 2.6.13) called inotify.
inotify is an event-driven notifier, its notifications are exported from kernel space to user space through three
system calls. pyinotify binds these system calls and provides an implementation on top of them offering a generic and
abstract way to manipulate those functionalities.

Follow the official documentation to [install pyinotify](https://github.com/seb-m/pyinotify/wiki/Install).
- [patoolib](http://wummel.github.io/patool/)

Patool is a library for creating, extracting, testing archives, including in the RAR format.

How to install patool is described [here](https://github.com/wummel/patool/blob/master/doc/install.txt).

## Intallation and Running
1. Clone or download repository
2. Put the [pdf_watchdog.py](https://github.com/AlexanderKhudoev/pdf-to-rar-compress/blob/master/pdf_watchdog.py) in any directory you want
3. Run the script from Terminal

## More info ##
- [Article](https://bit.ly/python-pdf-to-rar-script) about how I developed this script
- [Youtube Tutorial](https://youtu.be/EFdjKJ9xP0g) and Working Demo