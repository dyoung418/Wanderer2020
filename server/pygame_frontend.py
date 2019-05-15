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
from pygame.locals import *
from location import Location

from wand_gamelogic import LevelExitException
from wand_gamelogic import HeroDiedException
from wand_gamelogic import ExitGame

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
KR_DELAY = 250 # controls key repeat behavior (when holding down key)
KR_INTERVAL = 30 # controls key repeat behavior (when holding down key)
FPS = 90 # Frames per second
BUTTON_OK_CANCEL, BUTTON_YES_NO, BUTTON_OK = list(range(3))

def getFrontEnd(rows, cols, size='m'):
    '''Factory function for getting a window.  This function
    determines which window implementation (e.g. pygame, tkinter,
    curses) to use'''
    #DAY - eventually, read from options which windows system to use
    return Window_Pygame(rows, cols, size=size)

class Window_Pygame(object):
    '''Window defines a logical interface. Subclasses implement specific system
    Window keeps a dictionary which maps GameObject objects to structures
    (such as sprite objects or image objects) needed to paint that GameObject
    on the screen.
    '''
    def __init__(self, rows, cols, size='m'):
        self.handlerdb = {}
        pygame.init()
        if pygame.display.get_init() != 1:
            print("Display was not initialized")
            pygame.quit()
        self.boom_on = False
        self.rows = rows
        self.cols = cols
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

        self.objectGraphics = {
            ' ': {"name":"Empty", "imagefile":"blank.gif"}, # these will have 'surface' key/value pairs added
            '-': {"name":"Empty", "imagefile":"blank.gif"},
            'A': {"name":"Teleport destination",
                         "imagefile":"teleportdestination.gif"},
            'B': {"name":"Bomb", "imagefile":"bomb.gif"},
            '#': {"name":"Stone wall", "imagefile":"stonewall.gif"},
            '=': {"name":"Brick wall", "imagefile":"brickwall.gif"},
            '/': {"name":"Ramp", "imagefile":"rightupramp.gif"},
            "\\": {"name":"Ramp", "imagefile":"leftupramp.gif"},
            ':': {"name":"Dirt", "imagefile":"dirt.gif"},
            'F': {"name":"Funky Dirt", "imagefile":"funkydirt.gif"},
            '!': {"name":"Poison", "imagefile":"poison.gif"},
            'X': {"name":"Exit", "imagefile":"exit.gif"},
            '*': {"name":"Money bag", "imagefile":"money.gif"},
            'T': {"name":"Teleport booth", "imagefile":"teleporter.gif"},
            'C': {"name":"Time capsule", "imagefile":"clock.gif"},
            '+': {"name":"Cage", "imagefile":"cage.gif"},
            'O': {"name":"Rock", "imagefile":"rock.gif"},
            '>': {"name":"Arrow", "imagefile":"rightarrow.gif"},
            '<': {"name":"Arrow", "imagefile":"leftarrow.gif"},
            '^': {"name":"Balloon", "imagefile":"balloon.gif"},
            'M': {"name":"Hungry monster", "imagefile":"monster.gif"},
            'S': {"name":"Baby monster", "imagefile":"babymonster.gif"},
            '~': {"name":"Rug", "imagefile":"rug.gif"},
            '@': {"name":"Player", "imagefile":"player.gif"},
            'E': {"name":"Edge", "imagefile":"edge.gif"},
            'W': {"name":"Wrapping edge", "imagefile":"wrapping edge.gif"},
        }
        boom_imagefile = 'boom.gif'

        self.screen = pygame.display.\
            set_mode((self.cols * self.cellWidth,
                      self.rows * self.cellHeight))
        pygame.mouse.set_visible(0)
        # Set key repeat parameters -- delay and interval
        pygame.key.set_repeat(KR_DELAY, KR_INTERVAL)
        self.clock = pygame.time.Clock()
        self.boom = pygame.sprite.Sprite()
        self.boom.image, self.boom.rect = self._load_image(
            os.path.join(self.imageDir, boom_imagefile))
        self.initialize_obj_images()
        self.updated_rects = []

    def initialize_obj_images(self):
        for key in self.objectGraphics.keys():
            surface, rec = self._load_image(\
                os.path.join(self.imageDir, self.objectGraphics[key]['imagefile']))
            self.objectGraphics[key]['surface'] = surface

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
        self.set_status_line('Wanderer 2020')

    def set_status_line(self, message):
        pygame.display.set_caption(message)

