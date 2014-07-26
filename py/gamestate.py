
'''
The status of the fruit is a number which is a countdown to the expiry of
the current fruit, if any.
'''
import json


class GameState:
    # The Ghosts' vitality is an enumeration:
    gVital = {'standard': 0,
              'fright mode': 1,
              'invisible': 2,
              }

    # The Ghosts' and Lambda-Man's direction is an enumeration:
    direction = {'up': 0,
                 'right': 1,
                 'down': 2,
                 'left': 3,
                 }
    '''
    * 0: Wall (`#`)
    * 1: Empty (`<space>`)
    * 2: Pill
    * 3: Power pill
    * 4: Fruit location
    * 5: Lambda-Man starting position
    * 6: Ghost starting position
    '''
    tiles = {
        'wall': 0,
        'empty': 1,
        'pill': 2,
        'superPill': 3,
        'fruit': 4,
        'lambdaMan': 5,
        'ghost': 6,
    }

    mapItem = {
        '#': 0,
        ' ': 1,
        '.': 2,
        'o': 3,
        '%': 4,
        '\\': 5,
        '=': 6,
    }

    def __init__(self):
        """
        The state of the world is encoded as follows:

        A 4-tuple consisting of
        1. The map;
        2. the status of Lambda-Man;
        3. the status of all the ghosts;
        4. the status of fruit at the fruit location.

        Note that the map does reflect the current status of all the pills and
        power pills. The map does not however reflect the current location of
        Lambda-Man or the ghosts, nor the presence of fruit. These items are
        represented separately from the map.
        """
        self.board = []
        self.ghosts = []
        self.lambdaMan = None
         

    def addGhost(self, loc, vitality=gVital['standard'], dir=direction['down']):
        """
        The status of all the ghosts is a list with the status for each ghost.
        The list is in the order of the ghost number, so each ghost always appears
        in the same location in the list.

        The status for each ghost is a 3-tuple consisting of
        1. the ghost's vitality
        2. the ghost's current location, as an (x,y) pair
        3. the ghost's current direction

        At the start of the game, all ghosts and Lambdaman face down
        """
        myGhost = {'vitality': vitality,
                   'location': loc,
                   'direction': dir,
                   }
        self.ghosts.append(myGhost)

    def addLambdaMan(self, loc, dir=direction['down'], vitality=0, lives=3, score=0):
        """
        The Lambda-Man status is a 5-tuple consisting of:
        1. Lambda-Man's vitality;
        2. Lambda-Man's current location, as an (x,y) pair;
        3. Lambda-Man's current direction;
        4. Lambda-Man's remaining number of lives;
        5. Lambda-Man's current score.

        Lambda-Man's vitality is a number which is a countdown to the expiry of
        the active power pill, if any. It is 0 when no power pill is active.
        * 0: standard mode;
        * n > 0: power pill mode: the number of game ticks remaining while the
        power pill will will be active

        At the start of the game, all ghosts and Lambdaman face down
        """
        self.lambdaMan = {
            'vitality': vitality,
            'location': loc,
            'direction': dir,
            'lives': lives,
            'score': score,
        }

    def loadMap(self, filename):
        """
        The map is encoded as a list of lists (row-major) representing the 2-d
        grid. An enumeration represents the contents of each grid cell:
        """
        with open(filename, 'r') as f:
            x = 0
            y = 0
            for line in f:
                row = []
                for char in line:
                    if char in GameState.mapItem:
                        if GameState.mapItem[char] == GameState.tiles['lambdaMan']:
                            self.addLambdaMan((x, y))
                            row.append(GameState.tiles['empty'])
                        elif GameState.mapItem[char] == GameState.tiles['ghost']:
                            self.addGhost((x, y))
                            row.append(GameState.tiles['empty'])
                        else:
                            row.append(GameState.mapItem[char])
                    x += 1
                self.board.append(row)
                y += 1
                x = 0

    def printMap(self):
        for row in self.board:
            print(row)

    def getJSON(self):
        return json.dumps(
            {'ghosts': self.ghosts,
             'lambdaMan': self.lambdaMan,
             'board': self.board,
             })

    def saveToFile(self, filename):
        f = open(filename, 'w')
        f.write(self.getJSON())
        f.close()


if __name__ == "__main__":
    game = GameState()
    game.loadMap('../common/maps/world-1.txt')
    print(game.getJSON())
    game.saveToFile('sample2.json')