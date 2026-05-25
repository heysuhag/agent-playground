
class Board:
    def __init__(self):

        self.board: list[list[str | None]] = [[None]*3, [None]*3, [None]*3]
        

    def move(self, position, marker):

        if self.validate_position(position):
            
            self.board[position[0]][position[1]] = marker
            return True

        else:
            print("You went off the board there...think within the box")
            return False


    def validate_position(self, position):
        
        x, y = position[0], position[1]

        if 0 <= x <= 2 and 0 <= y <=2 and self.board[x][y]==None:
            return True
        
        else:
            return False
        

    def board_reset(self):

        self.board = [[None]*3, [None]*3, [None]*3]


    def win_detection(self):

        n_rows = 3
        n_cols = 3

        # row complete 
        for r in range(n_rows):
            if (self.board[r][0] == self.board[r][1] == self.board[r][2]) and (self.board[r][0] is not None):
                return self.board[r][0]
            
        # column complete 
        for c in range(n_cols):
            if (self.board[0][c] == self.board[1][c] == self.board[2][c]) and (self.board[0][c] is not None):
                return self.board[0][c]

        # diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] is not None):
            return self.board[0][0] 

        if (self.board[0][2] == self.board[1][1] == self.board[2][0]) and (self.board[0][2] is not None):
            return self.board[0][2]


    def is_draw(self):

        if (self.win_detection() is None) and self.board_full():
            return True
        
        return False
        
    def board_full(self):

        if not any(None in sl for sl in self.board):
            return True
        
        return False


        


            
            

            
