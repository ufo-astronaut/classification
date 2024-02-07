import os
import shutil
import tkinter
from tkinter import filedialog, Label, Button, Tk, StringVar, Entry, messagebox, PhotoImage
from PIL import Image, ImageTk, ImageSequence 
from tkinter import ttk


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


if __name__ == "__main__":
    window = tkinter.Tk()
    window.title("UFO-Astronaut 드론 이미지 분류 프로그램")
    window.geometry("640x400+100+100")
    window.resizable(False, False)

    source_folder_var = tkinter.StringVar()
    target_folder_var = tkinter.StringVar()

    lab1 = tkinter.Label(window, text="원본 폴더:", anchor='w')#.pack()
    lab1.place(x = 30, y= 30 )

    ent1= tkinter.Entry(window, textvariable=source_folder_var, width=40 )#.pack()
    ent1.place(x = 100, y = 30)

    btn1 = tkinter.Button(window, text="원본 폴더 선택", command=select_source_folder)#.pack()
    btn1.place(x = 500, y  = 28)

    lab2 = tkinter.Label(window, text="대상 폴더:", anchor='w')#.pack()
    lab2.place(x = 30, y = 80)

    ent2 = tkinter.Entry(window, textvariable=target_folder_var, width=40)#.pack()
    ent2.place(x = 100 , y = 80)

    btn2 = tkinter.Button(window, text="대상 폴더 선택", command=select_target_folder)#.pack()
    btn2.place(x = 500, y = 80)

    btn3 = tkinter.Button(window, text="분류 시작", command=classify_files, bg = "blue", fg = "white" )#.pack()
    btn3.place(x = 270, y = 120 )

# GIF 파일 로드
    gif_path = "/Users/dhl/Desktop/ufo-ezgif.com-video-to-gif-converter.gif"
    new_width = 200
    new_height = 200

    style = ttk.Style()

    #photo = PhotoImage(file=gif_path)

    #gif_label = Label(window, image=photo)
    #gif_label.pack()


    def load_and_resize_gif(path, width, height):
        frames = []
        img = Image.open(path)
        for frame in ImageSequence.Iterator(img):
            resized_frame = frame.resize((width, height), Image.LANCZOS)  # Image.LANCZOS 사용
            frames.append(ImageTk.PhotoImage(image=resized_frame))
        return frames
gif_label = Label(window)
gif_label.pack()
# photo = PhotoImage(file="/Users/dhl/Desktop/ufo-ezgif.com-video-to-gif-converter.gif")
# gif_label.config(image=photo)

    # GIF의 프레임을 순환하는 함수
    def update_frame(frames, index=0):
        frame = frames[index]
        gif_label.config(image=frame)
        index = (index + 1) % len(frames)  # 다음 프레임, 또는 처음으로
        window.after(100, update_frame, frames, index)

        # 크기가 조절된 GIF 프레임 로드
        resized_frames = load_and_resize_gif(gif_path, new_width, new_height)

        gif_label = tkinter.Label(window)
        gif_label.place(x = 210, y = 170)

        # 애니메이션 시작
        update_frame(resized_frames)

        window.mainloop()
