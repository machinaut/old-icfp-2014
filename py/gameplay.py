__author__ = 'joe'
from gamestate import GameState
from lambdaman_cpu import LambdaManCPU

class GamePlay:

    move = {0: [0, -1],
            1: [1, 0],
            2: [0, 1],
            3: [-1, 0],
            }

    def __init__(self):

        self.state = GameState()
        self.lman = LambdaManCPU()
        self.scores = {'pill': 10,
                       'superPill': 50,
                       'fruit': self.fruitScore()}
        self.EOL = 20   #TODO Fix this value
        self.lambda_step_fnc = None

    def fruitScore(self):
        return 376  #TODO Fix this value

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


        # Run Lamda-Man CPU
        limit = 1024

        self.lman.clear()  # Since state is not allowed to persist within the emulator between function calls this is needed

        self.lman.c = 4
        #if self.lambda_step_fnc[0] != None:
        #    self.lman.c = self.lambda_step_fnc[0]

        game.lman.control.append({'tag': 'TAG_STOP'})       # Setup the final return control code
        self.lman.status = 'RUNNING'
        for tick in self.lman:
            if limit == 0:
                print('Execution limit reached')
                break
            limit -= 1
        # Save AI State
        ret_pair = self.lman.data[0]['data']  # Load AI move
        ret_dat = self.lman.heap[ret_pair]['data']
        AIstate =ret_dat[0]
        AImove = ret_dat[1]['data']

        if AImove in GamePlay.move:
            proposed_move = [0, 0]
            proposed_move[0] = GamePlay.move[AImove][0] + self.state.lambdaMan['location'][0]
            proposed_move[1] = GamePlay.move[AImove][1] + self.state.lambdaMan['location'][1]
            if self.state.board[proposed_move[1]][proposed_move[0]] != GameState.mapItem['#']:
                self.state.lambdaMan['location'] = proposed_move

        # Run Ghosts


        #actions


        #simple points
        lambda_tile = game.getTileType(game.state.lambdaMan['location'])
        if lambda_tile == GameState.tiles['pill']:
            game.state.meta['score'] += self.scores['pill']
            game.setTileType(game.state.lambdaMan['location'], GameState.tiles['empty'])
        elif lambda_tile == GameState.tiles['superPill']:
            game.state.meta['score'] += self.scores['superPill']
            game.setTileType(game.state.lambdaMan['location'], GameState.tiles['empty'])
        elif lambda_tile == GameState.tiles['fruit']:
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
        return self.state.board[loc[1]][loc[0]]

    def setTileType(self, loc, type):
        self.state.board[loc[1]][loc[0]] = type

    def runLambdaManMain(self):
        # Run Lamda-Man CPU
        limit = 2048    # TODO fix this fictional number
        self.lman.c = 0
        self.lman.status = 'RUNNING'
        for tick in self.lman:
            if limit == 0:
                print('Execution limit reached')
                break
            limit -= 1

        #Check for correct execution
        if self.lman.status == 'STOP':
            self.lambda_step_fnc = self.lman.environ[0]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Execute λ-LISP programs")
    parser.add_argument('source', nargs='?', default='/dev/stdin', help="File to compile (default=stdin)")
    args = parser.parse_args()

    game = GamePlay()
    game.state.loadMap(args.source)
    game.lman.load('./test/goRight.asm')                # args.source
    game.lman.control.append({'tag': 'TAG_STOP'})       # Setup the final return control code

    game.runLambdaManMain()                             # Run the lambdaMan main function

    game.state.print_raw_map()
    game.state.printMap()
    game.state.saveToFile('sample2.json')
    print(game.state.meta['utc'])
    for step in game:
        print('tick')
        print('utc   ', step.state.meta['utc'])
        print('pills ', step.pills())
        print('score ', step.state.meta['score'])
        game.state.printMap()