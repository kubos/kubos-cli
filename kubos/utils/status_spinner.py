# Kubos SDK
# Copyright (C) 2016 Kubos Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import threading
import time


class StatusSpinner(threading.Thread):

    def __init__(self, interval):
        threading.Thread.__init__(self)
        self.interval = interval
        self.stop_lock = threading.Lock()
        self.stop_signal = False

    def stop(self):
        with self.stop_lock:
            self.stop_signal = True

    def run(self):
        spinner = self.get_spinner()
        while True:
            sys.stdout.write("%s" % spinner.next())
            sys.stdout.flush()
            sys.stdout.write('\b')
            with self.stop_lock:
                if self.stop_signal:
                    return
            time.sleep(self.interval)

    def get_spinner(self):
        while True:
            for symbol in '|/-\\':
                yield symbol


def start_spinner():
    """ Start a status spinner that prints a spinning character to stdout.

    This method starts a thread, and writes to stdout from that thread, so
    using this method introduces concerns of thread safe access to stdout.

    The spinner will lock stdout_lock when writing to stdout, and all
    other writers to stdout should do the same to prevent interleaving
    stdout output.

    Returns the StatusSpinner object, to be later passed to
    stop_spinner(spinner) when the spinner should stop.
    """
    spinner = StatusSpinner(0.1)
    spinner.daemon = True
    spinner.start()
    return spinner


def stop_spinner(spinner):
    """ Stops the provided StatusSpinner.

    This method blocks on the status spinner thread exiting, and the caller
    can be guaranteed that the thread is terminated once this method returns.
    """
    spinner.stop()
    spinner.join()
