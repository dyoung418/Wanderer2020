#!/usr/bin/env python
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

from past.utils import old_div

from location import Location
import window

sys.py3kwarning = True  #Turn on Python 3 warnings

#import future_builtins

#import multiprocessing, Decimal, collections, numbers, fractions
#from abc import ABCMeta, abstractmethod, abstractproperty

sys.setrecursionlimit(2000)

# Globals
#DEBUGFLAG = True
LOG_INDENT = 1

# Constants
SOLUTION_PLAYBACK_DELAY = 25
PUSHED, FALL, MOVE = list(range(3))
(NO, YES, PUSH, SLIDE_ROCK, DIE, WRAP, EXIT, TELEPORT,
 CAPTURE, BOMB, CHECK_STANDSTILL, COEXIST, SPOOK) = list(range(13))
IMAGEDIR = 'images'
SOUNDDIR = 'sounds'
LEVELDIR = 'screens'
TESTDIR = 'tests'
KEYBOARD_EVENT, MOUSE_EVENT = list(range(2))
DIR_NORTH = SLIDE_NORTH = Location((0, -1))
DIR_SOUTH = SLIDE_SOUTH = Location((0, 1))
DIR_EAST = SLIDE_EAST = Location((1, 0))
DIR_WEST = SLIDE_WEST = Location((-1, 0))
INVERSE_DIR = Location((-1, -1))
EMPTY = frozenset([' ', '-', 'A'])
DIRT_SCORE = 1
MONEY_SCORE = 10
TIME_SCORE = 5 # Time capsules increase score by 5 points
TIME_CAPSULE_AMOUNT = 250 # Time capsules give 250 more time
TELEPORT_SCORE = 20
MONSTER_SCORE = 100
BABY_MONSTER_CAPTURE_SCORE = 20
PLAYER_MOVES = frozenset(['LEFT', 'H', 'h', 'RIGHT', 'L', 'l',
                          'UP', 'K', 'k', 'DOWN', 'J', 'j',
                          'SPACE', ' ', '-'])

class GameObj(object):
    def __init__(self, window, gameobj_type, mediator, grid, location):
        self._window = window # Windowing system object
        self._type = gameobj_type   # a single-character string denoting type
        self._mediator = mediator # Handles all obj-to-obj interactions
        self._grid = grid # aggregation of grid objects which store list of
                          # GameObj's at that location
        self._location = location
        self._fallvector = None # must be initialized by subclasses
        self._pushvectors = None # must be initialized by subclasses
        # Call the Window object to initialize a data structure which will hold
        # info needed to draw me.  I (GameObj) don't know the format of this
        # data, but I'll hold it in self._drawdata and pass it to my Window
        # object which will know how to use it to draw me on whatever specific
        # window system is being used.
        self.standstill = True  #e.g. A rock starting at standstill doesn't fall into hero

        # being_pushed: a flag to not falsely trigger falls from origin place when
        #   being pushed. This is needed because when hero pushes, say, a hanging
        #   rock to the right, 
        #                            @O     (hero pushed rock right)
        #                           >  ##
        #                                   
        #   hero.execute_move is called before the pushed rock.
        #   However, the hero.execute_move will cause triggering of the spot under
        #   the hero, which will trigger the arrow
        #   The arrow's movement will inturn trigger the rock (which hasn't had
        #   (execute_move() called on it yet, so it is still in pre-pushed position
        #   This will in turn cause the rock to call _continue_fall() and go all the
        #   way down triggering other things below even though it shouldn't have
        #   done that at all because it is pushed to the right.
        self.being_pushed = False
        self.alive = True
        self.causewake = True   #i.e. do I cause a wake, as in the wake of a boat
        self._cell = self._grid.get_cell(self._location)
        self._drawdata = self._window.initialize_gameobj_data(self)
        self.draw() # now draw myself

    def __repr__(self):
        return "GameObj('{0}', {1!s} )".format(self._type, self._location)

    @property
    def location(self):
        '''Return location'''
        return self._location

    @property
    def obj_type(self):
        '''Return object type'''
        return self._type

    @property
    def draw_data(self):
        '''Return draw_data'''
        return self._drawdata

    @property
    def fallvector(self):
        '''Return fallvector'''
        return self._fallvector

    @property
    def pushvectors(self):
        '''Return pushvectors'''
        return self._pushvectors

    def delete(self):
        '''Do any cleanup before I get deleted'''
        self._window.remove_gameobj(self)
        self._drawdata = None

    def draw(self, redraw_screen=False):
        '''Draw self at current location using my reference to Window obj'''
        self._window.draw_obj(self, redraw=redraw_screen)

    def react_to_visitor(self, movetype, special_instructions=None):
        '''Another object just moved into my space -- React to it (usually by dying)'''
        if special_instructions == 'coexist':
            return
        self.die()

    def fall(self, location):
        return False

    def allow_slider(self, slide_dir, fall_vector):
        return None

    def spooked(self, from_location):
        pass  # relevant only for baby monsters

    def die(self):
        '''I die -- execute anything that happens at my death'''
        logging.debug("        DIE - {0}".format(self))
        self.alive = False
        self._cell.remove_gameobj(self)
        self._window.remove_gameobj(self)
        self._drawdata = None #remove last reference to this var


class Static_GameObj(GameObj):
    '''Game objects that don't move or change (other than dying).
    In the future, I may implement FLYWEIGHT pattern on these, but for now
    it is not worth the effort.'''
    def __init__(self, window, gameobj_type, mediator, grid, location):
        super(Static_GameObj, self).__init__(window, gameobj_type, mediator,
                                             grid, location)
class Space(Static_GameObj):
    '''Blank space'''
    def react_to_visitor(self, movetype, special_instructions=None):
        pass #do nothing (in particular, don't die like the superclass)

class Dirt(Static_GameObj):
    '''Used for both sand and funky sand.  Just need to increment score when I die'''
    def react_to_visitor(self, movetype, special_instructions=None):
        self._grid.score += DIRT_SCORE
        super(Dirt, self).react_to_visitor(movetype, special_instructions)

class Money(Static_GameObj):
    '''Used for Money.  Just need to increment score and decrement money remaining when I die'''
    def react_to_visitor(self, movetype, special_instructions=None):
        self._grid.score += MONEY_SCORE
        self._grid.remaining_money_and_cages -= 1
        super(Money, self).react_to_visitor(movetype, special_instructions)

class TimeCapsule(Static_GameObj):
    def react_to_visitor(self, movetype, special_instructions=None):
        self._grid.score += TIME_SCORE
        self._grid.change_time(delta=TIME_CAPSULE_AMOUNT)
        super(TimeCapsule, self).react_to_visitor(movetype, special_instructions)

class Teleporter(Static_GameObj):
    def react_to_visitor(self, movetype, special_instructions=None):
        self._grid.score += TELEPORT_SCORE
        super(Teleporter, self).react_to_visitor(movetype, special_instructions)

class Cage(Static_GameObj):
    def react_to_visitor(self, movetype, special_instructions=None):
        #The only visitor will be a baby monster
        self._grid.score += BABY_MONSTER_CAPTURE_SCORE
        super(Cage, self).react_to_visitor(movetype, special_instructions)

class Ramp(Static_GameObj):
    def allow_slider(self, slide_dir, fall_vector):
        '''I am an object that causes something else to slide
        The moving object falls in "fall_vector" and has been pushed by me
        according to "slide_dir" (i.e. SLIDE_NORTH or SLIDE_WEST, etc.)
        Determine if the slide succeeds by checking neighbor locations.  Return
        the location that the object ends up in.'''
        try:
            cell_list = self._cell.slide_locations[(slide_dir, fall_vector)]
            result = True
            # Unlike Rocks, Ramps only require the *first* location
            # in slide_locations be *empty* (' ' or 'A') in order to
            # allow slides.
            # for example, a '>' sliding north on a ramp '/' requires that the
            # spot north of the arrow be blank, but doesn't necessarily require
            # the spot northeast of the arrow is blank (that spot will still
            # need to allow the mover to move into it, but not necessarily be
            # blank)
            for obj in cell_list[0].get_gameobjs():
                if obj.obj_type not in EMPTY:
                    result = False
            if result:
                # DAY note this return val is different than for ROCK.
                return (self._location + slide_dir +
                        (fall_vector * INVERSE_DIR))#location mover should end up
            else:
                return False
        except KeyError:
            # if the entry doesn't exist, then we are near an edge so don't allow slide
            return False

class Bomb(Static_GameObj):
    def __init__(self, window, gameobj_type, mediator, grid, location):
        super(Bomb, self).__init__(window, gameobj_type, mediator,
                                   grid, location)
    def react_to_visitor(self, movetype, special_instructions=None):
        c = self._cell
        for cell in [c.northwest, c.north, c.northeast, c.west, c.east,
                     c.southwest, c.south, c.southeast]:
            if cell:
                for obj in cell.get_gameobjs():
                    if obj.obj_type not in self._mediator.unbombables:
                        obj.die()
        self._window.turn_boom_on(self._location)
        self.die()
    def fall(self, location):
        return False

