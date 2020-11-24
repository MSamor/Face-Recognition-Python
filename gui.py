import tkinter as tk
import tkinter.messagebox
import requests
import threading
from pygame import mixer
from PIL import ImageTk
from face_recognition_use import *
from face_recognition_init import *
from multiprocessing.pool import ThreadPool

pool = ThreadPool(processes=1)

# 初始化窗口
window = tk.Tk()
# 窗口标题
window.title('人脸识别系统')
# 创建一个主frame，长在主window窗口上
frame = tk.Frame(window)
frame.grid()
# 窗口图标路径
IMGPATH = "toast/recong.gif"
# 人脸图片位置，自动导入时用
AUTOPATH = "img/face_recognition"
# 音乐地址
MUSIC = "music/music.mp3"

# 需要用到的已知人脸数据
know_face_encodings = []
konw_face_names = []

# 播放音乐组件
mixer.init()


# 显示弹窗
def showmodle(content):
    tkinter.messagebox.showinfo(title='提示', message=content)


# 自定义扫描人脸数据（为优化程序体验，没有使用此方法）
def scan_path():
    text = tk.StringVar()
    text.set('请输入已知人脸目录加载数据(图片名为识别人名)')
    r = tk.Label(frame, textvariable=text, bg='blue', font=('Arial', 12), width=50, height=2)
    r.grid(row=1, column=0)

    def load_lfw():
        global know_face_encodings
        global konw_face_names
        if input1.get() == "":
            showmodle("目录不能为空")
        else:
            text.set("加载中……请稍等……")
            btn1.grid_forget()
            try:
                async_result = pool.apply_async(load_known_face, (input1.get(),))
                know_face_encodings, konw_face_names = async_result.get()
                showmodle("数据加载完成……")
                r.grid_forget()
                input1.grid_forget()
                start_face_recog()
            except:
                text.set("路径有误，请重新输入……")
                btn1.grid(row=3, column=0)

    input1 = tk.Entry(frame, show=None, font=('Arial', 14), width=40)
    input1.grid(row=2, column=0)
    btn1 = tk.Button(frame, text='加载', font=('Arial', 12), width=10, height=1, command=load_lfw)
    btn1.grid(row=3, column=0)


# 自动扫面人脸数据
def scan_path_auto():
    global know_face_encodings
    global konw_face_names
    global AUTOPATH
    async_result = pool.apply_async(load_known_face, (AUTOPATH,))
    know_face_encodings, konw_face_names = async_result.get()
    start_face_recog()


# 显示图片在窗口
def show_face_to_windiw():
    photo = ImageTk.PhotoImage(file=IMGPATH)
    label_show = tk.Label(frame, imag=photo)
    label_show.grid(row=0, column=0, columnspan=2)
    label_show.image = photo


# 开始人脸识别
def start_face_recog():
    def run(know_face_encodings, konw_face_names):
        btn.grid_forget()
        face_run(know_face_encodings, konw_face_names)
        show_photo()
        btn.grid(row=2, column=0, columnspan=2)

    label = tk.Label(frame, text='点击开始打开摄像头-按“S”获取识别结果', font=('Arial', 12), width=50, height=2)
    label.grid(row=1, column=0, columnspan=2)
    btn = tk.Button(frame, text='开始', font=('Arial', 12), width=20, height=1,
                    command=lambda: run(know_face_encodings, konw_face_names))
    btn.grid(row=2, column=0, columnspan=2)


# 读取文件列表、动态加载、显示识别结果
def show_photo():
    res = load_face_data_file("photo")
    if len(res) == 0:
        return
    for i in res:
        texts = tk.StringVar()
        try:
            unknow_face_encodings, unknow_face_locations = face_init_unknown_res_file("photo/face.jpg")
            name = face_use_test(know_face_encodings, unknow_face_encodings, konw_face_names)
            texts.set("识别结果：" + name)
        except:
            texts.set("未检测到人脸")
        showmodle("检测完成")

        photo = ImageTk.PhotoImage(file=i['path'])
        label_show = tk.Label(frame, imag=photo)
        label_show.grid(row=0, column=1)
        label_show.image = photo

        label = tk.Label(frame, textvariable=texts, bg='yellow', font=('Arial', 12), width=30, height=2)
        label.grid(row=1, column=1)


# 获取音乐
def get_music():
    # 接口跳转获取真实地址
    def get_redirect_url(url):
        url = url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        return response

    res = requests.get("https://api.uomg.com/api/rand.music?sort=热歌榜&format=json")
    res = res.json()
    res = get_redirect_url(res['data']['url'])
    if os.path.exists(MUSIC):
        os.remove(MUSIC)
    with open(MUSIC, 'wb') as f:
        f.write(res.content)
    print("播放")
    mixer.music.load(MUSIC)
    mixer.music.play()


# 音乐播放、停止
def music():
    # 停止播放
    def stop_music():
        btn1.grid(row=6, column=0, columnspan=2)
        btn2.grid_forget()
        mixer.music.stop()
        mixer.music.unload()

    # 开始播放
    def play_music():
        threading.Thread(target=get_music).start()
        btn1.grid_forget()
        btn2.grid(row=6, column=0, columnspan=2)

    r = tk.Label(frame, text="点击随机播放歌曲", font=('Arial', 12), width=50, height=2)
    r.grid(row=4, column=0, columnspan=2)
    btn1 = tk.Button(frame, text='播放', font=('Arial', 12), width=10, height=1, command=play_music)
    btn1.grid(row=6, column=0, columnspan=2)
    btn2 = tk.Button(frame, text='停止', font=('Arial', 12), width=10, height=1, command=stop_music)


# 菜单
def menu():
    def hello():
        newWindow = tk.Toplevel(window)
        tk.Label(newWindow, text="作者：貌似", font=('Arial', 15), width=20, height=2).pack()
        tk.Label(newWindow, text="版本：1.1", font=('Arial', 15), width=20, height=2).pack()
        tk.Button(newWindow, text="确定", font=('Arial', 12), width=5, height=1, command=newWindow.destroy).pack()

    menubar = tk.Menu(window)
    menubar.add_command(label="关于", command=hello)
    menubar.add_command(label="退出", command=window.quit)
    window.config(menu=menubar)


# 实时天气
def weather():
    text = tk.StringVar(value="")
    r = tk.Label(frame, textvariable=text, font=('Arial', 12), width=50, height=2)
    r.grid(row=7, column=0, columnspan=2)

    res = requests.get("http://pv.sohu.com/cityjson?ie=utf-8")
    res = res.text.split(":")[-1].split("\"")[1][-3:]
    res = requests.get(
        "https://geoapi.heweather.net/v2/city/lookup?key=1f64433544784f98bce18756551005a4&location=" + str(res))
    res = res.json()
    res = requests.get("https://devapi.heweather.net/v7/weather/now?location=" + res["location"][0][
        "id"] + "&key=1f64433544784f98bce18756551005a4")
    res = res.json()
    text.set("气温：" + res['now']["temp"] + "℃，天气：" + res['now']["text"])


if __name__ == "__main__":
    # 这里开启多线程是为了加载后台数据，如：人脸数据，天气数据。没有加载完成就不显示按钮和提示
    threading.Thread(target=weather).start()
    show_face_to_windiw()
    threading.Thread(target=scan_path_auto).start()
    music()
    menu()
    # 主窗口循环显示
    window.mainloop()
