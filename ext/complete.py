#!/usr/bin/python

import json
import sys


def main():
    # print >>sys.stderr, '  '
    completer = Completer()
    completions = completer.get_completions()
    if completions is not None:
        for c in completions:
            print str(c) + '  ',
    else:
        print 'No-complettions'


class Completer(object):
    JSON_FILE = '/home/vagrant/.options.json'

    def __init__(self):
        self.arg_data = self.get_kubos_data()
        self.args = sys.argv[2:] #chop off the initial kubos
        self.subcommands = self.get_subcommands()
        self.global_options = self.get_global_options()


    def get_completions(self):
        global_options = self.eval_global_options()
        subcommands = self.eval_subcommands()
        # if global_options is not None:
            # completions = global_options + subcommands
        # else:
        completions = subcommands
        # active_subcommand = get_current_subcommand(subcommands)
        return completions


    def eval_global_options(self):
        num_args = len(self.args)
        if num_args == 0:
            return self.global_options
        if num_args >= 1:
            val = self.args[-1]
            ret_list = []
            for option in self.global_options:
                if option.startswith(val):
                    ret_list.append(val)
            return ret_list
        return None


    def eval_subcommands(self):
        num_args = len(self.args)
        if num_args == 0:
            #nothing has been entered - return every subcommand
            return self.subcommands
        elif num_args == 1:
            return self.get_subcommand_completion()
        elif num_args >= 1:
            subcommand = self.get_subcommand()
            if subcommand == None:
                return None
            else:
                return self.get_cmd_arg_choices(subcommand)


    def get_subcommand_completion(self):
        #something has been entered. Check if it's a subcommand or the start of one
        arg_val = self.args.pop(0) #we should get the subcommand name first
        if arg_val in self.subcommands:
            choices = self.get_cmd_arg_choices(arg_val)
            return choices
        else:
            ret_list = []
            for cmd in self.subcommands:
                if cmd.startswith(arg_val):
                    ret_list.append(cmd)
            return ret_list


    def get_subcommand(self):
        val = self.args.pop(0)
        if val in self.subcommands:
            return val
        else:
            return None


    def get_cmd_arg_choices(self, cmd):
        args = self.arg_data['subcommands'][cmd]
        choices = []
        for arg in args:
            if arg.startswith('--'):
                choices.append(arg)
            else:
                choices = choices + args[arg]['choices']
        return choices


    def get_current_subcommand(subcommands):
        valids = sys.argv[2:]
        for arg in valids:
            if arg in subcommands:
                return arg
        return None


    def get_subcommands(self):
        subcommands = self.arg_data['subcommands']
        return subcommands.keys()


    def get_global_options(self):
        options = self.arg_data['options']
        return options.keys()


    def get_kubos_data(self):
        with open(self.JSON_FILE, 'r') as _file:
            return json.loads(_file.read())


if __name__ == '__main__':
    main()

