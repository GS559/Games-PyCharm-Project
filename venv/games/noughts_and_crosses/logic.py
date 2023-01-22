class Game:

    def __init__(self, icons: list[str]) -> None:
        self._board = [[None] * 3] * 3
        self.icons = icons
        self.turn = icons[0]
        self.finished = False

    def _change_turn(self) -> None:
        if not self.finished: self.turn = self.icons[0] if self._turn == self.icons[1] else self.icons[1]
        else: raise ValueError('Game is already finished')

    def _check_win(self) -> tuple[bool]:
        '''
        Returns a tuple of the form (isTheGameFinished, isItADraw)
        The person who won can be found by looking at the .turn property.
        '''

        # verifies every win case
        l = self._board.copy()
        if (l[0][0] == l[1][1] == l[2][2] and l[0][0] is not None) or (l[0][2] == l[1][1] == l[2][0] and l[0][2] is not None):
            self.finished = True
            return True, False
        for i in range(len(l)):
            if (l[i][0] == l[i][1] == l[i][2] and l[i][0] is not None) or (l[0][i] == l[1][i] == l[2][i] and l[0][i] is not None):
                self.finished = True
                return True, False

        # searches for a draw situation
        isBoardFull = True
        for i in l:
            for j in l[i]:
                if not l[i][j] in self.icons:
                    isBoardFull = False
                    break
        if isBoardFull:
            self.finished = True
            return True, True

        return False, False


    def play(self, row: int, col: int) -> tuple[bool]:
        if not self.finished:
            if row >= 0 and row <= 2:
                if col >= 0 and col <= 2:
                    if self._board[row][col] is None:
                        self._board[row][col] = self.turn
                        if self._check_win()[0]: return self._check_win()
                        else:
                            self._change_turn()
                            return self._check_win()

                    else: raise ValueError('Targeted cell already played')
                else: raise ValueError('Invalid column parameter. Must be 0, 1 or 2')
            else: raise ValueError('Invalid row parameter. Must be 0, 1 or 2')
        else: raise ValueError('Game is already finished.')