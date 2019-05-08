# Wanderer2020 Development Notes 

## Table of Contents
1. [Design](#design)
1. [Interfaces](#interfaces)
1. [Installation](#installation)
    1. [Python server](#python) 
    1. [Optional Pygame standalone](#pygame) 
    1. [Web Front End](#web) 
2. [Level Status](#levelstatus)
1. [License](#license)

---
## License 

Wanderer2020 is licensed under the GPL.  See [LICENSE](LICENSE.md) for more information.

---
## Design
Wanderer2020 is primarily a web-based version of wanderer, but it has been designed to be able to use several different front-end displays.  The python server code encapsulates all its calls to display anything into a **Window** object.  This Window object in one case is implemented as a Flask server which communicates with html/css/javascript front-end.  In another case, it is implemented in pygame in [window.py](server/window.py).

## Interfaces <a name="interfaces"></a>

| Front End | Server | Game Logic |
| --------- | ------ | ---------- |
| \> Request a new game (req: level number) | Receive new game request | | 
|  | \> Send request to Game Logic | Load the requested Level |
|  | Save the state json on MongoDB under a newly assigned GameID | \< Send back a state json and a list of display updates |
| Store gameID, update DOM from display update list | \< Send GameID and display updates | | 
| \> Send move request with GameID | Receive move request, lookup state in MongoDB using GameID | | 
|  | \> Send state json and move request to Game Logic |  Unpack state, execute move |
|  | Save updated state to MongoDB using GameID | \< Pack up and send updated state along with display update list |
| Update display using display update list | \< send display update list | | 

## Installation <a id="installation"></a>

### Python Server <a id="python"></a>
* Use python3's built-in venv library to create a virtual environment.  Run `python3 -m venv venv` in the `server/` directory to create a sub-directory called venv.
* Activate the new virtual environment by running `. venv/bin/activate`
* Install the needed python libraries in the virtual environment

```
pip install flask
pip install bson 
pip install pymongo
```

### Mongodb Server <a id="mongodb"></a>
* The wanderer backend requires a MongoDB server.  You can find [MongoDB installation instructions here](https://docs.mongodb.com/manual/installation/)

---

### (Optional) Pygame standalone <a id="pygame"></a>
* If you would like to run a standalone version of the game offline, you need to install the following in the virtual environment:

```
pip install pygame
```

* Then you run the game by typing `python wanderer.py` in the `server/` directory

---
### Web Front-End <a id="web"></a>
* There is no special setup for the Web front-end
* Using python, you can test the front-end by going to `public/` and typing as follows:

```
python3 -m http.server 8000 --bind 127.0.0.1
```

Alternatively you can install extensions on Visual Studio Code that will allow you to open the **index.html** directly in your default browser without the hassle.

## License
Wanderer2020 is licensed under the GPL.  See [LICENSE](LICENSE.md) for more information.

---
## Level status <a id="levelstatus"></a>
* After babymonster fix (spooked by arrows)
* 1-28: OK
* 29: Player Dies by an arrow!
* 30: Player dies!
* 31: OK
* 32-33: Player dies!
* 34-41: OK
* 42-45: Player dies!
* 46-48: OK
* 49-52: Player dies!
* 53: OK
* 54-56: Player dies!
* 57: OK (my level)
* 58: ERROR AND CRASH 
* After babymonster fix (spooked by arrows)
* 1-28: OK
* 29: Player Dies by an arrow!

* Updated DEBUG 2019:
* 1-7: OK
* 8: OK - new solution to get monster
* 9-28: OK 
* 29: Player dies!
* 30: OK
* 31: OK - new solution
* 32: OK
* 33: Player dies!
  
  ---
### Notes from Source before importing into git:

TODO:

12/17/09: Decided to break backwards compatibility wrt complex trigger/slide logic.  
I will just revamp any levels that this breaks or abandon them.  
I have already successfully fixed several levels.  
Look at the list of levels below and continue fixing/modifying to make all of them run (and find other bugs)  Background info: * Original wanderer is tricky on triggers and slide logic.  
In .check_trigger() (check 4 compass points for trigger into a single cell), all 4 points are triggered (i.e. it doesn't stop at the first trigger), however, when something triggers, slide logic is applied to the situation as it was before anything else triggered into that spot.  
This is why a rock falling toward a balloon stacks on top of the balloon:  The rock fills the gap between them and then stops since it can't slide around a balloon.  
The balloon is triggered into that spot that the rock filled, but the slide logic isn't employed because it looks at a frozen configuration before the rock fell and finds an empty spot (which doesn't cause the slide logic to employ).  
This also impacts arrows that slide up and over a rock that *used* to be in that spot, but had already triggered and fallen down out of it.  
Also, if the spot was originally empty, but now has a rock, the arrow *won't* slide up and over it since the frozen configuration had an empty space which doesn't cause slide logic to employ.  
I think I am going to break backwards compatibility on this.  
My original notes says that this will only break about 5 levels.  One of them is level 29 (rock/balloon early in the level).

12/17/09: Need to fix bug exhibited on level 25.  
I think it is a problem with the "second push" logic which tries to delete an object which has already been deleted.


* Think about making the "falls" non-recursive
* Fix bug with baby monsters in first baby monster stage (when rocks fall on top of the last 2)
* Fix bomb so the Boom stays up until next move.
* Implement player dying and giving message
* Pushing objects causes a different trigger pattern in original -- it is convoluted though -- see GetPushTriggerSpots in original wandobj.py
	    def GetPushTriggerSpots(self, vector): #for Rock
	        '''ROCK: Return sequence of tuples which represent
	        locations which should be checked using self.TriggerFallsIntoLocation().
	        This is used because each object triggers a slightly different
	        pattern of locations when it is pushed.  Note that this is called
	        *before* self is pushed'''
	        pusher_x = self.x - vector[0]
	        pusher_y = self.y - vector[1]
	        return [ (self.x*2-pusher_x, pusher_y+1), (pusher_x*2-self.x, pusher_y),
	                 (pusher_x, pusher_y), (pusher_x, pusher_y-1),
	                 (pusher_x, pusher_y+1) ]

	    def GetPushTriggerSpots(self, vector): #for Balloon
	        '''BALLOON:  Return sequence of tuples which represent
	        locations which should be checked using self.TriggerFallsIntoLocation().
	        This is used because each object triggers a slightly different
	        pattern of locations when it is pushed.   Note that this is called
	        *before* self is pushed'''
	        pusher_x = self.x - vector[0]
	        pusher_y = self.y - vector[1]
	        return [ (self.x*2-pusher_x, pusher_y-1), (pusher_x*2-self.x, pusher_y),
	                 (pusher_x, pusher_y), (pusher_x, pusher_y+1),
	                 (pusher_x, pusher_y-1) ]

	    def GetPushTriggerSpots(self, vector): #for Arrow
	        '''ARROW:  Return sequence of tuples which represent
	        locations which should be checked using self.TriggerFallsIntoLocation().
	        This is used because each object triggers a slightly different
	        pattern of locations when it is pushed.   Note that this is
	        called *before* self is pushed'''
	        pusher_x = self.x - vector[0]
	        pusher_y = self.y - vector[1]
	        if self.y > pusher_y:
	            return [ (pusher_x, pusher_y),
	                     (pusher_x-1, pusher_y), (pusher_x+1, pusher_y),
	                     (pusher_x-1, self.y*2-pusher_y),
	                     (pusher_x+1, self.y*2-pusher_y)]
	        else:
	            return [ (pusher_x, pusher_y),
	                     (pusher_x-1, pusher_y-1), (pusher_x+1, pusher_y-1),
	                     (pusher_x-1, self.y*2-pusher_y),
	                     (pusher_x+1, self.y*2-pusher_y)]

* My current pushing implementation only allows 2-level pushing.  I may want to break out .try_move() into 2 parts
  to allow pushing to arbitrary levels using recursion.  See DAY comment in .try_move() secondary push section
* Original wanderer is tricky on triggers and slide logic.  
In .check_trigger() (check 4 compass points for trigger into a single cell), all 4 points are triggered (i.e. it doesn't stop at the first trigger), however, when something triggers, slide logic is applied to the situation as it was before anything else triggered into that spot.  
This is why a rock falling toward a balloon stacks on top of the balloon:  The rock fills the gap between them and then stops since it can't slide around a balloon.  
The balloon is triggered into that spot that the rock filled, but the slide logic isn't employed because it looks at a frozen configuration before the rock fell and finds an empty spot (which doesn't cause the slide logic to employ).  
This also impacts arrows that slide up and over a rock that *used* to be in that spot, but had already triggered and fallen down out of it.  
Also, if the spot was originally empty, but now has a rock, the arrow *won't* slide up and over it since the frozen configuration had an empty space which doesn't cause slide logic to employ.  
I think I am going to break backwards compatibility on this. 
My original notes says that this will only break about 5 levels.  One of them is level 29 (rock/balloon early in the level).

* DEBUG:
* 1-9: OK
* 10: OK - new solution, old one didn't work on filakowski
* 12: OK - new solution
* 13: OK
* 14: OK - new solution
* 15: OK
* 16: OK - new screen and new solution (only changed one rock to dirt) Problem is related to complex trigger/slide logic from original
* 17-22: OK
* 23: OK - new screen and new solution
* 24: OK
* 25: OK (fixed error with second_push moving)
* 26: Dies with baby monster on left hand side
* 27-28: OK
* 29: NO -- problem is the *frozen* config for slide logic on a trigger (break compatibility?)
* 30: Program gets an error trying to remove an object
* 31: No -- seems to get messed up early on but doesn't die
* 32: OK
* 33: Dies on a baby monster
* 34-38: OK
* 39: Program gets an error trying to remove an object
* 40-41: OK
* 42: Dies on arrow
* 43: OK
* 44: Dies on baby monster
* 45: Dies on arros
* 46-48: OK
* 49: Dies on falling rock
* 50: Dies on baby monster
* 51: Program gets an error trying to remove an object
* 52: Dies on baby monster
* 53: OK
* 54: No -- get's messed up
* 55: Gets messed up, then dies on rock
* 56: Dies on rock
* 57: NO - gets messed up (my level)
* 58: FIRST RUG: program gets an error
* 59: Program gets an error
* 60: Dies on baby monster
* 61: Key error after arrow pushes rug
* 62: Doesn't load (solution problem)



1. Rather than every object needing to know how it interacts with other objects (making it difficult to add a new one).  Consolidate interaction detail in an "Interactions" object which holds a table that determines interactions.  That way, my game objects can have a consistent interface and even consistent implementation.  Each carries a reference to the interaction object and calls it to determine if it can move, if it slides, if it dies, etc.  Specific objects can have custom methods, of course (like bomb's blowing up when they die), but determining when they get called is the interaction object's job.  This might be considered the MEDIATOR pattern.  Use SINGLETON for the Interactions object.
2. I considered using the FLYWEIGHT pattern, but the work of making any changeable state information extrinsic instead of intrinsic sounds like too much complication given that there really aren't too many objects in the grid.  However, thinking about scaling the game up to larger screens makes me think that I will put in FLYWEIGHT, but only implement it for static objects (like walls, dirt, etc.)
3. Use a FACTORY METHOD or BUILDER to build the game board with game objects.
4. If I wanted to get *really* ambitious, I could abstract the windowing system (using BRIDGE) so that the game could be played "retro" style with just characters instead of graphics.  This could also help port the game to Jython (for internet play) or IronPython.
5. Grid/Cell:  I have decided that I need an object to encapsulate a location (cell) (and possibly an object to be a collection of those locations, such as "board").  However, I'm not going to try to make the cell object a COMPOSITE design pattern (i.e. where the individual element has the same interface as the collection element).  The main job of the "cell" object is to hold all the game objects currently residing there (since there can be more than one) and to be called during trigger logic.  The reason the cell object is called during trigger logic is because the Wanderer trigger logics doesn't ask "can this object fall anywhere?", it asks "can any objects fall into this location?".  Hence, it makes sense to me to have a cell.trigger() method which would call surrounding cell objects which in turn would call their occupant gameobj objects to see if they fall.
Here was my older thinking on this topic:  
5(old1). Should there be a Grid object?  Does each object keep track of its "wake" for triggering, or should this be the job of a Grid object?  The trouble with a Grid object is that it would have to have knowledge of each type of game object.  I don't think I should do that.  I could consider using the previously mentioned "interactions" object, but it could be argued that the wake of an object is unique to that object and doesn't change relative to other objects, therefore the Interactions object isn't needed (i.e. the wake code wouldn't have to be re-written in all my game objects when I add a new game object -- this is true only if I want to stay with the current status quo of static wakes.  If I wanted the wake to be something determined by interactions between objects, for example, a rock triggers a balloon from far off, but needs to get very close to an arrow to trigger, then in that case, it should be in "Interactions")
5(old1). I should have objects that represent locations in the grid.  These grid objects could hold a list of references to the occupying object(s).  This grid object should be the thing 'triggered' because the original logic of triggering checks if anything can fall into a specific *location*.  In my logic, it would be the location object calling objects around it to see if they can fall into that location.  The implementation for whether they can fall there can be built into the game objects since there (shouldnt) be any object/object interaction code in that decision (if there were, we want to encapsulate object/object interactions in the "interactions" object).  Implement Grid as a COMPOSITE so that the object that holds all the Grid intersections (the list of Grid objects) has the same interface as an individual Grid object (which holds the list of GameObj's at that location).
6. Define a consistent vocabulary to describe things.  For example, each of the triggerpoints that gets triggered when an object moves.  Also the points an object checks and travels along when it slides around other objects.  Our interaction object is going to need this vocabulary to be clear.  For example, one obect can go through another in some contexts (like an arrow thru a monster), but not in other contexts (i.e. the same arrow will now slide around a ramp if that monster is in the way).  There are also contexts that represent a shooting/falling object vs. a "pushed" object (perhaps an object includes whether it is shooting/falling or being pushed when it calls the interface object.  the object knows this because if it is going in it's normal vector, then it is shooting/falling, otherwise, it is being pushed).
7. **Game Object**
	* Knows how to draw itself (really just passes off a call to the Window object)
	* Knows its wake (does it call trigger code itself, or just pass it's wake up to a client that calls it?)
	* Knows which direction it falls (?)
	* Knows which direction it is pushed in (?)
	* Calls Interactions object to determine outcome of fall or push (and takes no further action -- Interaction object calls the game object's appropriate method to take action if needed -- game object just calls self._interactions.TryPush(self, destination), it get's back a success or failure code from Interactions, but it does nothing with it except pass it back up to whatever called it's own method to initiate the push -- if it is succesful, the Interactions object will have already made it happen by calling the game object's "move" method before it returned successful. (for example, if it can push, then it will call that object's "move" method which simply changes it's location data and calls the windowing system's move method with it's graphical representation data).
		* Here is an interaction
			1. Client calls Hero's .Push() method (with 'command' parameter to note that this move attempt is being triggered by the human player's command) (DAY - perhaps the hero object being moved by the human's command is exactly analogous to an object being "pushed"?  If so, make it logically the same to increase transparency of the hero object.
			2. Hero calls Interaction's .TryMove() method, passing itself and destination (and whether it is falling/shooting or being pushed?)
			3. Interaction looks at what's in Hero's path (say, Rock1) and determines if it is successful by first looking in it's table.  The table in this case can't determine, so Interaction calls Rock1's Push() method with appropriate parameters (i.e. pushed)
			4. Rock1 calls Interaction's .TryMove() method, passing itself and destination (and the fact that it is being pushed)
			5. Interaction looks' at what's in Rock1's path (say, Empty1) and determines through it's table lookup that the move is sucessful.  It then calls Rock1's .ExecuteMove() method, which will actually execute the move (i.e. update Rock1's internal data on location, register itself with the object representing that grid object and call the window objects' draw function to animate the move (or just redraw the Rock1 in the right place).
			6. After Interaction (in it's .TryMove() method) calls Rock1's .ExecuteMove() method, it returns SUCCESS to the whoever called it, which in this case is Rock1's .Push() method.  .Push() doesn't do anything with this except return this result to its own caller (in particular, it doesn't try to execute any of the move, since this was already done by Interaction object.
			7. Rock1's .Push() returns the SUCCESS to Interaction's .TryMove(), which executes the move by calling Hero's .ExecuteMove() method.  It then returns SUCCESS to Hero's .Push() method
			
			5(a) In an alternate scenario, let's say hero tries to push Rock1, but this time instead of an Empty1 in the path, it is Rock 2 in the path.  So everything goes the same through step 4, but in step 5, Interaction look's up in its table and determines that Rock1 cannot be pushed into Rock2, so it returns an UNSUCCESSFUL.
			6(a) Rock1's .Push() method gets the unsuccessful and return it to it's own caller, which is Interactions .TryMove() object.
			7(a) The original call to Interactions' .TryMove() method (from step 2/3) was not initially able to tell whether hero's push of Rock1 would succeed, but now with this return value, knows that it does not succeed and returns that value.
			8(a) Interaction's .TryMove() method returns the UNSUCCESSFUL back to Hero's .Push() method.  Hero's .Push() method has been reimplemented so that it does something a little extra by playing a sound and incrementing the move counter.
---

