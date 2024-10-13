class TicTacToeGame:
    """
    A class representing a Tic-Tac-Toe game, supporting both AI and player moves.
    
    Attributes:
    -----------
    board : list
        Represents the 3x3 Tic-Tac-Toe board as a list of 9 spaces.
    current_player : str
        The current player, either 'X' or 'O'.
    ai_enabled : bool
        Flag to indicate whether AI is enabled for single-player mode.
    game_over : bool
        Flag to indicate if the game is over.
    """

    def __init__(self, ai_enabled=False):
        """
        Initializes the TicTacToeGame class, setting up the board, player, and AI flag.
        
        Parameters:
        -----------
        ai_enabled : bool, optional
            If True, AI will be enabled to play against the user (default is False).
        """
        self.board = [" " for _ in range(9)]  # Initialize the empty board with 9 spaces
        self.current_player = "X"  # X starts first by default
        self.ai_enabled = ai_enabled  # Enable or disable AI
        self.game_over = False  # Track if the game has ended

    def check_winner(self, mark):
        """
        Checks if the given player has won the game by matching one of the winning conditions.
        
        Parameters:
        -----------
        mark : str
            The mark ('X' or 'O') to check for a winning combination.
        
        Returns:
        --------
        bool
            True if the player has won, False otherwise.
        """
        # Define the winning conditions (rows, columns, diagonals)
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        # Check each condition
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] == mark:
                return True
        return False

    def board_full(self):
        """
        Checks if the board is completely full with no empty spaces left.
        
        Returns:
        --------
        bool
            True if the board is full, False otherwise.
        """
        return " " not in self.board

    def minimax(self, board, depth, is_maximizing, max_depth=50):
        """
        Recursive implementation of the Minimax algorithm to find the best possible move.
        
        Parameters:
        -----------
        board : list
            The current game board state.
        depth : int
            The current depth of the recursion (used to limit search).
        is_maximizing : bool
            True if it's the maximizing player's (AI) turn, False if it's the minimizing player's (opponent) turn.
        max_depth : int, optional
            Maximum depth of recursion to avoid infinite recursion in complex situations (default is 50).
        
        Returns:
        --------
        int
            The score for the current game state (1 for AI win, -1 for player win, 0 for draw).
        """
        # Check if AI ('O') wins
        if self.check_winner("O"):
            return 1  # AI wins

        # Check if player ('X') wins
        if self.check_winner("X"):
            return -1  # Player wins

        # Check if the board is full or depth limit reached (draw)
        if self.board_full() or depth == max_depth:
            return 0  # Draw

        # Maximizing player's (AI's) turn
        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"  # Simulate AI move
                    score = self.minimax(board, depth + 1, False, max_depth)
                    board[i] = " "  # Undo move (backtrack)
                    best_score = max(score, best_score)  # Get best score
            return best_score

        # Minimizing player's (opponent's) turn
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"  # Simulate player move
                    score = self.minimax(board, depth + 1, True, max_depth)
                    board[i] = " "  # Undo move (backtrack)
                    best_score = min(score, best_score)  # Get best score
            return best_score

    def ai_move(self):
        """
        Determines the best move for the AI by applying the Minimax algorithm to each possible move.
        
        Returns:
        --------
        int
            The index of the best move for the AI on the board.
        """
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"  # Simulate AI move
                score = self.minimax(self.board, 0, False, max_depth=9)
                self.board[i] = " "  # Undo move
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def make_move(self, idx):
        """
        Places the current player's mark on the specified index of the board.
        
        Parameters:
        -----------
        idx : int
            The index of the board where the current player wants to place their mark.
        
        Returns:
        --------
        bool
            True if the move was valid and successful, False if the spot was already taken.
        """
        if self.board[idx] == " ":
            self.board[idx] = self.current_player  # Place the mark
            return True
        return False

    def switch_player(self):
        """
        Switches the turn between player 'X' and player 'O'.
        """
        self.current_player = "O" if self.current_player == "X" else "X"
        print("Switched to player:", self.current_player)

    def reset_game(self):
        """
        Resets the game to its initial state, clearing the board and resetting the turn to player 'X'.
        """
        self.board = [" " for _ in range(9)]  # Clear the board
        self.current_player = "X"  # Reset the player to 'X'
        self.game_over = False  # Reset game over status
        print("Game reset. Player:", self.current_player)
