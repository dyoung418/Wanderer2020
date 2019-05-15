'''
The server sits between the front end and game logic modules.

In one sense, the server + front-end together form a client
for the game logic backend -- where the front-end
provides the display and the server does the communicating
of commands to the game logic and getting the results of those
commands from the game logic.  The server also is the module which
stores game state in cases where the game logic might serve many
games.

In another sense, however, you can think of the server + game logic
as the backend to the front-end client.  In the case of web-based
wanderer, the server+game logic both run on backend servers together
whereas the front-end is a web app running in the browser.

In any case, it is always the server that communicates betweeen
these two modules -- the front-end and game logic never directly
interface.
'''

import copy
import flask
from flask import request
from pymongo import MongoClient
import bson.json_util
from bson.objectid import ObjectId
import json
from wand_gamelogic import GameDirector

app = flask.Flask(__name__)

client = MongoClient('localhost', 27017)
gameDB = client['gameDB']
gameCollection = gameDB['gameCollection']


@app.route('/wanderer/newlevel', methods=['POST'])
def newlevel():
    global wandererGame
    payload = request.form
    wandererGame = WandererGame(int(payload['level']))
    updates = wandererGame.get_updates()
    state = wandererGame.get_state()
    gameId = gameCollection.insert_one(state).inserted_id
    response = {
        'gameId': str(gameId),
        'updates': updates,
    }
    return repr(response)

@app.route('/wanderer/move/', methods=['POST'])
def move():
    global wandererGame
    payload = flask.Request.form
    if not (('playerMove' in payload) and ('gameId' in payload)):
        flask.abort('404')
    game_state = gameCollection.find_one({
        "_id": ObjectId(payload['gameId'])
        })
    wandererGame.restore_state(game_state)
    wandererGame.event_handler(payload['playerMove'])
    game_state = gDirector.game_state_dict()
    gameCollection.find_one({
        "_id": ObjectId(payload['gameId'])
        }).update(game_state) #update game_state in mongo
    # get display updates for front-end
    updates = gDirector.get_display_updates()
    response = {
        'updates': updates,
    }
    return response


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
        self.updates = self.gameLogic.update_all()

    def get_updates(self):
        return_copy = copy.deepcopy(self.updates)
        self.updates = []
        return return_copy

    def get_state(self):
        return self.gameLogic.game_state_dict()

    def restore_state(self, state):
        self.gameLogic.restore_state(state)

    def event_handler(self, event):
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
            # TODO: DAY send all other events to game logic.  For pygame, we don't 
            # need to send the state with each event, but for the
            # server of the web version, we will.
            state, self.updates = self.gameLogic.event_handler(event)
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
        '''Start the event loop'''
        pass


#######################################################



if __name__ == '__main__':
    app.run(port=8000, debug=True)

