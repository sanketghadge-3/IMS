from  tkinter import * 
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3

class categoryClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System ")
        self.root.config(bg="white")
        self.root.focus_force()
        #=====Variable======
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        #=====Title=====
        lbl_title=Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg="#184a45",fg="white" ,bd=3,relief=RIDGE,).pack(side=TOP,fill=X,padx=10,pady=20)


        lbl_name=Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg="white").place(x=50,y=100)
        lbl_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",25),bg="lightyellow").place(x=50,y=170,width=300)

        lbl_add=Button(self.root,text="ADD",command=self.add,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=40)
        lbl_delete=Button(self.root,text="DELETE",command=self.delete,font=("goudy old style",15),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=40)

        #===Category Details===
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=400,height=100)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.category_Table=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.category_Table.xview)
        scrolly.config(command=self.category_Table.yview)
        self.category_Table.heading("cid",text="C ID")
        self.category_Table.heading("name",text="Name")
        self.category_Table["show"]="headings"
        self.category_Table.column("cid",width=90)
        self.category_Table.column("name",width=100)
        self.category_Table.pack(fill=BOTH,expand=1)
        self.category_Table.bind("<ButtonRelease-1>",self.get_data)
        
        #====Images=====
        self.im1=Image.open("images/cat.jpg")
        self.im1=self.im1.resize((500,250))
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=220)

        self.im2=Image.open("images/category.jpg")
        self.im2=self.im2.resize((500,250))
        self.im2=ImageTk.PhotoImage(self.im2)

        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
        self.lbl_im2.place(x=580,y=220)

        self.show()


    def add(self):
            con=sqlite3.connect(database=r"ims.db")
            cur=con.cursor()
            try:
              if self.var_name.get()=="":
                messagebox.showerror("Error",f" Category Name  should be re quired",parent=self.root)
              else:
                cur.execute("select * from cat13 where name=?",(self.var_name.get(),))
                row =cur.fetchone()
                if row!=None:
                  messagebox.showerror("Error","This Category  already present , try different",parent=self.root)
                else:
                    cur.execute("Insert into cat13 (name) values(?)",(self.var_name.get(),))
                con.commit()
                messagebox.showinfo("success","Category Addedd Successfully",parent=self.root)
                self.show()
                
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to :{str(ex)}")

    def show(self):
       con=sqlite3.connect(database=r"ims.db")
       cur=con.cursor()
       try:
          cur.execute("select * from cat13")
          rows=cur.fetchall()
          self.category_Table.delete(*self.category_Table.get_children())
          for row in rows:
             self.category_Table.insert('',END,values=row)
             
          
       except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}")
    
    def get_data(self,ev):
       f=self.category_Table.focus()
       content=(self.category_Table.item(f))
       row=content['values']
       self.var_cat_id.set(row[0])
       self.var_name.set(row[1])

    def delete(self):
       con=sqlite3.connect(database=r"ims.db")
       cur=con.cursor() 
       try:
          if self.var_cat_id.get()=="":
                messagebox.showerror("Error",f" please select ofr enter category name",parent=self.root)
          else:
               cur.execute("select * from cat13 where cid=?",(self.var_cat_id.get(),))
               row =cur.fetchone()
               if row==None:
                 messagebox.showerror("Error","Error , Please try again",parent=self.root)
               else:
                  op=messagebox.askyesno("Confirm","Do you really want to Delete?",parent=self.root)
                  if op==True:
                    cur.execute("delete from cat13 where cid=?",(self.var_cat_id.get(),))
                    con.commit()
                    messagebox.showinfo("Delete","Category Delete Successfully")
                    self.show()
                    self.var_cat_id.set("")
                    self.var_name.set("")
       except Exception as ex:
         messagebox.showerror("Error",f"Error due to :{str(ex)}")
       
if __name__ == "__main__":
   root = Tk()
   obj =  categoryClass(root)
   root .mainloop()
                    