#!/usr/bin/env python3
import groupy
from chat.Chat import *

class GroupMe(Chat):
    def __init__(self):
        super().__init__(prompt="GROUPME")
        self.groups = groupy.Group.list()
        assert(len(self.groups) > 0)

        self.get_chat()

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

    def get_chat(self):
        self.group = None
        while self.group is None:
            choice = input(bcolors.OKBLUE + "pick your chat from: \n%s\n" % self.choices)
            if choice.isdigit() and int(choice) < len(self.groups):
                self.group = self.groups[int(choice)]


    def post_message(self, line):
        self.group.post(line)

    def get_messages(self):
        return self.group.messages()

    def handle_command(self, line):
        # it probably shouldn't be a strcontains
        if "change" in line:
            self.get_chat()
