# -*- coding: utf-8 -*-
import os
import pyinotify
import patoolib
from datetime import datetime

flags = pyinotify.ALL_EVENTS
files_dir = 'pdf/'
log_file = 'log_watcher.log'

class FileWatcher:
    notifier = None

    def start_watch(self, _dir, callback):
        wm = pyinotify.WatchManager()
        self.notifier = pyinotify.Notifier(wm, EventProcessor(callback))
        mask = (pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_DELETE
                | pyinotify.IN_DELETE_SELF | pyinotify.IN_MOVED_FROM
                | pyinotify.IN_MOVED_TO | pyinotify.IN_CLOSE_WRITE)
        wdd = wm.add_watch(_dir, mask, rec=True)
        write_log('Watchdog running...')
        while True:
            self.notifier.process_events()
            if self.notifier.check_events():
                self.notifier.read_events()

SUFFIXES = {'.pdf', '.txt', '.rar'}

def suffix_filter(event):
    # return True to stop processing of event (to 'stop chaining')
    return os.path.splitext(event.name)[1] not in SUFFIXES

def write_log(log_str):
    date_str = str(datetime.now().strftime('%Y.%m.%d %H:%M:%S')) + ': '
    res_str = date_str +log_str
    f1 = open(files_dir + log_file, 'a+')
    f1.write(res_str + '\r\n')
    f1.close()

class EventProcessor(pyinotify.ProcessEvent):

    def __init__(self, callback):
        self.event_callback = callback

    def __call(self, event):
        if not suffix_filter(event):
            super(EventProcessor, self).__call(event)

    def process_IN_CREATE(self, event):
        write_log('in CREATE: ' + event.pathname)

    def process_IN_DELETE(self, event):
        write_log('in DELETE: ' + event.pathname)

    def process_IN_DELETE_SELF(self, event):
        write_log('in DELETE_SELF: ' + event.pathname)

    def process_IN_MOVED_FROM(self, event):
        write_log('in MOVED_FROM: ' + event.pathname)

    def process_IN_CLOSE_WRITE(self, event):
        write_log('in CLOSE_WRITE: ' + event.pathname)
        file_name = files_dir + event.pathname
        if os.path.splitext(event.name)[1] == '.pdf':
            # if RAR exists - delete
            if os.path.exists(file_name + '.rar'):
                os.remove(file_name + '.rar')
                # if TXT-marker exists - delete
                if os.path.exists(file_name + '.rar.txt'):
                    os.remove(file_name + '.rar.txt')
                # archiving
                patoolib.create_archive(file_name + '.rar', (file_name,))
            else:
                # archiving
                patoolib.create_archive(file_name + '.rar', (file_name,))
        if os.path.splitext(event.name)[1] == '.rar':
            if not os.path.exists(file_name + '.rar'):
                write_log('OK. RAR Archive created: ' + event.pathname)
                # create txt-marker
                f = open(file_name + '.txt', 'a')
                f.write('OK')
                f.close()

                # delete sorce pdf
                if os.path.exists(event.pathname[0:-4]):
                    os.remove(event.pathname[0:-4])
                else:
                    write_log('The file does not exist: ' + event.pathname)

f = FileWatcher()
f.start_watch(files_dir, None)

































