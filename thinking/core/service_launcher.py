from __future__ import print_function
import logging
import signal
import threading
import time
import os
import random
import signal
import sys
import eventlet
from eventlet import event
from eventlet import greenpool

try:
    # Importing just the symbol here because the io module does not
    # exist in Python 2.6.
    from io import UnsupportedOperation  # noqa
except ImportError:
    # Python 2.6
    UnsupportedOperation = None

LOG = logging.getLogger(__name__)


def _sighup_supported():
    return hasattr(signal, 'SIGHUP')


def _signo_to_signame(signo):
    signals = {signal.SIGTERM: 'SIGTERM',
               signal.SIGINT: 'SIGINT'}
    if _sighup_supported():
        signals[signal.SIGHUP] = 'SIGHUP'
    return signals[signo]


def _set_signals_handler(handler):
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)
    if _sighup_supported():
        signal.signal(signal.SIGHUP, handler)


class SignalExit(SystemExit):
    def __init__(self, signo, exccode=1):
        super(SignalExit, self).__init__(exccode)
        self.signo = signo


class ServiceLauncher(object):

    def __init__(self):
        self.pool = greenpool.GreenPool(10)
        self.threads = []
        self.done = event.Event()

    def _handle_signal(self, signo, frame):
        # Allow the process to be killed again and die from natural causes
        _set_signals_handler(signal.SIG_DFL)
        raise SignalExit(signo)

    def handle_signal(self):
        _set_signals_handler(self._handle_signal)

    def _wait_for_exit_or_signal(self):
        status = None
        signo = 0

        try:

            current = threading.current_thread()

            # Iterate over a copy of self.threads so thread_done doesn't
            # modify the list while we're iterating
            for x in self.threads[:]:
                if x is current:
                    continue
                try:
                    # x.wait()
                except eventlet.greenlet.GreenletExit:
                    pass
                except Exception as ex:
                    print(ex)
        except SignalExit as exc:
            signame = _signo_to_signame(exc.signo)
            print(('Caught SignalExit %s, exiting') % signame)
            status = exc.code
            signo = exc.signo
        except SystemExit as exc:
            status = exc.code
        finally:
            self.stop()

        return status, signo

    def wait(self):
        while True:
            self.handle_signal()
            status, signo = self._wait_for_exit_or_signal()

    def launch_service(self, function, *args, **kwargs):
        def func_wrapper():
            function(*args, **kwargs)
            print("start to wait")
            self.done.wait()
            print("finish wait")

        gt = self.pool.spawn(func_wrapper, *args, **kwargs)
        self.threads.append(gt)

    def stop(self):
        if not self.done.ready():
            self.done.send()

def hello_world():
    print("hello world")

if __name__ == '__main__':
    print('\nStart to instantiate a new MyClass object')
    launcher = ServiceLauncher()
    launcher.launch_service(hello_world)
    launcher.wait()
