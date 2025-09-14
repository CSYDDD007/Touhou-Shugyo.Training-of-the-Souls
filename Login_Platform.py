import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import Login_System
from global_var import *
set_value("Login_Valid", False)

ctk.set_default_color_theme("dark-blue") 
ctk.set_appearance_mode("light")

class Login_Platform(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login Platform")
        self.iconbitmap('resource/image/icon_aEm_icon.ico')
        self.geometry("800x800")
        self.resizable(False, False)
        self.title = ctk.CTkFrame(self, height=50, width=760)
        ctk.CTkLabel(self.title, text="Login Platform", font=("Arial", 40)).pack(side=LEFT, padx=100, pady=20)
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self.title, text="ViewMode",font=("Arial", 30), command=self.switch_event, variable=self.switch_var, onvalue="on", offvalue="off").pack(side=LEFT, pady=10)
        self.page = Login_Page(self)
        self.remind = ctk.CTkFrame(self, height=50, width=760)
        ctk.CTkLabel(self.remind, text="Bad Apple!!", font=("Arial", 20)).pack(side=LEFT, padx=100, pady=20)
        self.title.pack(padx=20, pady=10, fill=X)
        self.page.pack(padx=20, pady=10, fill=BOTH, expand=True)
    def switch_event(self):
        if self.switch_var.get()=='on':
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    def Logout(self):
        self.page.destroy()
        self.page = Login_Page(self)
        self.page.pack(padx=20, pady=10, fill=BOTH, expand=True)
    def Register(self, username='', password=''):
        self.page.destroy()
        self.page = Register_Page(self, username, password)
        self.page.pack(padx=20, pady=10, fill=BOTH, expand=True)
    def VerifyPassword(self, username, password):
        self.page.destroy()
        self.page = Verify_Page(self, username, password)
        self.page.pack(padx=20, pady=10, fill=BOTH, expand=True)
    def Admin(self, var=''):
        self.page.destroy()
        self.page = Admin_Page(self, var)
        self.page.pack(padx=20, pady=10, fill=BOTH, expand=True)
    def User_Detail(self,name):
        self.page.destroy()
        self.page = User_Detail_Page(self,name)
        self.page.pack(padx=20, pady=10, fill=BOTH, expand=True)
        
