import os, sys
import pyinotify

PATH = '%s/tests' % os.getcwd()

class EventHandler(pyinotify.ProcessEvent):
    def process_default(self, event):
        print "==> ", event.maskname, ": ", event.pathname

notifier = pyinotify.Notifier(wm, EventHandler(), 0, 0, 10)

wm.add_watch(PATH, pyinotify.ALL_EVENTS, rec=True)

notifier.loop()
