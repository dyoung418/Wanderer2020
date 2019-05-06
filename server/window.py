#! /usr/bin/python
from __future__ import with_statement, print_function, unicode_literals
from __future__ import division
from builtins import range
from builtins import object
import collections
import os.path
import logging
import sys
import pygame
import pygame.locals
from location import Location
from past.utils import old_div
sys.py3kwarning = True  #Turn on Python 3 warnings
#import future_builtins
#import multiprocessing, Decimal, collections, numbers, fractions
#from abc import ABCMeta, abstractmethod, abstractproperty

#DEBUGFLAG = True


# Constants
PUSH, FALL, MOVE = list(range(3))
SOUNDDIR = 'sounds'
LEVELDIR = 'screens'
GRIDWIDTH = 40+2 # # cells in logical tile grid, +2 is for edges added by code
GRIDHEIGHT = 17+2
KEYBOARD_EVENT, MOUSE_EVENT = list(range(2))
KEY_LEFT = 276 # Keyboard codes (specific to py-game for now)
KEY_RIGHT = 275
KEY_DOWN = 274
KEY_UP = 273
KEY_ESCAPE = 27
KEYDOWN = pygame.locals.KEYDOWN
KR_DELAY = 250 # controls key repeat behavior (when holding down key)
KR_INTERVAL = 30 # controls key repeat behavior (when holding down key)
##FPS = 90 # Frames per second
FPS = 3000 # Frames per second
BUTTON_OK_CANCEL, BUTTON_YES_NO, BUTTON_OK = list(range(3))

OGTuple = collections.namedtuple('OGTuple', 'name imagefile')
objectGraphics = {' ': OGTuple(name="Empty", imagefile="blank.gif"),
                  '-': OGTuple(name="Empty", imagefile="blank.gif"),
                  'A': OGTuple(name="Teleport destination",
                               imagefile="teleportdestination.gif"),
                  'B': OGTuple(name="Bomb", imagefile="bomb.gif"),
                  '#': OGTuple(name="Stone wall", imagefile="stonewall.gif"),
                  '=': OGTuple(name="Brick wall", imagefile="brickwall.gif"),
                  '/': OGTuple(name="Ramp", imagefile="rightupramp.gif"),
                  "\\": OGTuple(name="Ramp", imagefile="leftupramp.gif"),
                  ':': OGTuple(name="Dirt", imagefile="dirt.gif"),
                  'F': OGTuple(name="Funky Dirt", imagefile="funkydirt.gif"),
                  '!': OGTuple(name="Poison", imagefile="poison.gif"),
                  'X': OGTuple(name="Exit", imagefile="exit.gif"),
                  '*': OGTuple(name="Money bag", imagefile="money.gif"),
                  'T': OGTuple(name="Teleport booth", imagefile="teleporter.gif"),
                  'C': OGTuple(name="Time capsule", imagefile="clock.gif"),
                  '+': OGTuple(name="Cage", imagefile="cage.gif"),
                  'O': OGTuple(name="Rock", imagefile="rock.gif"),
                  '>': OGTuple(name="Arrow", imagefile="rightarrow.gif"),
                  '<': OGTuple(name="Arrow", imagefile="leftarrow.gif"),
                  '^': OGTuple(name="Balloon", imagefile="balloon.gif"),
                  'M': OGTuple(name="Hungry monster", imagefile="monster.gif"),
                  'S': OGTuple(name="Baby monster", imagefile="babymonster.gif"),
                  '~': OGTuple(name="Rug", imagefile="rug.gif"),
                  '@': OGTuple(name="Player", imagefile="player.gif"),
                  'E': OGTuple(name="Edge", imagefile="edge.gif"),
                  'W': OGTuple(name="Wrapping edge", imagefile="wrapping edge.gif"),
                 }
boom_imagefile = 'boom.gif'

def getWindow(size='m'):
    '''Factory function for getting a window.  This function determines which
    window implementation (e.g. pygame, tkinter, curses) to use'''
    #DAY - eventually, read from options which windows system to use
    return Window_Pygame(size=size)

