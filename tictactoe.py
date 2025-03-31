import math
import random
import time

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print(' | ' + ' | '.join(row) + ' | ')

    @staticmethod
    def print_board_nums():
        #---Nos. are displayed for player reference---#
        num_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in num_board:
            print(' | ' + ' | '.join(row) + ' | ')

    def empty_cells(self):
        return ' ' in self.board

    def num_empty_cells(self):
        return len(self.possible_moves())

    def possible_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, cell, letter):
        #---Places the letter in the selected cell if it is valid, if not - returns False, also checks if move is a winner---#
        if self.board[cell] == ' ':
            self.board[cell] = letter
            if self.winner(cell, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, cell, letter):
        row_ind = cell // 3
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        col_ind = cell % 3
        col = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in col]):
            return True

        if cell % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True

            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False

    def clone(self):
        #---a deepcopy of this game is created in current state---#
        new_board = TicTacToe()
        new_board.board = self.board.copy()
        new_board.current_winner = self.current_winner
        return new_board


class AIPlayer:
    #---AI uses minimax algo. combined with alpha-beta pruning---#
    def __init__(self, letter):
        self.letter = letter
        self.opponent_letter = 'O' if letter == 'X' else 'X'

    def get_move(self, game):
        #---if board is empty then cell is randomly chosen---#
        if len(game.possible_moves()) == 9:
            return random.choice([0, 2, 4, 6, 8])
    #---alpha beta variables are initialized---#
        alpha = -math.inf
        beta = math.inf
        best_score = -math.inf
        best_move = None

        for move in game.possible_moves():
            temp_game = game.clone()
            temp_game.make_move(move, self.letter)
            score = self.minimax(temp_game, 0, False, alpha, beta)

            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)

        return best_move

    def minimax(self, game, depth, is_maximizing, alpha, beta):
        if game.current_winner == self.letter:
            return 10 - depth
        elif game.current_winner == self.opponent_letter:
            return depth - 10
        elif not game.empty_cells():
            return 0

        if is_maximizing:
            #---AI maximizes score using alpha-beta pruning---#
            best_score = -math.inf
            for move in game.possible_moves():
                temp_game = game.clone()
                temp_game.make_move(move, self.letter)
                score = self.minimax(temp_game, depth + 1, False, alpha, beta)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = math.inf
            for move in game.possible_moves():
                temp_game = game.clone()
                temp_game.make_move(move, self.opponent_letter)
                score = self.minimax(temp_game, depth + 1, True, alpha, beta)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score


class HumPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        valid_cell = False
        val = None
        while not valid_cell:
            cell = input(f"{self.letter}'s turn. Input move(0-8): ")
            try:
                val = int(cell)
                if val not in game.possible_moves():
                    raise ValueError
                valid_cell = True
            except ValueError:
                print(f"Invalid move. Try again.")
        return val


def play(game, x_player, o_player, print_game=True):
    if print_game:
        #---cell nos. displayed at the start---#
        game.print_board_nums()

    letter = 'X'
    while game.empty_cells():
        if letter == 'X':
            cell = x_player.get_move(game)
        else:
            cell = o_player.get_move(game)

        if game.make_move(cell, letter):
            if print_game:
                print(f"{letter} makes a move to cell {cell}")
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(f"{letter} wins!")
                return letter

            letter = 'O' if letter == 'X' else 'X'
            time.sleep(0.5)

    if print_game:
        print("It's a tie!")
    return None


if __name__ == '__main__':
    print("Welcome, Let's play TIC-TAC-TOE!")
    print("The position of cells are displayed below:")
    TicTacToe.print_board_nums()

    while True:
        #---player gets to choose---#
        player_letter = ''
        while player_letter not in ['X', 'O']:
            player_letter = input("Player choose 'X' or 'O': ").upper()
        #---initializing players based on choice made---#
        if player_letter == 'X':
            human_player = HumPlayer('X')
            ai_player = AIPlayer('O')
            result = play(TicTacToe(), human_player, ai_player)
        else:
            human_player = HumPlayer('O')
            ai_player = AIPlayer('X')
            result = play(TicTacToe(), ai_player, human_player)

        play_again = input("Play again? (yes/no): ").lower()
        if play_again != 'yes':
            break
