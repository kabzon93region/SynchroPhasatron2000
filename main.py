from datetime import datetime as dt
from tkinter import filedialog
from pathlib import Path
import tkinter as tk
import shutil
import time
import os


dirList = []
try:
    cfgFile = open("config.cfg", 'r', encoding='Windows-1251')
    for line in cfgFile:
        strLine = line.replace("\n", '')
        dirList.append(strLine)
    cfgFile.close()
except FileNotFoundError:
    cfgFile = open("config.cfg", 'w', encoding='Windows-1251')
    cfgFile.close()




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
    if i <= 5:
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
                font=fontvar, command=lambda: startSync(textarea))
btn3.grid(row=0, column=4, sticky='nwes', columnspan=1, rowspan=2)
#print(btn3.cget('text'))
btn4 = tk.Button(window, text="Настройки", bg=bgcolor, fg=txtcolor, activebackground=actbgcolor, activeforeground=acttxtcolod, font=fontvar, command=lambda: btn4_f())
btn4.grid(row=0, column=3, sticky='nwes', columnspan=1, rowspan=2)
    
def btn4_f():
    btn4.config(state="disabled")
    WCFG()


def btn1_f(ent: tk.Entry, console_area: tk.Text = None):
    ent.delete(0, 'end')
    ent.insert(0, str(Path(filedialog.askdirectory(title="Выберите исходную папку, из которой будет произведена копия(синхронизация)"))))
    now = dt.now().strftime("%H:%M:%S:%f")
    if console_area != None:
        console_area.insert('end', f"\n{now}: Исходная папка выбрана: '{ent.get()}'\nОбъем диска: Общий = {round(shutil.disk_usage(ent.get()).total/1073741824, 2)} GB , Используется = {round(shutil.disk_usage(ent.get()).used/1073741824, 2)} GB , Свободно = {round(shutil.disk_usage(ent.get()).free/1073741824, 2)} GB\n\n")
        console_area.see('end')
        window.update()
    print(f"{now}: Исходная папка выбрана: '{ent.get()}'")  
    



def btn2_f(ent: tk.Entry, console_area: tk.Text = None):
    ent.delete(0, 'end')
    ent.insert(0, str(Path(filedialog.askdirectory(title="Выберите конечную папку, в которую будет произведена копия(синхронизация)"))))
    now = dt.now().strftime("%H:%M:%S:%f")
    if console_area != None:
        console_area.insert('end', f"\n{now}: Конечная папка выбрана: '{ent.get()}'\nОбъем диска: Общий = {round(shutil.disk_usage(ent.get()).total/1073741824, 2)} GB , Используется = {round(shutil.disk_usage(ent.get()).used/1073741824, 2)} GB , Свободно = {round(shutil.disk_usage(ent.get()).free/1073741824, 2)} GB\n\n")
        console_area.see('end')        
        window.update()
    print(f"{now}: Конечная папка выбрана: '{ent.get()}'")


def startSync(console_area: tk.Text):
    start_timer = time.time()  # точка отсчета времени работы программы

    for list in dirList:
        msgList = list.split(" ===>>> ")            
        dir1 = str(msgList[0])
        dir2 = str(msgList[1])
        cff_timer(str(dir1), str(dir2), console_area)

    end_timer = time.time() - start_timer  # собственно время работы программы
    now = dt.now().strftime("%H:%M:%S:%f")
    console_area.insert('end', f"\n{now}: Синхронизация списка завершена за {end_timer} секунд\n")
    console_area.see('end')
    window.update()
    print(f"{now}: Синхронизация списка завершена за {end_timer} секунд")
    

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


