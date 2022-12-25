import tkinter
from tkinter.ttk import Combobox
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
from threading import Thread
import threading
from detect_mask_video import *
from msvcrt import getch
from time import strftime
import urllib.request
from playsound import playsound
import requests
import datetime
import json

top = tk.Tk()

username = tk.StringVar(top)
password = tk.StringVar(top)
busInfo = ["", "", "0"]
staffInfo = ["", "", "", "",0]
result = [0, 0, ""]
total_people = 0
total_people_violate = 0
statusWaring = True
statusCamera = False


def login_page():
    global username, password
    Label(top, text="ĐĂNG NHẬP ",
          font=(130), bg='gray').place(x=550, y=180)
    Label(top, text="Tài khoản", font=(65), bg='gray').place(x=400, y=245)

    Entry(top, textvariable=username, width=100, font=40).place(
        x=500, y=245, width=300, height=30)

    Label(top, text="Mật khẩu", font=(65), bg='gray').place(x=400, y=345)

    Entry(top, textvariable=password, width=100, font=40,
          show="*").place(x=500, y=345, width=300, height=30)

    Button(top, text=" Đăng nhập ", fg="red", font=(25),
           bg='black', command=handle_login).place(x=650, y=450)
    Button(top, text="   Thoát   ", fg="red", font=(25),
           bg='black', command=exit).place(x=450, y=450)


def exit():
    top.quit()


def log_sum_people():
    global total_people, total_people_violate
    Label(top, text=str(total_people), font=(
        65), bg='gray').place(x=340, y=300)
    Label(top, text=str(total_people_violate),
          font=(65), bg='gray').place(x=320, y=350)
    time = strftime('%H:%M')
    if (time == "23:59"):
        total_people = 0
        total_people_violate = 0


def log_result(guest_number, violate, time):
    table_x = 65
    table_y = 690
    global result
    result[0] = guest_number
    result[1] = violate
    result[2] = time
    table_y = table_y+50
    Label(top, text=busInfo[0], font=(65), bg='black',
          fg="white").place(x=table_x, y=table_y)
    Label(top, text=busInfo[1], font=(65), bg='black',
          fg="white").place(x=table_x+250, y=table_y)
    Label(top, text=str(result[0])+"/"+str(busInfo[2])+"  ", font=(65), bg='black',
          fg="white").place(x=table_x+400, y=table_y)
    Label(top, text=str(result[1]), font=(65), bg='black',
          fg="white").place(x=table_x+600, y=table_y)
    Label(top, text=result[2], font=(65), bg='black',
          fg="white").place(x=table_x+830, y=table_y)


def start_oclock():
    canvas1 = Canvas(top, width=300, height=180, bg='black')
    canvas1.place(x=50, y=400)
    lbl1 = Label(top, font=('calibri', 35, 'bold'),
                 background='black',
                 foreground='white', text="oke")
    lbl2 = Label(top, font=('calibri', 28, 'bold'),
                 background='black',
                 foreground='white', text="oke")

    def time():
        string = strftime('%H:%M:%S %p')
        lbl1.config(text=string)
        string = strftime('%d/%m/%Y')
        lbl2.config(text=string)
        lbl1.after(1000, time)
    lbl1.place(x=80, y=420)
    lbl2.place(x=100, y=500)
    time()


def get_data_staff_api():
    print(username.get(), " ", password.get())
    try:
        source = urllib.request.urlopen(
            'http://localhost:1337/api/nhanviens/'+username.get()).read()
        list_of_data = json.loads(source)['data']['attributes']
        arrBirthday = list_of_data['NGAYSINH'].split("-")
        staffInfo[0] = username.get()
        staffInfo[1] = list_of_data['HOTEN']
        staffInfo[2] = list_of_data['CHUCVU']
        staffInfo[3] = arrBirthday[2]+"/"+arrBirthday[1]+"/"+arrBirthday[0]
        staffInfo[4] = list_of_data["IDXE"]
        if (list_of_data['PASSWORD'] == password.get()):
            return True
        else:
            messagebox.showinfo("Thông báo", "Mật khẩu không đúng !!!")
            return False
    except:
        messagebox.showinfo("Thông báo", "ID không tồn tại !!!")
        return False


