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
        # Base case: Check if the AI (O) has won
        if self.check_winner("O"):
            return 1  # AI win
        
        # Base case: Check if the opponent (X) has won
        if self.check_winner("X"):
            return -1  # Opponent win
        
        # Base case: If the board is full or the maximum depth is reached, it's a draw
        if self.board_full() or depth == max_depth:
            return 0  # Draw
    
        # Recursive case: If it's the AI's turn (maximizing player)
        if is_maximizing:
            best_score = -float('inf')  # Initialize best score to negative infinity
            # Loop through all 9 spaces on the board
            for i in range(9):
                # If the spot is empty, simulate the AI's move
                if board[i] == " ":
                    board[i] = "O"  # Place AI's marker ('O')
                    # Recursively call minimax for the opponent's turn (minimizing player)
                    score = self.minimax(board, depth + 1, False, max_depth)
                    board[i] = " "  # Undo the move (backtrack)
                    # Maximize the score
                    best_score = max(score, best_score)
            return best_score  # Return the best score found
    
        # Recursive case: If it's the opponent's turn (minimizing player)
        else:
            best_score = float('inf')  # Initialize best score to positive infinity
            # Loop through all 9 spaces on the board
            for i in range(9):
                # If the spot is empty, simulate the opponent's move
                if board[i] == " ":
                    board[i] = "X"  # Place opponent's marker ('X')
                    # Recursively call minimax for the AI's next move (maximizing player)
                    score = self.minimax(board, depth + 1, True, max_depth)
                    board[i] = " "  # Undo the move (backtrack)
                    # Minimize the score
                    best_score = min(score, best_score)
            return best_score  # Return the best score found

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

