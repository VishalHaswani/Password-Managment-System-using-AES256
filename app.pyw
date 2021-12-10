from tkinter import *
from tkinter import ttk

from passwordGenerator import generatePassword
import hexAndString
import AES

file_location = "data.TXT"
root = Tk()
root.geometry("1380x560")
root.title("Login Page")
folder_location = "D:\\Programming\\Projects\\SE - Inventory Mng System\\Final\\"
data = ""
#data = [['Facebook', 'vishal21haswani', '.e8/07c%T9', 'This is not the real password'], ['insta', 'Vishal', 'OC#KW#U8ss%$Gk5r7Sr1FyVX', 'sample2']]
root_password = "" #Vishal@2001
hex_key_size = 64

def data2mat(str_data):
    """
    converts string data to matrix format
    """
    str_data = str_data.split("\n")
    mat_data = [i.split("-::!::-") for i in str_data]
    return mat_data

def mat2data(mat_data):
    """
    converts matrix data to string
    """
    mat_data = ["-::!::-".join(i) for i in mat_data]
    str_data = "\n".join(mat_data)
    return str_data

def login_page():

    def login():
        """
        Tries to login 
            if the password is correct then login success
            else "wrong passsword" is shown
        """
        global root_password, hex_key_size
        root_password = loginvar.get()
        hex_password = hexAndString.string2hex(root_password, hex_key_size//2)
        hex_password[-2] = hex_password[-2][: int("0x" + hex_password[-1], 16)]
        hex_password = hex_password[:-1]
        hex_password[-1] = (hex_password[-1] + (hex_password[0] * 10))[: hex_key_size]

        file = open(file_location, "r")
        enc_data = file.read()
        file.close()
        hex_data = enc_data.split("\n")

        j = 0
        hex_password_len = len(hex_password)
        for i in range(len(hex_data)):
            hex_data[i] = AES.AES256(hex_password[j], hex_data[i], 2)
            j = (j + 1) % hex_password_len
        dec_data = hexAndString.hex2string(hex_data)
        
        if(dec_data == ""):
            print("Wrong Password")
        else:
            loginframe.destroy()
            global data
            data = data2mat(dec_data)
            print(data)
            return password_managment_window()
        
        return None


    loginframe = Frame(root, width=500, height=200, bg="sky blue")
    loginframe.place(x=440, y=180)

    loginvar = StringVar(value="Password")
    loginentry = Entry(loginframe, textvariable=loginvar, font="georgia 15", width=25, bg="white")
    loginentry.config(show='*')
    loginentry.place(x=50, y=80, height=40)

    loginbtn = Button(loginframe, text="  Log In  ", font="Georgia 11 bold", bg="white", bd=5, command=login)
    loginbtn.place(x=380, y=80, height=40)

    root.config(bg='sky blue')
    root.mainloop()
    return None

def password_managment_window():
    root.config(bg='sky blue')
    root.title("Password Managment Window")
    
    def put_in_table(tree_obj, data):
        for i in tree_obj.get_children():
            tree_obj.delete(i)
        for i in range(len(data)):
            tree_obj.insert(parent="", index=i, iid=i, values=data[i])
        return None

    def check_row_in_data(row, data):
        """Returns 1-Indexed values"""
        for i in range(len(data)):
            if data[i][0] == row[0] and data[i][1] == row[1]:
                return i
        return None

    def update_entry():
        if website.get() in ["", "Mandatory Entry"]:
            website.set("Mandatory Entry")
            return None
        if username.get() in ["", "Mandatory Entry"]:
            username.set("Mandatory Entry")
            return None
        global data
        row = [website.get(), username.get(), password.get(), note_text.get("1.0", "end-1c")]
        selected_item = check_row_in_data(row, data)
        if selected_item != None:
            data[selected_item][0] = row[0]
            data[selected_item][1] = row[1]
            data[selected_item][2] = row[2]
            data[selected_item][3] = row[3]
        else:
            data.append(row)
        put_in_table(tree, data)
        return None

    def delete_entry():
        global data
        selected_item = tree.focus()
        if selected_item != "":
            data.pop(int(selected_item))
            selected_item = None
            clear_entry()
            put_in_table(tree, data)
        return None

    def clear_entry():
        website.set("")
        username.set("")
        password.set("")
        note_text.delete("1.0", "end-1c")
        return None
    
    def double_click(event = None):
        if tree.focus() != "":
            selected_item = int(tree.focus())
            itm = tree.item(tree.focus(), "values")
            website.set(itm[0])
            username.set(itm[1])
            password.set(itm[2])
            note_text.delete("1.0", "end-1c")
            note_text.insert("1.0", itm[3])
        return None

    def generate_password_window():
        def generate_password():
            if pas_length.get() not in ["", "Number Only"]:
                try:
                    pas_len = int(pas_length.get())
                except:
                    pas_length.set("Number Only")
                    return None
            else:
                pas_len = None
            symbols_to_add = [i for i in symbols_to_include if symbols_to_include[i].get() == 1]
            generator = generatePassword()
            password.set(generator.generate(symbols=symbols_to_add, length=pas_len))
            root2.destroy()
            return None

        root2 = Toplevel(root, bg="sky blue")
        root2.geometry("400x500")
        formframe2 = Frame(root2, width=360, height=400, bg="#FFFFFF")
        formframe2.place(x=20, y=50)
        
        pas_length = StringVar(value = "Number Only")
        Label(formframe2, text="Length", font="Georgia 11 bold", bg="#FFFFFF").place(x=10, y=20)
        Entry(formframe2, textvariable=pas_length, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=20,height=30)
        Label(formframe2, text="Symbols to be Included:", font="Georgia 11 bold", bg="#FFFFFF").place(x=10, y=70)
        default_symbols = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '*', '(', ')', '<']
        symbols_to_include = dict()
        xval, yval = 50, 120
        for i in default_symbols:
            symbols_to_include[i] = IntVar(value=1)
            Checkbutton(formframe2, text=i, font="georgia 11 bold", bg="white",variable=symbols_to_include[i]).place(x=xval, y=yval, anchor="w")
            xval += 60
            if xval == 290:
                xval = 50
                yval += 60
        Button(formframe2, text="Generate", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=generate_password).place(x=230, y=330)

        root2.mainloop()
        pass

    def commit_changes():
        global data, root_password, hex_key_size
        str_data = mat2data(data)

        hex_data = hexAndString.string2hex(str_data, 16)
        hex_password = hexAndString.string2hex(root_password, hex_key_size//2)
        hex_password[-2] = hex_password[-2][: int("0x" + hex_password[-1], 16)]
        hex_password = hex_password[:-1]
        hex_password[-1] = (hex_password[-1] + (hex_password[0] * 10))[: hex_key_size]

        j = 0
        hex_password_len = len(hex_password)
        for i in range(len(hex_data)):
            hex_data[i] = AES.AES256(hex_password[j], hex_data[i], 1)
            j = (j + 1) % hex_password_len
        
        enc_data = "\n".join(hex_data)
        file = open("data.TXT", "w")
        file.write(enc_data)
        file.close()
        return None

    def change_password_window():
        def change_password():
            if password_var.get() != confirm_password_var.get():
                output_msg.set("Password didn't match Try again")
                return None
            if len(password_var.get()) < 10:
                output_msg.set("Password must have atleast 10 charecters")
                return None
            global root_password
            root_password = password_var.get()
            commit_changes()
            root3.destroy()
            return None

        root3 = Toplevel(root, bg="sky blue")
        root3.geometry("440x320+500+300")
        root3.title("Change Password")
        formframe3 = Frame(root3, width=400, height=280, bg="#FFFFFF")
        formframe3.place(x=20, y=20)
        output_msg = StringVar()
        Label(formframe3, textvariable=output_msg, font="Georgia 11 bold", bg="#FFFFFF", fg="red").place(x=10, y=20)
        Label(formframe3, text="Password", font="Georgia 11 bold", bg="#FFFFFF").place(x=10, y=60)
        Label(formframe3, text="Confirm Password", font="Georgia 11 bold", bg="#FFFFFF").place(x=10, y=120)
        password_var = StringVar()
        confirm_password_var = StringVar()
        Entry(formframe3, show="*", textvariable=password_var, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=170, y=60,height=30)
        Entry(formframe3, show="*", textvariable=confirm_password_var, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=170, y=120,height=30)
        Button(formframe3, text="Change", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=change_password).place(x=250, y=180)

        root3.mainloop()
        return None

    formframe = Frame(root, width=500, height=400, bg="#FFFFFF")
    formframe.place(x=20, y=50)

    tableframe = LabelFrame(root, width=1000, height=1000, bg = "#FFFFFF")
    tableframe.place(x=540, y=50)
    scrollbarx = Scrollbar(tableframe, orient=HORIZONTAL)
    scrollbary = Scrollbar(tableframe, orient=VERTICAL)
    column_width = {'#0': 0, '#1': 100, '#2': 200, '#3': 200, "#4": 300}
    column_heading = ["Website", "User Name", "Password", "Note"]
    tree = ttk.Treeview(tableframe, columns=column_heading, selectmode="browse", height=18, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    for i in column_width:
        tree.column(i, stretch=YES, minwidth=0, width=column_width[i])
    for i in column_heading:
        tree.heading(i, text=i, anchor=CENTER)
    tree.grid(row=1, column=0, sticky="W")
    scrollbary.config(command=tree.yview)
    scrollbarx.grid(row=2, column=0, sticky="we")
    scrollbarx.config(command=tree.xview)
    scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
    formframe.focus_set()
    global data
    put_in_table(tree, data)
    tree.bind("<Double-1>", double_click)
    website = StringVar()
    username = StringVar()
    password = StringVar()
    va = 20
    for i in column_heading:
        Label(formframe, text=i, font="Georgia 11 bold", bg="#FFFFFF").place(x=10, y=va)
        va += 60
    Entry(formframe, textvariable=website, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142, y=20,height=30)
    Entry(formframe, textvariable=username, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=80,height=30)
    Entry(formframe, textvariable=password, font="georgia 11 bold", bg="#FFFFFF", width=20).place(x=142,y=140,height=30)
    note_text = Text(formframe, font="georgia 11 bold", bg="#FFFFFF", width=20)
    note_text.place(x=142,y=200,height=90)
    Button(formframe, text="Generate", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=generate_password_window).place(x=370, y=130)
    Button(formframe, text="Save", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=commit_changes).place(x=10, y=320)
    Button(formframe, text="Update", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=update_entry).place(x=130, y=320)
    Button(formframe, text="Remove", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=delete_entry).place(x=250, y=320)
    Button(formframe, text="Clear", font="Georgia 11 bold", bg="sky blue", bd=5, width=10, height=2,command=clear_entry).place(x=370, y=320)
    Button(root, text="Change Password", font="Georgia 11 bold", bg="sky blue", bd=5, width=15, height=2,command=change_password_window).place(x=1200, y=470)
    root.mainloop()

login_page()
#password_managment_window()