#     def initialize_gameobj_data(self, gameobj):
#         '''Called with each gameobj created.  Return any structures
#         (sprites, etc.) needed to draw and move. The GameObj will
#         store that structure and we can use it later to draw objects
#         that request our .draw_obj()'''
#         s = pygame.sprite.Sprite()
#         # DAY -- eventually just read all image data into a dict
#         #        and reuse it for each game type
#         s.image, s.rect = self._load_image(
#             os.path.join(self.imageDir,   
#                 objectGraphics[gameobj.obj_type].imagefile))
#         loc = gameobj.location
#         s.rect.top, s.rect.left = (loc.y * self.cellHeight,
#                                    loc.x * self.cellWidth)
# ##        s.rect.move(loc.x * self.cellWidth, loc.y * self.cellHeight)
#         return s

    def display_updates(self, update_list):
        for obj_type, loc in update_list:
            self.draw_obj(obj_type, loc)
        self.update_screen()

    def draw_obj(self, obj_type, location, update_screen=False):
        surface = self.objectGraphics[obj_type]['surface']
        rec = self.convert_loc(location)
        self.screen.blit(surface, rec)
        self.updated_rects.append(rec)
        if update_screen:
            self.update_screen()

    def convert_loc(self, loc):
        '''convert a tuple location corresponding to the game grid
        to a pygame Rect object of the screen (x,y) coordinates of the
        top-left corner'''
        return pygame.Rect(loc[0] * self.cellWidth, # left
            loc[1] * self.cellHeight, # top
            self.cellWidth, # width
            self.cellHeight, # height
        )

    def update_screen(self):
        if self.updated_rects:
            pygame.display.update(self.updated_rects)
            self.updated_rects = []
        else:
            pygame.display.update()
        self.clock.tick(FPS)

    def register_event(self, event_value, handler,
                       event_type=KEYBOARD_EVENT):
        '''Register a callback function to be invoked when an event
        happens'''
        self.handlerdb[event_value] = handler

    def _onEvent(self, event):
        '''Called for all events, this method looks up appropriate
        handler as stored by .register_event()'''
        if 'ANY' in self.handlerdb:
            # Call a handler for 'Any' key, if available
            self.handlerdb['ANY'](event)
        if event in self.handlerdb:
            #call key-specific handler, if any
            self.handlerdb[event](event)

    def generate_event(self, event_value,
                       event_type=KEYBOARD_EVENT,
                       timedelay=None):
        '''Used to artificially create an event (such as a timer
        event)'''
        # DAY, need to finish implementation with timer events, etc.
        if event_type == KEYBOARD_EVENT:
            key_event = pygame.event.Event(KEYDOWN,
                                           {'unicode':event_value,
                                            'key': event_value,
                                            'mod':None})
        pygame.event.post(key_event)

    def start_event_loop(self):
        '''Begin processing mouse and keyboard and window
        system events'''
        EventTrans = {K_LEFT: 'LEFT', K_RIGHT: 'RIGHT', K_UP: 'UP',
            K_DOWN: 'DOWN', K_SPACE: 'SPACE', K_MINUS: 'SPACE',
            K_ESCAPE: 'Q', K_RETURN: 'RETURN', K_a:'A', K_b:'B',
            K_c:'C', K_d:'D', K_e:'E', K_f:'F', K_g:'G', K_h:'H',
            K_i:'I', K_j:'J', K_k:'K', K_l:'L', K_m:'M', K_n:'N',
            K_o:'O', K_p:'P', K_q:'Q', K_r:'R', K_s:'S', K_t:'T',
            K_u:'U', K_v:'V', K_w:'W', K_x:'X', K_y:'Y', K_z:'Z',
            K_0:'0', K_1:'1', K_2:'2', K_3:'3', K_4:'4', K_5:'5',
            K_6:'6', K_7:'7', K_8:'8', K_9:'9',
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
                self.updated_rects.append(self.boom.rect)
            self.update_screen() 

    def wait(self, milliseconds):
        pygame.time.wait(milliseconds)

    def turn_boom_on(self, loc):
        top_right = loc + Location((-1, -1))
        self.boom.rect.top, self.boom.rect.left = (top_right.y * self.cellHeight,
                                                   top_right.x * self.cellWidth)
        self.boom_on = True

    def quit(self):
        '''Do necessary steps to quit game'''
        pygame.display.quit()
        #sys.exit()

    def user_prompt(self, message,
                    button_options=BUTTON_OK_CANCEL,
                    input_field=False):
        raise NotImplementedError
