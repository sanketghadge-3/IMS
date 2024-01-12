from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os,time
import email_pass
import smtplib
class Login_System:
    def __init__(self,root):
        self.root = root
        self.root.title("Login System ")
        self.root.geometry("1600x800+0+0")
        #=========Image================================
        self.phone_image=ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=200,y=90)
        self.root.config(bg="#fafafa")
        
        #==========login Frame================================
        self.employee_id=StringVar()
        self.password=StringVar()
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=150,width=350,height=490)

        titlr=Label(login_frame,text="Login System",font=("elephant",30,"bold"),bg="white").place(x=0,y=30,relwidt=1)

        lbl_user=Label(login_frame,text="Employee ID",font=("Andlus",15,),bg="white",fg="#767171").place(x=50,y=100)
        txt_username=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15,),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_password=Label(login_frame,text="Password",font=("Andlus",15,),bg="white",fg="#767171").place(x=50,y=200)
        txt_password=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15,),bg="#ECECEC").place(x=50,y=230,width=250)

        btn_login=Button(login_frame,command=self.login,text="Log In",font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00B0F0",fg="white",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="OR",bg="white",fg="lightgray",font=("times new roman",15,"bold")).place(x=150,y=355)

        btn_forget_pass=Button(login_frame,text="Forget Password?",command=self.forget_window,font=("times new roman",13,"bold"),bg="white",fg="#00759E",bd=0,activebackground="white",activeforeground="blue",cursor="hand2").place(x=100,y=390)

        #========animation =====
        self.im1=ImageTk.PhotoImage(file="images/im1.png")
        self.im2=ImageTk.PhotoImage(file="images/im2.png")
        self.im3=ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image=Label(self.root,bg="white")
        self.lbl_change_image.place(x=367,y=193,width=240,height=428)

        self.animation()
    def animation(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animation)

    def login(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="" :
                 messagebox.showerror("Error","All Fileds are required",parent=self.root)
            else:
               cur.execute('select utype  from emp13 where eid=? AND pass=?',(self.employee_id.get(),self.password.get()))
               user=cur.fetchone()
               if user==None:
                   messagebox.showerror("Error","Invalid USERNAME/PASSWORD",parent=self.root) 
               else:
                #    print(user)
                   if user[0]=="Admin":    
                     self.root.quit()
                     os.system("python dashbord.py")
                   else:
                       self.root.quit()
                       os.system("python billing.py")
                       
               
        except Exception as ex:
                print("Error",f"Error due to :{str(ex)}")
 
    def forget_window(self):
        con=sqlite3.connect(database=r"ims.db")
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror("Error","Employee ID must be reqired",parent=self.root)
            else:
                cur.execute('select email  from emp13 where eid=? ',(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                   messagebox.showerror("Error","Invalid Employee ID,try again",parent=self.root) 
                else:
                    #=======Forgrt WIndow =====
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    # call send _email_function
                    chk=self.send_email(email[0])
                    if chk=='fail':
                        print(chk[0])
                        messagebox.showerror("Error","Connection Error,try again",parent=self.root)
                    else:
                      self.forget_win=Toplevel(self.root)
                      self.forget_win.title("REST PASSWORD")
                      self.forget_win.geometry('400x350+500+100')
                      self.forget_win.focus_force()

                      title=Label(self.forget_win,text="Rest Password",font=("goudy old style",15,"bold"),bg="red",fg="white")
                      title.pack(side=TOP,fill=X)

                      lbl_reset=Label(self.forget_win,text="Enter OTP Sent on Registererd Email",font=("time new roman",15)).place(x=20,y=60)
                      txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("time new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)
                      self.btn_reset=Button(self.forget_win,text="Submit",command=self.validate_otp,font=("time new roman",15),bg="lightblue")
                      self.btn_reset.place(x=280,y=100,width=100,height=30)
                     
                      lbl_new_pass=Label(self.forget_win,text="New Password",font=("time new roman",15)).place(x=20,y=160)
                      txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,show="*",font=("time new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)
                    
                      lbl_con_pass=Label(self.forget_win,text="Confirm Password",font=("time new roman",15)).place(x=20,y=225)
                      txt_con_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,show="*",font=("time new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)
                    
                      self.btn_update=Button(self.forget_win,text="Update",command=self.update_passwords,state=DISABLED,font=("time new roman",15),bg="lightblue")
                      self.btn_update.place(x=150,y=300,width=100,height=30)
        except Exception as ex:
                print("Error",f"Error due to :{str(ex)}")

    def update_passwords(self):
        if self.var_new_pass.get() ==''or self.var_conf_pass.get() =='':
            messagebox.showerror("Error","Pasword is Required",parent=self.forget_win)
        elif self.var_new_pass.get() != self.var_conf_pass.get() :
            messagebox.showerror("Error","Pasword & Confirm Password should be same",parent=self.forget_win)
        else:
            con=sqlite3.connect(database=r"ims.db")
            cur=con.cursor()
            try:
                cur.execute('Update  emp13 set pass=?   where eid=?',(self.var_new_pass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("INFORMATION","Password updated successfully")
                os.root.quit()
            except Exception as ex:
                print("Error",f"Error due to :{str(ex)}")
 
    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            # self.btn_update.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP,try again",parent=self.forget_win)

    
    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_
        
        s.login(email_,pass_)
        
        self.otp=int(time.strftime("%H%M%S"))+int(time.strftime("%S"))
        # print(self.otp)

        subj='IMS-Reset Password OTP'
        msg=f'Dear Sir/Madam,\n\nYour Reset OTP is {self.otp}.\n\nWith Regards,\nIMS Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        print(s.ehlo())
        if chk[0]==250:
            return 'Done'
        else:
            return 'fail'

root=Tk()
obj=Login_System(root)
root.mainloop()