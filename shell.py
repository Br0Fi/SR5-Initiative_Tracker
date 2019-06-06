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
        if len(parse(arg)) != 2:
            print("*** expected two arguments. Got ", len(parse(arg)))
        else:
            try:
                initiative.add(parse(arg)[0], int(parse(arg)[1]))
            except ValueError:
                print("***The second argument must be an Integer.")

    def do_cycle(self, arg):
        'Move the turn order to the next character: CYCLE'
        if len(parse(arg)) != 0:
            print("*** expected zero arguments. Got ", len(parse(arg)))
        else:
            initiative.cycle()

    def do_back(self, arg):
        'To be used to cycle one step backwards: BACK'
        if len(parse(arg)) != 0:
            print("*** expected zero arguments. Got ", len(parse(arg)))
        else:
            initiative.back()

    def do_seize(self, arg):
        'Let a character chose to use his edge to seize the initiative: \
SEIZE Tim'
        if len(parse(arg)) != 1:
            print("*** expected one argument. Got ", len(parse(arg)))
        else:
            initiative.seize_initiative(arg)

    def do_change(self, arg):
        'Change a characters initiative, whenever neccessary.'
        if len(parse(arg)) != 2:
            print("*** expected two arguments. Got ", len(parse(arg)))
        else:
            try:
                initiative.change_initiative(parse(arg)[0], int(parse(arg)[1]))
            except ValueError:
                print("***The second argument must be an Integer.")

    def do_exit(self, arg):
        'close the initiative tracker, losing all previosly input characters: \
EXIT'
        print('Thank you for using the SR5 Initiative Tracker')
        # TODO unfitting, if just the next turn is invoced
        return True

    def do_reset(self, arg):
        'start a new combat turn and reset everything: RESET'
        if len(parse(arg)) != 0:
            print("*** expected zero arguments. Got ", len(parse(arg)))
        else:
            for i in range(0, 10):
                print('\n')
            initiative.reset()

    initiative.initialize()


def parse(arg):
    ''''Convert a series of zero or more objects (usually int or string)
        to an argument tuple'''
    return tuple(arg.split())


if __name__ == '__main__':
    InitiativeShell().cmdloop()
