__author__ = 'joe'
from gamestate import GameState


class GamePlay:

    def __init__(self):
        self.state = GameState()
        self.scores = {'pill': 10,
                       'superPill': 50,
                       'fruit': self.fruitScore()}
        self.EOL = 20

    def fruitScore(self):
        return 376

    def __iter__(self):
        return self

    def __next__(self):
        """
        On each tick:
        All Lambda-Man and ghost moves scheduled for this tick take place. The next move is also scheduled at this point.
        Next, any actions (fright mode deactivating, fruit appearing/disappearing) take place.
        Next, we check if Lambda-Man is occupying the same square as pills, power pills, or fruit:
            If Lambda-Man occupies a square with a pill, the pill is eaten by Lambda-Man and removed from the game.
            If Lambda-Man occupies a square with a power pill, the power pill is eaten by Lambda-Man, removed from the game, and fright mode is immediately activated, allowing Lambda-Man to eat ghosts.
            If Lambda-Man occupies a square with a fruit, the fruit is eaten by Lambda-Man, and removed from the game.
        Next, if one or more visible ghosts are on the same square as Lambda-Man, then depending on whether or not fright mode is active, Lambda-Man either loses a life or eats the ghost(s).
        Next, if all the ordinary pills (ie not power pills) have been eaten, then Lambda-Man wins and the game is over.
        Next, if the number of Lambda-Man lives is 0, then Lambda-Man loses and the game is over.
        Finally, the tick counter is incremented.
        """
        #move


        #actions


        #simple points
        lambda_tile = game.getTileType(game.state.lambdaMan['location'])
        if lambda_tile == GameState.tiles['pill']:
            print('standing on a pill')
            game.state.meta['score'] += self.scores['pill']
            game.setTileType(game.state.lambdaMan['location'], GameState.tiles['empty'])
        elif lambda_tile == GameState.tiles['superPill']:
            print('standing on a SUPER pill')
            game.state.meta['score'] += self.scores['superPill']
            game.setTileType(game.state.lambdaMan['location'], GameState.tiles['empty'])
        if lambda_tile == GameState.tiles['fruit']:
            print('hmmmmm fruity')
            game.state.meta['score'] += self.scores['fruit']
            game.setTileType(game.state.lambdaMan['location'], GameState.tiles['empty'])

        #ghosts
        ghosts = self.ghostsOnTile(self.state.lambdaMan['location'])
        if len(ghosts) > 0:
            for ghost in ghosts:
                if ghost['vitality'] == GameState.gVital['fright mode']:
                    print('Ghost is eaten')
                elif ghost['vitality'] == GameState.gVital['standard']:
                    print('LambdaMan is eaten!')
                    break

        #pills remaining
        if self.pills() == 0:
            raise StopIteration

        #lives remaining
        if self.state.lambdaMan['lives'] <= 0:
            raise StopIteration

        #tick
        self.state.meta['utc'] += 1
        if self.state.meta['utc'] >= self.EOL:
            raise StopIteration

        return self

    def ghostsOnTile(self, tile_loc):
        ghosts_on_tile = []
        for ghost in self.state.ghosts:
            if ghost['location'] == tile_loc:
                ghosts_on_tile.append(ghost)
        return ghosts_on_tile

    def pills(self):
        pill_count = 0
        for row in self.state.board:
            for tile in row:
                if tile == GameState.tiles['pill']:
                    pill_count += 1
        return pill_count

    def getTileType(self, loc):
        return self.state.board[loc[0]][loc[1]]

    def setTileType(self, loc, type):
        self.state.board[loc[0]][loc[1]] = type

if __name__ == "__main__":
    game = GamePlay()
    game.state.loadMap('../common/maps/world-1.txt')
    game.state.printMap()
    game.state.saveToFile('sample2.json')

    print(game.state.meta['utc'])
    for step in game:
        print('tick')
        print('utc   ', step.state.meta['utc'])
        print('pills ', step.pills())
        print('score ', step.state.meta['score'])

        if step.state.meta['utc'] == 2:
            step.state.lambdaMan['location'] = (1, 1)
        elif step.state.meta['utc'] == 4:
            step.state.lambdaMan['location'] = (1, 2)
        elif step.state.meta['utc'] == 6:
            step.state.lambdaMan['location'] = (1, 6)
        elif step.state.meta['utc'] == 8:
            step.state.ghosts[0]['location'] = step.state.lambdaMan['location']
        elif step.state.meta['utc'] == 14:
            step.state.ghosts[1]['location'] = step.state.lambdaMan['location']