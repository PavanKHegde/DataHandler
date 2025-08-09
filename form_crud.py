import tkinter as tk
from tkinter import ttk,messagebox
import sqlite3

conn= sqlite3.connect('contancts.db')
cursor=conn.cursor()
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS
    contancts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    '''
)
conn.commit()

class ContactApp:
    def __init__(self,root):
        self.root=root
        self.root.title("Conatact Form app")
        self.name_var=tk.StringVar()
        self.email_var=tk.StringVar()
        self.phone_var=tk.StringVar()
        
        tk.Label(root,text="Name").grid(row=0,column=0,padx=7,pady=5)
        tk.Entry(root,textvariable=self.name_var).grid(row=0,column=1,padx=7,pady=5)
        
        tk.Label(root,text="Email").grid(row=1,column=0,padx=7,pady=5)
        tk.Entry(root,textvariable=self.email_var).grid(row=1,column=1,padx=7,pady=5)
        
        tk.Label(root,text="phone").grid(row=2,column=0,padx=7,pady=5)
        tk.Entry(root,textvariable=self.phone_var).grid(row=2,column=1,padx=7,pady=5)
        
        tk.Button(root,text="Add", command=self.add_contanct).grid(row=3,column=0,pady=10)
        tk.Button(root,text="Update",command=self.update_contanct).grid(row=3,column=1)
        tk.Button(root,text="Delete",command=self.delete_contanct).grid(row=3,column=2)
        
        self.tree=ttk.Treeview(root,columns=('ID','Name','Email','Phone'),show='headings')
        self.tree.heading('ID',text='ID')
        self.tree.heading('Name',text='Name')
        self.tree.heading('Email',text='Email')
        self.tree.heading('Phone',text='Phone')
        self.tree.column('ID',width=25)
        
        self.tree.bind('<ButtonRelease-1>',self. select_contanct)
        self.tree.grid(row=4,column=0,columnspan=3,padx=7,pady=10)
        
        self.load_contancts()
        
        
    def add_contanct(self):
        name,email,phone=self.name_var.get(),self.email_var.get(),self.phone_var.get()
        if name and email and phone:
            cursor.execute("INSERT INTO contancts(name,email,phone)VALUES(?,?,?)",(name,email,phone))
            conn.commit()
            self.clear_form()
            self.load_contancts()
    
    def load_contancts(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursor.execute("SELECT * FROM contancts")
        for row in cursor.fetchall():
            self.tree.insert("",tk.END,values=row)
            
    def select_contanct(self,event):
        selected=self.tree.focus()
        if selected:
            values=self.tree.item(selected,'values')
            
            self.name_var.set(values[1])
            self.email_var.set(values[2])
            self.phone_var.set(values[3])
            
            
    def update_contanct(self):
        selected= self.tree.focus()
        if not selected:
            messagebox.showwarning("select an record")
            return
        values=self.tree.item(selected,'values')
        contanct_id=values[0]
        name,email,phone=self.name_var.get(),self.email_var.get(),self.phone_var.get()
        
        if name and email and phone:
            cursor.execute("UPDATE contancts SET name=?,email=?,phone=? WHERE id=?",(name,email,phone,contanct_id))
            conn.commit()
            self.clear_form()
            self.load_contancts()
            
    def delete_contanct(self):
        selected=self.tree.focus()
        if not selected:
            messagebox.showerror("select a record")
        
        values=self.tree.item(selected,'values')
        contact_id=values[0]
        confirm= messagebox.askyesno("Confirm Delete")
        
        if confirm:
            cursor.execute("DELETE FROM contancts WHERE id=?",(contact_id))
            conn.commit()
            self.clear_form()
            self.load_contancts()
            
    def clear_form(self):
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
      
        
if __name__=="__main__":
    root = tk.Tk()
    app=ContactApp(root)
    root.mainloop()        
                
        
    
        
        
        
        
        
        
    