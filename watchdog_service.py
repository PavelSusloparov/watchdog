from datetime import datetime
import time
import threading
import os
import sys
import re
from optparse import OptionParser

import psutil

from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent, ALL_EVENTS, IN_DELETE_SELF, IN_OPEN

#Apache notify env
APACHE_PID = "/var/run/apache2.pid"

#TRS service log notify env
TRS_LOG =  '%s/testRunService/testRunService/logs/trs.log' % os.getcwd()
TRS_LOG_DIR = '/'.join(TRS_LOG.split('/')[:-1])
watch_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']

#System metrics
METRICS_TIMEOUT = 10

def LOG(msg):
    """
    Add datetime to current msg.

    @msg: print message.
    """
    print "[%s] %s" %  (str(datetime.now()), msg)

def mail_to_admin(time, msg, cpu=None):
    """
    Send mail to watch system administrator.
    Can be implemented. If really need.

    @time: current time, when event is occured.
    @msg: event explanations.
    @cpu: cpu metrics.
    """
    pass

def follow(thefile):
    """
    Follow a file like tail -f.

    @thefile: instance of following file.
    """
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

class FileWatcher(threading.Thread):
    """
    Thread is watching on TRS_LOG file and report if log the same as in watch_levels list.
    """
    def run(self):
       logfile = open(TRS_LOG, "r")
       loglines = follow(logfile)
       for line in loglines:
           LOG("LINE: %s" % line)
           log_level_raw = re.match('.* (?P<log_level>\w+) .*', line)
           log_level = log_level_raw.group('log_level')
           LOG("Log level: %s" % log_level)
           if log_level in watch_levels:
               res = "TRS log: Log level: %s. Log line: %s" % (log_level, line)
               LOG(res)
               if log_level == 'ERROR':
                   time_now = str(datetime.now())
                   mail_to_admin(time_now(), res)


class Metrics(threading.Thread):
    """
    Thread get system metrics every METRICS_TIMEOUT period.
    """
    def run(self):
        while True:
            LOG(psutil.cpu_times())
            time.sleep(METRICS_TIMEOUT)


class EventHandler(ProcessEvent):
    """
    ProvessEvent overload. Handling events.
    """
    def __init__(self):
        self.first_modify = True

    def process_IN_DELETE_SELF(self, event):
        """
        This method process a specific kind of event (IN_DELETE).

        @event: instance of Event.
        """
        if event.pathname == APACHE_PID:
            LOG("Apache is down. Restart..")
            if not os.system("/etc/init.d/apache2 start"):
                res = "Apache is succesfully restarted."
            else:
                res = "Can not restart apache. Please notify system administrator about accident."
            LOG(res)
            time_now = str(datetime.now())
            cpu = psutil.cpu_times()
            mail_to_admin(time_now(), res, cpu)

    def process_IN_MODIFY(self, event):
        """
        This method process a specific kind of event (IN_DELETE).

        @event: instance of Event.
        """
        if event.pathname == TRS_LOG and self.first_modify:
            fw = FileWatcher()
            fw.daemon = True
            fw.start()
            self.first_modify = False

    def process_default(self, event):
        """
        Ultimately, this method is called for all others kind of events.
        This method can be used when similar processing can be applied to various events.
        @event: instance of Event.
        """
        LOG("==> %s : %s" % (event.maskname, event.pathname))


class Notify():
    """
    File system watcher service. It watchs on files and directories.

    @watch_attr: dictionary with watcher path and watcher actions mask.
    """
    def __init__(self, watch_attr):
        self.wm = WatchManager()
        self.watch_attr = watch_attr

    def _addWatchers(self):
        for attr in self.watch_attr:
            self.wm.add_watch(attr['path'], ALL_EVENTS if not attr['mask'] else attr['mask'])

    def run(self):
        notifier = ThreadedNotifier(self.wm, EventHandler(), 0, 0, 10)
        self._addWatchers()
        notifier.loop()


class NotifyActions():
    """
    Includes watchdog actions.

    @need_actions: actions, which will be performed by Watchdog system.
    """
    def __init__(self, need_actions):
        self.actions = []
        if need_actions['apache']:
            self._restartApache()
        if need_actions['watch_log']:
            self._notifyTrsLog()
        if need_actions['system_metrics']:
            self._metrics()

    def getActions(self):
        return self.actions

    def _restartApache(self):
        if os.path.isfile(APACHE_PID):
            self.actions.append({'path': APACHE_PID, 'mask': IN_DELETE_SELF})
        else:
            raise Exception("Apache is down. Please execute 'sudo /etc/init.d/apache2 start'")

    def _notifyTrsLog(self):
        self.actions.append({'path': TRS_LOG_DIR, 'mask': ALL_EVENTS})

    def _metrics(self):
        m = Metrics()
        m.daemon = True
        m.start()

def main():
    parser = OptionParser(usage="python watchdog_service.py [options]",
                          description="Watchdog service, which allow watch on apache status, watch on Test Run Service log, get system metrics." )
    parser.add_option("-p", "--apache", action="store_true", dest="apache",
                  help="Watch on apache process.")
    parser.add_option("-l", "--watch_log", action="store_true", dest="watch_log",
                  help="Watch on Test Run Service log.")
    parser.add_option("-m", "--system_metrics", action="store_true", dest="system_metrics", help="Get system metrics.")
    parser.add_option("-a", "--all", action="store_true", dest="all",
                  help="Run all watchers.")

    (options, args) = parser.parse_args()

    need_actions = {'apache': False,
                    'watch_log': False,
                    'system_metrics': False
                    }

    if options.apache or options.all:
        need_actions['apache'] = True
    if options.watch_log or options.all:
        need_actions['watch_log'] = True
    if options.system_metrics or options.all:
        need_actions['system_metrics'] = True

    allow_run = False
    for status in need_actions.values():
        if status:
            allow_run = True

    if allow_run:
        actions = NotifyActions(need_actions).getActions()
        Notify(actions).run()
    else:
        print "Please specify watcher.\n"
        parser.print_help()


if __name__ == "__main__":
    main()
