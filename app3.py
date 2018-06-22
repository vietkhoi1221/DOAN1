"""Import các thư viện cần dùng"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
import sendemailfull
import webbrowser
import serial
import threading
import dong

"""Khai báo biến"""
name = ''
hr = ''
bpm= ''
meo = ''
j= 1    
data = serial.Serial('com3',9600)       #Thiết lập cổng Serial COM3, tốc độ baud 9600

class Application(Frame):               #Lớp Application kế thừa lớp Frame     
    def __init__(self, parent):         #Tạo constructor cho lớp Application
        Frame.__init__(self, parent)    #Tạo constructor từ lớp Frame
        self.parent = parent
        self.initUI()
    #Hàm khởi tạo
    def initUI(self):                   
        self.parent.title("Đồ án 1")    #Đặt tên cho widget
        """Lấy ảnh và thu nhỏ"""
        self.imgmail = PhotoImage(file = 'D:\\Code\\Python\\HTN\\email.png').subsample(35,35)
        self.imgweb = PhotoImage(file = 'D:\\Code\\Python\\HTN\\web.png').subsample(15,15)
        """Thiết lập các label và button"""
        self.label6 = ttk.Label(self.parent, text = "Heart Rate", width = 8)
        self.label7 = ttk.Label(self.parent, text = "Bpm/SpO2", compound = "right")
        self.label6.grid(row = 0, column = 1)
        self.label7.grid(row = 0, column = 2)
        self.btn5 = ttk.Button(self.parent, text = "Gửi gmail", width = 0,image = self.imgmail, compound = 'left', command = self.gmail)
        self.btn5.grid(row = 2, column = 0, columnspan =2)
        self.btn6 = ttk.Button(self.parent, text = "Mở web", width = 0,image = self.imgweb, compound = 'left', command = self.web)
        self.btn6.grid(row = 2, column = 2)
    #Hàm mở web
    def web(self):
        webbrowser.open("http://127.0.0.1:5000")
    #Hàm tạo giao diện để gửi gmail
    def gmail(self):
        self.second_win = Toplevel(self.parent)         #Tạo một Toplevel từ Toplevel gốc
        self.second_win.title("Gmail")                  #Đặt tên title
        self.second_win_lbl1 = ttk.Label(self.second_win, text = "Name:", width =7)
        self.second_win_lbl1.grid(row =0, column = 0,pady =5, padx =5)
        self.second_win_txt1 = Entry(self.second_win, width = 30)
        self.second_win_txt1.grid(row =0, column = 1)
        self.second_win_lbl2 = ttk.Label(self.second_win, text = "Email:", width =7)
        self.second_win_lbl2.grid(row =1, column = 0)
        self.second_win_txt2 = Entry(self.second_win, width = 30)
        self.second_win_txt2.grid(row =1, column = 1, pady =5,padx =5)
        self.second_win_lbl3 = ttk.Label(self.second_win, text = "Subject:", width =9)
        self.second_win_lbl3.grid(row =2, column = 0)
        self.second_win_txt3 = Entry(self.second_win, width = 30)
        self.second_win_txt3.grid(row =2, column = 1, pady =5,padx =5)
        self.second_win_btn1 = ttk.Button(self.second_win, text = "Quit", width = 10, command = self.second_win.quit)
        self.second_win_btn1.grid(row =3, column = 0, sticky = 'sw')
        self.second_win_btn2 = ttk.Button(self.second_win, text = "Send", width = 10, command = self.sendmeo)
        self.second_win_btn2.grid(row =3, column = 1)
        self.second_win.mainloop()
    #Hàm gửi email
    def sendmeo(self):
        """Lấy dữ liệu từ các entry"""
        self.name = self.second_win_txt1.get()
        self.meo = self.second_win_txt2.get()
        self.sub = self.second_win_txt3.get()
        self.obj = sendemailfull.MessageUser()  #Tạo một đối tượng obj từ lớp MessageUser
        self.obj.add_user(self.name, self.hr, self.bpm, self.sub, email = self.meo) #Thêm dữ liệu người gửi
        self.obj.get_details()  #Thiết lập nội dung gửi
        self.obj.send_email()   #Tiến hành gửi
    #Hàm lấy dữ liệu
    def get_data(self):
        while True:
            """Khai báo các biến toàn cục"""
            global hr
            global bpm
            global j
            if (data.inWaiting() > 0):          #Kiểm tra có nhận được dữ liệu hay không
                self.i = str(data.readline())   #gán dữ liệu nhận cho i
                self.y = re.findall('[0-9]+',self.i)    #Tách dữ liệu
                self.hr = self.y[0]
                self.bpm = self.y[2]
                file = open("example.txt", "a")         #Mở file
                self.chuoi = str(j) + ',' + str(self.hr) + ',' + str(self.bpm)+'\n'
                file.write(self.chuoi)  #Ghi vào file
                file.close()    #Đóng file
                j += 1
                """Thiết lập label để hiển thị nhịp tim và nồng độ oxi"""
                label4 = ttk.Label(self.parent, text = self.hr)
                label5 = ttk.Label(self.parent, text = self.bpm + " %")
                label4.grid(row = 1, column = 1)
                label5.grid(row = 1, column = 2)
#Hàm tạo biểu đồ
def bieudo():
    dong.app.run_server(debug=False)

if __name__ == '__main__':
    root = Tk()
    ex = Application(root)
    """Tạo 2 luồng để hiện dữ liệu và tạo biểu đồ"""
    thread1 = threading.Thread(target=ex.get_data)
    thread2 = threading.Thread(target=bieudo)
    """Cho 2 luồng chạy"""
    thread1.start()
    thread2.start()
    root.mainloop()
    
