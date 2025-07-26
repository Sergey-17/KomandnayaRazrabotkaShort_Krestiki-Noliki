import tkinter as tk
import random

BG_COLOR = "#222831"
BTN_COLOR = "#393e46"
BTN_ACTIVE = "#00adb5"
X_COLOR = "#f38181"
O_COLOR = "#fce38a"
LABEL_COLOR = "#eeeeee"

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-Нолики")
        self.root.configure(bg=BG_COLOR)
        self.mode = None
        self.difficulty = None
        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.create_mode_selection()

    def create_mode_selection(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(pady=40)
        label = tk.Label(frame, text="Выберите режим игры", font=("Arial", 18, "bold"), bg=BG_COLOR, fg=LABEL_COLOR)
        label.pack(pady=10)
        btn1 = tk.Button(frame, text="Два игрока", font=("Arial", 16), bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE, width=15, command=lambda: self.start_game("human"))
        btn1.pack(pady=5)
        btn2 = tk.Button(frame, text="С компьютером", font=("Arial", 16), bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE, width=15, command=self.create_difficulty_selection)
        btn2.pack(pady=5)

    def create_difficulty_selection(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(pady=40)
        label = tk.Label(frame, text="Выберите сложность", font=("Arial", 18, "bold"), bg=BG_COLOR, fg=LABEL_COLOR)
        label.pack(pady=10)
        
        difficulties = [
            ("Легкий", "easy"),
            ("Средний", "medium"),
            ("Сложный", "hard")
        ]
        
        for text, diff in difficulties:
            btn = tk.Button(frame, text=text, font=("Arial", 16), bg=BTN_COLOR, fg=LABEL_COLOR, 
                           activebackground=BTN_ACTIVE, width=15,
                           command=lambda d=diff: self.start_game("ai", d))
            btn.pack(pady=5)

    def start_game(self, mode, difficulty=None):
        self.mode = mode
        self.difficulty = difficulty
        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.clear_window()
        self.create_widgets()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack()
        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text="", font=("Arial", 40, "bold"), width=5, height=2,
                                bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE,
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j, padx=3, pady=3)
                self.buttons[i][j] = btn
        
        mode_text = "Режим: " + ("2 игрока" if self.mode == "human" else f"Компьютер ({self.get_difficulty_name()})")
        self.mode_label = tk.Label(self.root, text=mode_text, font=("Arial", 12), bg=BG_COLOR, fg=LABEL_COLOR)
        self.mode_label.pack(pady=5)
        
        self.status_label = tk.Label(self.root, text="Ходит: X", font=("Arial", 16), bg=BG_COLOR, fg=LABEL_COLOR)
        self.status_label.pack(pady=10)
        
        self.restart_button = tk.Button(self.root, text="Перезапустить", font=("Arial", 14), 
                                      bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE, 
                                      command=self.restart)
        self.restart_button.pack(pady=5)
        
        self.menu_button = tk.Button(self.root, text="В меню", font=("Arial", 12), 
                                   bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE, 
                                   command=self.create_mode_selection)
        self.menu_button.pack(pady=5)

    def get_difficulty_name(self):
        names = {
            "easy": "Легкий",
            "medium": "Средний",
            "hard": "Сложный"
        }
        return names.get(self.difficulty, "Неизвестно")

    def on_click(self, row, col):
        if (self.game_over or 
            self.board[row][col] is not None or
            (self.mode == "ai" and self.current_player == "O")):
            return
            
        self.make_move(row, col, self.current_player)
        
        if self.game_over:
            return
            
        if self.mode == "ai" and self.current_player == "O":
            self.disable_buttons()
            self.root.after(400, self.ai_move)

    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.buttons[row][col]["text"] = player
        self.buttons[row][col]["fg"] = X_COLOR if player == "X" else O_COLOR
        
        if self.check_winner(player):
            self.status_label["text"] = f"Победил: {player}!"
            self.game_over = True
            self.highlight_winner(player)
        elif self.is_board_full():
            self.status_label["text"] = "Ничья!"
            self.game_over = True
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label["text"] = f"Ходит: {self.current_player}"

    def ai_move(self):
        if self.game_over:
            return
            
        if self.difficulty == "easy":
            self.easy_ai_move()
        elif self.difficulty == "medium":
            self.medium_ai_move()
        elif self.difficulty == "hard":
            self.hard_ai_move()
            
        if not self.game_over:
            self.enable_buttons()

    def easy_ai_move(self):
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] is None]
        if empty:
            row, col = random.choice(empty)
            self.make_move(row, col, "O")

    def medium_ai_move(self):
        # Попытка выиграть
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    self.board[i][j] = "O"
                    if self.check_winner("O"):
                        self.board[i][j] = None
                        self.make_move(i, j, "O")
                        return
                    self.board[i][j] = None
        
        # Блокировка игрока
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    self.board[i][j] = "X"
                    if self.check_winner("X"):
                        self.board[i][j] = None
                        self.make_move(i, j, "O")
                        return
                    self.board[i][j] = None
        
        # Случайный ход
        self.easy_ai_move()

    def hard_ai_move(self):
        best_score = float('-inf')
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    self.board[i][j] = "O"
                    score = self.minimax(0, False)
                    self.board[i][j] = None
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        if best_move:
            self.make_move(best_move[0], best_move[1], "O")

    def minimax(self, depth, is_maximizing):
        if self.check_winner("O"):
            return 10 - depth
        if self.check_winner("X"):
            return depth - 10
        if self.is_board_full():
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] is None:
                        self.board[i][j] = "O"
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = None
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] is None:
                        self.board[i][j] = "X"
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = None
                        best_score = min(score, best_score)
            return best_score

    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell is None:
                    return False
        return True

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                self.winning_cells = [(i, j) for j in range(3)]
                return True
            if all(self.board[j][i] == player for j in range(3)):
                self.winning_cells = [(j, i) for j in range(3)]
                return True
        if all(self.board[i][i] == player for i in range(3)):
            self.winning_cells = [(i, i) for i in range(3)]
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            self.winning_cells = [(i, 2 - i) for i in range(3)]
            return True
        return False

    def highlight_winner(self, player):
        for i, j in getattr(self, 'winning_cells', []):
            self.buttons[i][j]["bg"] = BTN_ACTIVE

    def disable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state=tk.DISABLED)

    def enable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state=tk.NORMAL)

    def restart(self):
        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False
        
        for i in range(3):
            for j in range(3):
                btn = self.buttons[i][j]
                btn["text"] = ""
                btn["bg"] = BTN_COLOR
                btn["fg"] = LABEL_COLOR
                btn["state"] = tk.NORMAL
                
        self.status_label["text"] = "Ходит: X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()