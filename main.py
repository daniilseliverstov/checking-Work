import tkinter as tk
import time
import datetime
import sqlite3
from results_window import ResultsWindow


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Счетчик ДЗ')
        self.root.geometry("350x180")

        # Таймер
        self.time_label = tk.Label(root, text='00:00:00', font=('Comic Sans MS', 10))
        self.time_label.pack()

        self.start_button = tk.Button(root, font=('Comic Sans MS', 10), text='Начать',
                                      width=10, command=self.start_timer)
        self.start_button.pack()

        self.pause_button = tk.Button(root, text='Пауза', font=('Comic Sans MS', 10),
                                      width=10, command=self.pause_timer)

        self.stop_button = tk.Button(root, text='Завершить', font=('Comic Sans MS', 10),
                                     width=10, command=self.stop_timer)
        self.results_button = tk.Button(root, text="Результаты", font=('Comic Sans MS', 10),
                                        command=self.open_results_window,)
        self.results_button.place(x=150, y=105)

        # Проверка заданий
        self.correct_button = tk.Button(root, text=f'Верно', width=10, background='#00FF7F', command=self.correct_answer)
        self.correct_button.place(x=20, y=80)
        self.correct_button['state'] = 'disabled'

        self.incorrect_button = tk.Button(root, text='Неверно', width=10, background='#FF4500',
                                          command=self.incorrect_answer)
        self.incorrect_button.place(x=20, y=120)
        self.incorrect_button['state'] = 'disabled'

        self.undo_button = tk.Button(root, text='Мисклик', width=10, command=self.undo_action)
        self.undo_button.place(x=250, y=80)
        self.undo_button['state'] = 'disabled'

        # Статистика
        self.result_label = tk.Label(root, text='Проверено: 0, Успеваемость: 0.0%', font=('Comic Sans MS', 10))
        self.result_label.pack()
        self.midl_time = tk.Label(root, text='В среднем на проверку: 00:00:00', font=('Comic Sans MS', 10))
        self.midl_time.place(x=40, y=150)

        # Инициализация
        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.total_checked = 0
        self.correct_checked = 0
        self.incorrect_checked = 0
        self.last_action = None
        self.now = datetime.datetime.now()

        self.conn = sqlite3.connect("results.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        start_time TEXT NOT NULL,
                        elapsed_time TEXT NOT NULL,
                        total_checked INTEGER NOT NULL,
                        success_rate REAL NOT NULL
                    )
                """)
        self.conn.commit()

    def save_result(self):
        start_time = self.now.strftime("%Y-%m-%d %H:%M:%S")
        elapsed_time = self.time_label.cget("text")
        total_checked = self.total_checked
        success_rate = (self.correct_checked / self.total_checked) * 100 if self.total_checked > 0 else 0.0

        self.cursor.execute("""
            INSERT INTO results (start_time, elapsed_time, total_checked, success_rate)
            VALUES (?, ?, ?, ?)
        """, (start_time, elapsed_time, total_checked, success_rate))
        self.conn.commit()

    def update_time(self):
        if self.running:
            current_time = time.time()
            elapsed = self.elapsed_time + (current_time - self.start_time)
            self.elapsed_time = elapsed
            self.start_time = current_time

            hours, remainder = divmod(int(elapsed), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

            if self.total_checked > 0:
                avg_seconds = self.elapsed_time / self.total_checked
                avg_hours, avg_remainder = divmod(int(avg_seconds), 3600)
                avg_minutes, avg_seconds = divmod(avg_remainder, 60)
                self.midl_time.config(text=f"В среднем на проверку: {avg_hours:02}:{avg_minutes:02}:{avg_seconds:02}")

            self.root.after(1000, self.update_time)

    def start_timer(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.correct_button['state'] = 'normal'
            self.incorrect_button['state'] = 'normal'
            self.undo_button['state'] = 'normal'
            self.stop_button.place(x=250, y=120)
            self.pause_button.pack()
            self.update_time()
            self.start_button.forget()

    def pause_timer(self):
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.running = False
            self.correct_button['state'] = 'disabled'
            self.incorrect_button['state'] = 'disabled'
            self.start_button.pack()
            self.pause_button.forget()
            self.start_button.configure(text='Продолжить')

    def stop_timer(self):
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.running = False
        self.correct_button['state'] = 'disabled'
        self.incorrect_button['state'] = 'disabled'
        self.undo_button['state'] = 'disabled'
        self.start_button.forget()
        self.pause_button.forget()
        self.stop_button.forget()
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.running = False
        self.save_result()

    def correct_answer(self):
        self.total_checked += 1
        self.correct_checked += 1
        self.correct_button.configure(text=f'Верно: {self.correct_checked}')
        self.last_action = 'correct'
        self.update_results()

    def incorrect_answer(self):
        self.total_checked += 1
        self.incorrect_checked += 1
        self.incorrect_button.configure(text=f'Неверно: {self.incorrect_checked}')
        self.last_action = 'incorrect'
        self.update_results()

    def undo_action(self):
        if self.last_action == 'correct' and self.correct_checked > 0:
            self.total_checked -= 1
            self.correct_checked -= 1
            self.correct_button.configure(text=f'Верно: {self.correct_checked}')
        elif self.last_action == 'incorrect' and self.incorrect_checked > 0:
            self.total_checked -= 1
            self.incorrect_checked -= 1
            self.incorrect_button.configure(text=f'Неверно: {self.incorrect_checked}')
        self.last_action = None
        self.update_results()

    def update_results(self):
        if self.total_checked > 0:
            percentage = (self.correct_checked / self.total_checked) * 100
        else:
            percentage = 0.0

        self.result_label.config(
            text=f'Проверено: {self.total_checked}, Успеваемость: {percentage:.1f}%'
        )

    def open_results_window(self):
        results_window = tk.Toplevel(self.root)
        ResultsWindow(results_window, "results.db")


if __name__ == "__main__":
    root = tk.Tk()
    # Меняем иконку
    icon = tk.PhotoImage(file="icon.png")
    root.iconphoto(False, icon)

    app = TimerApp(root)

    root.attributes("-topmost", True)
    root.mainloop()
    app.conn.close()