class Window(object):
    '''Window defines a logical interface. Subclasses implement specific system
    Window keeps a dictionary which maps GameObject objects to structures
    (such as sprite objects or image objects) needed to paint that GameObject
    on the screen.
    '''
    def __init__(self):
        raise NotImplementedError
    def post_init_setup(self, grid):
        '''Called after __init__ to finalize graphic setup
        (after level objects are defined, etc.'''
        raise NotImplementedError
    def set_status_line(self, message):
        raise NotImplementedError
    def initialize_gameobj_data(self, gameobj):
        '''Called with each gameobj created.  Return any structures
        (sprites, etc.) needed to draw and move
        The GameObj will store that structure and we can use it later
        to draw objects that request our .draw_obj()'''
        raise NotImplementedError
    def draw_obj(self, gameobj):
        raise NotImplementedError
    def move_obj(self, mover, old_location, new_location, replacement):
        raise NotImplementedError
    def register_event(self, event_type, event_value):
        '''Register a callback function to be invoked when an event happens'''
        raise NotImplementedError
    def _onEvent(self, event):
        '''Called for all events, this method looks up appropriate
        handler as stored by .register_event()'''
        raise NotImplementedError
    def generate_event(self, event_type, event_value, timedelay):
        '''Used to artificially create an event (such as a timer event)'''
        raise NotImplementedError
    def mark_dirty(self, dirty_area):
        '''tag a portion of the screen as 'dirty' (i.e. in need of refresh)'''
        raise NotImplementedError
    def refresh_dirty(self):
        '''Refresh the dirty areas of the screen and mark them as clean'''
        raise NotImplementedError
    def refresh_all(self):
        '''Refresh entire screen and mark all areas as clean'''
        raise NotImplementedError
    def start_event_loop(self):
        '''Begin processing mouse and keyboard and window system events'''
        raise NotImplementedError
    def quit(self):
        '''Do necessary steps to quit game'''
        raise NotImplementedError
    def draw_boom_till_next_turn(self):
        raise NotImplementedError
    def user_prompt(self, message, button_options=BUTTON_OK_CANCEL, input_field=False):
        raise NotImplementedError

class Window_Pygame(Window):
    '''Window defines a logical interface. Subclasses implement specific system
    Window keeps a dictionary which maps GameObject objects to structures
    (such as sprite objects or image objects) needed to paint that GameObject
    on the screen.
    '''
    def __init__(self, size='m'):
        self.handlerdb = {}
        pygame.init()
        if pygame.display.get_init() != 1:
            print("Display was not initialized")
            pygame.quit()
        self.boom_on = False
        if size == 's':
            self.cellSize = '16x20'
            self.imageDir = 'images/16x20'
            self.cellWidth = 16
            self.cellHeight = 20
        else:
            self.cellSize = '64x80'
            self.imageDir = 'images/64x80'
            self.cellWidth = 64
            self.cellHeight = 80

    def post_init_setup(self, grid):
        '''Called after __init__ to finalize graphic setup
        (after level objects are defined, etc.)'''
        self.screen = pygame.display.set_mode((grid.num_cols * self.cellWidth,
                                               grid.num_rows * self.cellHeight))
        self.grid = grid
        pygame.mouse.set_visible(0)
        # Set key repeat parameters -- delay and interval
        pygame.key.set_repeat(KR_DELAY, KR_INTERVAL)
        self.boom = pygame.sprite.Sprite()
        self.boom.image, self.boom.rect = self._load_image(
            os.path.join(self.imageDir, boom_imagefile))
    def set_status_line(self, message):
        pygame.display.set_caption(message) #DAY - do a better job here
##        pygame.display.flip() #DAY is this needed?
    def initialize_gameobj_data(self, gameobj):
        '''Called with each gameobj created.  Return any structures
        (sprites, etc.) needed to draw and move. The GameObj will store
        that structure and we can use it later to draw objects that
        request our .draw_obj()'''
        s = pygame.sprite.Sprite()
        # DAY -- eventually just read all image data into a dict and reuse it for each game type
        s.image, s.rect = self._load_image(
            os.path.join(self.imageDir, objectGraphics[gameobj.obj_type].imagefile))
        loc = gameobj.location
        s.rect.top, s.rect.left = (loc.y * self.cellHeight, loc.x * self.cellWidth)
##        s.rect.move(loc.x * self.cellWidth, loc.y * self.cellHeight)
        return s
    def remove_gameobj(self, gameobj):
        gameobj.draw_data.kill() #DAY not really needed since I'm not using groups yet
    def update_obj_location(self, gameobj):
        s = gameobj.draw_data
        loc = gameobj.location
        s.rect.top, s.rect.left = (loc.y * self.cellHeight, loc.x * self.cellWidth)
    def draw_obj(self, gameobj, redraw=True, from_loc=None):
        #DAY - eventually add animation when passed a from_loc
        sprite = gameobj.draw_data
        self.screen.blit(sprite.image, sprite.rect)
        if redraw:
            self.redraw()
    def move_obj(self, mover, old_location, new_location, replacement):
        raise NotImplementedError
    def register_event(self, event_value, handler, event_type=KEYBOARD_EVENT):
        '''Register a callback function to be invoked when an event happens'''
        self.handlerdb[event_value] = handler
    def _onEvent(self, event):
        '''Called for all events, this method looks up appropriate handler
        as stored by .register_event()'''
        if 'ANY' in self.handlerdb: # Call a handler for 'Any' key, if available
            self.handlerdb['ANY'](event)
        if event in self.handlerdb:
            self.handlerdb[event](event) #call key-specific handler, if any
    def generate_event(self, event_value, event_type=KEYBOARD_EVENT, timedelay=None):
        '''Used to artificially create an event (such as a timer event)'''
        # DAY, need to finish implementation with timer events, etc.
        if event_type == KEYBOARD_EVENT:
