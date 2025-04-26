import time
import copy
from typing import List, Tuple, Optional

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def is_winner(self, player: str) -> bool:
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def is_board_full(self) -> bool:
        return all(cell != ' ' for row in self.board for cell in row)

    def is_game_over(self) -> bool:
        return self.is_winner('X') or self.is_winner('O') or self.is_board_full()

    def make_move(self, row: int, col: int) -> bool:
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

class TicTacToeAI:
    def __init__(self):
        self.nodes_visited_minimax = 0
        self.nodes_visited_alpha_beta = 0

    def evaluate(self, game: TicTacToe) -> int:
        if game.is_winner('X'):
            return 1
        if game.is_winner('O'):
            return -1
        return 0

    def minimax(self, game: TicTacToe, depth: int, is_maximizing: bool) -> int:
        self.nodes_visited_minimax += 1
        
        if game.is_game_over():
            return self.evaluate(game)

        if is_maximizing:
            max_eval = float('-inf')
            for row, col in game.get_empty_cells():
                game_copy = copy.deepcopy(game)
                game_copy.make_move(row, col)
                eval = self.minimax(game_copy, depth + 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in game.get_empty_cells():
                game_copy = copy.deepcopy(game)
                game_copy.make_move(row, col)
                eval = self.minimax(game_copy, depth + 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def alpha_beta(self, game: TicTacToe, depth: int, alpha: float, beta: float, is_maximizing: bool) -> int:
        self.nodes_visited_alpha_beta += 1
        
        if game.is_game_over():
            return self.evaluate(game)

        if is_maximizing:
            max_eval = float('-inf')
            for row, col in game.get_empty_cells():
                game_copy = copy.deepcopy(game)
                game_copy.make_move(row, col)
                eval = self.alpha_beta(game_copy, depth + 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in game.get_empty_cells():
                game_copy = copy.deepcopy(game)
                game_copy.make_move(row, col)
                eval = self.alpha_beta(game_copy, depth + 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, game: TicTacToe, use_alpha_beta: bool = False) -> Optional[Tuple[int, int]]:
        best_move = None
        best_value = float('inf')  # Minimize for O
        for row, col in game.get_empty_cells():
            game_copy = copy.deepcopy(game)
            game_copy.make_move(row, col)
            if use_alpha_beta:
                move_value = self.alpha_beta(game_copy, 0, float('-inf'), float('inf'), True)  # X's turn
            else:
                move_value = self.minimax(game_copy, 0, True)  # X's turn
            if move_value < best_value:
                best_value = move_value
                best_move = (row, col)
        return best_move

def compare_performance():
    game = TicTacToe()
    ai = TicTacToeAI()
    
    start_time = time.time()
    ai.nodes_visited_minimax = 0
    move_minimax = ai.get_best_move(game, use_alpha_beta=False)
    minimax_time = time.time() - start_time
    minimax_nodes = ai.nodes_visited_minimax

    start_time = time.time()
    ai.nodes_visited_alpha_beta = 0
    move_alpha_beta = ai.get_best_move(game, use_alpha_beta=True)
    alpha_beta_time = time.time() - start_time
    alpha_beta_nodes = ai.nodes_visited_alpha_beta

    print("Performance Comparison:")
    print(f"Minimax:")
    print(f"  Time: {minimax_time:.4f} seconds")
    print(f"  Nodes visited: {minimax_nodes}")
    print(f"Alpha-Beta Pruning:")
    print(f"  Time: {alpha_beta_time:.4f} seconds")
    print(f"  Nodes visited: {alpha_beta_nodes}")
    print(f"Node reduction: {(minimax_nodes - alpha_beta_nodes)/minimax_nodes*100:.2f}%")

if __name__ == "__main__":
    
    game = TicTacToe()
    ai = TicTacToeAI()
    
    print("\nStarting Tic-Tac-Toe game (Player vs AI with Alpha-Beta):")
    while not game.is_game_over():
        game.print_board()
        if game.current_player == 'X':
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter col (0-2): "))
            if not game.make_move(row, col):
                print("Invalid move, try again.")
                continue
        else:
            move = ai.get_best_move(game, use_alpha_beta=False)
            if move:
                game.make_move(move[0], move[1])
                print(f"AI moves to position ({move[0]}, {move[1]})")
    
    game.print_board()
    if game.is_winner('X'):
        print("Player X wins!")
    elif game.is_winner('O'):
        print("AI (O) wins!")
    else:
        print("It's a draw!")
    
    # comparing performance with the best moves, both getting the best moves 
    compare_performance()
