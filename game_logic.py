class TicTacToeGame:
    def __init__(self, ai_enabled=False):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.ai_enabled = ai_enabled
        self.game_over = False  # Attribute to track if the game is over

    def check_winner(self, mark):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] == mark:
                return True
        return False

    def board_full(self):
        return " " not in self.board

    def minimax(self, board, depth, is_maximizing, max_depth=50):
        if self.check_winner("O"):
            return 1
        if self.check_winner("X"):
            return -1
        if self.board_full() or depth == max_depth:  # Stop at a certain depth
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False, max_depth)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True, max_depth)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False, max_depth=9)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def make_move(self, idx):
        if self.board[idx] == " ":
            self.board[idx] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        print("switched to player: ", self.current_player)

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.game_over = False  # Reset game over state
        print("Reset to player: ", self.current_player)