def get_data_bus_api():
    # print(username.get(), " ", password.get())
    try:
        source = urllib.request.urlopen(
            'http://localhost:1337/api/xes/'+str(staffInfo[4])).read()
        list_of_data = json.loads(source)['data']['attributes']
        busInfo[0] = list_of_data['BIENSO']
        busInfo[1] = list_of_data['SUCCHUA']
        busInfo[2] = list_of_data['SOTUYEN']
        if (list_of_data['TRANGTHAI'] == True):
            return True
        else:
            messagebox.showinfo("Thông báo", "Xe không còn hoạt động !!!")
            return False
    except:
        messagebox.showinfo("Thông báo", "Xe không còn hoạt động !!!")


def handle_login():
    if (get_data_staff_api() and get_data_bus_api()):
        home_page()


def home_page():
    clear()
    x = 80
    y = 100
    title = ["Biển số xe", "Tuyến", "Số luợt",
             "Không đeo khẩu trang", "Thời gian"]

    Label(top, text="HỆ THỐNG CẢNH BÁO ĐEO KHẨU TRANG TRÊN XE BUÝT ",
          font=(80), bg='gray').place(x=300, y=15)
    Label(top, text="Mã nhân viên : "+staffInfo[0],
          font=(65), bg='gray').place(x=x, y=y)
    Label(top, text="Họ và tên : "+staffInfo[1],
          font=(65), bg='gray').place(x=x, y=y+50)
    Label(top, text="Chức vụ :  "+staffInfo[2],
          font=(65), bg='gray').place(x=x, y=y+100)
    Label(top, text="Ngày sinh : "+staffInfo[3],
          font=(65), bg='gray').place(x=x, y=y+150)
    Label(top, text="Tổng lượt khách trong ngày : ",
          font=(65), bg='gray').place(x=x, y=y+200)
    Label(top, text="Tổng lượt khách vi phạm : ",
          font=(65), bg='gray').place(x=x, y=y+250)

    canvas1 = Canvas(top, width=1100, height=120, bg='black')
    canvas1.place(x=50, y=670)
    Label(top, text="Thông tin xe", font=(70),
          bg='pink', fg="black").place(x=500, y=630)
    table_x = 65
    table_y = 690
    Label(top, text=title[0], font=(65), bg='black',
          fg="white").place(x=table_x, y=table_y)
    Label(top, text=title[1], font=(65), bg='black',
          fg="white").place(x=table_x+250, y=table_y)
    Label(top, text=title[2], font=(65), bg='black',
          fg="white").place(x=table_x+400, y=table_y)
    Label(top, text=title[3], font=(65), bg='black',
          fg="white").place(x=table_x+550, y=table_y)
    Label(top, text=title[4], font=(65), bg='black',
          fg="white").place(x=table_x+900, y=table_y)

    time = strftime('%H:%M:%S - %d/%m/%Y %p')
    log_result(0, 0, time)
    # log_sum_people(0,0)

    start_oclock()

    Button(top, text="  Mở camera   ", fg="red", font=(25),
           bg='black', command=handle_start).place(x=800, y=625)
    Button(top, text="  Đăng xuất   ", fg="red", font=(25),
           bg='black', command=logout).place(x=150, y=625)


def logout():
    global statusCamera
    if (statusCamera == False):
        global busInfo, staffInfo, result, total_people, total_people_violate, statusWaring
        busInfo = ["", "", "0"]
        staffInfo = ["", "", "", ""]
        result = [0, 0, ""]
        total_people = 0
        total_people_violate = 0
        statusWaring = True
        clear()
        login_page()
    else:
        messagebox.showinfo(
            "Thông báo", "Hãy tắt camera trước khi đăng xuất !!!")