##            key_event = pygame.event.Event(KEYDOWN,
##                            {'unicode':None, 'key': ord(event_value.encode('ASCII')), 'mod':None})
            # note that I should change this to be just unicode for py3, but want py2 compat.
##            key_event = pygame.event.Event(KEYDOWN,
##                            {'unicode':None, 'key': event_value.encode('ASCII'), 'mod':None})
            key_event = pygame.event.Event(KEYDOWN,
                                           {'unicode':event_value,
                                            'key': event_value,
                                            'mod':None})
        pygame.event.post(key_event)

    def mark_dirty(self, dirty_area):
        '''tag a portion of the screen as 'dirty' (i.e. in need of refresh)'''
        raise NotImplementedError
    def refresh_dirty(self):
        '''Refresh the dirty areas of the screen and mark them as clean'''
        raise NotImplementedError
##    def refresh_all(self):
##        '''Refresh entire screen and mark all areas as clean'''
##        raise NotImplementedError
    def start_event_loop(self):
        '''Begin processing mouse and keyboard and window system events'''
        EventTrans = {pygame.K_LEFT: 'LEFT', pygame.K_RIGHT: 'RIGHT', pygame.K_UP: 'UP',
                      pygame.K_DOWN: 'DOWN', pygame.K_SPACE: 'SPACE', pygame.K_MINUS: 'SPACE',
                      pygame.K_ESCAPE: 'Q', pygame.K_RETURN: 'RETURN',
                      pygame.K_a:'A', pygame.K_b:'B', pygame.K_c:'C', pygame.K_d:'D',
                      pygame.K_e:'E', pygame.K_f:'F', pygame.K_g:'G', pygame.K_h:'H',
                      pygame.K_i:'I', pygame.K_j:'J', pygame.K_k:'K', pygame.K_l:'L',
                      pygame.K_m:'M', pygame.K_n:'N', pygame.K_o:'O', pygame.K_p:'P',
                      pygame.K_q:'Q', pygame.K_r:'R', pygame.K_s:'S', pygame.K_t:'T',
                      pygame.K_u:'U', pygame.K_v:'V', pygame.K_w:'W', pygame.K_x:'X',
                      pygame.K_y:'Y', pygame.K_z:'Z',
                      pygame.K_0:'0', pygame.K_1:'1', pygame.K_2:'2', pygame.K_3:'3',
                      pygame.K_4:'4', pygame.K_5:'5', pygame.K_6:'6', pygame.K_7:'7',
                      pygame.K_8:'8', pygame.K_9:'9',
                     }
        while True:
            for event in pygame.event.get():
                if self.boom_on:
                    self.boom_on = False
                    self.grid.refresh_all()
                if event.type == pygame.QUIT:
                    self._onEvent('Q')
                elif event.type == pygame.KEYDOWN:
                    logging.debug("***Received key {0}".format(event.key))
                    if event.key in EventTrans:
                        self._onEvent(EventTrans[event.key])
                    else:
                        self._onEvent(event.key)
            if self.boom_on:
                self.screen.blit(self.boom.image, self.boom.rect)
            self.redraw() #DAY is this needed?
    def redraw(self):
        pygame.display.flip()
        pygame.time.wait(old_div(1000, FPS))
    def wait(self, milliseconds):
        pygame.time.wait(milliseconds)
    def _load_image(self, name, colorkey=None):
        """ Load image and return image object"""
        try:
            image = pygame.image.load(name)
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)
        except pygame.error as message:
            print('Cannot load image:'.format(name))
            raise SystemExit(message)
        return image, image.get_rect()
    def turn_boom_on(self, loc):
        top_right = loc + Location((-1, -1))
        self.boom.rect.top, self.boom.rect.left = (top_right.y * self.cellHeight,
                                                   top_right.x * self.cellWidth)
        self.boom_on = True
    def quit(self):
        '''Do necessary steps to quit game'''
        pygame.display.quit()
        #sys.exit()
    def user_prompt(self, message, button_options=BUTTON_OK_CANCEL, input_field=False):
        raise NotImplementedError
