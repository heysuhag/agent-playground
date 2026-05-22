
class Game:

    def __init__(self, board, player1, player2):
        self.board = board
        self.p1 = player1
        self.p2 = player2
        self.marker = {self.p1: "X", self.p2: "O"}
        self.current_player = self.p1


    def switch_turn(self):
        if self.current_player == self.p1:
            self.current_player = self.p2 

        else: 
            self.current_player = self.p1 


    def play(self, position):
            
        if self.board.move(position, self.marker[self.current_player]):
            print(f"Position {position} played by {self.current_player} ")
            if self.game_over() == False:
                self.switch_turn()
            elif self.board.win_detection():
                print(f"{self.current_player} has won this round !")
            else:
                print("We have a draw")

    def game_over(self):

        if self.board.board_full() or self.board.win_detection():
            return True 
        else:
            return False
