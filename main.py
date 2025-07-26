import tkinter as tk
import random

# Цвета для современного оформления
BG_COLOR = "#222831"         # Цвет фона окна
BTN_COLOR = "#393e46"       # Цвет кнопок
BTN_ACTIVE = "#00adb5"      # Цвет активной кнопки/выигрышной линии
X_COLOR = "#f38181"         # Цвет крестика
O_COLOR = "#fce38a"         # Цвет нолика
LABEL_COLOR = "#eeeeee"     # Цвет текста

class TicTacToe:
    """
    Класс реализует игру Крестики-Нолики с графическим интерфейсом на tkinter.
    Поддерживаются два режима: два игрока и игра против компьютера с выбором сложности.
    """
    def __init__(self, root):
        """
        Инициализация главного окна и стартового состояния игры.
        """
        self.root = root
        self.root.title("Крестики-Нолики")
        self.root.configure(bg=BG_COLOR)
        self.mode = None  # Режим игры: 'human' или 'ai'
        self.ai_level = None  # Уровень сложности: 'easy' или 'hard'
        self.current_player = "X"  # Текущий игрок
        self.board = [[None for _ in range(3)] for _ in range(3)]  # Игровое поле
        self.buttons = [[None for _ in range(3)] for _ in range(3)]  # Кнопки поля
        self.game_over = False  # Флаг окончания игры
        self.create_mode_selection()  # Показываем меню выбора режима

    def create_mode_selection(self):
        """
        Отображает меню выбора режима игры.
        """
        self.clear_window()
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(pady=40)
        label = tk.Label(frame, text="Выберите режим игры", font=("Arial", 18, "bold"), bg=BG_COLOR, fg=LABEL_COLOR)
        label.pack(pady=10)
        # Кнопка для режима "два игрока"
        btn1 = tk.Button(frame, text="Два игрока", font=("Arial", 16), bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE, width=15, command=lambda: self.start_game("human"))
        btn1.pack(pady=5)
        # Кнопка для режима "с компьютером" (открывает выбор сложности)
        btn2 = tk.Button(frame, text="С компьютером", font=("Arial", 16), bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE, width=15, command=self.create_ai_level_selection)
        btn2.pack(pady=5)

    def create_ai_level_selection(self):
        """
        Отображает меню выбора уровня сложности для игры с компьютером.
        """
        self.clear_window()
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(pady=40)
        label = tk.Label(frame, text="Выберите уровень сложности", font=("Arial", 18, "bold"), bg=BG_COLOR, fg=LABEL_COLOR)
        label.pack(pady=10)
        btn_easy = tk.Button(frame, text="Лёгкий", font=("Arial", 16), bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE, width=15, command=lambda: self.start_ai_game("easy"))
        btn_easy.pack(pady=5)
        btn_hard = tk.Button(frame, text="Сложный", font=("Arial", 16), bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE, width=15, command=lambda: self.start_ai_game("hard"))
        btn_hard.pack(pady=5)
        btn_back = tk.Button(frame, text="Назад", font=("Arial", 12), bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE, width=10, command=self.create_mode_selection)
        btn_back.pack(pady=10)

    def start_ai_game(self, level):
        """
        Запускает игру против компьютера с выбранным уровнем сложности.
        """
        self.ai_level = level
        self.start_game("ai")

    def start_game(self, mode):
        """
        Запускает игру в выбранном режиме.
        :param mode: 'human' или 'ai'
        """
        self.mode = mode
        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.clear_window()
        self.create_widgets()

    def clear_window(self):
        """
        Очищает все виджеты из главного окна.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):
        """
        Создаёт игровое поле, статус и кнопки управления.
        """
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack()
        for i in range(3):
            for j in range(3):
                # Создаём кнопку для каждой клетки поля
                btn = tk.Button(frame, text="", font=("Arial", 40, "bold"), width=5, height=2,
                                bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE,
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j, padx=3, pady=3)
                self.buttons[i][j] = btn
        # Статус текущего игрока
        self.status_label = tk.Label(self.root, text="Ходит: X", font=("Arial", 16), bg=BG_COLOR, fg=LABEL_COLOR)
        self.status_label.pack(pady=10)
        # Кнопка перезапуска
        self.restart_button = tk.Button(self.root, text="Перезапустить", font=("Arial", 14), bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE, command=self.restart)
        self.restart_button.pack(pady=5)
        # Кнопка возврата в меню
        self.menu_button = tk.Button(self.root, text="В меню", font=("Arial", 12), bg=BTN_COLOR, fg=LABEL_COLOR, activebackground=BTN_ACTIVE, command=self.create_mode_selection)
        self.menu_button.pack(pady=5)

    def on_click(self, row, col):
        """
        Обрабатывает нажатие на клетку поля.
        :param row: строка
        :param col: столбец
        """
        if self.game_over or self.board[row][col] is not None:
            return  # Игнорируем, если игра окончена или клетка занята
        self.make_move(row, col, self.current_player)
        if self.game_over:
            return
        # Если режим с компьютером и сейчас ход O, запускаем AI
        if self.mode == "ai" and self.current_player == "O":
            self.root.after(400, self.ai_move)

    def make_move(self, row, col, player):
        """
        Делает ход игрока и обновляет интерфейс.
        :param row: строка
        :param col: столбец
        :param player: 'X' или 'O'
        """
        self.board[row][col] = player
        self.buttons[row][col]["text"] = player
        self.buttons[row][col]["fg"] = X_COLOR if player == "X" else O_COLOR
        if self.check_winner(player):
            self.status_label["text"] = f"Победил: {player}!"
            self.game_over = True
            self.highlight_winner(player)
        elif all(all(cell is not None for cell in row) for row in self.board):
            self.status_label["text"] = "Ничья!"
            self.game_over = True
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label["text"] = f"Ходит: {self.current_player}"

    def ai_move(self):
        """
        Делает ход компьютера в зависимости от выбранного уровня сложности.
        """
        if self.game_over:
            return
        if self.ai_level == "hard":
            move = self.find_best_move()
            if move:
                row, col = move
            else:
                empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] is None]
                row, col = random.choice(empty)
        else:
            empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] is None]
            row, col = random.choice(empty)
        self.make_move(row, col, "O")

    def find_best_move(self):
        """
        Находит лучший ход для компьютера (выиграть или заблокировать игрока).
        :return: (row, col) или None
        """
        # 1. Попробовать выиграть
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    self.board[i][j] = "O"
                    if self.check_winner("O"):
                        self.board[i][j] = None
                        return (i, j)
                    self.board[i][j] = None
        # 2. Заблокировать игрока
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    self.board[i][j] = "X"
                    if self.check_winner("X"):
                        self.board[i][j] = None
                        return (i, j)
                    self.board[i][j] = None
        # 3. Нет критических ходов
        return None

    def check_winner(self, player):
        """
        Проверяет, выиграл ли указанный игрок.
        :param player: 'X' или 'O'
        :return: True, если есть победа
        """
        for i in range(3):
            # Проверка строк
            if all(self.board[i][j] == player for j in range(3)):
                self.winning_cells = [(i, j) for j in range(3)]
                return True
            # Проверка столбцов
            if all(self.board[j][i] == player for j in range(3)):
                self.winning_cells = [(j, i) for j in range(3)]
                return True
        # Проверка главной диагонали
        if all(self.board[i][i] == player for i in range(3)):
            self.winning_cells = [(i, i) for i in range(3)]
            return True
        # Проверка побочной диагонали
        if all(self.board[i][2 - i] == player for i in range(3)):
            self.winning_cells = [(i, 2 - i) for i in range(3)]
            return True
        return False

    def highlight_winner(self, player):
        """
        Подсвечивает выигрышную линию.
        """
        for i, j in getattr(self, 'winning_cells', []):
            self.buttons[i][j]["bg"] = BTN_ACTIVE

    def restart(self):
        """
        Перезапускает игру, очищая поле и сбрасывая статус.
        """
        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False
        for i in range(3):
            for j in range(3):
                btn = self.buttons[i][j]
                btn["text"] = ""
                btn["bg"] = BTN_COLOR
                btn["fg"] = LABEL_COLOR
        self.status_label["text"] = "Ходит: X"

if __name__ == "__main__":
    # Точка входа: создаём окно и запускаем игру
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
