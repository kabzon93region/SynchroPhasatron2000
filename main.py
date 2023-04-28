from datetime import datetime as dt
from tkinter import filedialog
from pathlib import Path
import tkinter as tk
import shutil
import time
import os



# задаем пути к папкам 1 и 2
window = tk.Tk()
bgcolor = '#1E1F22'
actbgcolor = '#575A63'
txtcolor = '#B8BAC0'
acttxtcolod = '#15161A'
title_str = "Синхрофазатрон 2000"
#icon_str = "main.ico"
fontvar = ('Consolas', 10)
xw = 640  # задаем ширину окна
yw = 300  # задаем высоту окна
xspos = (window.winfo_screenwidth() - xw) / 2  # рассчитываем отступ по ширине для создания окна на экране по центру
yspos = (window.winfo_screenheight() - yw) / 2  # рассчитываем отступ по высоте для создания окна на экране по центру

window.title(title_str)  # задаем название окна
window.geometry("%dx%d+%d+%d" % (xw, yw, xspos, yspos))  # задаем ширину, высоту окна и отступы по ширине и высоте для создания окна
window.resizable(False, False)  # задаем возможность изменять размер окна по ширине, высоте
#window.iconbitmap(icon_str)  # задаем иконку окна
window.config(bg=bgcolor)  # задаем цвет фона в hex формате

for i in range(5):
    window.grid_rowconfigure(i, minsize=60)
    window.grid_columnconfigure(i, minsize=128)

ent1 = tk.Entry(window)
ent2 = tk.Entry(window)

textarea = tk.Text(window, bg=bgcolor, fg=txtcolor, font=fontvar, height=1)
textarea.grid(row=2, column=0, sticky='nwes', columnspan=5, rowspan=3)

btn1 = tk.Button(window, text="Выбрать исходную папку", bg=bgcolor, fg=txtcolor, activebackground=actbgcolor, activeforeground=acttxtcolod, font=fontvar, command=lambda: btn1_f(ent1, textarea))
btn1.grid(row=0, column=0, sticky='nwes', columnspan=3)
btn2 = tk.Button(window, text="Выбрать конечную папку", bg=bgcolor, fg=txtcolor, activebackground=actbgcolor, activeforeground=acttxtcolod, font=fontvar, command=lambda: btn2_f(ent2, textarea))
btn2.grid(row=1, column=0, sticky='nwes', columnspan=3)
btn3 = tk.Button(window, text="Старт", bg=bgcolor, fg=txtcolor, activebackground=actbgcolor, activeforeground=acttxtcolod,
                font=fontvar, command=lambda: cff_timer(str(ent1.get()), str(ent2.get()), textarea))
btn3.grid(row=0, column=3, sticky='nwes', columnspan=2, rowspan=2)
print(btn3.cget('text'))
def btn1_f(ent: tk.Entry, console_area: tk.Text):
    ent.delete(0, 'end')
    ent.insert(0, str(Path(filedialog.askdirectory(title="Выберите исходную папку, из которой будет произведена копия(синхронизация)"))))
    now = dt.now().strftime("%H:%M:%S:%f")
    console_area.insert('end', f"\n{now}: Исходная папка выбрана: '{ent.get()}'\nОбъем диска: Общий = {round(shutil.disk_usage(ent.get()).total/1073741824, 2)} GB , Используется = {round(shutil.disk_usage(ent.get()).used/1073741824, 2)} GB , Свободно = {round(shutil.disk_usage(ent.get()).free/1073741824, 2)} GB\n\n")
    console_area.see('end')
    window.update()
    print(f"{now}: Исходная папка выбрана: '{ent.get()}'")  
    



