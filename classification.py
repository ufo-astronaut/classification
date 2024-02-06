import os
import shutil
import tkinter
from tkinter import filedialog, Label, Button, PhotoImage

# 파일과 폴더 처리 기능
def fileList(path_before: str) -> list:
    file_list = os.listdir(path_before)
    category = [file.split("_")[1] for file in file_list if "_" in file]
    return list(set(category))

def makeFolder(path_after: str, file_list: list):
    for file in file_list:
        try:
            os.makedirs(os.path.join(path_after, file))
        except FileExistsError:
            pass

def moveFile(path_before, path_after, file_list):
    for file in file_list:
        category = file.split("_")[1] if "_" in file else "기타"
        shutil.move(os.path.join(path_before, file), os.path.join(path_after, category))

# tkinter GUI
def select_source_folder():
    dirName = filedialog.askdirectory()
    if dirName:
        source_folder_var.set(dirName)

def select_target_folder():
    dirName = filedialog.askdirectory()
    if dirName:
        target_folder_var.set(dirName)

def classify_files():
    path_before = source_folder_var.get()
    path_after = target_folder_var.get()
    if path_before and path_after:
        file_list = fileList(path_before)
        makeFolder(path_after, file_list)
        moveFile(path_before, path_after, os.listdir(path_before))
        tkinter.messagebox.showinfo("완료", "파일 분류가 완료되었습니다.")

window = tkinter.Tk()
window.title("이미지 분류 프로그램")
window.geometry("640x400+100+100")
window.resizable(False, False)

source_folder_var = tkinter.StringVar()
target_folder_var = tkinter.StringVar()

tkinter.Label(window, text="원본 폴더:").pack()
tkinter.Entry(window, textvariable=source_folder_var, width=50).pack()
tkinter.Button(window, text="원본 폴더 선택", command=select_source_folder).pack()

tkinter.Label(window, text="대상 폴더:").pack()
tkinter.Entry(window, textvariable=target_folder_var, width=50).pack()
tkinter.Button(window, text="대상 폴더 선택", command=select_target_folder).pack()

tkinter.Button(window, text="분류 시작", command=classify_files).pack()


gif_label = Label(window)
gif_label.pack()
photo = PhotoImage(file="/Users/dhl/Desktop/ufo-ezgif.com-video-to-gif-converter.gif")
gif_label.config(image=photo)

window.mainloop()
