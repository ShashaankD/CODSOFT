from tkinter import *
import tkinter.messagebox
import random
import os

# Window setup
root = Tk()
root.title('Tic-Tac-Toe')
icon_image=PhotoImage(file=os.path.join(os.path.dirname(__file__),"tic-tac-toe.png"))
root.iconphoto(False,icon_image)
root.resizable(False, False)

click = True
count = 0

# Button variables
btn1 = StringVar()
btn2 = StringVar()
btn3 = StringVar()
btn4 = StringVar()
btn5 = StringVar()
btn6 = StringVar()
btn7 = StringVar()
btn8 = StringVar()
btn9 = StringVar()

xPhoto = PhotoImage(file=os.path.join(os.path.dirname(__file__), "cross.png"))
oPhoto = PhotoImage(file=os.path.join(os.path.dirname(__file__), "round.png"))

# Grid buttons
def start():
    button_grid = [
        (btn1, 0, 0, 1), (btn2, 0, 1, 2), (btn3, 0, 2, 3),
        (btn4, 1, 0, 4), (btn5, 1, 1, 5), (btn6, 1, 2, 6),
        (btn7, 2, 0, 7), (btn8, 2, 1, 8), (btn9, 2, 2, 9)
    ]

    for btn, r, c, num in button_grid:
        Button(root, height=9, width=19, bd=.5, relief='sunken', bg='#ccfff7',
               textvariable=btn, command=lambda n=num, x=r, y=c: press(n, x, y)).grid(row=r, column=c)

# Check for a winner
def check_winner(board):
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    
    for comb in winning_combinations:
        if board[comb[0]] == board[comb[1]] == board[comb[2]] and board[comb[0]] != '':
            return board[comb[0]]  # Returns 'X' or 'O' if there's a winner
    
    return None  # No winner

# Minimax without Alpha-Beta Pruning
def minimax(board, depth, is_ai_turn):
    winner = check_winner(board)
    if winner == "O":
        return 1  # AI wins
    elif winner == "X":
        return -1  # Player wins
    elif "" not in board:
        return 0  # Tie game

    if is_ai_turn:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == '':
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = ''
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == '':
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = ''
                best_score = min(best_score, score)
        return best_score

# MCTS-based move selection
def simulate_game(board, player):
    temp_board = board[:]
    moves = [i for i, x in enumerate(temp_board) if x == '']
    
    while moves:
        move = random.choice(moves)
        temp_board[move] = player
        winner = check_winner(temp_board)
        if winner:
            return 1 if winner == "O" else -1
        player = "X" if player == "O" else "O"
        moves = [i for i, x in enumerate(temp_board) if x == '']

    return 0  # Draw

def mcts(board):
    best_move = None
    best_win_rate = -float("inf")
    
    moves = [i for i, x in enumerate(board) if x == '']
    
    for move in moves:
        wins = 0
        for _ in range(1000):  # Simulate 1000 random games
            board_copy = board[:]
            board_copy[move] = "O"  # AI makes the move
            result = simulate_game(board_copy, "X")  # Simulate the rest of the game
            wins += result

        win_rate = wins / 1000
        if win_rate > best_win_rate:
            best_win_rate = win_rate
            best_move = move

    return best_move

# AI move function choosing between Minimax & MCTS dynamically
def ai_move():
    global count
    board_state = [btn.get() if btn.get() != '' else '' for btn in [btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9]]

    if count < 3:  # Use MCTS for early-game randomization
        best_move = mcts(board_state)
    else:  # Use Minimax for optimal late-game decisions
        best_score = -float("inf")
        best_move = None

        for i in range(9):
            if board_state[i] == '':
                board_state[i] = "O"
                score = minimax(board_state, 0, False,)
                board_state[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i

    if best_move is not None:
        press(best_move + 1, best_move // 3, best_move % 3)

# Handle button press
def press(num, r, c):
    global click, count
    labelPhoto = Label(root, image=xPhoto if click else oPhoto)
    labelPhoto.grid(row=r, column=c)

    eval(f'btn{num}').set('X' if click else 'O')
    count += 1
    click = not click

    checkWin()
    if not click and count < 9:
        ai_move()

# Check winner
def checkWin():
    global count, click

    winner = check_winner([btn1.get(), btn2.get(), btn3.get(), btn4.get(), btn5.get(), btn6.get(), btn7.get(), btn8.get(), btn9.get()])
    if winner == "O":
        tkinter.messagebox.showinfo("Game Result", "O Wins!")
        reset_game()
        return
    elif winner == "X":
        tkinter.messagebox.showinfo("Game Result", "X Wins!")
        reset_game()
        return
    elif count == 9:
        tkinter.messagebox.showinfo("Game Result", "Tie Game!")
        reset_game()

# Reset game
def reset_game():
    global count, click
    count, click = 0, True
    for btn in [btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9]:
        btn.set('')
    start()

start()
root.mainloop()