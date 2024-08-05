'''
Shreeji Patel
Professor Smith
Project 3
'''

import random

class Minesweeper:
    def __init__(self, size=5, mines=4):
        self.size = size  # Board size (5x5 by default)
        self.mines = mines  # Number of mines on the board
        self.board = [['#' for _ in range(size)] for _ in range(size)]  # Initialize board with unopened cells
        self.mine_positions = self.place_mines()  # List of mine positions
        self.user_moves = []  # List to log user moves
        self.revealed_board = [[0 for _ in range(size)] for _ in range(size)]  # Board with counts of adjacent mines
        self.flags = set()  # Set to keep track of flagged cells
        self.place_numbers()  # Calculate numbers for each cell based on adjacent mines
        self.game_over = False  # Flag to indicate if the game is over

    def place_mines(self):
        mine_positions = []
        while len(mine_positions) < self.mines:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)  # Random position for a mine
            if (x, y) not in mine_positions:
                mine_positions.append((x, y))  # Add position if not already occupied
        return mine_positions

    def place_numbers(self):
        for (x, y) in self.mine_positions:
            self.revealed_board[x][y] = 'M'  # Place mine on the revealed board
            for nx, ny in self.get_adjacent_cells(x, y):
                if self.revealed_board[nx][ny] != 'M':
                    self.revealed_board[nx][ny] += 1  # Increment number for adjacent cells

    def display_board(self):
        print("   " + " ".join(f"\033[1;34m{i+1}\033[0m" for i in range(self.size)))  # Print column headers
        for idx, row in enumerate(self.board):
            row_display = ' '.join(self.format_cell(cell) for cell in row)  # Format each cell
            print(f"\033[1;34m{idx+1}\033[0m  {row_display}")  # Print row with row number
        print()

    def format_cell(self, cell):
        # Return formatted cell string based on its content
        if cell == 'M':
            return "\033[1;31mM\033[0m"  # Red for mines
        elif cell == 'F':
            return "\033[1;33mF\033[0m"  # Yellow for flags
        elif cell == '0':
            return "\033[1;34m0\033[0m"  # Blue for zeroes
        elif cell == '#':
            return "\033[1;30m#\033[0m"  # Dark gray for unopened cells
        elif cell.isdigit():
            return f"\033[1;32m{cell}\033[0m"  # Green for numbers
        else:
            return f"\033[1;37m{cell}\033[0m"  # Default for other cells

    def get_adjacent_cells(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        adjacent_cells = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                adjacent_cells.append((nx, ny))  # Add valid adjacent cells
        return adjacent_cells

    def open_cell(self, x, y, user_initiated=True):
        if (x, y) in self.flags:
            return True  # Do nothing if the cell is flagged
        if self.board[x][y] != '#':
            return True  # Do nothing if the cell is already opened

        if user_initiated:
            self.user_moves.append((x+1, y+1, 'user open'))  # Log user-initiated open move
        else:
            self.user_moves.append((x+1, y+1, 'auto open'))  # Log auto-open move

        if (x, y) in self.mine_positions:
            self.game_over = True
            self.board[x][y] = 'M'
            return False  # Hit a mine

        if self.revealed_board[x][y] == 0:
            self.board[x][y] = '0'
            for nx, ny in self.get_adjacent_cells(x, y):
                if self.board[nx][ny] == '#':
                    self.open_cell(nx, ny, user_initiated=False)  # Recursively open adjacent cells
        else:
            self.board[x][y] = str(self.revealed_board[x][y])

        return True

    def flag_cell(self, x, y):
        if self.board[x][y] == '#':
            self.board[x][y] = 'F'
            self.flags.add((x, y))
            self.user_moves.append((x+1, y+1, 'flag'))  # Log flag move
        elif self.board[x][y] == 'F':
            self.board[x][y] = '#'
            self.flags.remove((x, y))
            self.user_moves.append((x+1, y+1, 'unflag'))  # Log unflag move

    def play(self):
        while not self.game_over:
            self.display_board()
            move = input("Enter move (row col action): ").split()
            try:
                x, y, action = int(move[0])-1, int(move[1])-1, move[2]
            except (ValueError, IndexError):
                print("Invalid input. Please enter row, column, and action (o for open, f for flag).")
                continue
            
            if x < 0 or x >= self.size or y < 0 or y >= self.size:
                print("Invalid move. Row and column must be within the board size.")
                continue

            if action == 'o':
                if not self.open_cell(x, y):
                    print("You hit a mine! Game Over.")
                    break
            elif action == 'f':
                self.flag_cell(x, y)
            else:
                print("Invalid action. Use 'o' for open and 'f' for flag.")
                continue

            # Check for win condition (all non-mine cells are opened)
            if self.check_win_condition():
                print("Congratulations, you've won!")
                break

        self.display_final_board()
        self.write_to_file()

    def check_win_condition(self):
        # Check if all non-mine cells are opened
        return all(self.board[x][y] != '#' for x in range(self.size) for y in range(self.size) if (x, y) not in self.mine_positions)

    def display_final_board(self):
        for x, y in self.mine_positions:
            self.board[x][y] = 'M'  # Reveal all mines
        self.display_board()

    def write_to_file(self):
        with open('minesweeper_results.txt', 'w') as f:
            f.write("Final Board:\n")
            for row in self.board:
                f.write(' '.join(row) + '\n')  # Write board state to file
            f.write("\nMoves:\n")
            for move in self.user_moves:
                f.write(f"{move}\n")  # Write user moves to file
        print("Results have been written to 'minesweeper_results.txt'")

if __name__ == "__main__":
    game = Minesweeper()  # Create a Minesweeper game instance
    game.play()  # Start the game
