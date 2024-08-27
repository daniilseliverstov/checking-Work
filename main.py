import time
from tkinter import *
from datetime import datetime

temp = 0
after_id = ''
corr = 0
incorr = 0
start_time = 0
stop_time = 0


def update_grade():
    all_homework = corr + incorr
    if all_homework > 0:
        grade = (corr / all_homework) * 100
        average_time = (stop_time - start_time) / all_homework
    else:
        grade = 0
        average_time = 0
    label_res.configure(text=f"Успеваемость: {grade:.2f}%")
    label_h.configure(text=f"Проверено {all_homework} дз")
    label_time.configure(text=f'В среднем на проверку: {average_time:.2f} сек')


def tick():  # Функция секундомера
    global temp, after_id
    after_id = root.after(1000, tick)
    hour = int(datetime.fromtimestamp(temp).strftime('%H')) - 3
    f_temp = datetime.fromtimestamp(temp).strftime(f'{hour}:%M:%S')  # Формат времени
    label.configure(text=str(f_temp))
    temp += 1


def stop_tick():  # Функция остановки таймера
    global stop_time
    btn_end.forget()  # Убираем кнопку
    btn_correct['state'] = 'disabled'  # деактивация кнопки
    btn_incorrect['state'] = 'disabled'
    root.after_cancel(after_id)
    stop_time = time.time()
    update_grade()


def start_tick():
    global start_time
    btn_start.forget()
    btn_end.pack()
    btn_correct['state'] = 'normal'
    btn_incorrect['state'] = 'normal'
    label_res.pack()
    tick()
    start_time = time.time()


def correct_answer():
    global corr
    corr += 1
    btn_correct.configure(text=f"Зачет ({corr})")
    update_grade()


def incorrect_answer():
    global incorr
    incorr += 1
    btn_incorrect.configure(text=f'Незачет ({incorr})')
    update_grade()


root = Tk()  # создаем корневой объект - окно
root.title("Счетчик ДЗ")  # устанавливаем заголовок окна
root.geometry("350x200")  # устанавливаем размеры окна

icon = PhotoImage(file="icon.png")  # Меняем иконку
root.iconphoto(False, icon)

label = Label(root, font=('Comic Sans MS', 15), text="00:00:00")  # создаем текстовую метку, таймер
label.pack()  # размещаем метку в окне

btn_start = Button(root, font=('Comic Sans MS', 10), text="Начать", width=10, command=start_tick)  # создаем кнопки
btn_start.pack()

btn_end = Button(root, font=('Comic Sans MS', 10), text="Завершить", width=10, command=stop_tick)

btn_correct = Button(root, font=('Comic Sans MS', 10), text=f"Зачет ({corr})", width=10, command=correct_answer)
btn_correct.place(x=20, y=80)
btn_correct['state'] = 'disabled'

btn_incorrect = Button(root, font=('Comic Sans MS', 10), text=f"Незачет ({incorr})", width=10, command=incorrect_answer)
btn_incorrect.place(x=20, y=120)
btn_incorrect['state'] = 'disabled'

label_res = Label(root, font=('Comic Sans MS', 10), text=f"Успеваемость: %")
label_h = Label(root, font=('Comic Sans MS', 10), text=f"Проверено 0 дз")
label_h.place(x=200, y=90)
label_time = Label(root, font=('Comic Sans MS', 10), text=f"В среднем на проверку:")
label_time.place(x=20, y=170)

root.mainloop()