class Dynamic_GameObj(GameObj):
    def __init__(self, window, gameobj_type, mediator, grid, location):
        super(Dynamic_GameObj, self).__init__(window, gameobj_type, mediator,
                                              grid, location)
    def fall(self, location):       # Dynamic_GameObj
        '''Fall into location if possible'''
        if not self._fallvector:
            return False
        if self.being_pushed:
            return False # see explanation in GameObj.__init__()
        fall_succeeded = False
        if self._location + self._fallvector == location:
            fall_succeeded = self._mediator.trymove(self, self._fallvector, FALL)
        return fall_succeeded

    def _continue_fall(self, location):       # Dynamic_GameObj
        '''Called for continuing falls so I can change .standstill state'''
        # Standing rocks and arrows that would start their fall on the Hero
        # don't kill the Hero, but rocks and arrows that are already in motion
        # when they hit the Hero do.  The self.standstill state captures this.
        self.standstill = False
        # When we continue the fall, we don't necessarily cause ourself to move,
        #   instead, we call trigger_falls on the spot in front of us.  If we are
        #   the first to fall into that spot, great; but we aren't always the first.
        #   As an example, when a right arrow (>) moves towards a left arrow (<), the
        #   left arrow closes the last gap because EAST triggers into the spot between
        #   them before WEST.
        self._grid.get_cell(location).check_triggers()
        self.standstill = True

    def execute_move(self, new_location, wake_location=None,
                     wake_old_location=None): # Dynamic_GameObj
        '''Move myself to new_location with no checking if move is possible'''
        logging.debug("  Execute_move: moving {0} to {1}".format(self, new_location))
        logging.debug(self._grid.string_view(highlight=new_location)) # DAY delete this later?
        old_location = self._location
        old_cell = self._cell
        self._location = new_location
        self._cell = self._grid.get_cell(new_location)
        old_cell.remove_gameobj(self)
        self._cell.insert_gameobj(self)
        self._window.update_obj_location(self)
        # Redraw myself (possibly animate the move). redraw_screen=True means
        #   this spot drawn, then FPS is waited
        self.draw(redraw_screen=True)
        if self.being_pushed:
            self.being_pushed = False
        # Call ._continue_fall() on myself for the spot in front of me (my
        # fallvector) to cause continued falling (normal wakes won't cause this).
        # In original wanderer this is done prior to the wake from my last
        # fall/move.
        if self._fallvector:
            logging.debug("  Execute_move: calling _continue_fall on {1} to {0}"
                          .format(self._location + self._fallvector, self))
            self._continue_fall(self._location + self._fallvector)
        if self.causewake: # some objs like hungry monsters don't cause wake
            if wake_location:
                # Sometimes (like when sliding) we cause a wake into a different location
                # than the one we moved to.  In these circumstances, wake_location will
                # be set
                if wake_old_location:
                    self._grid.get_cell(
                        wake_old_location).cause_wake(wake_location - wake_old_location)
                else:
                    old_cell.cause_wake(wake_location - old_location)
            else:
                old_cell.cause_wake(new_location - old_location)

class Hero(Dynamic_GameObj):
    def __init__(self, window, gameobj_type, mediator, grid, location):
        super(Hero, self).__init__(window, gameobj_type, mediator,
                                   grid, location)
    def move(self, vector):
        logging.debug(str(self._grid))
        logging.debug("-------------------HERO MOVE from {0} on vector {1} -"\
                "------------".format(self._location, vector))
        move_succeeded = self._mediator.trymove(self, vector, movetype=MOVE)
        if not move_succeeded:
            pass #DAY - ring bell here

    def fall(self, location):
        return False

    def die(self):
        self.alive = False
        logging.info("Player died!!") # DAY -- implement here
        raise HeroDiedException

class Rock(Dynamic_GameObj):

    def __init__(self, window, gameobj_type, mediator, grid, location):
        super(Rock, self).__init__(window, gameobj_type, mediator,
                                   grid, location)
        self._fallvector = DIR_SOUTH
        self._pushvectors = [DIR_WEST, DIR_EAST]

    def allow_slider(self, slide_dir, fall_vector):
        '''I am an object that causes something else to slide
        The moving object falls in "fall_vector" and has been pushed by me
        according to "slide_dir" (i.e. SLIDE_NORTH or SLIDE_WEST, etc.)
        Determine if the slide succeeds by checking neighbor locations.  Return
        the location that the object ends up in.'''
        try:
            cell_list = self._cell.slide_locations[(slide_dir, fall_vector)]
            result = True
            # Rocks require that *all* the locations in slide_locations be
            # *empty* (' ' or 'A') in order to allow slides.
            # for example, a '>' sliding north on a rock requires that the
            # spot north of the arrow *and* the spot northeast of the arrow
            # is blank.
            for cell in cell_list:
                for obj in cell.get_gameobjs():
                    if obj.obj_type not in EMPTY:
                        result = False
            if result:
                return self._location + slide_dir #location mover should end up
        except KeyError:
            # if the entry doesn't exist, then we are near an edge so don't allow slide
            return False

class Arrow(Dynamic_GameObj):

    def __init__(self, window, gameobj_type, mediator, grid, location):
        super(Arrow, self).__init__(window, gameobj_type, mediator,
                                    grid, location)
        if gameobj_type == '<':
            self._fallvector = DIR_WEST
        else:
            self._fallvector = DIR_EAST
        self._pushvectors = [DIR_NORTH, DIR_SOUTH]

class Balloon(Dynamic_GameObj):

    def __init__(self, window, gameobj_type, mediator, grid, location):
        super(Balloon, self).__init__(window, gameobj_type, mediator,
                                      grid, location)
        self._fallvector = DIR_NORTH
        self._pushvectors = [DIR_WEST, DIR_EAST]

class Monster(Dynamic_GameObj):

    def __init__(self, window, gameobj_type, mediator, grid, location):
        super(Monster, self).__init__(window, gameobj_type, mediator,
                                      grid, location)
        self.causewake = False

    def react_to_visitor(self, movetype, special_instructions=None):
        self._grid.score += MONSTER_SCORE
        self._grid.alive_monsters -= 1
        super(Monster, self).react_to_visitor(movetype, special_instructions)

    def fall(self, location): # Monster
        return False

    def move(self): # Monster
        if not self.alive: return
        delta = self._grid.hero.location - self.location
        # delta may be (12, -5), convert to vector like (1, -1)
        if delta.x == 0: move_x = 0
        else: move_x = old_div(delta.x, abs(delta.x))
        if delta.y == 0: move_y = 0
        else: move_y = old_div(delta.y, abs(delta.y))
        move_vector = Location((move_x, move_y))
        m = self._mediator
        if delta.y == 0: # on the same row as the hero
            if not m.trymove(self, move_vector, MOVE):
                # on the same row as hero, but can't move horizontally, so try down
                if self.alive:
                    m.trymove(self, DIR_SOUTH, MOVE)
            return
        if delta.x == 0: # on same column as the hero
            if not m.trymove(self, move_vector, MOVE):
                # on the same col as hero, but can't move vertically, so try left
                if self.alive:
                    m.trymove(self, DIR_WEST, MOVE)
            return
        # In rest of cases, test which direction is further away and move there first
        if abs(delta.y) >= abs(delta.x):
            if not m.trymove(self, Location((0, move_vector.y)), MOVE): #move vertical
                # Vertical not successful, so try horizontal
                if self.alive:
                    m.trymove(self, Location((move_vector.x, 0)), MOVE)
            return
        else:
            if not m.trymove(self, Location((move_vector.x, 0)), MOVE): #move horizontal
                # Horizontal not successful, so try vertical
                if self.alive:
                    m.trymove(self, Location((0, move_vector.y)), MOVE)
            return

