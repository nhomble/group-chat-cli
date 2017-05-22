#!/usr/bin/env python3
import groupy
import sys

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

class GroupMe(object):
    def __init__(self):
        self.groups = groupy.Group.list()
        assert(len(self.groups) > 0)

        self.get_chat()
        self._is_done = False

    @property
    def group_names(self):
        ret = [ g.name for g in self.groups ]
        if ret is None:
            return []
        else:
            return ret

    @property
    def choices(self):
        arr = []
        for (index, name) in enumerate(self.group_names):
            arr.append("%d  ::  %s" % (index, name))
        return "\n".join(arr)

    @property
    def is_done(self):
        return self._is_done

    def get_chat(self):
        self.group = None
        while self.group is None:
            choice = input(bcolors.OKBLUE + "pick your chat from: \n%s\n" % self.choices)
            if choice.isdigit() and int(choice) < len(self.groups):
                self.group = self.groups[int(choice)]


    def handle(self, line):
        if not self.has_text(line):
            pass
        elif self.is_cmd(line):
            self.handle_command(line)
        else:
            self.group.post(line)

    def run(self):
        while not self.is_done:
            try:
                self.clear()
                print(str(self.get_messages()))
                line = input(bcolors.OKBLUE + "GROUPME: " + bcolors.OKGREEN)
                self.handle(line)
            except (EOFError, KeyboardInterrupt):
                self._is_done = True
        print()

    def get_messages(self, n=100):
        messages = self.group.messages()
        up = min(len(messages), n)
        ret = []
        for m in messages[0:up]:
            ret.append("%s(%s) %s%s... %s%s" % (bcolors.HEADER, str(m.created_at), bcolors.WARNING, m.name, bcolors.OKGREEN,  m.text))
        ret = list(reversed(ret))
        return "\n".join(ret)

    def handle_command(self, line):
        # it probably shouldn't be a strcontains
        if "change" in line:
            self.get_chat()

    def clear(self):
        print("\033[2J")

    def has_text(self, line):
        return len(line) > 0

    def is_cmd(self, line):
        return line.startswith(">")
