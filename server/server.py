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

import flask
from flask import request
from pymongo import MongoClient
import bson.json_util
from bson.objectid import ObjectId
import json
import wanderer

app = flask.Flask(__name__)

client = MongoClient('localhost', 27017)
gameDB = client['gameDB']
gameCollection = gameDB['gameCollection']

# TODO Make this into a class so that the interface with
# the front-end can be standardized.

#gDirector = wanderer.GameDirector()

@app.route('/wanderer/newlevel', methods=['POST'])
def newlevel():
    #payload = bson.json_util.loads(flask.request.get_json())
    payload = request.form
    print(payload)
    #return 'mischief managed'
    gDirector = wanderer.GameDirector()
    gDirector.read_new_level_num(int(payload['level']))
    game_state = gDirector.game_state_dict()
    gameId = gameCollection.insert_one(game_state).inserted_id
    response = {
        'gameId': str(gameId),
        'level': [],
    }
    for rowList in game_state['grid_objs']:
        for cell in rowList:
            response['level'].append({
                'row': cell.location[1],
                'col': cell.location[0],
                'add': cell.type,
                })
    return response

if False:
    if 'level' in payload:
        gDirector = wanderer.GameDirector()
        gDirector.read_new_level_num(int(payload['level']))
        game_state = gDirector.game_state_dict()
        gameId = gameCollection.insert_one(game_state).inserted_id
        response = {
            'gameId': str(gameId),
            'level': [],
        }
        for rowList in game_state['grid_objs']:
            for cell in rowList:
                response['level'].append({
                    'row': cell.location[1],
                    'col': cell.location[0],
                    'add': cell.type,
                    })
        return response
    else:
        flask.abort('404') #resource not found

@app.route('/wanderer/move/')
def move():
    #payload = bson.json_util.loads(flask.request.get_json())
    payload = flask.Request.data
    if not ('playerMove' in payload) and ('gameId' in payload):
        flask.abort('404')
    game_state = gameCollection.find_one({
        "_id": ObjectId(payload['gameId'])
        })
    gDirector.restore_state(game_state)
    # game logic does the move...
    gDirector.event_handler(payload['playerMove'])
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

if __name__ == '__main__':
    app.run(port=8000, debug=True)

