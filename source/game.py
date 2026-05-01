from playingstate import PlayingState
from errorstate import ErrorState
from player import Player
class Game:
    '''Main game class, handles game state and switching between states.'''
    def __init__(self):
        self.playingstate = PlayingState(Player("Player 1"), Player("Player 2"))
        self.errorstate = ErrorState()
        self.game_state = self.playingstate
    def run(self):
        '''Runs the game in playingstate, if setup fails, runs the error state.'''
        if not self.playingstate.setup():
            self.game_state = self.errorstate
        self.game_state.run()
game = Game()