def btn2_f(ent: tk.Entry, console_area: tk.Text):
    ent.delete(0, 'end')
    ent.insert(0, str(Path(filedialog.askdirectory(title="Выберите конечную папку, в которую будет произведена копия(синхронизация)"))))
    now = dt.now().strftime("%H:%M:%S:%f")
    console_area.insert('end', f"\n{now}: Конечная папка выбрана: '{ent.get()}'\nОбъем диска: Общий = {round(shutil.disk_usage(ent.get()).total/1073741824, 2)} GB , Используется = {round(shutil.disk_usage(ent.get()).used/1073741824, 2)} GB , Свободно = {round(shutil.disk_usage(ent.get()).free/1073741824, 2)} GB\n\n")
    console_area.see('end')
    window.update()
    print(f"{now}: Конечная папка выбрана: '{ent.get()}'")


def copy_files(source_folder=None, dest_folder=None, console_area: tk.Text = None):  # рекурсивная функция для копирования файлов
    if len(source_folder) <= 3 or len(dest_folder) <= 3:
        now = dt.now().strftime("%H:%M:%S:%f")
        console_area.insert('end', f"\n{now}: !ОШИБКА! : Не заданы пути папок для синхронизации\n")
        console_area.see('end')
        window.update()
        print(f"{now}: !ОШИБКА! : Не заданы пути папок для синхронизации")
        btn3.config(state="normal")
    else:
        for root, dirs, files in os.walk(source_folder):  # проходимся по всем файлам и подпапкам внутри source_folder для каждого файла в папке
            if(btn3.cget('text') == "Старт"):
                    break
            for filename in files:
                if(btn3.cget('text') == "Старт"):
                    break
                source_path = os.path.join(root, filename)  # получаем полный путь к файлу
                #now = dt.now().strftime("%H:%M:%S:%f")
                #print(f"{now}: source_path={source_path}")

                relative_path = os.path.relpath(source_path, source_folder)  # очищаем имя файла от пути к нему
                #now = dt.now().strftime("%H:%M:%S:%f")
                #print(f"{now}: relative_path={relative_path}")

                dest_path = os.path.join(dest_folder, relative_path)  # получаем путь к файлу в папке 2, сохраняя структуру папок
                #now = dt.now().strftime("%H:%M:%S:%f")
                #print(f"{now}: dest_path={dest_path}")

                dest_dir = os.path.dirname(dest_path)  # получаем путь к папке 2 к исходному файлу из папки 1
                #now = dt.now().strftime("%H:%M:%S:%f")
                #print(f"{now}: dest_dir={dest_dir}")

                if not os.path.exists(dest_dir):  # если папки для файла в папке 2 не существует, создаем ее
                    os.makedirs(dest_dir)
                    now = dt.now().strftime("%H:%M:%S:%f")
                    console_area.insert('end', f"\n{now}: Создана папка: '{dest_dir}'\n")
                    console_area.see('end')
                    window.update()
                    print(f"{now}: Создана папка: '{dest_dir}'")

                if os.path.exists(dest_path):  # если файл существует в папке 2, проверяем, нужно ли его заменить
                    source_stat = os.stat(source_path)  # получаем статы файла из папки 1
                    #now = dt.now().strftime("%H:%M:%S:%f")
                    #print(f"{now}: source_stat={source_stat}")

                    dest_stat = os.stat(dest_path)  # получаем статы файла из папки 2
                    #now = dt.now().strftime("%H:%M:%S:%f")
                    #print(f"{now}: dest_stat={dest_stat}")

                    if source_stat.st_mtime > dest_stat.st_mtime and source_stat.st_size >= dest_stat.st_size:  # сравниваем дату изменения и размер файлов
                        shutil.copy2(source_path, dest_path)  # копируем файл из папки 1 в папку 2 с заменой если первый новее или больше
                        now = dt.now().strftime("%H:%M:%S:%f")
                        console_area.insert('end', f"\n{now}: Файл '{source_path}' скопирован в '{dest_path}' с заменой, т.к. новее\n")
                        console_area.see('end')
                        window.update()
                        print(f"{now}: Файл '{source_path}' скопирован в '{dest_path}' с заменой, т.к. новее")
                        # os.remove(source_path)  # удаляем скопированный файл из папки 1

                    elif source_stat.st_mtime >= dest_stat.st_mtime and source_stat.st_size > dest_stat.st_size:  # сравниваем дату изменения и размер файлов
                        shutil.copy2(source_path, dest_path)  # копируем файл из папки 1 в папку 2 с заменой если первый новее или больше
                        now = dt.now().strftime("%H:%M:%S:%f")
                        console_area.insert('end', f"\n{now}: Файл '{source_path}' скопирован в '{dest_path}' с заменой, т.к. больше\n")
                        console_area.see('end')
                        window.update()
                        print(f"{now}: Файл '{source_path}' скопирован в '{dest_path}' с заменой, т.к. больше")
                        # os.remove(source_path)  # удаляем скопированный файл из папки 1

                    elif source_stat.st_mtime <= dest_stat.st_mtime and source_stat.st_size < dest_stat.st_size:
                        # os.remove(source_path)  # удаляем не скопированный файл из папки 1
                        now = dt.now().strftime("%H:%M:%S:%f")
                        console_area.insert('end', f"\n{now}: Файл '{source_path}' удален, т.к. меньше и не новее\n")
                        console_area.see('end')
                        window.update()
                        print(f"{now}: Файл '{source_path}' удален, т.к. меньше и не новее")

                    elif source_stat.st_mtime < dest_stat.st_mtime and source_stat.st_size <= dest_stat.st_size:
                        # os.remove(source_path)  # удаляем не скопированный файл из папки 1
                        now = dt.now().strftime("%H:%M:%S:%f")
                        console_area.insert('end', f"\n{now}: Файл '{source_path}' удален, т.к. старее и не больше\n")
                        console_area.see('end')
                        window.update()
                        print(f"{now}: Файл '{source_path}' удален, т.к. старее и не больше")

                else:  # если файла в папке 2 вообще нет
                    shutil.copy2(source_path, dest_path)  # копируем его туда
                    now = dt.now().strftime("%H:%M:%S:%f")
                    console_area.insert('end', f"\n{now}: Файл '{source_path}' скопирован в '{dest_path}'\n")
                    console_area.see('end')
                    window.update()
                    print(f"{now}: Файл '{source_path}' скопирован в '{dest_path}'")
                    # os.remove(source_path)  # удаляем скопированный файл из папки 1

            for dirname in dirs:  # для каждой подпапки в source_folder рекурсивно вызываем эту же функцию
                source_path = os.path.join(root, dirname)  # получаем полный путь к файлу
                #now = dt.now().strftime("%H:%M:%S:%f")
                #print(f"{now}: source_path={source_path}")

                relative_path = os.path.relpath(source_path, source_folder)  # очищаем имя файла от пути к нему
                #now = dt.now().strftime("%H:%M:%S:%f")
                #print(f"{now}: relative_path={relative_path}")

                dest_path = os.path.join(dest_folder, relative_path)  # получаем путь к файлу в папке 2, сохраняя структуру папок
                #now = dt.now().strftime("%H:%M:%S:%f")
                #print(f"{now}: dest_path={dest_path}")

                copy_files(source_path, dest_path, console_area)
        # for
    # if none
# def copy_files


def cff_timer(source_folder, dest_folder, console_area: tk.Text):
    if(btn3.cget('text')=="Старт"):
        #btn3.config(state="disabled")
        start_time = time.time()  # точка отсчета времени работы программы

        btn3.config(text="Стоп")        

        copy_files(source_folder, dest_folder, console_area)

        btn3.config(text="Старт")

        end_time = time.time() - start_time  # собственно время работы программы
        now = dt.now().strftime("%H:%M:%S:%f")
        console_area.insert('end', f"\n{now}: Синхронизация завершена за {end_time} секунд\n")
        console_area.see('end')
        window.update()
        print(f"{now}: Синхронизация завершена за {end_time} секунд")
        #btn3.config(state="normal")
    else:
        btn3.config(text="Старт")

window.mainloop()