def clear():
    canvas1 = Canvas(top, width=2400, height=1200, bg='gray')
    canvas1.place(x=0, y=0)


def addNotifyApi():
    try:
        def addNotify():
            global result,busInfo
            data = {
                "data": {
                    "HKKHONGKHAUTRANG": result[1],
                    "THOIGIAN": str(datetime.datetime.now()),
                    "HANHKHACH": result[0],
                    "xe": staffInfo[4]
                },
                "meta": {}
            }
            requests.post("http://localhost:1337/api/thongbaos", json=data)
        thread_waring = threading.Thread(target=addNotify, args=())
        thread_waring.start()
    except:
        print("error add notify")


def read_waring():
    global statusWaring
    if (statusWaring):
        statusWaring = False
        thread_waring = threading.Thread(target=handle_waring, args=())
        thread_waring.start()


def handle_waring():
    playsound("waring.mp3")
    global statusWaring
    statusWaring = True


def handle_start():
    thread_camera = threading.Thread(target=handle_camera, args=())
    thread_camera.start()


def handle_camera():
    global total_people, total_people_violate, statusCamera
    try:
        statusCamera = True
        prototxtPath = r"face_detector\deploy.prototxt"
        weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
        faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

        # load the face mask detector model from disk
        maskNet = load_model("mask_detector.model")
        vs = VideoStream(src=0).start()
        global top
        app = Frame(top, background="gray", width=800, height=550)
        app.grid(padx=400, pady=55)
        # Create a label in the frame
        lmain = Label(app, width=800, height=550, background="gray")
        lmain.grid()

        def close_camera():
            print("close")
            global statusCamera
            statusCamera = False
            Label(top, width=50, height=3, background="gray").place(x=950, y=617)
            app.destroy()
            vs.stream.release()

        Button(top, text="  Tăt camera   ", fg="red", font=(25),
               bg='black', command=close_camera).place(x=950, y=625)
        while True:
            try:
                frame = vs.read()
                frame = imutils.resize(frame, width=800, height=550)
                # detect faces in the frame and determine if they are wearing a
                # face mask or not
                (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
                # loop over the detected face locations and their corresponding
                # locations
                # print(len(locs)," - ", len(preds))
                number = len(locs)
                violate = 0
                for (box, pred) in zip(locs, preds):
                    # unpack the bounding box and predictions
                    (startX, startY, endX, endY) = box
                    (mask, withoutMask) = pred
                    # print(mask,withoutMask)

                    # determine the class label and color we'll use to draw
                    # the bounding box and text
                    label = "Mask" if mask > withoutMask else "No Mask"
                    if label == "No Mask":
                        violate = violate + 1
                    color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

                    # include the probability in the label
                    label = "{}: {:.2f}%".format(
                        label, max(mask, withoutMask) * 100)

                    # display the label and bounding box rectangle on the output
                    # frame
                    cv2.putText(frame, label, (startX, startY - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                    cv2.rectangle(frame, (startX, startY),
                                  (endX, endY), color, 2)

                if (number != result[0] or violate != result[1]):
                    read_waring()
                    if (number > result[0]):
                        total_people = total_people + (number-result[0])
                    if (violate > result[1]):
                        total_people_violate = total_people_violate + (violate - result[1])
                    log_sum_people()
                    time = strftime('%H:%M:%S - %d/%m/%Y %p')
                    log_result(number, violate, time)
                    addNotifyApi()

                # show the output frame
                # def video_stream():
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                lmain.imgtk = imgtk
                lmain.configure(image=imgtk)
            except:
                print("error")
                break
        print("stop")
        app.destroy()
        time = strftime('%H:%M:%S - %d/%m/%Y %p')
        log_result(0, 0, time)
    except:
        print("error 4")


if __name__ == "__main__":
    top.geometry("1200x800")
    top.title("Hệ thống cảnh báo đeo khẩu trang")
    top.configure(background="gray")
    login_page()
    # handle_login()
    top.mainloop()
