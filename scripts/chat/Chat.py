#!/usr/bin/env python3

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
    def __init__(self, prompt="CHAT"):
        self._is_done = False
        self.prompt = prompt

    def run(self):
        while not self.is_done:
            try:
                self.clear()
                print(self.print_messages())
                line = input(bcolors.OKBLUE + " " + self.prompt + ": " + bcolors.OKGREEN)
                self.handle(line)
            except (EOFError, KeyboardInterrupt):
                self._is_done = True
        print()

    def get_messages(self):
        raise NotImplementedError("unimplemented")

    def handle_command(self, line):
        raise NotImplementedError("unimplemented")

    def print_messages(self, n=100):
        messages = self.get_messages()
        up = min(len(messages), n)
        ret = []
        for m in messages[0:up]:
            ret.append("%s(%s) %s %s... %s %s" % (bcolors.HEADER, str(m.created_at), bcolors.WARNING, ascii(m.name), bcolors.OKGREEN,  ascii(m.text)))
        ret = list(reversed(ret))
        return "\n".join(ret)

    def handle(self, line):
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
