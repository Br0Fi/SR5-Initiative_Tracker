import cmd
import initiative


class InitiativeShell(cmd.Cmd):
    '''The class allowing the tracker to be used as a shell'''
    intro = 'Welcome to the Shadowrun, Fifth Editition, Initiaitve Tracker.\
            Type help or ? to list commands.\n'
    prompt = '(tracker) '

    # ----- basic initiative commands -----
    def do_add(self, arg):
        'Add a Character to the initiative order: ADD Tim 10'
        initiative.add(parse(arg)[0], int(parse(arg)[1]))

    def do_cycle(self, arg):
        'Move the turn order to the next character: CYCLE'
        initiative.cycle(*parse(arg))

    def do_seize(self, arg):
        'Let a character chose to use his edge to seize the initiative: \
SEIZE Tim'
        initiative.seize_initiative(*parse(arg))

    def do_exit(self, arg):
        'close the initiative tracker, losing all previosly input characters'
        print('Thank you for using the SR5 Initiative Tracker')
        # TODO unfitting, if just the next turn is invoced
        return True

    initiative.initialize()


def parse(arg):
    ''''Convert a series of zero or more objects (usually int or string)
        to an argument tuple'''
    return tuple(arg.split())


if __name__ == '__main__':
    InitiativeShell().cmdloop()