class BabyMonster(Dynamic_GameObj):

    def __init__(self, window, gameobj_type, mediator, grid, location):
        super(BabyMonster, self).__init__(window, gameobj_type, mediator,
                                          grid, location)
        self.mywall = None
        self.spooked_location = None

    def fall(self, location): # BabyMonster
        return False

    def react_to_visitor(self, movetype, special_instructions=None):
        pass # Nothing kills the baby monster by moving into it's spot

    def set_wallvector(self, vector=None):
        '''Initialize a baby monster's wall vector'''
        if self.mywall:
            return # if this has already been set, don't reset
        if vector:
            self.mywall = vector
            return
        c = self._cell
        passables = self._mediator.babymonster_passables
        if not self.mywall:
            #Check the four corners of the compass in the following order
            #  (N, E, S, W) -- first one with a 'wall' (any obstruction) is the
            #  initial wall.  Another baby monster counts as passable
            logging.debug("BabyMonster set wall vector: "\
                    "North obj is {0}".format(c.north.get_topmost_gameobj))
            if c.north.get_topmost_gameobj().obj_type not in passables:
                self.mywall = DIR_NORTH
            elif c.east.get_topmost_gameobj().obj_type not in passables:
                self.mywall = DIR_EAST
            elif c.south.get_topmost_gameobj().obj_type not in passables:
                self.mywall = DIR_SOUTH
            elif c.west.get_topmost_gameobj().obj_type not in passables:
                self.mywall = DIR_WEST
            else:
                #Default wall if I'm next to nothing is West
                self.mywall = DIR_WEST

    def spooked(self, from_location):
        '''Called when a shooting arrow wizzes past and makes baby monster
        not move in the direction from which the arrow was comming'''
        logging.debug("Spooked: {0} spooked at {1}".format(self, from_location))
        self.spooked_location = from_location

    def move(self): # BabyMonster
        #New logic for baby monsters as of the rewrite:
        #   Imagine that the baby monster literally puts his nose against
        #   his 'wall'.  Then the rule is that on his move he attempts
        #   the following:
        #   1. Try to move forward (toward 'wall').
        #       a) if it is a cage, I'll turn into a moneybag and die.  Done.
        #       b) if the move is otherwise successful (e.g. empty space)
        #          the move holds, but I then rotate counter-clockwise,
        #          (toward my left hand).  Thus if my 'wall' was North
        #           before, it now becomes West).   Done.
        #       c) if the move is unsuccessful, go to 2.
        #   2. Try to move toward my right hand (e.g. if my 'wall' is North,
        #       try to move East)
        #       a) if successful, Done
        #       b) if not successful, go to 3.
        #   3. Try to move opposite my wall
        #       a) if successful, the move holds, but I rotate my 'wall' to
        #           be in the right-hand direction of my original 'wall'
        #           (e.g. if I started this routine with NORTH as my 'wall'
        #           then this spot would change 'wall' to EAST.)
        #       b) if not successful, go to 4.
        #   4. Try to move toward my left hand (e.g. if 'wall' is North, try to
        #       move West)
        #       a) if successful, the move holds, but I rotate my 'wall' to
        #           be in the opposite direction of my original 'wall'
        #           (e.g. if I started this routine with NORTH as my 'wall'
        #           then this spot would change 'wall' to SOUTH.)
        #       b) if not successful, end.  No movement this turn
        if not self.alive:
            return
        logging.debug("Baby move: {0} spooked={1}".format(self, self.spooked_location))
        m = self._mediator
        if self.spooked_location:
            dir_spooked = self.spooked_location - self._location
        else:
            dir_spooked = Location((0, 0)) # won't match below
        self.spooked_location = None
        wx = self.mywall[0]
        wy = self.mywall[1]
        dir_toward_my_wall = self.mywall
        dir_my_right = Location((-1*wy, wx))
        dir_away_my_wall = Location((-1*wx, -1*wy))
        dir_my_left = Location((wy, -1*wx))
        dir_opposite_my_wall = Location((-1*wx, -1*wy))

        #Compass dir #1: toward my wall
        if dir_toward_my_wall != dir_spooked:
            if m.trymove(self, self.mywall, MOVE):
                # move toward my wall suceeded.  I either died in a cage, or I
                #   saw open space and now need to rotate counter-clockwise
                #   (toward my 'left')
                if self.alive:
                    #set wall dir to left-hand side of old wall direction
                    self.mywall = dir_my_left
                return
        #Compass dir #2: Try toward my right.
        if dir_my_right != dir_spooked:
            if m.trymove(self, dir_my_right, MOVE):
                #no change in wall direction needed
                return
        #Compass dir #3: away from my wall
        if dir_away_my_wall != dir_spooked:
            if m.trymove(self, dir_away_my_wall, MOVE):
                if self.alive:
                    # set wall dir to right-hand side of old wall direction
                    self.mywall = dir_my_right
                return
        #Compass dir #4: Toward my left
        if dir_my_left != dir_spooked:
            if m.trymove(self, dir_my_left, MOVE):
                if self.alive:
                    # set wall dir to opposite side of old wall direction
                    self.mywall = dir_opposite_my_wall
                return
        # when all else fails, set wall dir to opposite side of old wall dir
        self.mywall = dir_opposite_my_wall

class Rug(Dynamic_GameObj):

    def __init__(self, window, gameobj_type, mediator, grid, location):
        super(Rug, self).__init__(window, gameobj_type, mediator,
                                  grid, location)
        self._pushvectors = [DIR_NORTH, DIR_SOUTH, DIR_WEST, DIR_EAST]

    def fall(self, location):
        return False

