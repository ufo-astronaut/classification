import os
import shutil
import tkinter
from tkinter import filedialog, Label, Button, PhotoImage

def fileList(path_before: str) -> list:
    file_list = os.listdir(path_before)
    categories = set()  # 중복을 방지하기 위해 set을 사용합니다.
    for file in file_list:
        if "_" in file:
            category = file.split("_", 1)[1]  # 언더스코어를 기준으로 파일명을 두 부분으로 나누고, 두 번째 부분을 카테고리로 사용합니다.
            categories.add(category)
    return list(categories)

def makeFolder(path_after: str, file_list: list):
    for file in file_list:
        try:
            os.makedirs(os.path.join(path_after, file))
        except FileExistsError:
            pass

def moveFile(path_before, path_after, file_list):
    for file in file_list:
        # 파일이름에 '_'가 있는 경우에만 처리
        if '_' in file:
            filename, category = file.split('_', 1)  # '_'를 기준으로 최대 한 번만 나눕니다.
            category_folder = os.path.join(path_after, category)
            subcategory_folder = os.path.join(category_folder, filename.split('_')[0])

            # 카테고리 폴더와 서브카테고리 폴더 생성
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)
            if not os.path.exists(subcategory_folder):
                os.makedirs(subcategory_folder)
            
            # 파일 이동
            shutil.move(os.path.join(path_before, file), subcategory_folder)
        else:
            # '_'가 없는 경우에도 카테고리 폴더 생성 후 이동
            category_folder = os.path.join(path_after, file.split('_')[0])
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)
            shutil.move(os.path.join(path_before, file), category_folder)


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
# photo = PhotoImage(file="/Users/dhl/Desktop/ufo-ezgif.com-video-to-gif-converter.gif")
# gif_label.config(image=photo)

window.mainloop()