def WCFG():
    windowCFG = window = tk.Toplevel() #tk.Tk()
    windowCFG.protocol("WM_DELETE_WINDOW", lambda: cencelWCFG(windowCFG))
    windowCFG.title("Новое окно")
    xw = 865  # задаем ширину окна
    yw = 420  # задаем высоту окна
    xspos = (windowCFG.winfo_screenwidth() - xw) / 2  # рассчитываем отступ по ширине для создания окна на экране по центру
    yspos = (windowCFG.winfo_screenheight() - yw) / 2  # рассчитываем отступ по высоте для создания окна на экране по центру
    windowCFG.geometry("%dx%d+%d+%d" % (xw, yw, xspos, yspos))  # задаем ширину, высоту окна и отступы по ширине и высоте для создания окна
    #windowCFG.resizable(False, False)  # задаем возможность изменять размер окна по ширине, высоте
    windowCFG.config(bg=bgcolor)  # задаем цвет фона в hex формате
    windowCFG.grab_set() 

    for i in range(14):
        windowCFG.grid_rowconfigure(i, minsize=30)
        if i <= 8:
            windowCFG.grid_columnconfigure(i, minsize=100)

    entc1 = tk.Entry(windowCFG)
    entc1.grid(row=0, column=0, columnspan=6, rowspan=1, sticky='nwes')
    entc2 = tk.Entry(windowCFG)
    entc2.grid(row=1, column=0, columnspan=6, rowspan=1, sticky='nwes')


    wcfgBtn1=tk.Button(windowCFG, text="OK", bg=bgcolor, fg=txtcolor, activebackground=actbgcolor,
                        activeforeground=acttxtcolod, font=fontvar, command=lambda: okWCFG(windowCFG, dir_lb))
    wcfgBtn1.grid(row=0, column=7, columnspan=1, rowspan=1, sticky='nwes')
    wcfgBtn2=tk.Button(windowCFG, text="Отмена", bg=bgcolor, fg=txtcolor, activebackground=actbgcolor,
                        activeforeground=acttxtcolod, font=fontvar, command=lambda: cencelWCFG(windowCFG))
    wcfgBtn2.grid(row=1, column=7, columnspan=1, rowspan=1, sticky='nwes')

    wcfgBtn3=tk.Button(windowCFG, text="Выбрать исходную папку", bg=bgcolor, fg=txtcolor, activebackground=actbgcolor,
                        activeforeground=acttxtcolod, font=fontvar, command=lambda: btn1_f(entc1))
    wcfgBtn3.grid(row=0, column=6, columnspan=1, rowspan=1, sticky='nwes')
    wcfgBtn4=tk.Button(windowCFG, text="Выбрать конечную папку", bg=bgcolor, fg=txtcolor, activebackground=actbgcolor,
                        activeforeground=acttxtcolod, font=fontvar, command=lambda: btn2_f(entc2))
    wcfgBtn4.grid(row=1, column=6, columnspan=1, rowspan=1, sticky='nwes')

    wcfgBtn3=tk.Button(windowCFG, text="Редактировать", bg=bgcolor, fg=txtcolor, activebackground=actbgcolor,
                        activeforeground=acttxtcolod, font=fontvar, command=lambda: selItem(dir_lb))
    wcfgBtn3.grid(row=2, column=0, columnspan=2, rowspan=1, sticky='nwes')
    wcfgBtn3=tk.Button(windowCFG, text="Сохранить", bg=bgcolor, fg=txtcolor, activebackground=actbgcolor,
                        activeforeground=acttxtcolod, font=fontvar, command=lambda: saveItem(dir_lb))
    wcfgBtn3.grid(row=2, column=2, columnspan=2, rowspan=1, sticky='nwes')
    wcfgBtn4=tk.Button(windowCFG, text="Удалить", bg=bgcolor, fg=txtcolor, activebackground=actbgcolor,
                        activeforeground=acttxtcolod, font=fontvar, command=lambda: deleteItem(dir_lb))
    wcfgBtn4.grid(row=2, column=4, columnspan=2, rowspan=1, sticky='nwes')

    dir_lb = tk.Listbox(windowCFG, bg=bgcolor, fg=txtcolor, selectbackground=actbgcolor, selectforeground=acttxtcolod, font=fontvar)
    dir_lb.grid(row=3, column=0, sticky='nwes', columnspan=8, rowspan=12)

    for line in dirList:
        dir_lb.insert('end', line)


    def selItem(ListBox: tk.Listbox = None):
        selected_indices= ListBox.curselection()
        if len(selected_indices) > 0:
            selected_langs = ",".join([ListBox.get(i) for i in selected_indices])
            msg = selected_langs
            msg = str(msg)
            msgList = msg.split(" ===>>> ")            
            entc1.delete(0, 'end')
            entc1.insert(0, str(msgList[0]))
            entc2.delete(0, 'end')
            entc2.insert(0, str(msgList[1]))
        else:
            tk.messagebox.showinfo("Информационное сообщение", "Не выбран в списке элемент для редактирования.") #, command=open_info)
    
    def saveItem(ListBox: tk.Listbox = None):
        if len(entc1.get()) > 0 and len(entc2.get()) > 0 :
            selected_indices: str = str(ListBox.curselection())
            if len(selected_indices) > 2:
                disallowed_characters = "(,) "
                for character in disallowed_characters:
                    selected_indices = selected_indices.replace(character, "")
                selected_indices = int(selected_indices)
                msgList = f"{entc1.get()} ===>>> {entc2.get()}"
                dir_lb.delete(selected_indices, selected_indices)
                dir_lb.insert(selected_indices, msgList)
            else:
                msgList = f"{entc1.get()} ===>>> {entc2.get()}"
                dir_lb.insert('end', msgList)
        else:
            tk.messagebox.showinfo("Информационное сообщение", "Не заполнены поля путей папок для сохранения в список.") #, command=open_info)

    def deleteItem(ListBox: tk.Listbox = None):
        selected_indices: str = str(ListBox.curselection())
        if len(selected_indices) > 2:
            disallowed_characters = "(,) "
            for character in disallowed_characters:
                selected_indices = selected_indices.replace(character, "")
            selected_indices = int(selected_indices)
            dir_lb.delete(selected_indices, selected_indices)
        else:
            tk.messagebox.showinfo("Информационное сообщение", "Не выбран элемент списка для удаления.") #, command=open_info)


    def okWCFG(W: tk.Tk, dirlb: tk.Listbox):
        dirList.clear()
        for x in dirlb.get(0, 'end'):
            dirList.append(x)

        cfgFile = open("config.cfg", 'w', encoding='Windows-1251')
        for line in dirList:
            cfgFile.write(f"{line}\n")
        cfgFile.close()

        try:
            btn4.config(state="normal")
        except:
            print("error: no found window as tk.Tk()")
        finally:
            W.grab_release()
            W.destroy() 


def cencelWCFG(W: tk.Tk):
    try:
        btn4.config(state="normal")
    except:
        print("error: no found window as tk.Tk()")
    finally:                
        W.grab_release()
        W.destroy() 









window.mainloop()
