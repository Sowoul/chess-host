class Piece:
    def __init__(self, val=0, color=None, type=None, alias=None):
        self.val = val
        self.color = color
        self.type = type
        self.alias = alias

    def __str__(self):
        return f"[{self.alias}({self.color})]"

    def to_dict(self):
        return {
            'val': self.val,
            'color': self.color,
            'type': self.type,
            'alias': self.alias
        }

    def is_valid_move(self, start, end, board):
        raise NotImplementedError("This method should be implemented in subclasses.")


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(1, color, '♟' if color == 'B' else '♙', 'p')

    def is_valid_move(self, start, end, board):
        x1, y1 = ord(start[0]) - ord('a'), 8 - int(start[1])
        x2, y2 = ord(end[0]) - ord('a'), 8 - int(end[1])
        dx = x2 - x1
        dy = y2 - y1
        if self.color == 'W':
            if x1 == x2 and dy == -1 and board.getpiece(end) is None:
                return True
            if x1 == x2 and dy == -2 and y1 == 6 and board.getpiece(end) is None:
                return True
            if abs(dx) == 1 and dy == -1 and board.getpiece(end) is not None and board.getpiece(end).color == 'B':
                return True
        if self.color == 'B':
            if x1 == x2 and dy == 1 and board.getpiece(end) is None:
                return True
            if x1 == x2 and dy == 2 and y1 == 1 and board.getpiece(end) is None:
                return True
            if abs(dx) == 1 and dy == 1 and board.getpiece(end) is not None and board.getpiece(end).color == 'W':
                return True

        return False


class Rook(Piece):
    def __init__(self, color):
        super().__init__(5, color, '♜' if color == 'B' else '♖', 'r')

    def is_valid_move(self, start, end, board):
        x1, y1 = ord(start[0]) - ord('a'), 8 - int(start[1])
        x2, y2 = ord(end[0]) - ord('a'), 8 - int(end[1])

        if x1 != x2 and y1 != y2:
            return False
        
        if x1 == x2: 
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if board.getpiece(chr(x1 + ord('a')) + str(8 - y)):
                    return False
        else:  # horizontal movement
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if board.getpiece(chr(x + ord('a')) + str(8 - y1)):
                    return False

        destination = board.getpiece(end)
        if destination and destination.color == self.color:
            return False

        return True


class Knight(Piece):
    def __init__(self, color):
        super().__init__(3, color, '♞' if color == 'B' else '♘', 'n')

    def is_valid_move(self, start, end, board):
        x1, y1 = ord(start[0]) - ord('a'), 8 - int(start[1])
        x2, y2 = ord(end[0]) - ord('a'), 8 - int(end[1])
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        if (dx == 2 and dy == 1) or (dx == 1 and dy == 2):
            destination = board.getpiece(end)
            if destination and destination.color == self.color:
                return False
            return True

        return False


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(3, color, '♝' if color == 'B' else '♗', 'b')

    def is_valid_move(self, start, end, board):
        x1, y1 = ord(start[0]) - ord('a'), 8 - int(start[1])
        x2, y2 = ord(end[0]) - ord('a'), 8 - int(end[1])

        if abs(x2 - x1) != abs(y2 - y1):
            return False
        
        step_x = 1 if x2 > x1 else -1
        step_y = 1 if y2 > y1 else -1
        x, y = x1 + step_x, y1 + step_y

        while x != x2 and y != y2:
            if board.getpiece(chr(x + ord('a')) + str(8 - y)):
                return False
            x += step_x
            y += step_y

        destination = board.getpiece(end)
        if destination and destination.color == self.color:
            return False

        return True


class Queen(Piece):
    def __init__(self, color):
        super().__init__(9, color, '♛' if color == 'B' else '♕', 'q')

    def is_valid_move(self, start, end, board):
        x1, y1 = ord(start[0]) - ord('a'), 8 - int(start[1])
        x2, y2 = ord(end[0]) - ord('a'), 8 - int(end[1])

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        if x1 == x2 or y1 == y2 or dx == dy:
            step_x = 1 if x2 > x1 else -1
            step_y = 1 if y2 > y1 else -1
            
            if x1 == x2: 
                for y in range(y1 + step_y, y2, step_y):
                    if board.getpiece(chr(x1 + ord('a')) + str(8 - y)):
                        return False
            elif y1 == y2: 
                for x in range(x1 + step_x, x2, step_x):
                    if board.getpiece(chr(x + ord('a')) + str(8 - y1)):
                        return False
            else:  # diagonal movement
                x, y = x1 + step_x, y1 + step_y
                while x != x2 and y != y2:
                    if board.getpiece(chr(x + ord('a')) + str(8 - y)):
                        return False
                    x += step_x
                    y += step_y

            destination = board.getpiece(end)
            if destination and destination.color == self.color:
                return False

            return True
        
        return False


class King(Piece):
    def __init__(self, color):
        super().__init__(100, color, '♚' if color == 'B' else '♔', 'k')

    def is_valid_move(self, start, end, board):
        x1, y1 = ord(start[0]) - ord('a'), 8 - int(start[1])
        x2, y2 = ord(end[0]) - ord('a'), 8 - int(end[1])
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        if dx <= 1 and dy <= 1:
            destination = board.getpiece(end)
            if destination and destination.color == self.color:
                return False
            return True
        
        return False


class Board:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
    
    def setup(self):
        self.board[1] = [Pawn('B')] * 8
        self.board[-2] = [Pawn('W')] * 8
        self.board[0][0] = self.board[0][-1] = Rook('B')
        self.board[-1][0] = self.board[-1][-1] = Rook('W')
        self.board[0][1] = self.board[0][-2] = Knight('B')
        self.board[-1][1] = self.board[-1][-2] = Knight('W')
        self.board[0][2] = self.board[0][-3] = Bishop('B')
        self.board[-1][2] = self.board[-1][-3] = Bishop('W')
        self.board[0][4] = King('B')
        self.board[-1][4] = King('W')
        self.board[0][3] = Queen('B')
        self.board[-1][3] = Queen('W')

    def move(self, start, end):
        piece = self.getpiece(start)
        if piece is None:
            raise ValueError("No piece at start position")
        
        if not piece.is_valid_move(start, end, self):
            raise ValueError("Invalid move for piece")

        x1, y1 = ord(start[0]) - ord('a'), 8 - int(start[1])
        x2, y2 = ord(end[0]) - ord('a'), 8 - int(end[1])
        
        if piece.alias == 'p' and end[1] == "8" and piece.color == 'W':
            piece = Queen('W')
        elif piece.alias == 'p' and end[1] == "1" and piece.color == 'B':
            piece = Queen('B')
        self.board[y1][x1] = None
        self.board[y2][x2] = piece

    def getpiece(self, location):
        x, y = ord(location[0]) - ord('a'), 8 - int(location[1])
        return self.board[y][x]

    def to_dict(self):
        return [
            [piece.to_dict() if piece else None for piece in row]
            for row in self.board
        ]

    def __str__(self):
        final = "     "
        for elem in ['   a   ', '   b   ', '   c   ', '   d   ', '   e   ', '   f   ', '   g   ', '   h   ']:
            final += f"{elem}"
        final += '\n'
        rw = 1
        for row in self.board:
            final += f"{rw}    "
            for elem in row:
                final += f"{elem} " if elem else '   .   '
            final += '\n\n'
            rw += 1
        return final