class Mediator(object):     #DAY - make this a SINGLETON?
    '''This object encapsulates all the interactions between game objects so
    that each game object doesn't have to be programmed to know about all the
    others.  In pattern terms, this Mediator object is a MEDIATOR between the
    game objects.'''

    def __init__(self): #MEDIATOR

        # fall_into_dict:  key = stationary object, value = mover_dict
        #       mover_dict: key = mover object, value = return_val for
        #                   can_fall_into()
        # Note that default is NO.  only other values are in the dicts
        # YES --  move succeeds unconditionally -- go ahead and implement
        # NO  --  move fails
        # PUSH -- must test whether a push of the stationary object succeeds
        #         before you know if the move works
        # SLIDE -- must test whether a slide of the moving object succeeds
        #         before you know if the move works
        # DIE --  The mover dies
        # KILL -- The stationary object is killed by the mover
        # SPECIAL-Special circumstances (e.g. exit, money bag, baby monsters and cages, etc.)
        self.fall_into_dict = {
            ' ': {'O':YES, '>':YES, '<':YES, '^':YES, '~':YES}, #Blank
            '-': {'O':YES, '>':YES, '<':YES, '^':YES, '~':YES}, #Blank
            'A': {'O':YES, '>':YES, '<':YES, '^':YES, '~':YES}, #Teleport Dest
            'B': {'O':BOMB, '>':BOMB, '<':BOMB, '^':NO, '~':BOMB}, #Bomb
            '/': {'O':SLIDE_WEST, '>':SLIDE_NORTH, '<':SLIDE_SOUTH, '^':SLIDE_EAST, '~':NO},
            '\\':{'O':SLIDE_EAST, '>':SLIDE_SOUTH, '<':SLIDE_NORTH, '^':SLIDE_WEST, '~':NO},
            ':': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Dirt
            'F': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Funky Dirt
            '#': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Stone Wall
            '=': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Brick Wall
            'E': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Edge
            'W': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Wrapping Edge
            '!': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Poison
            'X': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Exit
            '*': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Money
            'T': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Teleporter
            'C': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Time Capsule
            '+': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Cage
            'O': {'O':SLIDE_ROCK, '>':SLIDE_ROCK,
                  '<':SLIDE_ROCK, '^':SLIDE_ROCK, '~':NO}, #Rock
            '>': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Arrow, Right
            '<': {'O':NO, '>':NO, '<':NO, '^':NO, '~':NO}, #Arrow, Left
            '^': {'O':NO, '>':YES, '<':YES, '^':NO, '~':NO}, #Balloon
            'M': {'O':YES, '>':YES, '<':YES, '^':YES, '~':YES}, #Hungry Monster
            #'S': {'O':YES, '>':YES, '<':YES, '^':YES, '~':YES}, #Baby Monster
            # In the original baby monsters are complex and a bit inconsistent:
            # 1. *falling* rocks are stopped by baby monsters, but a rock
            #    on top of a baby monster is triggered when that monster
            #    moves and falls thru the monster.
            #    The rock falling on top of a baby monster can alter the
            #    path of that monster (e.g. if it was trying to move up at the
            #    time)
            # 2. *falling* arrows *go thru* baby monsters, HOWEVER, they do
            #    potentially alter the baby monster's path anyway (e.g. if
            #    the monster was trying to go the direction from which the
            #    arrow comes).  Level 29 is an example of a level where this
            #    is important.  I am going to use status SPOOK to capture
            #    this altering of the baby monster's path
            #    A level which starts with an arrow behind a baby monster will
            #    end up with the monster triggering that arrow, which then
            #    shoots thru the baby monster (not killing it).  Level 13
            #    is an example level where this is important.
            'S': {'O':NO, '>':SPOOK, '<':SPOOK, '^':NO, '~':NO}, #Baby Monster
            '~': {'O':PUSH, '>':PUSH, '<':PUSH, '^':PUSH, '~':NO},  #Rug
            '@': {'O':CHECK_STANDSTILL, '>':CHECK_STANDSTILL,
                  '<':CHECK_STANDSTILL, '^':NO, '~':NO}, #Hero
        }

        # push_into_dict:  key = stationary object, value = mover_dict
        #    mover_dict: key = mover object, value = return_val for can_push_into()
        self.push_into_dict = {
            ' ': {'@':YES, 'O':YES, '>':YES, '<':YES, '^':YES, 'M':YES, 'S':YES, '~':YES}, #Blank
            '-': {'@':YES, 'O':YES, '>':YES, '<':YES, '^':YES, 'M':YES, 'S':YES, '~':YES}, #Blank
            'A': {'@':YES, 'O':YES, '>':YES, '<':YES, '^':YES, 'M':YES, 'S':YES,
                  '~':YES}, #Teleport Dest
            'B': {'@':BOMB, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':BOMB}, #Bomb
            '/': {'@':NO, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Ramp
            '\\':{'@':NO, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Ramp
            ':': {'@':YES, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':COEXIST, '~':NO}, #Dirt
            'F': {'@':YES, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Funky Dirt
            '#': {'@':NO, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Stone Wall
            '=': {'@':NO, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Brick Wall
            'E': {'@':NO, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Edge
            'W': {'@':WRAP, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Wrapping Edge
            '!': {'@':DIE, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Poison
            'X': {'@':EXIT, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Exit
            '*': {'@':YES, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Money
            'T': {'@':TELEPORT, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO,
                  '~':NO}, #Teleporter
            'C': {'@':YES, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Time Capsule
            '+': {'@':NO, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':CAPTURE, '~':NO}, #Cage
            'O': {'@':PUSH, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Rock
            '>': {'@':PUSH, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Arrow
            '<': {'@':PUSH, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Arrow
            '^': {'@':PUSH, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Balloon
            'M': {'@':DIE, 'O':YES, '>':YES, '<':YES, '^':YES, 'M':NO, 'S':NO,
                  '~':YES}, #Hungry Monster
            'S': {'@':DIE, 'O':YES, '>':YES, '<':YES, '^':YES, 'M':NO, 'S':COEXIST,
                  '~':YES}, #Baby Monster
            '~': {'@':PUSH, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':NO, 'S':NO, '~':NO}, #Rug
            '@': {'@':NO, 'O':NO, '>':NO, '<':NO, '^':NO, 'M':YES, 'S':YES, '~':NO}, #Hero
        }

        self.slide_into_dict = {
            ' ': {'O':YES, '>':YES, '<':YES, '^':YES}, #Blank
            '-': {'O':YES, '>':YES, '<':YES, '^':YES}, #Blank
            '^': {'O':NO, '>':YES, '<':YES, '^':NO}, #Monster
            'A': {'O':YES, '>':YES, '<':YES, '^':YES}, #Teleport Dest
            'M': {'O':YES, '>':YES, '<':YES, '^':YES}, #Monster
        }

        self.unbombables = [' ', 'A', 'S', '#', '+', 'E', 'W'] #Things bombs can't blow up

        self.babymonster_passables = [' ', '-', 'A', ':', 'S', '+']
        #DAY -- Check balloons.  Can kill a monster by pushing into it,
        #       but what about falling up into a monster?
        #DAY -- Implement rug -- when pushed by player, it doesn't detonate bombs,
        #       but when pushed by falling object (not from standstill), it does
        #       detonate bombs. Rug being pushed by arrow/rock does *not*
        #       kill the hero

    def set_grid(self, grid): # MEDIATOR
        self._grid = grid

    def _can_fall_into(self, moving, stationary_list, vector): # MEDIATOR
        result_list = []
        for stationary in stationary_list:
            fallvector = moving.fallvector
            if fallvector:
                if vector == fallvector:
                    result = self.fall_into_dict[stationary.obj_type]\
                                 .get(moving.obj_type, NO)
                    if result == CHECK_STANDSTILL:
                        if moving.standstill:
                            logging.debug("{0} didn't fall because of standstill".format(self))
                            result_list.append(NO)
                        else:
                            result_list.append(YES)
                    else:
                        result_list.append(result)
            else:
                result_list.append(NO)
        return self._determine_result(result_list)

    def _can_push_into(self, moving, stationary_list, vector): # MEDIATOR
        result_list = []
        for stationary in stationary_list:
            pushvectors = stationary.pushvectors
            if pushvectors:
                # if there is a pushvectors array then vector must be in it.
                if vector in pushvectors:
                    result_list.append(self.push_into_dict[stationary.obj_type]
                                       .get(moving.obj_type, NO))
                else:
                    result_list.append(NO)
            else:
                # if there is *not* a pushvectors array, the answer still might be YES
                result_list.append(self.push_into_dict[stationary.obj_type].
                                   get(moving.obj_type, NO))
        return self._determine_result(result_list)

    def _determine_result(self, result_list):
        '''common logic both _can_fall_into and _can_push_into use to
        return a single result based on several results from multiple objects
        in the way'''
        if len(result_list) == 1:
            return result_list[0]
        else:
            # turn results into a set to eliminate duplicates
            results = set(result_list)
            if len(results) == 1:
                return results.pop()
            # remove YES answers, since YES always yields to
            # whatever else is in the list
            results -= set((YES,))
            if NO in results:
                return NO
            else:
                #if all else fails, return topmost result that isn't YES or NO
                for result in result_list:
                    if result not in [YES, NO]:
                        return result

    def _can_slide_into(self, moving, stationary, vector): # MEDIATOR
        return self.slide_into_dict.get(stationary.obj_type, {}).get(moving.obj_type, NO)

    def trymove(self, mover, vector, movetype): # MEDIATOR
        '''Determine if mover gameobj can move in vector direction, then execute (in execute_move)
        if yes -- return whether successful or not.
        Movetype is int constant PUSHED, FALL, or MOVE'''
        # Algorithm for moves:
        # 1. GameDirector responds to player input by calling Hero's .move()
        # 2. Hero's .move() calls Mediator .trymove() with movetype == MOVE
        # 3. Mediator finds gameobj in path by looking in Grid/Cell and calls
        #    the mediator.can_push_into() method on the two objects (moving
        #    and stationary) to see if the move works.  Return value is
        #    things like YES, NO, PUSH or SLIDE. 
        # 4a. If YES, 
        #       A) mediator calls the stationary gameobj .react_to_visitor()
        #          (potentially with a list of special instructions).  The 
        #          .react method will do whatever is appropriate (for blank 
        #          space it is nothing, for sand it is to (potentially) kill 
        #          self and increase score, etc.)
        #       B) mediator then calls mover's .execute_move()
        # 5        The mover's .execute_move does the following:
        #          i ) make changes to the grid and refresh screen
        #          ii) call its (the mover's) own ._continue_fall() to see
        #             if it should continue falling.  NOTE that this sets
        #             up potential recursion that could end up at the top
        #             here at mediator.try_move().  Here is the recursion
        #             loop:
        #             1. mediator.try_move()
        #             2. mediator.can_push_into() OR can_fall_into()
        #             3. mover.execute_move() 
        #             4. mover._continue_fall()
        #             5. cell.check_triggers() (called on mover's fallvector spot
        #                                    to see if mover or something else
        #                                    falls into that spot)
        #             6. cell.fall_into() (called on 4 compass points of cell
        #                               that is executing check_triggers)
        #             7. object.fall(location) (called on all objects in the
        #                                    of the cells in 4 compass points
        #                                    to see if they fall into the spot)
        #             8. mediator.try_move() called if object fallvector matches
        #                                 the potential location to see if
        #                                 the stationary object there allows
        #                                 a fall.
        #          iii) Once this recursion exits partially back out at 
        #               .execute_move, it starts new potential recursion
        #               by calling 
        #             4b. cell.cause_wake()
        #             5b. cell.check_triggers() (on wake_locations)
        #             6b. cell.fall_into()
        #             7b. object.fall()
        #             8b. mediator.try_move()
        # 4a. If NO, .trymove() returns false and no action is taken
        # 4b. If PUSH, mediator looks to see if the object being pushed has a 
        #     space on the other side of it that it can be pushed into.
        #     Note that this is only good for one level of push -- if we want
        #     to add an object that is light and can push more than one thing,
        #     then this will need to be modified
        # 4c. if SLIDE, mediator calls logic which determines if a slide works
        # 5. The mover (in .execute_move()) is responsible for making the
        #    changes to which Cell it belongs to as well as calling it's old
        #    Cell's .cause_wake()
        if not mover.alive:
            return False
        new_location = mover.location + vector
        destination_cell = self._grid.get_cell(new_location)
        stationary_objs = list(destination_cell.get_gameobjs())
        top_stationary_obj = destination_cell.get_topmost_gameobj()
        if movetype in [PUSHED, MOVE]:
            result = self._can_push_into(mover, stationary_objs, vector,)
            if result == YES:
                logging.debug("trymove PUSH succeeded. "\
                              "Object is {0} dest is {1}".format(mover,
                    top_stationary_obj))
                for stationary_obj in stationary_objs:
                    stationary_obj.react_to_visitor(movetype)
                mover.execute_move(new_location)
                return True
            elif result == PUSH:
                logging.debug("trymove PUSH calling PUSH on stationary. "\
                              "Object is {0}, stationary is {1}".format(mover,
                    stationary_objs))
                # DAY, this approach only works for 2 level pushing.  In future,
                # I may want to split execute_move() into 2 parts where wake trigger
                # is done in the 2nd part, that way I can do this push checking
                # by calling .try_move() recursively for many levels of push
                second_push_mover = top_stationary_obj
                second_push_loc = new_location+vector
                second_push_stationaries = list(
                    self._grid.get_cell(second_push_loc).get_gameobjs())
                second_push = self._can_push_into(second_push_mover,
                    second_push_stationaries, vector)
                if second_push == YES:
                    second_push_mover.being_pushed = True
                    mover.execute_move(new_location)
                    second_push_mover.execute_move(second_push_loc) #will reset being_pushed
                    for second_push_stationary in second_push_stationaries:
                        second_push_stationary.react_to_visitor(PUSH, None)
                    return True
                return False
            elif result == NO:
                return False
            elif result == DIE:
                mover.die() #TODO: add a reason text here (e.g. "Killed by poison")
            elif result == BOMB:
                logging.debug("trymove BOMB. Object is {0}".format(mover))
                for stationary_obj in stationary_objs:
                    stationary_obj.react_to_visitor(movetype)
                return True
            elif result == EXIT:
                if self._grid.try_exit():
                    logging.info("Level complete!")
                else:
                    logging.debug("Cannot exit: {0.remaining_money_and_cages} gold to "\
                            "collect and {0.alive_monsters} monsters".format(self._grid))
            elif result == TELEPORT: # When hero walks into a teleport booth
                # Everything at TeleportDestination dies except teleport
                # destination ('A'), or empty space (' ') or baby monsters ('S').
                # Note that even hungry monsters die if they are at teleport location.
                # If a baby monster is at teleport location, the hero dies.
                #Original wanderer does the following wrt triggering
                #  after a teleport:
                #  1. Call Fall() on the teleport destination (this
                #     checks to see if anything falls/shoots *into* the
                #     teleport destination.
                #  2. Calls Check() on old teleport booth location as if the
                #     player moved from that booth location and out of it
                #     along his last movement vector. (Check() is the
                #     func that calls Fall() on the 6 'wakepoints' of mover
                teleport_dest = self._grid.teleport_destination
                teleport_dest_cell = self._grid.get_cell(teleport_dest)
                if teleport_dest:
                    for obj in teleport_dest_cell.get_gameobjs():
                        obj_type = obj.obj_type
                        if obj_type not in [' ', 'A']:
                            if obj_type == 'S': #hero dies if teleport on baby mon
                                mover.die() # TODO: Add reason code
                                return False
                            else:
                                # All other objects die when hero teleports on
                                # top of them (including hungry monsters)
                                obj.die()
                    for stationary_obj in stationary_objs:
                        stationary_obj.react_to_visitor(movetype)
                    # wake as if going out of teleporter along last vector
                    mover.execute_move(teleport_dest, wake_location=new_location+vector,
                                       wake_old_location=new_location)
                    # in addition, see if anything can fall into
                    # the teleport destination
                    teleport_dest_cell.check_triggers()
                    return True
                return False
            elif result == COEXIST: # When baby monsters overlap in a single cell
                for stationary_obj in stationary_objs:
                    stationary_obj.react_to_visitor(movetype, special_instructions='coexist')
                mover.execute_move(new_location)
                return True
            elif result == CAPTURE: # baby monsters captured by a cage
                for stationary_obj in stationary_objs:
                    stationary_obj.react_to_visitor(movetype)
                mover.execute_move(new_location) # First move to cause any wake
                mover.die()         # Then the baby moster dies
                # Now put in a money bag (but don't increase money count since
                # the cage was already counted)
                new_money = Money(self._grid.win, '*', self, self._grid, new_location)
                destination_cell.insert_gameobj(new_money)
                new_money.draw()
                return True
            elif result == WRAP: # Wrapping edges
                raise NotImplementedError
            else:
                raise NotImplementedError
        elif movetype == FALL:
            result = self._can_fall_into(mover, stationary_objs, vector)
            if result in [YES, SPOOK]:
                if result == SPOOK:
                    for obj in stationary_objs:
                        obj.spooked(mover.location)
                logging.debug("trymove FALL succeeded. "\
                              "Object is {0} dest is {1}".format(mover, top_stationary_obj))
                for stationary_obj in stationary_objs:
                    stationary_obj.react_to_visitor(movetype)
                mover.execute_move(new_location)
                return True
            elif result == NO:
                return False
            elif result == PUSH:
                # A falling rock or shooting arrow can push a rug -- implement here
                # Call trymove recursively on the stationary object -- if it works, then we succeed
                logging.debug("trymove FALL calling PUSH on stationary. "\
                        "Object is {0}, stationary is {1}".format(mover, stationary_objs))
                if self.trymove(top_stationary_obj, vector, PUSH):
                    #do *not* call stationary_obj.react_to_visitor since it has already been moved
                    mover.execute_move(new_location)
                    return True
                else:
                    return False
            elif result in [SLIDE_EAST, SLIDE_WEST, SLIDE_NORTH, SLIDE_SOUTH, SLIDE_ROCK]:
                if result == SLIDE_ROCK:
                    if vector in [DIR_NORTH, DIR_SOUTH]:
                        slide_dirs = [SLIDE_WEST, SLIDE_EAST]
                    if vector in [DIR_WEST, DIR_EAST]:
                        slide_dirs = [SLIDE_NORTH, SLIDE_SOUTH]
                    #if mover.standstill:
                    #    # don't slide if rock came down in front of me and I'm
                    #    # at a standstill.  This allows rocks to fall on balloons
                    #    # and land/stop in front of hanging arrows without triggering
                    #    # them (which is the original's behavior)
                    #    return False
                else:
                    slide_dirs = [result]
                mover_fall_vector = mover.fallvector
                for slide_dir in slide_dirs:
                    slide_destination = top_stationary_obj.allow_slider(slide_dir,
                                                                        mover_fall_vector)
                    if slide_destination:
                        # Just because the ramp or rock allows sliding doesn't mean mover
                        # can slide.  I must first check mover's slide rules.  For example:
                        #            O
                        #
                        #           :/:
                        #
                        # When the rock falls and hits the ramp, we will call ramp's .allow_slide().
                        # Since ramp only checks it's NW corner for blank, it will return True.
                        # However, we need to check that rock can slide into both ramp's NW and W
                        # neighbors.  It turns out it cannot slide into W (where the sand is) so
                        # the slide should fail.
                        slide_loc = mover.location + slide_dir
                        slide_loc_objs = list(self._grid.get_cell(slide_loc).get_gameobjs())
                        slide_loc_plus_fall_objs = list(self._grid.
                                                        get_cell(slide_loc + mover_fall_vector).
                                                        get_gameobjs())
                        for sl_obj in slide_loc_objs:
                            for slpf_obj in slide_loc_plus_fall_objs:
                                for obj, vector in [(sl_obj, slide_loc),
                                                    (slpf_obj, slide_loc + mover_fall_vector)]:
                                    if not self._can_slide_into(mover, obj, vector):
                                        return False
                        mover.execute_move(slide_destination, wake_location=new_location)
                        break
            elif result == BOMB:
                logging.debug("trymove BOMB. Object is {0}".format(mover))
                for stationary_obj in stationary_objs:
                    stationary_obj.react_to_visitor(movetype)
                return True
            else:
                raise NotImplementedError

class Grid(object):
    '''A collection of Cell objects representing the entire playing grid'''
    #DAY - implement __new__ to force Grid to be a singleton?

    def __init__(self):
        self.num_rows = self.num_cols = None
        self._grid = None
        self.score = 0
        self.time = None
        self.remaining_money_and_cages = None
        self.alive_monsters = None
        self.teleport_destination = None

    def __str__(self):
        return self.string_view()

    def string_view(self, highlight=None):
        '''Return sring of character representation of the grid
        with row and column headers at the left and top.  "highlight" is
        an optional Location argument which will mark the location with
        an "?"'''
        column_nums = ['{0:02}'.format(col) for col in range(self.num_cols)]
        col_header_first_digits = '\n  ' + ''.join([num[0] for num in column_nums])
        col_header_second_digits = '  ' + ''.join([num[1] for num in column_nums]) + '\n'
        outlist = [
            '{0:02}'.format(row) + ''.join([str(self._grid[row][col])
                for col in range(self.num_cols)])
            for row in range(self.num_rows)
            ]
        if highlight:
            rowstring = outlist[highlight.y]
            if rowstring[highlight.x+2] in [' ', ':']: #+2 because of row num added above
                outlist[highlight.y] =\
                    rowstring[:highlight.x+2]\
                    + '?' + rowstring[highlight.x+3:]
        outstr = col_header_first_digits\
            + '\n'\
            + col_header_second_digits\
            + '\n'.join(outlist)
        return outstr

    def set_win(self, win):
        self.win = win

    def set_mediator(self, mediator):
        self.mediator = mediator

    def try_exit(self):
        if self.alive_monsters == 0 and self.remaining_money_and_cages == 0:
            raise LevelExitException
            return True #DAY -- I don't think the code ever gets here
        else:
            return False

    def lost_game(self, message):
        logging.debug(message) #DAY -- need to implement here.
        raise HeroDiedException

    def set_hero(self, hero):
        self.hero = hero

    def set_size(self, rows, columns):
        self.num_rows = rows
        self.num_cols = columns
        # Create the grid populated with Cell objects
        self._grid = [[Cell(self, Location((col, row)))
                       for col in range(columns)] for row in range(rows)]
        # Now that Cell objects are all created, call init_refs() on each one
        for row in range(rows):
            for col in range(columns):
                self._grid[row][col].init_refs()

    def get_cell(self, loc):
        if loc.x < 0 or loc.x >= self.num_cols or loc.y < 0 or loc.y >= self.num_rows:
            return None
        else:
            return self._grid[loc.y][loc.x]

    def delete(self):
        ''' Delete all cell objects in me and ready myself for re-init'''
        for row in self._grid:
            for cell in row:
                cell.delete()
        self.__init__()

    def insert_gameobj(self, game_obj, location):
        self._grid[location.row][location.col].insert_gameobj(game_obj)

    def refresh_all(self):
        for row in self._grid:
            for cell in row:
                cell.refresh()
        self.win.redraw()

    def update_status(self, optional_message=None):
        if optional_message:
            self.win.set_status_line(optional_message)
        elif self.hero.alive:
            self.win.set_status_line("Level {0}: {1} , Score: {2}, Gold: {3}, Time: {4}".format(
                self.level_num, self.level_name, self.score,
                self.remaining_money_and_cages, self.time))
        else:
            self.win.set_status_line("YOU DIED!!     Level {0}: {1} , "\
                                     "Score: {2}, Gold: {3}, Time: {4}".format(
                                         self.level_num, self.level_name, self.score,
                                         self.remaining_money_and_cages, self.time))

    def change_time(self, delta=-1):
        if self.time:
            self.time += delta

    #DAY implement magic functions __ref__?? so I can say grid[location] and
    # get a cell reference


class Cell(object):
    '''Cell objects represent one location on the playing grid.  The main
    function of a Cell object is twofold:
    1. To hold a collection of all the GameObj objects that are currently
    occupying that cell (there can be more than one)
    2. To implement trigger logic.  Triggering in Wanderer is when moving
    objects 'triggger' movement/falling in nearby objects.  Since triggering
    is all about cell locations and whether gameobj objects fall into a location,
    it makes sense to have cell objects handle the logic (rather than
    forcing gameobj objects to be aware of the playing grid topology)'''
    def __init__(self, grid, location):    # Cell
        self._grid = grid
        self._location = location
        # ._gamobjs: Ordered list of gameobj objects in this cell, topmost at index -1
        self._gameobjs = []

        # ._triggerneighbors: list of ordered refs to neighboring cell objs
        #       which might hold gameobj which could fall into this cell
        self._triggerneighbors = []

        # ._wakelocations: dict with vectors as keys. the value for each vector
        #       key will be an ordered list of wake locations.  When an object
        #       moves out of this cell, this cell will call trigger() on each of
        #       the wakelocations based on the vector of movement
        self._wakelocations = {}

        # ._slidelocations: dict with a tuple of (slide_dir, fall_vector)
        #       as keys and list of locations as values.  The locations are the
        #       spots to check to make sure they are empty before allowing a
        #       slide around me. For example, an > arrow sliding around a '/'
        #       ramp will come into my .allow_slider() method with a slide_dir
        #       of SLIDE_NORTH and the arrow has a fall_vector of (1,0).
        #       Therefore, .allow_slider will check the locations in the
        #       dictionary entry that looks like this:
        #           { (SLIDE_NORTH, (1,0)):[location1, location2] }
        self._slidelocations = {}

    def __repr__(self):    # Cell
        return "Cell{0!s}".format(self._location)

    def __str__(self): #Cell
        obj_char = self._gameobjs[-1].obj_type
        if obj_char in ['E', 'W']:
            return '.' #show edges as '.' for simpler output
        else:
            return obj_char # char of topmost object

    @property
    def location(self):    # Cell
        return self._location

    @property
    def slide_locations(self):    # Cell
        return self._slidelocations

    def delete(self):    # Cell
        ''' Delete all objects in me (called before my one reference is deleted)'''
        for obj in self.get_gameobjs():
            obj.delete()
        self._gameobjs = None

    def init_refs(self):    # Cell
        '''Initializes lists of references to other Cell objects, particularly

        _triggerneighbors and _wakelocations.  This is not done in __init__()
        because all the other Cell objects aren't necessarily created yet at
        that point.'''
        myloc = self._location
        grid = self._grid
        # triggerneighbors are the compass point cells around me in the order of
        # North, East, West and South
        self.north = grid.get_cell(myloc + (0, -1))
        self.east = grid.get_cell(myloc + (1, 0))
        self.west = grid.get_cell(myloc + (-1, 0))
        self.south = grid.get_cell(myloc + (0, 1))
        if self.north: self._triggerneighbors.append(self.north)
        if self.east: self._triggerneighbors.append(self.east)
        if self.west: self._triggerneighbors.append(self.west)
        if self.south: self._triggerneighbors.append(self.south)
        # North, south, east and west are also used for slide logic.  In addition,
        # we need northeast, southeast, northwest and southwest
        self.northeast = grid.get_cell(myloc + (1, -1))
        self.northwest = grid.get_cell(myloc + (-1, -1))
        self.southeast = grid.get_cell(myloc + (1, 1))
        self.southwest = grid.get_cell(myloc + (-1, 1))
        # Now fill in the self._slidelocations structure
        # The key is a tuple of ( "slide_dir", "fall_vector" )
        # In the following circumstance:
        #    .1O..
        #    .2/..
        # It is slide_dir WEST and fall_vector SOUTH and I would check #1 first and #2 second,
        # which is [self.northwest, self.west]
        if self.north and self.northeast:
            self._slidelocations[(SLIDE_NORTH, DIR_WEST)] = [self.northeast, self.north]
        if self.east and self.northeast:
            self._slidelocations[(SLIDE_EAST, DIR_SOUTH)] = [self.northeast, self.east]
        if self.north and self.northwest:
            self._slidelocations[(SLIDE_NORTH, DIR_EAST)] = [self.northwest, self.north]
        if self.west and self.northwest:
            self._slidelocations[(SLIDE_WEST, DIR_SOUTH)] = [self.northwest, self.west]
        if self.south and self.southeast:
            self._slidelocations[(SLIDE_SOUTH, DIR_WEST)] = [self.southeast, self.south]
        if self.east and self.southeast:
            self._slidelocations[(SLIDE_EAST, DIR_NORTH)] = [self.southeast, self.east]
        if self.south and self.southwest:
            self._slidelocations[(SLIDE_SOUTH, DIR_EAST)] = [self.southwest, self.south]
        if self.west and self.southwest:
            self._slidelocations[(SLIDE_WEST, DIR_NORTH)] = [self.southwest, self.west]
        # When an object moves *out* of my location, I call check_triggers() on cells
        # around me (in .wakelocations) to see if they have objects that can
        # fall into any of those locations
        # Here is the shape of the wake:
        #
        #            . n .      n = new object location (object moving up in this example)
        #          . l m r .    m = "me" - just vacated old object location
        #          . 1 b 2 .    l, r, b, 1, 2 = left, right, behind, behind-left, behind-right
        #            . . .      . = addtnl spots where objects could fall into l, m, r, l, b or 2
        #                     
        for v in [Location((0, -1)), Location((1, 0)),
                  Location((-1, 0)), Location((0, 1))]: #for all vectors...
            me = grid.get_cell(myloc)
            behind_me = grid.get_cell(myloc - v)
            my_left = grid.get_cell(Location((myloc.x - v.y, myloc.y - v.x)))
            my_right = grid.get_cell(Location((myloc.x + v.y, myloc.y + v.x)))
            behind_left = grid.get_cell(Location((myloc.x - v.x - v.y, myloc.y - v.y - v.x)))
            behind_right = grid.get_cell(Location((myloc.x - v.x + v.y, myloc.y - v.y + v.x)))
            wakelist = []
            if me: wakelist.append(me) #i.e this is the just-vacated location
            if behind_me: wakelist.append(behind_me) # behind the just-vacated location
            if my_left: wakelist.append(my_left)
            if my_right: wakelist.append(my_right)
            if behind_left: wakelist.append(behind_left)
            if behind_right: wakelist.append(behind_right)
            self._wakelocations[v] = wakelist

    def cause_wake(self, vector):    # Cell
        ''' An object just moved out of me moving on vector.  Call
        .check_triggers() on all the locations near me as specified in the
        ._wakelocations structure (depending on the vector of movement).
        This will result in a domino as each of those locations looks to
        see if objects fall into them'''
        global LOG_INDENT
        LOG_INDENT += 3
        logging.debug("{1}++ causing wake at {0._location}".format(self, " "*LOG_INDENT))
        for cell in self._wakelocations[vector]:
            cell.check_triggers(wake=True)
        LOG_INDENT -= 3

    def check_triggers(self, wake=False):    # Cell
        ''' Check all the locations around me
        in ._triggerneighbors to see if any of them have objects that fall into
        me.  I do this by calling those neighbor location's .fall_into()
        method
        This is called by an object's ._continue_fall() method to see
        if it (the object) continues to fall into that spot and/or if other objects
        fall into it first.  In this case, standstill objects don't get triggered.
        It is also called by cause_wake().  In this case, standstill objects do
        get triggered.'''

        #Original wanderer behavior here is tricky: if multiple
        #  objects can trigger into the same space, they all do trigger
        #  (it does *not* stop triggering after the first one).  However, for
        #  the subsequent triggers, it applies sliding logic as if the situation
        #  were still as it was before anything triggered.  Thus, in the case
        #  below, the Rock triggers first, but the arrow doesn't slide because
        #  before the rock triggered, the spot was blank and therefore no sliding
        #  logic was employed (instead, it just sees that the spot in front of it
        #  is *not* empty so it does not trigger).  Likewise, if a rock was there
        #  initially, but by the time the next trigger object is processed, the
        #  rock is no longer there, the triggered object will slide as if the rock
        #  is still there.
        #    1 2 3
        #  1 . . .       (Rock triggers into (2,3) first, but arrow doesn't
        #  2 . O .        slide because arrow only 'slides' if there was a sliding
        #  3 . . <        object in (2,3) before anything triggers)
        #  4 . # .
        #One interesting case is balloons and rocks.
        #    1 2 3
        #  1 . . .
        #  2 . O .
        #  3 . . .
        #  4 . ^ .
        #If fall is called on the empty space at (2,3), the rock will
        #  trigger first, then stop (since it does not slide around balloons).
        #  Then the balloon will try to trigger into (2,3).  When it tries, it
        #  is not starting from the beginning where it would apply sliding rules
        #  around the rock, it just checks space (2,3) and if it is empty, it
        #  triggers.  In this case, since it is not empty, it does not trigger.
        #However, if there is another rock at (2,1), then after all of the
        #  above happens, this  other rock will trigger first into (2,2)
        #  (now empty) and then try to trigger into (2,3) (where the first
        #  rock is now). the rock will slide to (1,2), but then the balloon will
        #  take its turn triggering into (2,3).  This time, when the balloon
        #  checks for triggering into (2,3), the rock sliding logic is already
        #  applied (since the first rock was there to begin with) and so the
        #  balloon slides around to (3,3).  (level 29 & 30 test cases for this)
        #
        #First take a snapshot of which compass points can move (need to do
        #  this to 'freeze' the status of sliding because the initial setup
        #  determines whether sliding is allowed, not the setup when we finally
        #  get to each compass point.  This is complex and not entirely consistent.  In the future,
        #  I may break backward compatibility with the old game in this regard
        #  (it will only break about 5 levels).

        #logging.debug("{1}checktrigger at {0._location}".format(self, " "*LOG_INDENT))
        for cell in self._triggerneighbors:
            cell.fall_into(self._location, wake=wake)

    def fall_into(self, location, wake=False):    # Cell
        ''' Query my objects and see if any of them fall into location'''
        for obj in self._gameobjs:
            if (not wake) and  obj.standstill: #see dosstring for check_triggers()
                pass
            else:
                obj.fall(location)

    def insert_gameobj(self, gameobj):    # Cell
        ''' Gameobj came into my cell.  Put it as topmost object'''
        self._gameobjs.append(gameobj)

    def remove_gameobj(self, gameobj):    # Cell
        try:
            self._gameobjs.remove(gameobj)
        except ValueError as err_detail:
            logging.error("Tried to remove a gameobj that did "\
                    "not exist.  Gameobj={0}, Error={1}".format(gameobj, str(err_detail)))
            return
        if not self._gameobjs:
            blank = Static_GameObj(self._grid.win, ' ',
                                   self._grid.mediator, self._grid,
                                   self._location)
            self.insert_gameobj(blank)
            blank.draw()
        else:
            self._gameobjs[-1].draw()
    def get_topmost_gameobj(self):    # Cell
        return self._gameobjs[-1]
    def get_gameobjs(self):    # Cell
        '''iterable which returns all gameobjs starting with topmost'''
        for i in range(len(self._gameobjs)-1, -1, -1):
            # don't include "being_pushed" objects since this is a temp
            #   state that is just a delay of being in a diff cell
            if not self._gameobjs[i].being_pushed: 
                yield self._gameobjs[i]
    def refresh(self):    # Cell
        self._gameobjs[-1].draw()

class GridBuilder(object):
    '''Factory class for reading level file and building Grid object collection'''
    def __init__(self, window, mediator, grid=None):
        if not grid:
            self.grid = Grid()
        else:
            self.grid = grid
        self.win = window
        self.mediator = mediator
        self.types = {
            ' ': Space, # blank
            '-': Space, # blank
            'A': Static_GameObj, # teleport destination
            'B': Bomb, # bomb
            '#': Static_GameObj, # stone wall
            '=': Static_GameObj, # brick wall
            '/': Ramp, # right ramp
            "\\": Ramp,# left ramp
            ':': Dirt, # dirt
            'F': Dirt, # funky dirt
            '!': Static_GameObj, # poison
            'X': Static_GameObj, # exit
            '*': Money, # money
            'T': Teleporter, # teleport booth
            'C': TimeCapsule, # clock
            '+': Cage, # cage
            'O': Rock, # rock
            '>': Arrow, # right arrow
            '<': Arrow, # left arrow
            '^': Balloon, # balloon
            'M': Monster, # hungry monster
            'S': BabyMonster, # baby monster
            '~': Rug, # rug
            '@': Hero, # hero
            'E': Static_GameObj, # edge
            'W': Static_GameObj, # wrapping edge
        }

    def read_level(self, level_file, level_num, solution_file=None):
        '''Return Grid collection object after reading level file.'''
        level_dict = {}     #will be populated by _section_parser
        logging.debug("Reading {0}".format(level_file))
        self._level_parser(level_file, level_dict)
        rows = level_dict['num_rows']
        cols = level_dict['num_cols']
        grid = self.grid
        self.grid.set_size(rows, cols)
        self.win.post_init_setup(self.grid)
        type_count = {}
        money_and_cages = 0
        monster_count = 0
        hungry_monsters = []
        baby_monsters = []
        for irow in range(rows):
            row = level_dict['grid_data'][irow]
            for icol in range(cols):
                obj_type = row[icol]
                type_count[obj_type] = type_count.get(obj_type, 0) + 1
                loc = Location((icol, irow))
                game_obj = self._create_obj(obj_type, loc)
                if obj_type == '@': # the Hero
                    self.grid.set_hero(game_obj)
                elif obj_type in ['*', '+']: # Money and Cages
                    money_and_cages += 1
                elif obj_type == 'M': # Hungry monster
                    monster_count += 1
                    hungry_monsters.append(game_obj)
                elif obj_type == 'S': # Baby monster
                    baby_monsters.append(game_obj)
                elif obj_type == 'A': # Teleport Destination
                    self.grid.teleport_destination = loc
        for under_dict in level_dict['under_objects']:
            t = under_dict['type']
            l = under_dict['location']
            wall_vector = under_dict.get('wall_vector', None)
            game_obj = self._create_obj(t, l)
            if t == 'S':
                baby_monsters.append(game_obj)
                if wall_vector:
                    game_obj.set_wallvector(wall_vector)
            elif t == 'M':
                monster_count += 1
                hungry_monsters.append(game_obj)
            elif t in ['*', '+']: # Money and Cages
                money_and_cages += 1
            elif t == 'A': # Teleport Destination
                self.grid.teleport_destination = loc
        grid.time = int(level_dict['time'])
        if grid.time == -1:
            grid.time = None
        grid.remaining_money_and_cages = money_and_cages
        grid.alive_monsters = monster_count
        grid.hungry_monsters = hungry_monsters
        grid.baby_monsters = baby_monsters
        for bmonster in baby_monsters:
            bmonster.set_wallvector()
        if 'solution' in level_dict:
            grid.solution = level_dict['solution']
            grid.solution_count = level_dict['solution_moves']
            grid.solution_score = level_dict['solution_score']
        else:
            grid.solution = None
        if solution_file: # optional solution_file overwrites level solution
            with open(solution_file, 'r') as sf:
                lines = sf.readlines()
            solution = []
            for line in lines:
                solution.extend(line.strip())
            grid.solution = solution
            grid.solution_count = len(solution)
        grid.level_num = level_num
        grid.level_name = level_dict.get('title', None)
        grid.level_author = level_dict.get('author', None)
        return grid

    def _create_obj(self, obj_type, location):
        if obj_type in self.types:
            game_obj = self.types[obj_type](self.win, obj_type, self.mediator,
                                            self.grid, location)
        else:
            # Funky dirt replaces anything we don't recognize
            game_obj = self.types['F'](self.win, 'F', self.mediator,
                                       self.grid, location)
        self.grid.insert_gameobj(game_obj, location)
        return game_obj

    def _get_screenfile_lines(self, level_file):
        '''Open the file, trying several different directory locations.
        return the lines read'''
        lines = []
        try:
            with open(os.path.join(LEVELDIR, level_file), 'r') as lf:
                lines = lf.readlines()
        except FileNotFoundError:
            # try the tests directory
            try:
                with open(os.path.join(TESTDIR, level_file), 'r') as lf:
                    lines = lf.readlines()
            except FileNotFoundError:
                # try finding the file in the local directory
                with open(level_file, 'r') as lf:
                    lines = lf.readlines()
        return lines

    def _level_parser(self, level_file, level_dict):
        '''read input file and populate level_dict with section info'''
        lines = self._get_screenfile_lines(level_file)
        # match the first line of form "40x17", or "40 x 17"
        match = re.search(r'(\d+)\s*[xX]\s*(\d+)', lines[0])
        if not match:
            if self._level_parser_oldstyle(level_file, level_dict):
                return
            else:
                raise ValueError("First line of file ({0}) not in ddxdd format".format(level_file))
        num_cols, num_rows = int(match.group(1)), int(match.group(2))
        lines = lines[1:] # move past first line now
        # DAY - DEBUG - figure out how to make the below OS neutral
        grid_data = [line.rstrip('\r\n') for line in lines[:num_rows]]
        lines = lines[num_rows:]
        #Some old files assume space padding at end of incomplete lines.
        for i in range(num_rows):
            length_delta = num_cols-len(grid_data[i])
            if length_delta > 0:
                grid_data[i] += ' '*length_delta
        assert num_rows == len(grid_data), "Incorrect number of rows in screen file"
        #I only test the first line here -- could need DEBUG in future
        assert num_cols == len(grid_data[0]), "Incorrect number of columns in screen file"
        #Check if Edge (or Wrapping_Edge) objects already there. If not, insert
        if grid_data[0][0] not in ['E', 'e', 'W', 'w']:
            #Insert Edge objects around the perimeter
            for i in range(len(grid_data)):
                grid_data[i] = 'E' + grid_data[i] + 'E'
            edgerow = 'E' * (num_cols+2)
            grid_data.insert(0, edgerow)
            grid_data.append(edgerow)
            num_rows += 2
            num_cols += 2
        level_dict['num_rows'] = num_rows
        level_dict['num_cols'] = num_cols
        level_dict['grid_data'] = grid_data
        level_dict['under_objects'] = []
        in_solution = False
        for line in lines:
            lowline = line.lower().strip()
            if in_solution:
                if first_solution_line:
                    first_solution_line = False
                    numbers = lowline.split()
                    level_dict['solution_score'] = int(numbers[0])
                    level_dict['solution_moves'] = int(numbers[1])
                    solution = []
                elif lowline.startswith('end solution:'):
                    in_solution = False
                    if len(solution) != level_dict['solution_moves']:
                        logging.debug('Warning: Solution read ({0}) does not'\
                                      'equal solution_moves'.format(len(solution)))
#                    assert len(solution) == level_dict['solution_moves'], \
#                        "Solution captured ({0}) does not equal "\
#                            "solution_moves".format(len(solution))
                    level_dict['solution'] = solution
                else:
                    solution.extend(line.strip())
            elif lowline.startswith('solution:'):
                in_solution = True
                first_solution_line = True
            elif lowline.startswith('time:'):
                level_dict['time'] = int(lowline.split(':')[-1])
            elif lowline.startswith('author:'):
                level_dict['author'] = line.split(':')[-1].strip()
            elif lowline.startswith('title:'):
                level_dict['title'] = line.split(':')[-1].strip()
            elif lowline.startswith('under:'):
                under_dict = {}
                rhs = line.split(':')[-1].strip()
                rhslist = rhs.split(',')
                assert len(rhslist) >= 3
                under_dict['type'] = rhslist[0]
                under_dict['location'] = Location((int(rhslist[1]), int(rhslist[2])))
                if len(rhslist) >= 5:
                    under_dict['wall_vector'] = Location((int(rhslist[3]), int(rhslist[4])))
                level_dict['under_objects'].append(under_dict)
            else:
                pass
        #logging.debug(str(level_dict))

    def _level_parser_oldstyle(self, level_file, level_dict):
        '''Parse an old style wanderer level file.  Return
        true if successful'''
        OLD_ROWS = num_rows = 17
        OLD_COLS = num_cols = 40
        lines = self._get_screenfile_lines(level_file)
        grid_data = [line.rstrip('\r\n') for line in lines[:num_rows]]
        lines = lines[num_rows:]
        #Some old files assume space padding at end of incomplete lines.
        for i in range(num_rows):
            length_delta = num_cols-len(grid_data[i])
            if length_delta > 0:
                grid_data[i] += ' '*length_delta
        if grid_data[0][0] not in ['E', 'e', 'W', 'w']:
            #Insert Edge objects around the perimeter
            for i in range(len(grid_data)):
                grid_data[i] = 'E' + grid_data[i] + 'E'
            edgerow = 'E' * (num_cols+2)
            grid_data.insert(0, edgerow)
            grid_data.append(edgerow)
            num_rows += 2
            num_cols += 2
        if len(lines) > 0:
            level_dict['title'] = lines[0]
        lines = lines[1:]
        if len(lines) > 0:
            level_dict['time'] = int(lines[0])
        else:
            level_dict['time'] = 999
        level_dict['num_rows'] = num_rows
        level_dict['num_cols'] = num_cols
        level_dict['grid_data'] = grid_data
        level_dict['under_objects'] = []
        level_dict['solution_score'] = 0
        level_dict['solution_moves'] = 0
        level_dict['solution'] = ''
        return True

class GameDirector(object):
    def __init__(self,
                 startlevel=1,
                 startscreen=None,
                 solution_file=None,
                 size='m'):
        self.win = window.getWindow(size=size)
        self.mediator = Mediator()
        self.current_level = startlevel
        self.recorded_moves = []
        if startscreen:
            self.read_new_level(startscreen, self.current_level,
                                solution_file=solution_file)
        else:
            self.read_new_level('screen{0}.txt'.format(self.current_level),
                                self.current_level,
                                solution_file=solution_file)
        self.win.register_event('ANY', self.event_handler)
        while True:
            try:
                self.win.start_event_loop()
            except LevelExitException:
                logging.info("Level {0} successfully exited! "\
                             "Score is {1}".format(self.current_level, self.grid.score))
                if self.recorded_moves:
                    logging.info("Moves recorded on level {1}: \n {0}".format(
                        ''.join(self.recorded_moves), self.current_level))
                self.next_level()
            except HeroDiedException:
                self.grid.refresh_all()
                self.hero.alive = False
                self.grid.update_status() #DAY Add player death reason
            except ExitGame:
                if self.recorded_moves:
                    logging.info("Moves recorded in level{1}: \n {0}".format(
                        ''.join(self.recorded_moves), self.current_level))
                self.win.quit()
                return

    def next_level(self):
        self.current_level += 1
        logging.info("Loading level {0}".format(self.current_level))
        self.read_new_level('screen{0}.txt'.format(self.current_level),
                            self.current_level, self.grid)

    def restart(self):
        self.current_level -= 1
        self.next_level()

    def read_new_level(self, filename, level_num, grid=None, solution_file=None):
        if grid:
            grid.delete()
        self.grid = GridBuilder(self.win, self.mediator, grid=grid)\
            .read_level(filename, level_num, solution_file=solution_file)
        self.grid.set_win(self.win)
        self.mediator.set_grid(self.grid)
        self.grid.set_mediator(self.mediator)
        self.hero = self.grid.hero
        self.solution_index = 0
        self.playing_solution = False
        self.input_queue = []
        self.recorded_moves = []
        self.reading_input = False
        self.input_level = False
        self.grid.update_status()

    def event_handler(self, event):
        logging.debug("   GameDirector event_handler received event {0}".format(event))
        if self.grid.time and (self.grid.time == 0):
            self.grid.lost_game("You died by running out of time")
        if self.reading_input and event != 'RETURN':
            self.input_queue.append(event)
            if self.input_level:
                self.grid.update_status("Level: {0}".format(''.join(self.input_queue)))
            return
        if event in PLAYER_MOVES:
            if event in ['LEFT', 'H', 'h', b'H', b'h']:
                self.recorded_moves.append('H')
                self.hero.move(DIR_WEST)
            elif event in ['RIGHT', 'L', 'l', b'L', b'l']:
                self.recorded_moves.append('L')
                self.hero.move(DIR_EAST)
            elif event in ['UP', 'K', 'k', b'K', b'k']:
                self.recorded_moves.append('K')
                self.hero.move(DIR_NORTH)
            elif event in ['DOWN', 'J', 'j', b'J', b'j']:
                self.recorded_moves.append('J')
                self.hero.move(DIR_SOUTH)
            elif event in ['SPACE', ' ', '-', b' ', b'-']:
                #DAY - implement clicking down the clock
                self.recorded_moves.append('-')
                pass
            self.move_monsters()
            self.grid.change_time()

        elif event in ['Q', 'q', b'Q', b'q']:
            raise ExitGame
        elif event in ['N', 'n', b'N', b'n']:
            self.next_level()
        elif event in ['R', 'r', b'R', b'r']:
            self.restart()
        elif event in ['S', 's', b'S', b's']: # Play full solution
            if self.grid.solution:
                if self.playing_solution:
                    self.playing_solution = False
                else:
                    self.playing_solution = True
                    self.play_next_solution()
            else:
                logging.debug("There is no solution to play")
        elif event in ['P', 'p', b'P', b'p']: # Play one step of solution
            if self.grid.solution:
                self.play_next_solution()
            else:
                logging.debug("There is no solution step to play")
        elif event in ['O', 'o', b'O', b'o']: # Skip to level specified
            self.reading_input = True
            self.input_level = True
            self.grid.update_status("Level: ")
            return
        elif event == 'RETURN': # End reading input
            if self.input_level:
                try:
                    self.current_level = int(''.join(self.input_queue))-1
                    self.input_queue = []
                    self.next_level()
                except ValueError:
                    self.grid.update_status("Error, must enter an integer")
                finally:
                    self.input_level = False
            self.reading_input = False

        if self.playing_solution:
            self.play_next_solution()
            self.win.wait(SOLUTION_PLAYBACK_DELAY)
        self.grid.update_status()

    def move_monsters(self):
        for b in self.grid.baby_monsters:
            b.move()
        for m in self.grid.hungry_monsters:
            m.move()

    def play_next_solution(self):
        num_moves = self.grid.solution_count
        if self.solution_index >= num_moves:
            self.playing_solution = False
        else:
            self.win.generate_event(self.grid.solution[self.solution_index])
            self.solution_index += 1

class LevelExitException(Exception):
    pass
class HeroDiedException(Exception):
    pass
class ExitGame(Exception):
    pass

def main(startlevel=1, startscreen=None, debugflag=False):
    import argparse
    import argcomplete
    # Parse command-line arguments
    #fileCompleter = argcomplete.FilesCompleter(allowednames=['save','txt'], directories=False)
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--filename", action='store',
                       help="starting screen filename")#.completer = fileCompleter
    group.add_argument("-l", "--level", type=int, action='store',
                       help="starting screen number", default=1)
    parser.add_argument("-s", "--solution_file", action='store',
                        help="filename for optional external solution entry",
                        default=None)#.completer = fileCompleter
    parser.add_argument("-d", "--debug", action='store_true',
                        help="Start in debug mode",
                        default=False)
    parser.add_argument("-z", "--size", action='store', choices=['s', 'm', 'l'],
                        help="Specify size of window",
                        default='m')
    argcomplete.autocomplete(parser)
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
    logging.basicConfig(level=logging.DEBUG,
        format = '%(module)-7s l:%(lineno)4s %(message)s',\
        filename='logfile.txt', filemode='w') #'w' mode will overwrite
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

    try:
        GameDirector(startlevel=startlevel,
                    startscreen=startscreen,
                    solution_file=solution_filename,
                    size=size)
    except:
        logging.error("Error caught at top level", exc_info=sys.exc_info())
    finally:
        err_info = None  #allow garbage collection on the traceback info
        answer = input("\n\nPress return to exit")


if __name__ == "__main__":
    main()
