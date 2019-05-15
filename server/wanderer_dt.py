from __future__ import with_statement, print_function, unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import input
from builtins import str
from builtins import range
from builtins import object
import sys
import collections
import os.path
import logging
import re
import imp
import argparse
try:
    imp.find_module('simplejson')
    import simplejson as json
except ImportError:
    import json as json
from location import Location
from wand_gamelogic import GameDirector
import pygame_frontend as frontend

sys.py3kwarning = True  #Turn on Python 3 warnings

from wand_gamelogic import LevelExitException
from wand_gamelogic import HeroDiedException
from wand_gamelogic import ExitGame

class WandererGame(object):
    def __init__(self,
                 startlevel=1,
                 startscreen=None,
                 solution_file=None,
                 size='m'):
        self.gameLogic = GameDirector()
        if not startscreen:
            self.gameLogic.read_new_level_num(
                startlevel)
        else:
            self.gameLogic.read_new_level(
                filename=startscreen,
                solution_file=solution_file)
        self.frontEnd = frontend.getFrontEnd(\
            self.gameLogic.grid.num_rows,
            self.gameLogic.grid.num_cols,
            size=size)

        self.frontEnd.register_event('ANY', self.event_handler)

    def start_game(self):
        while True:
            try:
                updates = self.gameLogic.update_all()
                self.frontEnd.display_updates(updates)
                self.frontEnd.start_event_loop()
            except LevelExitException:
                logging.info("Level {0} successfully exited! "\
                    "Score is {1}".format(self.gameLogic.grid.current_level,
                    self.gameLogic.grid.score))
                if self.gameLogic.grid.recorded_moves:
                    logging.info("Moves recorded on level {1}: "\
                        "\n {0}".format(
                        ''.join(self.gameLogic.grid.recorded_moves),
                        self.gameLogic.grid.current_level))
                self.gameLogic.next_level()
            except HeroDiedException:
                self.gameLogic.hero.alive = False
                self.gameLogic.grid.update_status() #DAY Add player death reason
                return
            except ExitGame:
                if self.gameLogic.grid.recorded_moves:
                    logging.info("Moves recorded in level{1}: "\
                        "\n {0}".format(
                        ''.join(self.gameLogic.grid.recorded_moves),
                        self.gameLogic.grid.current_level))
                self.frontEnd.quit()
                return

    def event_handler(self, event):
        '''Is registered as an event handler with the front
        end.  This handles only "s" and "p" events (to play
        the solution) and calls the game_logic event_handler
        for all other events'''
        grid = self.gameLogic.grid
        if event in ['S', 's', b'S', b's']: # Play full solution
            if grid.solution:
                if grid.playing_solution:
                    grid.playing_solution = False
                else:
                    grid.playing_solution = True
                    self.play_next_solution()
            else:
                logging.debug("There is no solution to play")
        elif event in ['P', 'p', b'P', b'p']: # Play one step of solution
            if grid.solution:
                self.play_next_solution()
            else:
                logging.debug("There is no solution step to play")
        else:
            # send all other events to game logic.  For pygame, we don't 
            # need to send the state with each event, but for the
            # server of the web version, we will.
            state, updates = self.gameLogic.event_handler(event)
            self.frontEnd.display_updates(updates)
            if grid.playing_solution:
                self.play_next_solution()

    def play_next_solution(self):
        grid = self.gameLogic.grid
        num_moves = grid.solution_count
        if grid.solution_index >= num_moves:
            grid.playing_solution = False
        else:
            self.frontEnd.generate_event(grid.solution[grid.solution_index])
            grid.solution_index += 1

    def start_event_loop(self):
        '''Start the event loop.  In the case of pygame, this will just call
        the pygame front-end event loop.'''
        self.frontEnd.start_event_loop()



def main(startlevel=1, startscreen=None, debugflag=False):
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--filename", action='store',
                       help="starting screen filename")
    group.add_argument("-l", "--level", type=int, action='store',
                       help="starting screen number", default=1)
    parser.add_argument("-s", "--solution_file", action='store',
                        help="filename for optional external solution entry",
                        default=None)
    parser.add_argument("-d", "--debug", action='store_true',
                        help="Start in debug mode",
                        default=False)
    parser.add_argument("-z", "--size", action='store',
                        choices=['s', 'm', 'l'],
                        help="Specify size of window",
                        default='m')
    args = parser.parse_args()
    solution_filename = None
    size = 'm'
    if args.filename:
        startscreen = args.filename
    if args.level:
        startlevel = args.level
    if args.solution_file:
        solution_filename = args.solution_file
    if args.size:
        size = args.size
    debugflag = args.debug

    # Set up logging
    # define Handler to write INFO messages or higher to
    # the sys.stderr
    logging.basicConfig(
        level=logging.DEBUG,
        format = '%(module)-7s l:%(lineno)4s %(message)s',
        filename='logfile.txt',
        filemode='w') #'w' mode will overwrite
    logging.basicConfig(level=logging.INFO)
    console = logging.StreamHandler()
    #console.setLevel(logging.INFO)
    console.setLevel(logging.INFO) #Set this back to INFO after done debugging
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger(None).addHandler(console)
    logging.info('Logging turned on')

    if debugflag:
        import doctest
        doctest.testmod()
    else:
        logging.disable(logging.DEBUG)


    wGame = WandererGame(startlevel=startlevel,
        startscreen=startscreen,
        solution_file=solution_filename,
        size=size)
    wGame.start_game()
    err_info = None  #allow garbage collection on the traceback info
    answer = input("\n\nPress return to exit")

    # try:
    #     wGame = WandererGame(startlevel=startlevel,
    #                  startscreen=startscreen,
    #                  solution_file=solution_filename,
    #                  size=size)
    # except:
    #     logging.error("Error caught at top level", exc_info=sys.exc_info())
    # finally:
    #     err_info = None  #allow garbage collection on the traceback info
    #     answer = input("\n\nPress return to exit")




if __name__ == "__main__":
    main()


