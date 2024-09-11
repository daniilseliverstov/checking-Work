import tkinter as tk
import time


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Счетчик ДЗ')
        self.root.geometry("350x150")

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

        # Проверка заданий
        self.correct_button = tk.Button(root, text=f'Верно', width=10, command=self.correct_answer)
        self.correct_button.place(x=20, y=80)
        self.correct_button['state'] = 'disabled'

        self.incorrect_button = tk.Button(root, text='Неверно', width=10, command=self.incorrect_answer)
        self.incorrect_button.place(x=20, y=120)
        self.incorrect_button['state'] = 'disabled'

        # Статистика
        self.result_label = tk.Label(root, text='Проверено: 0, Успеваемость: 0.0%', font=('Comic Sans MS', 10))
        self.result_label.pack()
        self.midl_time = tk.Label(root, text='В среднем на проверку: ')
        self.midl_time.pack()

        # Инициализация
        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.total_checked = 0
        self.correct_checked = 0
        self.incorrect_checked = 0

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
                self.midl_time.config(text=f"{hours / self.total_checked}:{minutes / self.total_checked}:{seconds / self.total_checked}")

            self.root.after(1000, self.update_time)

    def start_timer(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.correct_button['state'] = 'normal'
            self.incorrect_button['state'] = 'normal'
            self.stop_button.place(x=250, y=110)
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
        self.start_button.forget()
        self.pause_button.forget()
        self.stop_button.forget()

    def correct_answer(self):
        self.total_checked += 1
        self.correct_checked += 1
        self.correct_button.configure(text=f'Верно: {self.correct_checked}')
        self.update_results()

    def incorrect_answer(self):
        self.total_checked += 1
        self.incorrect_checked += 1
        self.incorrect_button.configure(text=f'Неверно: {self.incorrect_checked}')
        self.update_results()

    def update_results(self):
        if self.total_checked > 0:
            percentage = (self.correct_checked / self.total_checked) * 100
        else:
            percentage = 0.0

        self.result_label.config(
            text=f'Проверено: {self.total_checked}, Успеваемость: {percentage:.1f}%'
        )


if __name__ == "__main__":
    root = tk.Tk()
    # Меняем иконку
    icon = tk.PhotoImage(file="icon.png")
    root.iconphoto(False, icon)

    app = TimerApp(root)

    root.attributes("-topmost", True)
    root.mainloop()