class Login_Page(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(width=800, height=600)
        ctk.CTkLabel(self, text="Login Page", font=("Arial", 40)).pack(pady=10)
        ctk.CTkLabel(self, text="Username:                                                 ", font=("Arial", 40)).pack(side=TOP, padx=10, pady=10, fill=X)
        self.entry_username=ctk.CTkEntry(self, placeholder_text="Username", font=("Arial", 30))
        self.entry_username.pack(side=TOP, padx=10, pady=10, fill=X)
        ctk.CTkLabel(self, text="Password:                                                 ", font=("Arial", 40)).pack(side=TOP, padx=10, pady=10, fill=X)
        self.entry_password=ctk.CTkEntry(self, placeholder_text="Password", font=("Arial", 30), show="*")
        self.entry_password.pack(side=TOP, padx=10, pady=10, fill=X)
        ctk.CTkButton(self, text="LOGIN", command=self.login, font=("Arial", 40), width=500, height=100).pack(pady=20)
        ctk.CTkButton(self, text="REGISTER", command=self.master.Register, font=("Arial", 40), width=500, height=100).pack(pady=20)
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not username:
            messagebox.showerror('Error','Please input username')
            return
        if not password:
            messagebox.showerror('Error','Please input password')
            return
        if username == 'admin' and password == 'admin':
            self.master.Admin()
            messagebox.showinfo('Success','Welcome to Admin Mode')
            return
        if Login_System.Login(username, password):
            set_value("Login_Valid", True)
            messagebox.showinfo('Success','Login successful!\nWelcome, '+username)
            set_value('username', username)
            with open('tmp.txt', 'w') as file:
                file.write(username)
            self.master.destroy()
            self.master.quit()
            return
        messagebox.showerror('Error','Login failed, please check your username and password again or register if you are new user')
        
class Register_Page(ctk.CTkFrame):
    def __init__(self, master, username, password):
        super().__init__(master)
        self.master = master
        self.configure(width=800, height=600)
        ctk.CTkLabel(self, text="Register Page", font=("Arial", 40)).pack(pady=10)
        ctk.CTkLabel(self, text="Username:                                                 ", font=("Arial", 40)).pack(side=TOP, padx=10, pady=10, fill=X)
        self.entry_username=ctk.CTkEntry(self, placeholder_text="Username", font=("Arial", 30))
        self.entry_username.insert(0, username)
        self.entry_username.pack(side=TOP, padx=10, pady=10, fill=X)
        ctk.CTkLabel(self, text="Password:                                                 ", font=("Arial", 40)).pack(side=TOP, padx=10, pady=10, fill=X)
        self.entry_password=ctk.CTkEntry(self, placeholder_text="Password", font=("Arial", 30), show="*")
        self.entry_password.insert(0, password)
        self.entry_password.pack(side=TOP, padx=10, pady=10, fill=X)
        ctk.CTkButton(self, text="REGISTER", command=self.register, font=("Arial", 40), width=500, height=75).pack(pady=20)
        ctk.CTkButton(self, text="BACK", command=self.master.Logout, font=("Arial", 40), width=500, height=75).pack(pady=20)
        
    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not username:
            messagebox.showerror('Error','Please input username')
            return
        if Login_System.Repeate_Username(username):
            messagebox.showerror('Error','Repeated Username')
            return
        if not username.isalnum():
            messagebox.showerror('Error','Username should be alphanumeric')
            return
        if not password:
            messagebox.showerror('Error','Please input password')
            return
        if len(password)<8:
            messagebox.showerror('Error','Password should be at least 8 characters')
            return
        if not password.isalnum():
            messagebox.showerror('Error','Password should be alphanumeric')
            return
        self.master.VerifyPassword(username, password)
        messagebox.showinfo('Success','Please verify your password')

class Verify_Page(ctk.CTkFrame):
    def __init__(self, master, username, password):
        super().__init__(master)
        self.master = master
        self.configure(width=800, height=600)
        ctk.CTkLabel(self, text="Register Page", font=("Arial", 40)).pack(pady=10)
        ctk.CTkLabel(self, text="Username:                                                 ", font=("Arial", 40)).pack(side=TOP, padx=10, pady=10, fill=X)
        self.entry_username=ctk.CTkEntry(self, placeholder_text="Username", font=("Arial", 30))
        self.entry_username.insert(0, username)
        self.entry_username.configure(state='disabled')
        self.entry_username.pack(side=TOP, padx=10, pady=10, fill=X)
        ctk.CTkLabel(self, text="Password:                                                 ", font=("Arial", 40)).pack(side=TOP, padx=10, pady=10, fill=X)
        self.entry_password=ctk.CTkEntry(self, placeholder_text="Password", font=("Arial", 30), show="*")
        self.entry_password.insert(0, password)
        self.entry_password.configure(state='disabled')
        self.entry_password.pack(side=TOP, padx=10, pady=10, fill=X)
        ctk.CTkLabel(self, text="Verify Password:                                        ", font=("Arial", 40)).pack(side=TOP, padx=10, pady=10, fill=X)
        self.entry_verify_password=ctk.CTkEntry(self, placeholder_text="Verify Password", font=("Arial", 30), show="*")
        self.entry_verify_password.pack(side=TOP, padx=10, pady=10, fill=X)
        ctk.CTkButton(self, text="REGISTER", command=self.register, font=("Arial", 40), width=500, height=75).pack(pady=20)
        ctk.CTkButton(self, text="BACK", command=self.master.Register, font=("Arial", 40), width=500, height=75).pack(pady=20)
        
    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        verify_password = self.entry_verify_password.get()
        if not verify_password:
            messagebox.showerror('Error','Please input verify password')
            return
        if password != verify_password:
            messagebox.showerror('Error','Password and Verify Password are not the same')
            return
        Login_System.Register(username, password)
        messagebox.showinfo('Success','Register is applied')
        self.master.Logout()
        
class Admin_Page(ctk.CTkFrame):
    def __init__(self, master, var=''):
        super().__init__(master)
        self.master = master
        self.configure(width=800, height=600)
        ctk.CTkLabel(self, text="Admin Page", font=("Arial", 40)).pack(pady=10)
        self.input = ctk.CTkEntry(self, font=("Arial", 20))
        self.input.insert(0, var)
        self.input.pack()
        ctk.CTkButton(self, text="Find", font=("Arial", 30), command=self.find_user).pack()
        user_lists = Login_System.Show_All_User() if var=='' else Login_System.Find_User(var)
        self.frame = ctk.CTkScrollableFrame(self)
        for i in user_lists:
            ctk.CTkLabel(self.frame, text=i, font=("Arial", 30)).grid(row=user_lists.index(i), column=0, padx=50, pady=10, sticky=W)
            ctk.CTkButton(self.frame, text="Detail", font=("Arial", 30), command=lambda x=i[0]: self.user_detail(x)).grid(row=user_lists.index(i), column=1, padx=10, pady=10, sticky=E)
            ctk.CTkButton(self.frame, text="Delete", font=("Arial", 30), command=lambda x=i[0]: self.delete_user(x), fg_color=("#DB3E39", "#821D1A")).grid(row=user_lists.index(i), column=2, padx=10, pady=10, sticky=E)
        self.frame.pack(padx=20, pady=20, fill=BOTH, expand=True)
        ctk.CTkButton(self, text="BACK", command=self.master.Logout, font=("Arial", 40), width=500, height=100).pack(pady=20)
        
    def user_detail(self,name):
        self.master.User_Detail(name)
    
    def find_user(self):
        key = self.input.get()
        self.master.Admin(key)
        messagebox.showinfo('Find', 'Find the users with KEY: {}'.format(key))
        
    def delete_user(self,name):
        if messagebox.askyesno('Question','Do you really want to delete USER: {}?'.format(name)):
            Login_System.Delete_User(name)
            self.master.Admin()
        
class User_Detail_Page(ctk.CTkFrame):
    def __init__(self, master,name):
        super().__init__(master)
        self.master = master
        self.configure(width=800, height=600)
        self.detail = Login_System.Get_User_Data(name)
        ctk.CTkLabel(self, text="User Detail Page", font=("Arial", 30)).pack(pady=10)
        ctk.CTkLabel(self, text="Username:                                                 ", font=("Arial", 40)).pack(side=TOP, padx=10, pady=10, fill=X)
        self.entry_username=ctk.CTkEntry(self, placeholder_text="Username", font=("Arial", 30))
        self.entry_username.insert(0, self.detail[0])
        self.entry_username.pack(side=TOP, padx=10, pady=10, fill=X)
        ctk.CTkLabel(self, text="Password:                                                 ", font=("Arial", 40)).pack(side=TOP, padx=10, pady=10, fill=X)
        self.entry_password=ctk.CTkEntry(self, placeholder_text="Password", font=("Arial", 30))
        self.entry_password.insert(0, self.detail[1])
        self.entry_password.pack(side=TOP, padx=10, pady=10, fill=X)
        ctk.CTkLabel(self, text="Highest Score:                                           ", font=("Arial", 40)).pack(side=TOP, padx=10, pady=10, fill=X)
        self.entry_score=ctk.CTkEntry(self, font=("Arial", 30))
        if self.detail[2] == -1:
            self.entry_score.insert(0, "No Record")
        else:
            self.entry_score.insert(0, str(self.detail[2]))
        self.entry_score.configure(state="disabled")
        self.entry_score.pack(side=TOP, padx=10, pady=10, fill=X)
        ctk.CTkButton(self, text="SAVE", command=self.save, font=("Arial", 40), width=500, height=75).pack(pady=15)
        ctk.CTkButton(self, text="BACK", command=self.master.Admin, font=("Arial", 40), width=500, height=75).pack(pady=15)
        
    def save(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username == self.detail[0] and password == self.detail[1]:
            #print("None")
            messagebox.showerror('Error','No change')
            return
        if not username:
            messagebox.showerror('Error','Please input username')
            return
        if len(username)<8:
            messagebox.showerror('Error','Username should be at least 8 characters')
            return
        if username != self.detail[0] and Login_System.Repeate_Username(username):
            messagebox.showerror('Error','Repeated Username')
            return
        if not username.isalnum():
            messagebox.showerror('Error','Username should be alphanumeric')
            return
        if not password:
            messagebox.showerror('Error','Please input password')
            return
        if len(password)<8:
            messagebox.showerror('Error','Password should be at least 8 characters')
            return
        if not password.isalnum():
            messagebox.showerror('Error','Password should be alphanumeric')
            return
        Login_System.Update_User_Data(self.detail[0], username, password)
        messagebox.showinfo('Success','Change is saved')
        self.master.Admin()
        
def main():
    root = Login_Platform()
    root.mainloop()

if __name__ == '__main__':
    main()