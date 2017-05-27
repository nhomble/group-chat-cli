#!/usr/bin/env python3

import signal

class InputTimeoutError(Exception):
    '''
    stupid exception I'll signal with an
    alarm to timeout input()
    '''
    pass

class bcolors:
    '''
    shamelessly copied from stackoverflow
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Chat(object):
    def __init__(self, prompt="CHAT", timeout=5):
        self._is_done = False
        self._prev_out = ""
        self.prompt = prompt
        self.timeout = timeout
        signal.signal(signal.SIGALRM, self._input_timeout)

    @staticmethod
    def _input_timeout(signum, frame):
        '''
        there seems to be no better way to set a timeout on input(), too bad
        this makes me not Windows compatible.. oh well. My netbook runs arch
        '''
        raise InputTimeoutError()

    def run(self):
        '''
        main loop
        '''
        while not self.is_done:
            try:
                signal.alarm(self.timeout)

                out = self._printable_message()
                self._update_screen(out)

                line = input(bcolors.OKBLUE + self.prompt + ": " + bcolors.OKGREEN)
                signal.alarm(0)

                self._handle(line)
            except (EOFError, KeyboardInterrupt):
                self._is_done = True
            except InputTimeoutError:
                continue
        print()

    def get_messages(self):
        raise NotImplementedError("unimplemented")

    def handle_command(self, line):
        raise NotImplementedError("unimplemented")

    def _update_screen(self, update):
        '''
        only clear/update the screen when the new output is different than
        what I had previously
        '''
        if update is not self._prev_out:
            self.clear()
            print(update)
            self._prev_out = update

    def _printable_message(self, n=100):
        '''
        print on the screen
        '''
        messages = self.get_messages()
        up = min(len(messages), n)
        ret = []
        for m in messages[0:up]:
            ret.append("%s(%s) %s %s... %s %s" % (bcolors.HEADER, str(m.created_at), bcolors.WARNING, ascii(m.name), bcolors.OKGREEN,  ascii(m.text)))
        ret = list(reversed(ret))
        return "\n".join(ret)

    def _handle(self, line):
        if not self.has_text(line):
            pass
        elif self.is_cmd(line):
            self.handle_command(line)
        else:
            self.post_message(line)

    @property
    def is_done(self):
        return self._is_done

    @staticmethod
    def clear():
        print("\033[2J")

    @staticmethod
    def has_text(line):
        return len(line) > 0

    @staticmethod
    def is_cmd(line):
        return line.startswith(">")
