#!/usr/bin/python3

# -*- coding: utf-8 -*-
"""
@author: BroFi
"""
from collections import deque


class Character:
    '''For this purpose a character only has a name and an initiative value.
    Any time bound objects like exploding granades are also considered
    a character and added in the same way.'''

    def __init__(self, name, initiative):
        self.name = name
        self.initiative = initiative
        self.seized = False
        # only true if "Seize the Initiative" has been used
        self.has_went = 0
        # The number of action phases this character has taken this turn

    def __repr__(self):
        return repr((self.name, self.initiative))

    def change_initiative(self, added_value):
        '''changes the characters initiative.
        Adds positive numbers and substracts negative ones.'''
        self.initiative += added_value


class PassTimer:
    '''Marks the start of a new initiative pass.
    Should always just exist once which might mean that it shouldn't be
    a class but the way it is used i think it's fine.'''

    def __init__(self):
        self.initiative_pass = 1
        self.name = "Pass Timer"

    def __repr__(self):
        '''Displays the current turn number. Should possibly be changed to
        display the next turns number because of the way it's displayed in the
        list.'''
        return repr(("Turn No. ", self.initiative_pass))

    def pass_start(self):
        self.initiative_pass += 1

    def new_turn(self):
        self.initiative_pass = 1


def add(character_name, character_initiative):
    '''Adds a character to the initiative order
    with the specified initiative value.
    ERIC is not included in this so that you do not have to look up these
    stats in advance. You'll just have to look them up, when two characters
    have equal initiative. I recomend to not cycle before all characters with
    the same initiative have made their action phase and then cycling that
    amount of times, so you don't forget anyone.'''
    char = Character(character_name, character_initiative)
    character_list.append(char)
    update()
    '''this can be removed if update() is invocted after
    all characters have been added'''


def cycle():
    '''To be used when a character finshes their action phase to let the turn
    order rotate to the next character. If every character has made their turn,
    it will start the next initiative pass.'''
    if hasattr(initiative_pass[len(initiative_pass)-1], 'initiative_pass'):
        PassTimer.pass_start(pass_timer)
#    elif hasattr(initiative_pass[len(initiative_pass)-2], 'initiative_pass'):
#        for i in [x for x in range(0, len(initiative_pass))
#                  if x != len(initiative_pass)-2]:
#            Character.change_initiative(initiative_pass[i], -10)
#        print("debug:")
#        print(initiative_pass[len(character_list)-1])
#        initiative_pass[len(character_list)-1].has_went += 1
    else:
        Character.change_initiative(initiative_pass[len(character_list)], -10)
        initiative_pass[len(character_list)].has_went += 1
    initiative_pass.rotate()
    print_order()


def update():
    '''Sorts character_list to a deque which represents the turn order.'''
    global initiative_pass
    # global turn_timer

    # Characters who already went this initiative pass:
    went_not_seized = []  # who also have not seized the initiative
    went_seized = []  # who also have seized the initiative

    # Characters who have not went yet this initiative pass:
    not_went_not_seized = []  # who also have not seized the initiative
    not_went_seized = []  # who also have seized the initiative

    for char in character_list:
        if char.has_went == pass_timer.initiative_pass - 1:
            if char.seized:
                went_seized.append(char)
            else:
                went_not_seized.append(char)
        else:
            if char.has_went != pass_timer.initiative_pass - 2:
                print(char.name, " was added in this \
initiative pass and treated accordingly.")
                char.has_went = pass_timer.initiative_pass - 2

            if char.seized:
                not_went_seized.append(char)
            else:
                not_went_not_seized.append(char)

    went_not_seized = sorted(went_not_seized, key=lambda char: char.initiative)
    went_seized = sorted(went_seized, key=lambda char: char.initiative)
    not_went_not_seized = sorted(not_went_not_seized,
                                 key=lambda char: char.initiative)
    not_went_seized = sorted(not_went_seized, key=lambda char: char.initiative)

    initiative_pass = deque(
            went_not_seized
            + went_seized
            + [pass_timer]
            + not_went_not_seized
            + not_went_seized
            )
    print_order()


def print_order():
    '''Prints out the current order players should take their turns in in the
    form of one tupel per line.'''
    for i in initiative_pass:
        print(i)
    print()


def seize_initiative(character_name):
    '''To be used if a character chooses to use their edge
    on seizing the initiative'''
    try:
        """not sure if this makes the most sense
        and it's definitely not necessary.
        TODO remove the manual raise cause the error is thrown anyways."""
        if character_name not in [x.name for x in character_list]:
            raise ValueError('Name not found')
        character_list[[x.name for x in character_list]
                       .index(character_name)].seized = True
        update()
    except ValueError:
        print('There was no character of that name found.')


def initialize():
    '''Meant to be executed at the start of combat
    before any characters are added.'''
    global character_list
    character_list = []
    global pass_timer
    pass_timer = PassTimer()
    update()


def change_initiative(character_name, added_value):
    '''Changes a characters initiative by the name of the character.
    To reduce the initiative value use a negative value.'''
    try:
        Character.change_initiative(character_list[
                [x.name for x in character_list].index(character_name)],
                                    added_value)
        update()
    except ValueError:
        print('There was no character of that name found.')


# TODO Should the seized value only be true for one initiative pass and not the whole turn? -> look that up
# TODO Characters entering combat during the turn -> implement Surprise?
# TODO reomove Characters (dead, unconscious, leaving, misspelled, etc.)
# TODO unseize + entsprechenden printout zur Bestätigung bei seize

# For testing:
#initialize()
#add("Hans", 5)
#add("Peter", 2)
#add("Chris", 7)
#add("Magnolia", 20)
#add("Sabine", 5)
#
#seize_initiative("Peter")
