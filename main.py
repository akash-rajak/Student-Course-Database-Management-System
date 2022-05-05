
'''
Constraints :
    i.) (Save and update)Batch mentor must be same, who is registering
    ii.) (Save)If student id is already registered, then again login details will not be sent to student via mail, and again data will not be inserted in the student1 table
    iii.) (Save and update)year and semester are selected in pair that matches
    iv.) (save and update)Details should match with previously registered student, if going to other semester or year
    v.) (save)If a student is in a particular sem and year, then he/she will be able to get registered only for the next combination of year and semester
    vi.) (update)will not be able to change the student id (assumed that person will update by filling the column by selecting the row from table) i.e set function then update
    vii.) (save and update)duplicate row cannot be inserted
    viii.) IMP : here we are considering not to update Sem and year once inserted
    ix.) if student fails in any subject in any course, his/her sgpa = 0.0
    x.) update will be done, for student with stud_id, sem comparison, not only stud_id(as it is not primary key)
    xi.) if subject button clicked by selecting unmatched year and sem, show error message

'''


# import tkinter
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import smtplib
import random
import array
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF


fname = ""
lusername = ""
susername = ""
stud_id = ""
var_sgpa = ""
prev_id = ""
dict = {"EX":10, "A":9, "B":8, "C":7, "D":6, "P":5, "F":0, "NA":0}
dict1 = {"SEM-1":1, "SEM-2":2, "SEM-3":3, "SEM-4":4, "SEM-5":5, "SEM-6":6, "SEM-7":7, "SEM-8":8}
dict2 = {1:"SEM-1", 2:"SEM-2", 3:"SEM-3", 4:"SEM-4", 5:"SEM-5", 6:"SEM-6", 7:"SEM-7", 8:"SEM-8"}
exit1 = False


class faculty_class:
    def __init__(self, root):
        global fname
        self.root = root
        # width = self.root.winfo_screenwidth()
        # height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (1440, 760))
        self.root.iconbitmap('Images/icon.ico')
        self.root.title("Faculty")

      # Variables
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_sid = StringVar()
        self.var_sname = StringVar()
        self.var_reg = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        self.var_searchby = StringVar()
        self.var_searchentry = StringVar()

        # # header
        # img1 = Image.open("images/head1.jpeg")
        # img1 = img1.resize((560, 100), Image.ANTIALIAS)
        # self.headerimg1 = ImageTk.PhotoImage(img1)
        #
        # h1_lbl1 = Label(self.root, image=self.headerimg1)
        # h1_lbl1.place(x=0, y=0, width=560, height=100)
        #
        # img2 = Image.open("images/iiitkalayani.png")
        # img2 = img2.resize((260, 100), Image.ANTIALIAS)
        # self.headerimg2 = ImageTk.PhotoImage(img2)
        #
        # h1_lbl2 = Label(self.root, image=self.headerimg2)
        # h1_lbl2.place(x=560, y=0, width=260, height=100)
        #
        # img3 = Image.open("images/head2.png")
        # img3 = img3.resize((560, 100), Image.ANTIALIAS)
        # self.headerimg3 = ImageTk.PhotoImage(img3)
        #
        # h1_lbl3 = Label(self.root, image=self.headerimg3)
        # h1_lbl3.place(x=820, y=0, width=560, height=100)

        # # background
        # img4 = Image.open("images/bg.jpg")
        # img4 = img4.resize((1380, 610), Image.ANTIALIAS)
        # self.headerimg4 = ImageTk.PhotoImage(img4)
        #
        # bg_img = Label(self.root, image=self.headerimg4)
        # bg_img.place(x=0, y=100, width=1380, height=610)

        # # title label
        # tlbl = Label(bg_img, text="STUDENT & COURSE MANAGEMENT SYSTEM", font=(
        #     "Times New Roman", 20, "bold"), fg="white", bg="black")
        # tlbl.place(x=0, y=0, width=1380, height=25)

# MAIN FRAME
        if(lusername!=""):
            fname = lusername
            Label(text="Welcome, " + lusername, font=("Arial", 15), fg="black").place(x=20, y=0)
        else:
            fname = susername
            Label(text="Welcome, " + susername, font=("Arial", 15), fg="black").place(x=20, y=0)
        mframe = Frame(bg="white")
        mframe.place(x=0, y=30, width=1440, height=740)

    # INNER LEFT FRAME
        left_frame = LabelFrame(mframe, bd=2, bg="white", relief=SOLID,text="Student Information", font=("Verdana", 15, "bold"))
        left_frame.place(x=25, y=10, width=650, height=700)

        img5 = Image.open("images/stud2.jpg")
        img5 = img5.resize((620, 200), Image.ANTIALIAS)
        self.headerimg5 = ImageTk.PhotoImage(img5)

        bg_img = Label(left_frame, image=self.headerimg5)
        bg_img.place(x=10, y=10, width=620, height=200)

        # Student Information
        si_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE,text="Student Information", font=("Verdana", 15))
        si_frame.place(x=10, y=220, width=620, height=200)

        # student id
        sid = Label(si_frame, text="Student Id", bg="white",font=("Verdana", 10, "bold"))
        sid.grid(row=0, column=0, padx=18, pady=3, sticky=W)

        sid_entry = ttk.Entry(si_frame, textvariable=self.var_sid, width=20, font=("Verdana", 10))
        sid_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # student name
        sname = Label(si_frame, text="Student Name",bg="white", font=("Verdana", 10, "bold"))
        sname.grid(row=0, column=2, padx=5, pady=3, sticky=W)

        sname_entry = ttk.Entry(si_frame, textvariable=self.var_sname, width=20, font=("Verdana", 10))
        sname_entry.grid(row=0, column=3, padx=5, pady=5, sticky=W)

        # Registration number
        regn = Label(si_frame, text="Reg No:", bg="white",font=("Verdana", 10, "bold"))
        regn.grid(row=1, column=0, padx=18, pady=3, sticky=W)

        regn_entry = ttk.Entry(si_frame, textvariable=self.var_reg, width=20, font=("Verdana", 10))
        regn_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        # role number
        rno = Label(si_frame, text="Role No:", bg="white",font=("Verdana", 10, "bold"))
        rno.grid(row=1, column=2, padx=5, pady=3, sticky=W)

        rno_entry = ttk.Entry(si_frame, textvariable=self.var_roll, width=20, font=("Verdana", 10))
        rno_entry.grid(row=1, column=3, padx=5, pady=5, sticky=W)

        # gender
        gen = Label(si_frame, text="Gender", bg="white",font=("Verdana", 10, "bold"))
        gen.grid(row=2, column=0, padx=18, pady=3, sticky=W)

        gen_combo = ttk.Combobox(si_frame, textvariable=self.var_gender, font=("Verdana", 10), width=18, state="readonly")
        gen_combo["values"] = ("Select Gender", "MALE", "FEMALE","OTHER")
        gen_combo.current(0)
        gen_combo.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        # date of birth
        dob = Label(si_frame, text="Date of Birth",bg="white", font=("Verdana", 10, "bold"))
        dob.grid(row=2, column=2, padx=5, pady=3, sticky=W)

        dob_entry = DateEntry(si_frame, textvariable=self.var_dob, width=18, font=("Verdana", 10))
        dob_entry.grid(row=2, column=3, padx=5, pady=5, sticky=W)

        # email address
        eml = Label(si_frame, text="Email", bg="white",font=("Verdana", 10, "bold"))
        eml.grid(row=3, column=0, padx=18, pady=3, sticky=W)

        eml_entry = ttk.Entry(si_frame, textvariable=self.var_email, width=20, font=("Verdana", 10))
        eml_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        # phone number
        phne = Label(si_frame, text="Phone No:", bg="white",font=("Verdana", 10, "bold"))
        phne.grid(row=3, column=2, padx=5, pady=3, sticky=W)

        phne_entry = ttk.Entry(si_frame, textvariable=self.var_phone, width=20, font=("Verdana", 10))
        phne_entry.grid(row=3, column=3, padx=5, pady=5, sticky=W)

        # Address
        adres = Label(si_frame, text="Address", bg="white",font=("Verdana", 10, "bold"))
        adres.grid(row=4, column=0, padx=18, pady=3, sticky=W)

        adres_entry = ttk.Entry(si_frame, textvariable=self.var_address, width=20, font=("Verdana", 10))
        adres_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        # Batch Mentor
        bthmen = Label(si_frame, text="Batch Mentor",bg="white", font=("Verdana", 10, "bold"))
        bthmen.grid(row=4, column=2, padx=5, pady=3, sticky=W)

        bthmen_entry = ttk.Entry(si_frame, textvariable=self.var_teacher, width=20, font=("Verdana", 10))
        bthmen_entry.grid(row=4, column=3, padx=3, pady=5, sticky=W)

        # Course Information
        ci_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Course Information",font=("Verdana", 15))
        ci_frame.place(x=10, y=440, width=620, height=130)

        # department
        depart = Label(ci_frame, text="Department", bg="white", font=("Verdana", 10, "bold"))
        depart.grid(row=0, column=0, padx=20, pady=5, sticky=W)

        depart_combo = ttk.Combobox(ci_frame, textvariable=self.var_dep, font=("Verdana", 10), width=18,state="readonly")
        depart_combo["values"] = ("Select Department", "CSE", "EEE", "ME", "CE", "CIVIL")
        depart_combo.current(0)
        depart_combo.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # course
        course = Label(ci_frame, text="Course", bg="white", font=("Verdana", 10, "bold"))
        course.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        course_combo = ttk.Combobox(ci_frame, textvariable=self.var_course, font=("Verdana", 10), width=18,state="readonly")
        course_combo["values"] = ("Select Course", "BE", "BTECH")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=5, pady=5, sticky=W)

        # year
        year = Label(ci_frame, text="Year", bg="white", font=("Verdana", 10, "bold"))
        year.grid(row=1, column=0, padx=20, pady=5, sticky=W)

        year_combo = ttk.Combobox(ci_frame, textvariable=self.var_year, font=("Verdana", 10), width=18,state="readonly")
        year_combo["values"] = ("Select Year", "FIRST", "SECOND", "THIRD", "FOURTH")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        # semster
        sems = Label(ci_frame, text="Semester", bg="white", font=("Verdana", 10, "bold"))
        sems.grid(row=1, column=2, padx=10, pady=5, sticky=W)

        sems_combo = ttk.Combobox(ci_frame, textvariable=self.var_semester, font=("Verdana", 10), width=18,state="readonly")
        sems_combo["values"] = ("Select Semester", "SEM-1", "SEM-2", "SEM-3", "SEM-4", "SEM-5", "SEM-6", "SEM-7", "SEM-8")
        sems_combo.current(0)
        sems_combo.grid(row=1, column=3, padx=5, pady=5, sticky=W)

        # subject
        sub = Label(ci_frame, text="Subject", bg="white", font=("Verdana", 10, "bold"))
        sub.grid(row=2, column=0, padx=20, pady=5, sticky=W)

        sub_button = Button(ci_frame, text="Subject", command=self.select_subjects, font=("Verdana", 10), width = 20, cursor="hand2",borderwidth=0, relief="raised")
        sub_button.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        # BUTTONS
        btnframe = Frame(left_frame, bg="white")
        btnframe.place(x=10, y=570, width=620, height=90)

        # Save button
        sav = Image.open("images/save.png")
        sav = sav.resize((150, 50), Image.ANTIALIAS)
        self.savimg = ImageTk.PhotoImage(sav)

        savbtn = Button(btnframe, command=self.save_data, bg="white", bd=0,image=self.savimg, cursor="hand2")
        savbtn.place(x=5, y=30, width=150, height=50)

        # Update button
        updat = Image.open("images/update.png")
        updat = updat.resize((150, 50), Image.ANTIALIAS)
        self.updatimg = ImageTk.PhotoImage(updat)

        updatbtn = Button(btnframe, command=self.update_data, bg="white", bd=0,image=self.updatimg, cursor="hand2")
        updatbtn.place(x=160, y=30, width=150, height=50)

        # Delete button
        delet = Image.open("images/delete.png")
        delet = delet.resize((150, 50), Image.ANTIALIAS)
        self.deletimg = ImageTk.PhotoImage(delet)

        deletbtn = Button(btnframe, command=self.delete_data, bg="white", bd=0,image=self.deletimg, cursor="hand2")
        deletbtn.place(x=315, y=30, width=150, height=50)

        # Reset button
        rset = Image.open("images/reset.jpg")
        rset = rset.resize((150, 50), Image.ANTIALIAS)
        self.rsetimg = ImageTk.PhotoImage(rset)

        rsetbtn = Button(btnframe, command=self.reset_data, bg="white", bd=0,image=self.rsetimg, cursor="hand2")
        rsetbtn.place(x=470, y=30, width=150, height=50)

    # INNER RIGHT FREAME
        right_frame = LabelFrame(mframe, bd=2, bg="white", relief=SOLID,text="Student Details", font=("Verdana", 15, "bold"))
        right_frame.place(x=700, y=10, width=700, height=700)

        img6 = Image.open("images/stud3.jpg")
        img6 = img6.resize((670, 200), Image.ANTIALIAS)
        self.headerimg6 = ImageTk.PhotoImage(img6)

        bg_img = Label(right_frame, image=self.headerimg6)
        bg_img.place(x=10, y=10, width=670, height=200)

      # Search System
        ss_frame = LabelFrame(right_frame, bd=2, bg="white", relief=RIDGE,text="View Student Details & Search System", font=("Verdana", 15))
        ss_frame.place(x=10, y=220, width=670, height=75)

        search_by = Label(ss_frame, text="Search By :", pady=3, bg="black",fg="white", font=("Times New Roman", 13, "bold"))
        search_by.place(x=5, y=5, width=110)

        serchby_combo = ttk.Combobox(ss_frame,textvariable=self.var_searchby, font=("Verdana", 10), state="readonly")
        serchby_combo["values"] = ("Select", "Student Id", "Student Name", "Department", "Course","Reg_No","Gender","Address","Batch_Mentor")
        serchby_combo.current(0)
        serchby_combo.place(x=120, y=5, width=120, height=30)

        search_entry = ttk.Entry(ss_frame,textvariable=self.var_searchentry, font=("Verdana", 12))
        search_entry.place(x=245, y=5, width=150, height=30)

        searchbtn = Button(ss_frame, text="Search", command=self.search_func, bg="blue", fg="white", font=("Times New Roman", 15, "bold"), bd=0, cursor="hand2")
        searchbtn.place(x=410, y=5, width=110, height=30)

        showallbtn = Button(ss_frame, text="Show All", command=self.fetch_data, bg="blue", fg="white", font=("Times New Roman", 15, "bold"), bd=0, cursor="hand2")
        showallbtn.place(x=535, y=5, width=115, height=30)

      # Table
        table_frame = Frame(right_frame, bg="white", bd=2, relief=RIDGE)
        table_frame.place(x=10, y=315, width=670, height=345)

        xbar = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        ybar = ttk.Scrollbar(table_frame, orient=VERTICAL)
        xbar.pack(side=BOTTOM, fill=X)
        ybar.pack(side=RIGHT, fill=Y)

        self.student_table = ttk.Treeview(table_frame, columns=("dep", "course", "year", "sem", "id", "name", "reg", "roll","gender", "dob", "email", "phone", "address", "teacher", "sgpa"), xscrollcommand=xbar.set, yscrollcommand=ybar.set)
        xbar.config(command=self.student_table.xview)
        ybar.config(command=self.student_table.yview)

        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("id", text="Student Id")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("reg", text="Reg No.")
        self.student_table.heading("roll", text="Roll No.")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="Date of Birth")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone No.")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Teacher")
        self.student_table.heading("sgpa", text="SGPA")
        self.student_table["show"] = "headings"

        self.student_table.column("dep", width=80)
        self.student_table.column("course", width=80)
        self.student_table.column("year", width=80)
        self.student_table.column("sem", width=80)
        self.student_table.column("id", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("reg", width=100)
        self.student_table.column("roll", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=100)
        self.student_table.column("teacher", width=100)
        self.student_table.column("sgpa", width=100)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>",self.set_data)
        self.fetch_data()

    def select_subjects(self):
        global var_sgpa
        d = self.var_dep.get()
        c = self.var_course.get()
        y = self.var_year.get()
        s = self.var_semester.get()
        # xi.) if subject button clicked by selecting unmatched year and sem, show error message
        if ((y == "FIRST" and (s != "SEM-1" and s != "SEM-2")) or (y == "SECOND" and (s != "SEM-3" and s != "SEM-4")) or (y == "THIRD" and (s != "SEM-5" and s != "SEM-6")) or (y == "FOURTH" and (s != "SEM-7" and s != "SEM-8"))):
            messagebox.showerror("Error", "Year and Semester details are not matching.", parent=self.root)
            return

        if(d == "CSE" and c == "BE" and y == "FIRST" and s == "SEM-1"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Engineering Maths - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Engineering Maths - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Engineering Physics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Engineering Physics(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="C Programming and DSA", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Computer Programming(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="Language(English)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            Label(windows, text="Computer Engineering Drawing", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10,state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s8.current(0)
            s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())]*3 + dict[str(s2.get())]*3 + dict[str(s3.get())]*3 + dict[str(s4.get())]*4 + dict[str(s5.get())]*3 + dict[str(s6.get())]*4 + dict[str(s7.get())]*2 + dict[str(s8.get())]*2
                v /= 24
                v = round(v,2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if(dict[str(s1.get())]==0 or dict[str(s2.get())]==0 or dict[str(s3.get())]==0 or dict[str(s4.get())]==0 or dict[str(s5.get())]==0 or dict[str(s6.get())]==0 or dict[str(s7.get())]==0 or dict[str(s8.get())]==0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue", cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BE" and y == "FIRST" and s == "SEM-2"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Elements of Mech. Eng.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Basic Electrical Eng.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Basic Electronics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Constitution & Ethics", font=("Arial", 17), fg="black", bg="white").place(x=80,y=200)
            Label(windows, text="Eng. Chemistry(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Eng. Chemistry(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80,y=280)
            Label(windows, text="Workshop Practice", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            Label(windows, text="Elements of Civil Eng.", font=("Arial", 17), fg="black", bg="white").place(x=80,y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s8.current(0)
            s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2 + dict[str(s8.get())] * 2
                v /= 24
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0 or dict[str(s8.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BE" and y == "SECOND" and s == "SEM-3"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Engineering Maths - III", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Elect. Circuit Logic Design", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Discrete Mathematics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Data Structure in C", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="OOPs in C++", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Data Structure in C/C++(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="Elect. Circuit Logic Design(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            Label(windows, text="Software Eng.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s8.current(0)
            s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2 + dict[str(s8.get())] * 2
                v /= 24
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0 or dict[str(s8.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BE" and y == "SECOND" and s == "SEM-4"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Engineering Maths - IV", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Graph Theory & Combinatorics", font=("Arial", 17), fg="black", bg="white").place(x=80,y=120)
            Label(windows, text="Design & Analysis Of Algorithms", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="UNIX & Shell Programming", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Microprocessors", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Computer Organization", font=("Arial", 17), fg="black", bg="white").place(x=80,y=280)
            Label(windows, text="Design & Analysis Of Algorithms(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            Label(windows, text="Microprocessors(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s8.current(0)
            s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2 + dict[str(s8.get())] * 2
                v /= 24
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0 or dict[str(s8.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",
                   cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BE" and y == "THIRD" and s == "SEM-5"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="System Software", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Operating Systems", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Database Management System", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Computer Networks - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Formal Lang. & Automata Theory", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Database Application(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="System Software(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            Label(windows, text="Operating System(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s8.current(0)
            s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2 + dict[str(s8.get())] * 2
                v /= 24
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0 or dict[str(s8.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BE" and y == "THIRD" and s == "SEM-6"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Management & Entrepreneurship", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Unix Systems Programming", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Compiler Design", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Computer Networks - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Computer Graphics & Visualization", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Comp. Graphics & Visualization(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="Unix Systems Programming(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            Label(windows, text="Compiler Design(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s8.current(0)
            s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2 + dict[str(s8.get())] * 2
                v /= 24
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0 or dict[str(s8.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BE" and y == "FOURTH" and s == "SEM-7"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Object Oriented Design", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Embedded Computing Systems", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Programming with Web Advanced", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Computer Architecture", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Java & J2EE", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Multimedia Computing", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="Data Warehousing & Mining", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            Label(windows, text="Neural Networks", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s8.current(0)
            s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2 + dict[str(s8.get())] * 2
                v /= 24
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0 or dict[str(s8.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BE" and y == "FOURTH" and s == "SEM-8"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Software Architectures", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="System Modelling & Simulation", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Internet of Things", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Project", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Internship", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            # Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            # s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s6.current(0)
            # s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3
                v /= 16
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BTECH" and y == "FIRST" and s == "SEM-1"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="English", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Mathematics - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Applied Physics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Computers & IT", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="C & Data Structures", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Engineering Drawing Practice", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="Semi Conductors", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2
                v /= 22
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())]):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BTECH" and y == "FIRST" and s == "SEM-2"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Mathematics - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Discrete Structures", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Data Processing", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Linear/Digital ICs Application", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Logic Theory", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Economics & Accountancy", font=("Arial", 17), fg="black", bg="white").place(x=80,y=280)
            Label(windows, text="IC Application", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2
                v /= 22
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())]):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BTECH" and y == "SECOND" and s == "SEM-3"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Probability & Statistics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Electrical Technology", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Computer Organization", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Design & Analysis of Algorithm", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Operating Systems", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Object Oriented Programming", font=("Arial", 17), fg="black", bg="white").place(x=80,y=280)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4
                v /= 20
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BTECH" and y == "SECOND" and s == "SEM-4"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Microprocessors Interfacing", font=("Arial", 17), fg="black", bg="white").place(x=80,y=80)
            Label(windows, text="Operations Research", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Data Communications", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Theory of Computation", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Principles of Prog. Lang.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="System Programming", font=("Arial", 17), fg="black", bg="white").place(x=80,y=280)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4
                v /= 20
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BTECH" and y == "THIRD" and s == "SEM-5"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Computer Architecture", font=("Arial", 17), fg="black", bg="white").place(x=80,y=80)
            Label(windows, text="Data Structures & Algorithm", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Neuro - Fuzzy", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Database Information System", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Computer Network", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Data Mining", font=("Arial", 17), fg="black", bg="white").place(x=80,y=280)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4
                v /= 20
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BTECH" and y == "THIRD" and s == "SEM-6"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Artificial Intelligence", font=("Arial", 17), fg="black", bg="white").place(x=80,y=80)
            Label(windows, text="Prog. Language Implementation", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Wireless Network", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Compiler Design", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Computer Graphics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Information Storage Management", font=("Arial", 17), fg="black", bg="white").place(x=80,y=280)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4
                v /= 20
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BTECH" and y == "FOURTH" and s == "SEM-7"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Software Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80,y=80)
            Label(windows, text="Distributed Systems", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Java Programming", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Image Processing", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Neural Networks", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Visual Programming", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4
                v /= 20
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if(d == "CSE" and c == "BTECH" and y == "FOURTH" and s == "SEM-8"):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Simulation & Modelling", font=("Arial", 17), fg="black", bg="white").place(x=80,y=80)
            Label(windows, text="Pattern Reognition", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Mobile Computing", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Formal Lang. & Automata Theory", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Computer Communication", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Projecgt management", font=("Arial", 17), fg="black", bg="white").place(x=80,y=280)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4
                v /= 20
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        # if(d == "CSE" and c == "MTECH" and y == "FIRST" and s == "SEM-1"):
        #     print()
        #
        # if(d == "CSE" and c == "MTECH" and y == "FIRST" and s == "SEM-2"):
        #     print()
        #
        # if(d == "CSE" and c == "MTECH" and y == "SECOND" and s == "SEM-3"):
        #     print()
        #
        # if(d == "CSE" and c == "MTECH" and y == "SECOND" and s == "SEM-4"):
        #     print()
        #
        # if(d == "CSE" and c == "MTECH" and y == "THIRD" and s == "SEM-5"):
        #     print()
        #
        # if(d == "CSE" and c == "MTECH" and y == "THIRD" and s == "SEM-6"):
        #     print()
        #
        # if(d == "CSE" and c == "MTECH" and y == "FOURTH" and s == "SEM-7"):
        #     print()
        #
        # if(d == "CSE" and c == "MTECH" and y == "FOURTH" and s == "SEM-8"):
        #     print()

        if((d == "EEE" and c == "BE" and y == "FIRST" and s == "SEM-1") or (d == "EEE" and c == "BTECH" and y == "FIRST" and s == "SEM-1")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Applied Mathematics - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Applied Physics - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Applied Chemistry - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Manufacturing Process", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Intro. to Computers & AutoCad", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Communication Skills - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="Impact of Science & Tech. on Soc.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2
                v /= 22
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "EEE" and c == "BE" and y == "FIRST" and s == "SEM-2") or (d == "EEE" and c == "BTECH" and y == "FIRST" and s == "SEM-2")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Applied Mathematics - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Applied Physics - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Applied Chemistry - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Introduction to Programming", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Engineering Mechanics", font=("Arial", 17), fg="black", bg="white").place(x=80,y=240)
            Label(windows, text="Electrical Science", font=("Arial", 17), fg="black", bg="white").place(x=80,y=280)
            Label(windows, text="Communication Skills - II.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2
                v /= 22
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "EEE" and c == "BE" and y == "SECOND" and s == "SEM-3") or (d == "EEE" and c == "BTECH" and y == "SECOND" and s == "SEM-3")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Applied Mathematics - III", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Analog Electronics - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Ciruits & Systems", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Elect. Engineering Materials", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="ElectroMech. Energy Conversion - I", font=("Arial", 17), fg="black", bg="white").place(x=80,y=240)
            Label(windows, text="Data Structures", font=("Arial", 17), fg="black", bg="white").place(x=80,y=280)
            # Label(windows, text="Impact of Science & Tech. on Soc.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4
                v /= 20
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "EEE" and c == "BE" and y == "SECOND" and s == "SEM-4") or (d == "EEE" and c == "BTECH" and y == "SECOND" and s == "SEM-4")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="ElectroMech. Energy Conversion - II", font=("Arial", 17), fg="black", bg="white").place(x=80,y=80)
            Label(windows, text="Analog Electronics - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Power System - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Control Engineering - I", font=("Arial", 17), fg="black", bg="white").place(x=80,y=200)
            Label(windows, text="Electromagnetic Field Theory", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Power Station Practice", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            # Label(windows, text="Impact of Science & Tech. on Soc.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4
                v /= 20
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "EEE" and c == "BE" and y == "THIRD" and s == "SEM-5") or (d == "EEE" and c == "BTECH" and y == "THIRD" and s == "SEM-5")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Digital Electronics", font=("Arial", 17), fg="black",bg="white").place(x=80, y=80)
            Label(windows, text="OOPs using C++", font=("Arial", 17), fg="black", bg="white").place(x=80,y=120)
            Label(windows, text="Comm. Systems & Circuits", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Elect. Measurement & Instrumentation", font=("Arial", 17), fg="black", bg="white").place(x=80,y=200)
            Label(windows, text="Database Management Systems", font=("Arial", 17), fg="black", bg="white").place(x=80,y=240)
            Label(windows, text="Organizational Behavior", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            # Label(windows, text="Impact of Science & Tech. on Soc.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4
                v /= 20
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "EEE" and c == "BE" and y == "THIRD" and s == "SEM-6") or (d == "EEE" and c == "BTECH" and y == "THIRD" and s == "SEM-6")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Microprocessor", font=("Arial", 17), fg="black",bg="white").place(x=80, y=80)
            Label(windows, text="Power System - II", font=("Arial", 17), fg="black", bg="white").place(x=80,y=120)
            Label(windows, text="Power Electronics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Digital Signal Processing", font=("Arial", 17), fg="black", bg="white").place(x=80,y=200)
            Label(windows, text="Utilization of Electrical Energy", font=("Arial", 17), fg="black", bg="white").place(x=80,y=240)
            Label(windows, text="VLSI Design & its Application", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            # Label(windows, text="Impact of Science & Tech. on Soc.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4
                v /= 20
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "EEE" and c == "BE" and y == "FOURTH" and s == "SEM-7") or (d == "EEE" and c == "BTECH" and y == "FOURTH" and s == "SEM-7")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Electrical Drives", font=("Arial", 17), fg="black",bg="white").place(x=80, y=80)
            Label(windows, text="HVDC Transmission", font=("Arial", 17), fg="black", bg="white").place(x=80,y=120)
            Label(windows, text="Electives", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            # Label(windows, text="Control Engineering - I", font=("Arial", 17), fg="black", bg="white").place(x=80,y=200)
            # Label(windows, text="Electromagnetic Field Theory", font=("Arial", 17), fg="black", bg="white").place(x=80,y=240)
            # Label(windows, text="Power Station Practice", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            # Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            # Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            # Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            # s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s4.current(0)
            # s4.place(x=700, y=200)
            # s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s5.current(0)
            # s5.place(x=700, y=240)
            # s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s6.current(0)
            # s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3
                v /= 9
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "EEE" and c == "BE" and y == "FOURTH" and s == "SEM-8") or (d == "EEE" and c == "BTECH" and y == "FOURTH" and s == "SEM-8")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Advanced Control Systems", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Flexible A.c. Transmission Systems", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Electives", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            # Label(windows, text="Control Engineering - I", font=("Arial", 17), fg="black", bg="white").place(x=80,y=200)
            # Label(windows, text="Electromagnetic Field Theory", font=("Arial", 17), fg="black", bg="white").place(x=80,y=240)
            # Label(windows, text="Power Station Practice", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            # Label(windows, text="", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            # Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            # Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            # Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            # Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            # s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s4.current(0)
            # s4.place(x=700, y=200)
            # s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s5.current(0)
            # s5.place(x=700, y=240)
            # s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s6.current(0)
            # s6.place(x=700, y=280)
            # s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s7.current(0)
            # s7.place(x=700, y=320)
            # s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            # s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            # s8.current(0)
            # s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3
                v /= 9
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        # if(d == "EEE" and c == "BTECH" and y == "FIRST" and s == "SEM-1"):
        #     print()
        #
        # if(d == "EEE" and c == "BTECH" and y == "FIRST" and s == "SEM-2"):
        #     print()
        #
        # if(d == "EEE" and c == "BTECH" and y == "SECOND" and s == "SEM-3"):
        #     print()
        #
        # if(d == "EEE" and c == "BTECH" and y == "SECOND" and s == "SEM-4"):
        #     print()
        #
        # if(d == "EEE" and c == "BTECH" and y == "THIRD" and s == "SEM-5"):
        #     print()
        #
        # if(d == "EEE" and c == "BTECH" and y == "THIRD" and s == "SEM-6"):
        #     print()
        #
        # if(d == "EEE" and c == "BTECH" and y == "FOURTH" and s == "SEM-7"):
        #     print()
        #
        # if(d == "EEE" and c == "BTECH" and y == "FOURTH" and s == "SEM-8"):
        #     print()

        # if(d == "EEE" and c == "MTECH" and y == "FIRST" and s == "SEM-1"):
        #     print()
        #
        # if(d == "EEE" and c == "MTECH" and y == "FIRST" and s == "SEM-2"):
        #     print()
        #
        # if(d == "EEE" and c == "MTECH" and y == "SECOND" and s == "SEM-3"):
        #     print()
        #
        # if(d == "EEE" and c == "MTECH" and y == "SECOND" and s == "SEM-4"):
        #     print()
        #
        # if(d == "EEE" and c == "MTECH" and y == "THIRD" and s == "SEM-5"):
        #     print()
        #
        # if(d == "EEE" and c == "MTECH" and y == "THIRD" and s == "SEM-6"):
        #     print()
        #
        # if(d == "EEE" and c == "MTECH" and y == "FOURTH" and s == "SEM-7"):
        #     print()
        #
        # if(d == "EEE" and c == "MTECH" and y == "FOURTH" and s == "SEM-8"):
        #     print()

        if((d == "ME" and c == "BE" and y == "FIRST" and s == "SEM-1") or (d == "ME" and c == "BTECH" and y == "FIRST" and s == "SEM-1")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="English", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Mathematics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Physics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Chemistry", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4
                v /= 13
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "ME" and c == "BE" and y == "FIRST" and s == "SEM-2") or (d == "ME" and c == "BTECH" and y == "FIRST" and s == "SEM-2")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Mathematics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Physics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Programming Language", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Electrical Technology", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4
                v /= 13
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "ME" and c == "BE" and y == "SECOND" and s == "SEM-3") or (d == "ME" and c == "BTECH" and y == "SECOND" and s == "SEM-3")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Mechanics of Solids", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Applied Thermodynamics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Theory of Mechanics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Machine Drawing", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4
                v /= 13
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "ME" and c == "BE" and y == "SECOND" and s == "SEM-4") or (d == "ME" and c == "BTECH" and y == "SECOND" and s == "SEM-4")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Fluid Mechanics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Dynamics of Machinery", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Mechanical Engineering Design", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Electrical Machines & Controls", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4
                v /= 13
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "ME" and c == "BE" and y == "THIRD" and s == "SEM-5") or (d == "ME" and c == "BTECH" and y == "THIRD" and s == "SEM-5")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Fluid Mechanics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Heat & Mass Transfer", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Adv. Mech. Eng. Design", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Industrial Eng. & Management", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4
                v /= 13
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "ME" and c == "BE" and y == "THIRD" and s == "SEM-6") or (d == "ME" and c == "BTECH" and y == "THIRD" and s == "SEM-6")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Internal Combustion Engines", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Mechanical Vibrations", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Production Technology", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Computer Aided Design", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4
                v /= 13
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "ME" and c == "BE" and y == "FOURTH" and s == "SEM-7") or (d == "ME" and c == "BTECH" and y == "FOURTH" and s == "SEM-7")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Measurements & Instructions", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Energy Conservation Equipments", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Operations Research", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Industrial Eng. & Management", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4
                v /= 13
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "ME" and c == "BE" and y == "FOURTH" and s == "SEM-8") or (d == "ME" and c == "BTECH" and y == "FOURTH" and s == "SEM-8")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Advanced Fluid Mechanics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Computer Sided Manufacturing", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Automobile Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Finite Element Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4
                v /= 13
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        # if(d == "ME" and c == "BTECH" and y == "FIRST" and s == "SEM-1"):
        #     print()
        #
        # if(d == "ME" and c == "BTECH" and y == "FIRST" and s == "SEM-2"):
        #     print()
        #
        # if(d == "ME" and c == "BTECH" and y == "SECOND" and s == "SEM-3"):
        #     print()
        #
        # if(d == "ME" and c == "BTECH" and y == "SECOND" and s == "SEM-4"):
        #     print()
        #
        # if(d == "ME" and c == "BTECH" and y == "THIRD" and s == "SEM-5"):
        #     print()
        #
        # if(d == "ME" and c == "BTECH" and y == "THIRD" and s == "SEM-6"):
        #     print()
        #
        # if(d == "ME" and c == "BTECH" and y == "FOURTH" and s == "SEM-7"):
        #     print()
        #
        # if(d == "ME" and c == "BTECH" and y == "FOURTH" and s == "SEM-8"):
        #     print()

        # if(d == "ME" and c == "MTECH" and y == "FIRST" and s == "SEM-1"):
        #     print()
        #
        # if(d == "ME" and c == "MTECH" and y == "FIRST" and s == "SEM-2"):
        #     print()
        #
        # if(d == "ME" and c == "MTECH" and y == "SECOND" and s == "SEM-3"):
        #     print()
        #
        # if(d == "ME" and c == "MTECH" and y == "SECOND" and s == "SEM-4"):
        #     print()
        #
        # if(d == "ME" and c == "MTECH" and y == "THIRD" and s == "SEM-5"):
        #     print()
        #
        # if(d == "ME" and c == "MTECH" and y == "THIRD" and s == "SEM-6"):
        #     print()
        #
        # if(d == "ME" and c == "MTECH" and y == "FOURTH" and s == "SEM-7"):
        #     print()
        #
        # if(d == "ME" and c == "MTECH" and y == "FOURTH" and s == "SEM-8"):
        #     print()

        if((d == "CE" and c == "BE" and y == "FIRST" and s == "SEM-1") or (d == "CE" and c == "BTECH" and y == "FIRST" and s == "SEM-1")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Biochemical Eng. & Bioinformatics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Corrosion Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Nanotechnology", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Metallurgy", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Process Design, Contol & Develop.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Thermodynamics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="Paper Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            Label(windows, text="Textile Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s8.current(0)
            s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2 + dict[str(s8.get())] * 2
                v /= 24
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0 or dict[str(s8.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CE" and c == "BE" and y == "FIRST" and s == "SEM-2") or (d == "CE" and c == "BTECH" and y == "FIRST" and s == "SEM-2")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Plastics Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Nuclear Reprocessing", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Industrial Gas", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Corrosion & Environmental Eng.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Chemical Process Modelling", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Biomedical Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="Study of Chemical Reactors", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            Label(windows, text="Electrochemistry", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s8.current(0)
            s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2 + dict[str(s8.get())] * 2
                v /= 24
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0 or dict[str(s8.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CE" and c == "BE" and y == "SECOND" and s == "SEM-3") or (d == "CE" and c == "BTECH" and y == "SECOND" and s == "SEM-3")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Engineering Chemistry - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Process Calculations", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Applied Mathematics - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Chemical Eng. Thermodynamics - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Fluid Flow Operations(FFO)", font=("Arial", 17), fg="black", bg="white").place(x=80,y=240)
            Label(windows, text="Chemical Technology", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="Eng. Chemistry(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80,y=320)
            Label(windows, text="Chemical Eng.(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s8.current(0)
            s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2 + dict[str(s8.get())] * 2
                v /= 24
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0 or dict[str(s8.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CE" and c == "BE" and y == "SECOND" and s == "SEM-4") or (d == "CE" and c == "BTECH" and y == "SECOND" and s == "SEM-4")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Eng. Chemistry - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Mechanical Equipment Design", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Applied Mathematics - IV", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Chemical Eng. Thermodynamics - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Solid-Fluid Mechanical Operations(SFMO)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Chemical Eng. Economics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="Engineering II(Lab)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)
            Label(windows, text="Chemical Eng. Lab III(SFMO)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=360)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=360)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)
            s8 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s8["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s8.current(0)
            s8.place(x=700, y=360)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2 + dict[str(s8.get())] * 2
                v /= 24
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0 or dict[str(s8.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CE" and c == "BE" and y == "THIRD" and s == "SEM-5") or (d == "CE" and c == "BTECH" and y == "THIRD" and s == "SEM-5")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Business Comm. & Ethics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Chemical Reaction Eng. - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Mass Transfer Operation - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Heat Transfer Operations(HTO)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Electives", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3
                v /= 16
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CE" and c == "BE" and y == "THIRD" and s == "SEM-6") or (d == "CE" and c == "BTECH" and y == "THIRD" and s == "SEM-6")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Transport Phenomenon", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Chemical Reaction Eng. - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Mass Transfer Operations - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Environmental Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Electives", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3
                v /= 16
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CE" and c == "BE" and y == "FOURTH" and s == "SEM-7") or (d == "CE" and c == "BTECH" and y == "FOURTH" and s == "SEM-7")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Process Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Process Equipment Design(PED)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Process Dynamics & Control(PDC)", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Electives", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Project/Seminar", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3
                v /= 16
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CE" and c == "BE" and y == "FOURTH" and s == "SEM-8") or (d == "CE" and c == "BTECH" and y == "FOURTH" and s == "SEM-8")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Energy Stream Design", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Modelling, Simulation & Optimization", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Project Eng. Management", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Electives", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Project/Seminar", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3
                v /= 16
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        # if(d == "CE" and c == "BTECH" and y == "FIRST" and s == "SEM-1"):
        #     print()
        #
        # if(d == "CE" and c == "BTECH" and y == "FIRST" and s == "SEM-2"):
        #     print()
        #
        # if(d == "CE" and c == "BTECH" and y == "SECOND" and s == "SEM-3"):
        #     print()
        #
        # if(d == "CE" and c == "BTECH" and y == "SECOND" and s == "SEM-4"):
        #     print()
        #
        # if(d == "CE" and c == "BTECH" and y == "THIRD" and s == "SEM-5"):
        #     print()
        #
        # if(d == "CE" and c == "BTECH" and y == "THIRD" and s == "SEM-6"):
        #     print()
        #
        # if(d == "CE" and c == "BTECH" and y == "FOURTH" and s == "SEM-7"):
        #     print()
        #
        # if(d == "CE" and c == "BTECH" and y == "FOURTH" and s == "SEM-8"):
        #     print()

        # if(d == "CE" and c == "MTECH" and y == "FIRST" and s == "SEM-1"):
        #     print()
        #
        # if(d == "CE" and c == "MTECH" and y == "FIRST" and s == "SEM-2"):
        #     print()
        #
        # if(d == "CE" and c == "MTECH" and y == "SECOND" and s == "SEM-3"):
        #     print()
        #
        # if(d == "CE" and c == "MTECH" and y == "SECOND" and s == "SEM-4"):
        #     print()
        #
        # if(d == "CE" and c == "MTECH" and y == "THIRD" and s == "SEM-5"):
        #     print()
        #
        # if(d == "CE" and c == "MTECH" and y == "THIRD" and s == "SEM-6"):
        #     print()
        #
        # if(d == "CE" and c == "MTECH" and y == "FOURTH" and s == "SEM-7"):
        #     print()
        #
        # if(d == "CE" and c == "MTECH" and y == "FOURTH" and s == "SEM-8"):
        #     print()

        if((d == "CIVIL" and c == "BE" and y == "FIRST" and s == "SEM-1") or (d == "CIVIL" and c == "BTECH" and y == "FIRST" and s == "SEM-1")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Engineering Maths - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Engineering Physics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Engineering Chemistry", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Systems in Mechanical Eng.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Basic Elect./Electro. Eng.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Engineering Mechanics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="Workshop", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2
                v /= 22
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CIVIL" and c == "BE" and y == "FIRST" and s == "SEM-2") or (d == "CIVIL" and c == "BTECH" and y == "FIRST" and s == "SEM-2")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Engineering Maths - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Engineering Phy/Chem", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Basic Elect./Eletro. Eng.", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Engineering Mechanics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Engineering Graphics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Project Based Learning", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)
            Label(windows, text="Physical Education", font=("Arial", 17), fg="black", bg="white").place(x=80, y=320)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)
            Label(windows, text="2", font=("Arial", 17), fg="black", bg="white").place(x=480, y=320)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)
            s7 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s7["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s7.current(0)
            s7.place(x=700, y=320)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4 + dict[str(s7.get())] * 2
                v /= 22
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0 or dict[str(s7.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CIVIL" and c == "BE" and y == "SECOND" and s == "SEM-3") or (d == "CIVIL" and c == "BTECH" and y == "SECOND" and s == "SEM-3")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Building Tech. & Archi. Planning", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Mechanics of Structure", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Fluid Mechanics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Engineering Maths - III", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Engineering Geology", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Electives", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4
                v /= 20
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CIVIL" and c == "BE" and y == "SECOND" and s == "SEM-4") or (d == "CIVIL" and c == "BTECH" and y == "SECOND" and s == "SEM-4")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Geotechnical Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Survey", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Concrete Technology", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Structural Analysis", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Project Management", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)
            Label(windows, text="Project Based Learning", font=("Arial", 17), fg="black", bg="white").place(x=80, y=280)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=280)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)
            s6 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s6["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s6.current(0)
            s6.place(x=700, y=280)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3 + dict[str(s6.get())] * 4
                v /= 20
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0 or dict[str(s6.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CIVIL" and c == "BE" and y == "THIRD" and s == "SEM-5") or (d == "CIVIL" and c == "BTECH" and y == "THIRD" and s == "SEM-5")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Hydrology Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Infrastructure Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Structural Design - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Structural Analysis - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Fluid Mechanics - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3
                v /= 16
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CIVIL" and c == "BE" and y == "THIRD" and s == "SEM-6") or (d == "CIVIL" and c == "BTECH" and y == "THIRD" and s == "SEM-6")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Advanced Surveying", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Engineering Economics", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Foundation Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)
            Label(windows, text="Structural Design - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=200)
            Label(windows, text="Environmental Eng. - I", font=("Arial", 17), fg="black", bg="white").place(x=80, y=240)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)
            Label(windows, text="4", font=("Arial", 17), fg="black", bg="white").place(x=480, y=200)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=240)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)
            s4 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s4["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s4.current(0)
            s4.place(x=700, y=200)
            s5 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s5["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s5.current(0)
            s5.place(x=700, y=240)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3 + dict[str(s4.get())] * 4 + dict[str(s5.get())] * 3
                v /= 16
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0 or dict[str(s4.get())] == 0 or dict[str(s5.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CIVIL" and c == "BE" and y == "FOURTH" and s == "SEM-7") or (d == "CIVIL" and c == "BTECH" and y == "FOURTH" and s == "SEM-7")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Environmental Eng. - II", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Transport Engineering", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Structural Design - III", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3
                v /= 9
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        if((d == "CIVIL" and c == "BE" and y == "FOURTH" and s == "SEM-8") or (d == "CIVIL" and c == "BTECH" and y == "FOURTH" and s == "SEM-8")):
            windows = Tk()
            windows.title("Subjects")
            windows.iconbitmap('Images/icon.ico')
            windows.geometry('1000x500')
            windows.configure(bg="white")

            Label(windows, text="Subjects", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=80, y=30)
            Label(windows, text="Credit", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=480, y=30)
            Label(windows, text="Grade", font=("Arial", 20, "bold"), fg="brown", bg="white").place(x=700, y=30)

            Label(windows, text="Dams & Hydraulic Structures", font=("Arial", 17), fg="black", bg="white").place(x=80, y=80)
            Label(windows, text="Quantity Surveying", font=("Arial", 17), fg="black", bg="white").place(x=80, y=120)
            Label(windows, text="Electives", font=("Arial", 17), fg="black", bg="white").place(x=80, y=160)

            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=80)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=120)
            Label(windows, text="3", font=("Arial", 17), fg="black", bg="white").place(x=480, y=160)

            s1 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s1["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s1.current(0)
            s1.place(x=700, y=80)
            s2 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s2["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s2.current(0)
            s2.place(x=700, y=120)
            s3 = ttk.Combobox(windows, font=("Arial", 10), width=10, state="readonly")
            s3["values"] = ("NA", "EX", "A", "B", "C", "D", "P", "F")
            s3.current(0)
            s3.place(x=700, y=160)

            def confirm_fun():
                global var_sgpa
                v = dict[str(s1.get())] * 3 + dict[str(s2.get())] * 3 + dict[str(s3.get())] * 3
                v /= 9
                v = round(v, 2)
                # ix.) if student fails in any subject in any course, his/her sgpa = 0.0
                if (dict[str(s1.get())] == 0 or dict[str(s2.get())] == 0 or dict[str(s3.get())] == 0):
                    v = 0.0
                var_sgpa = str(v)
                windows.destroy()

            Button(windows, text="Confirm", command=confirm_fun, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=435, y=410)
            window.mainloop()

        # if(d == "CIVIL" and c == "BTECH" and y == "FIRST" and s == "SEM-1"):
        #     print()
        #
        # if(d == "CIVIL" and c == "BTECH" and y == "FIRST" and s == "SEM-2"):
        #     print()
        #
        # if(d == "CIVIL" and c == "BTECH" and y == "SECOND" and s == "SEM-3"):
        #     print()
        #
        # if(d == "CIVIL" and c == "BTECH" and y == "SECOND" and s == "SEM-4"):
        #     print()
        #
        # if(d == "CIVIL" and c == "BTECH" and y == "THIRD" and s == "SEM-5"):
        #     print()
        #
        # if(d == "CIVIL" and c == "BTECH" and y == "THIRD" and s == "SEM-6"):
        #     print()
        #
        # if(d == "CIVIL" and c == "BTECH" and y == "FOURTH" and s == "SEM-7"):
        #     print()
        #
        # if(d == "CIVIL" and c == "BTECH" and y == "FOURTH" and s == "SEM-8"):
        #     print()

        # if(d == "CIVIL" and c == "MTECH" and y == "FIRST" and s == "SEM-1"):
        #     print()
        #
        # if(d == "CIVIL" and c == "MTECH" and y == "FIRST" and s == "SEM-2"):
        #     print()
        #
        # if(d == "CIVIL" and c == "MTECH" and y == "SECOND" and s == "SEM-3"):
        #     print()
        #
        # if(d == "CIVIL" and c == "MTECH" and y == "SECOND" and s == "SEM-4"):
        #     print()
        #
        # if(d == "CIVIL" and c == "MTECH" and y == "THIRD" and s == "SEM-5"):
        #     print()
        #
        # if(d == "CIVIL" and c == "MTECH" and y == "THIRD" and s == "SEM-6"):
        #     print()
        #
        # if(d == "CIVIL" and c == "MTECH" and y == "FOURTH" and s == "SEM-7"):
        #     print()
        #
        # if(d == "CIVIL" and c == "MTECH" and y == "FOURTH" and s == "SEM-8"):
        #     print()

    def create_password(self):
        # creating password
        MAX_LEN = 12

        DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's','t', 'u', 'v', 'w', 'x', 'y', 'z']
        UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q', 'R', 'S','T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '*', '(', ')', '<']

        # combines all the character arrays above to form one array
        COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

        # randomly select at least one character from each character set above
        rand_digit = random.choice(DIGITS)
        rand_upper = random.choice(UPCASE_CHARACTERS)
        rand_lower = random.choice(LOCASE_CHARACTERS)
        rand_symbol = random.choice(SYMBOLS)

        temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

        temp_pass_list = []
        for x in range(MAX_LEN - 4):
            temp_pass = temp_pass + random.choice(COMBINED_LIST)
            temp_pass_list = array.array('u', temp_pass)
            random.shuffle(temp_pass_list)

        password = ""
        for x in temp_pass_list:
            password = password + x
        return password

    # SAVE BUTTON FUNCTION
    def save_data(self):
        global var_sgpa, fname
        conn1 = mysql.connector.connect(host="localhost", username="root", password="blanklogin!1",database="dbms_project")
        my_cursor1 = conn1.cursor()

        if self.var_dep.get() != "Select Department" or self.var_course.get() != "Select Course" or self.var_year.get() != "Select Year" or self.var_semester.get() != "Select Semester" or self.var_sid.get() != ""  or self.var_sname.get() != "" or self.var_reg.get() != "" or self.var_roll.get() != "" or self.var_gender.get() != "Select Gender" or self.var_email.get() != "" or self.var_phone.get() != "" or self.var_address.get() != "" or self.var_teacher.get() != "":
            query1 = f"select * from students where sid={self.var_sid.get()}"
            my_cursor1.execute(query1)
            x1 = my_cursor1.fetchall() # x1 is list(mutable) of tuple(immutable)
            conn1.close()
            # print(query1, x1)
            # print(type(x1), type(x1[0]))

            # vii.) duplicate row cannot be inserted
            lis = []
            lis.append(self.var_dep.get())
            lis.append(self.var_course.get())
            lis.append(self.var_year.get())
            lis.append(self.var_semester.get())
            lis.append(int(self.var_sid.get()))
            lis.append(self.var_sname.get())
            lis.append(self.var_reg.get())
            lis.append(self.var_roll.get())
            lis.append(self.var_gender.get())
            lis.append(self.var_dob.get())
            lis.append(self.var_email.get())
            lis.append(self.var_phone.get())
            lis.append(self.var_address.get())
            lis.append(self.var_teacher.get())
            for x in x1:
                lis1 = []
                for i in range(0,14):
                    lis1.append(x[i])
                if(lis1 == lis):
                    messagebox.showerror("Error", "Duplicate Data cannot be inserted.", parent=self.root)
                    return

            # iv.) checking details must match with the existing student
            if(len(x1)>0):
                if(self.var_dep.get() != x1[0][0] or self.var_course.get() != x1[0][1] or self.var_sname.get() != x1[0][5] or self.var_reg.get() != x1[0][6] or self.var_roll.get() != x1[0][7] or self.var_gender.get() != x1[0][8] or self.var_dob.get() != x1[0][9] or self.var_email.get() != x1[0][10] or self.var_phone.get() != x1[0][11] or self.var_address.get() != x1[0][12]):
                    messagebox.showerror("Error", "Details not matching with registered student", parent=self.root)
                    return
            # i.) checking that batch mentor must be same
            if (self.var_teacher.get() != fname):
                messagebox.showerror("Error", "Batch Mentor must be yourself.", parent=self.root)
                return
            # iii.) checking that year and semester are selected in pair that matches
            if ((self.var_year.get() == "FIRST" and (self.var_semester.get() != "SEM-1" and self.var_semester.get() != "SEM-2")) or (self.var_year.get() == "SECOND" and (self.var_semester.get() != "SEM-3" and self.var_semester.get() != "SEM-4")) or (self.var_year.get() == "THIRD" and (self.var_semester.get() != "SEM-5" and self.var_semester.get() != "SEM-6")) or (self.var_year.get() == "FOURTH" and (self.var_semester.get() != "SEM-7" and self.var_semester.get() != "SEM-8"))):
                messagebox.showerror("Error", "Year and Semester details are not matching.", parent=self.root)
                return
            # v.) If a student is in a particular sem and year, then he/she will be able to get registered only for the next combination of year and semester
            if(len(x1)==8 and float(x1[7][14])>0.0):
                messagebox.showerror("Error", "Student has completed this course.", parent=self.root)
                return
            # print(dict1[self.var_semester.get()])
            # print(len(x1))
            if(len(x1)==0 and dict1[self.var_semester.get()]>1):
                messagebox.showerror("Error", "Student can't register for this course.", parent=self.root)
                return
            if(len(x1)>0):
                if(((dict1[self.var_semester.get()]-len(x1))!=1) or (dict1[self.var_semester.get()] == len(x1)+1  and float(x1[len(x1)-1][14])==0.0)):
                    messagebox.showerror("Error", "Student can't register for this course.", parent=self.root)
                    return

        # checking that all the field must be filled
        if self.var_dep.get() == "Select Department" or self.var_course.get() == "Select Course" or self.var_year.get() == "Select Year" or self.var_semester.get() == "Select Semester" or self.var_sid.get() == ""  or self.var_sname.get() == "" or self.var_reg.get() == "" or self.var_roll.get() == "" or self.var_gender.get() == "Select Gender" or self.var_email.get() == "" or self.var_phone.get() == "" or self.var_address.get() == "" or self.var_teacher.get() == "":
            messagebox.showerror("Error","All fields are Required",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",username="root",password="blanklogin!1",database="dbms_project")
                my_cursor=conn.cursor()
                my_cursor.execute("insert into students values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.var_dep.get(),self.var_course.get(),self.var_year.get(),self.var_semester.get(),self.var_sid.get(),self.var_sname.get(),self.var_reg.get(),self.var_roll.get(),self.var_gender.get(),self.var_dob.get(),self.var_email.get(),self.var_phone.get(),self.var_address.get(),self.var_teacher.get(), var_sgpa))

                # creating random password
                password = self.create_password()

                my_cursor.execute(f"select * from student1 where stud_id={self.var_sid.get()}")
                x2 = my_cursor.fetchall()
                if(len(x2)==0):
                    my_cursor.execute("insert into student1 values(%s,%s,%s)", (self.var_sid.get(), self.var_email.get(), password))

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Student has been added successfully",parent=self.root)

                # ii.) if student id is already registered, then login details will not be sent again
                if(len(x2)==0):
                    ## sending emails to student regarding student id and password
                    # email part
                    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
                    smtpserver.ehlo()
                    smtpserver.starttls()
                    smtpserver.ehlo()
                    smtpserver.login('aakashrajak02@gmail.com', 'blanklogin!1')
                    subject = "Login Details for Student"
                    email_body = "Your Student ID is : " + str(self.var_sid.get()) + "\nYour password is : " + password
                    finalMessage = 'Subject: {}\n\n{} '.format(subject, email_body)
                    smtpserver.sendmail("aakashrajak02@gmail.com",self.var_email.get() , finalMessage)
                    messagebox.showinfo("Success", "Student Login Details Sent Successfully.")

            except Exception as es:
                messagebox.showerror("Error",f"Due to {str(es)}",parent=self.root)
    
    # UPDATE BUTTON FUNCTION
    def update_data(self):
        global var_sgpa, fname, prev_id
        conn1 = mysql.connector.connect(host="localhost", username="root", password="blanklogin!1",database="dbms_project")
        my_cursor1 = conn1.cursor()

        if self.var_dep.get() != "Select Department" or self.var_course.get() != "Select Course" or self.var_year.get() != "Select Year" or self.var_semester.get() != "Select Semester" or self.var_sid.get() != "" or self.var_sname.get() != "" or self.var_reg.get() != "" or self.var_roll.get() != "" or self.var_gender.get() != "Select Gender" or self.var_email.get() != "" or self.var_phone.get() != "" or self.var_address.get() != "" or self.var_teacher.get() != "":
            query1 = f"select * from students where sid={self.var_sid.get()}"
            my_cursor1.execute(query1)
            x1 = my_cursor1.fetchall()
            conn1.close()
            # print(query1, x1)

            # vii.) duplicate row cannot be inserted
            lis = []
            lis.append(self.var_dep.get())
            lis.append(self.var_course.get())
            lis.append(self.var_year.get())
            lis.append(self.var_semester.get())
            lis.append(int(self.var_sid.get()))
            lis.append(self.var_sname.get())
            lis.append(self.var_reg.get())
            lis.append(self.var_roll.get())
            lis.append(self.var_gender.get())
            lis.append(self.var_dob.get())
            lis.append(self.var_email.get())
            lis.append(self.var_phone.get())
            lis.append(self.var_address.get())
            lis.append(self.var_teacher.get())
            lis.append(var_sgpa)
            for x in x1:
                lis1 = list(x)
                if (lis1 == lis):
                    messagebox.showerror("Error", "Duplicate Data cannot be inserted.", parent=self.root) # this will also come when sgpa is update but it came out to be same
                    return

            # iv.) checking details must match with the existing student
            if (len(x1) > 0):
                if (self.var_dep.get() != x1[0][0] or self.var_course.get() != x1[0][1] or self.var_sname.get() != x1[0][5] or self.var_reg.get() != x1[0][6] or self.var_roll.get() != x1[0][7] or self.var_gender.get() != x1[0][8] or self.var_dob.get() != x1[0][9] or self.var_email.get() != x1[0][10] or self.var_phone.get() != x1[0][11] or self.var_address.get() != x1[0][12]):
                    messagebox.showerror("Error", "Details not matching with registered student", parent=self.root)
                    return

        # i.) checking that batch mentor must be same
        if (self.var_teacher.get() != fname):
            messagebox.showerror("Error", "Batch Mentor must be yourself", parent=self.root)
            return
        # iii.) checking that year and semester are selected in pair that matches
        if ((self.var_year.get() == "FIRST" and (self.var_semester.get() != "SEM-1" and self.var_semester.get() != "SEM-2")) or (self.var_year.get() == "SECOND" and (self.var_semester.get() != "SEM-3" and self.var_semester.get() != "SEM-4")) or (self.var_year.get() == "THIRD" and (self.var_semester.get() != "SEM-5" and self.var_semester.get() != "SEM-6")) or (self.var_year.get() == "FOURTH" and (self.var_semester.get() != "SEM-7" and self.var_semester.get() != "SEM-8"))):
            messagebox.showerror("Error", "Year and Semester details are not matching.", parent=self.root)
            return
        # vi.) will not be able to update the student id
        if (self.var_sid.get() != prev_id):
            messagebox.showerror("Error", "Student Id cannot be changed.", parent=self.root)
            return

        if self.var_dep.get() == "Select Department" or self.var_course.get() == "Select Course" or self.var_year.get() == "Select Year" or self.var_semester.get() == "Select Semester" or self.var_sid.get() == ""  or self.var_sname.get() == "" or self.var_reg.get() == "" or self.var_roll.get() == "" or self.var_gender.get() == "Select Gender" or self.var_email.get() == "" or self.var_phone.get() == "" or self.var_address.get() == "" or self.var_teacher.get() == "":
            messagebox.showerror("Error","All fields are Required",parent=self.root)
        else:
            try:
                update=messagebox.askyesno("Update","Do you want to update the details",parent=self.root)
                if update>0:
                    conn=mysql.connector.connect(host="localhost",username="root",password="blanklogin!1",database="dbms_project")
                    my_cursor=conn.cursor()
                    # x.) update will be done, for student with stud_id, sem comparison, not only stud_id(as it is not primary key)
                    my_cursor.execute("update students set dep=%s,course=%s,sname=%s,reg=%s,roll=%s,gender=%s,dob=%s,email=%s,phone=%s,address=%s,teacher=%s,sgpa=%s  where sid=%s and semester=%s",(self.var_dep.get(),self.var_course.get(),self.var_sname.get(),self.var_reg.get(),self.var_roll.get(),self.var_gender.get(),self.var_dob.get(),self.var_email.get(),self.var_phone.get(),self.var_address.get(),self.var_teacher.get(),var_sgpa,self.var_sid.get(),self.var_semester.get()))
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Success","Details updated Successfully",parent=self.root)
                else:
                    return
            except Exception as es:
                messagebox.showerror("Error",f"Due to {str(es)}",parent=self.root)

    # DELETE BUTTON FUNCTION
    def delete_data(self):
        if self.var_sid.get()=="":
            messagebox.showerror("Error","Student id must be Required",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Delete","Do you want to delete the Student",parent=self.root)
                if delete>0:
                    conn=mysql.connector.connect(host="localhost",username="root",password="blanklogin!1",database="dbms_project")
                    my_cursor=conn.cursor()
                    my_cursor.execute("delete from students where sid=%s",(self.var_sid.get(),))
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Success","Student deleted Successfully",parent=self.root)
                else:
                    return
            except Exception as es:
                messagebox.showerror("Error",f"Due to {str(es)}",parent=self.root)
    
    # RESET BUTTON FUNCTION
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_sid.set("")
        self.var_sname.set("")
        self.var_reg.set("")
        self.var_roll.set("")
        self.var_gender.set("Select Gender")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")

    # FETCH DATA INTO TABLE  FROM DATABASE
    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="blanklogin!1",database="dbms_project")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from students")
        data = my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    # FETCH DATA AFTER CLICKING ON SEARCH BUTTON
    def search_func(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="blanklogin!1",
                                       database="dbms_project")
        my_cursor = conn.cursor()
        if self.var_searchby.get() == "Select":
            messagebox.showerror("Error", "Select an Attribute", parent=self.root)
        if self.var_searchby.get() == "Student Id":
            my_cursor.execute("select * from students where sid =%s", (self.var_searchentry.get(),))
        if self.var_searchby.get() == "Student Name":
            my_cursor.execute("select * from students where sname =%s", (self.var_searchentry.get(),))
        if self.var_searchby.get() == "Department":
            my_cursor.execute("select * from students where dep =%s", (self.var_searchentry.get().upper(),))
        if self.var_searchby.get() == "Course":
            my_cursor.execute("select * from students where course =%s", (self.var_searchentry.get().upper(),))
        if self.var_searchby.get() == "Reg_No":
            my_cursor.execute("select * from students where reg =%s", (self.var_searchentry.get(),))
        if self.var_searchby.get() == "Gender":
            my_cursor.execute("select * from students where gender =%s", (self.var_searchentry.get().upper(),))
        if self.var_searchby.get() == "Address":
            my_cursor.execute("select * from students where address =%s", (self.var_searchentry.get(),))
        if self.var_searchby.get() == "Batch_Mentor":
            my_cursor.execute("select * from students where teacher =%s", (self.var_searchentry.get(),))

        data = my_cursor.fetchall()

        if len(data) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("", END, values=i)
            conn.commit()
        else:
            self.student_table.delete(*self.student_table.get_children())
            messagebox.showerror("Error", "No data found", parent=self.root)
        conn.close()

    # SET DATA INTO ENTRY FILLS FROM TABLE
    def set_data(self,event=""):
        global prev_id
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]

        prev_id = str(data[4])
        self.var_dep.set(data[0]),
        self.var_course.set(data[1]),
        self.var_year.set(data[2]),
        self.var_semester.set(data[3]),
        self.var_sid.set(data[4]),
        self.var_sname.set(data[5]),
        self.var_reg.set(data[6]),
        self.var_roll.set(data[7]),
        self.var_gender.set(data[8]),
        self.var_dob.set(data[9]),
        self.var_email.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_address.set(data[12]),
        self.var_teacher.set(data[13]),

if __name__ == "__main__":
    ################
    window1 = Tk()
    window1.title("Student & Course Management System")
    window1.iconbitmap('Images/icon.ico')
    window1.geometry('1200x780')
    window1.configure(bg = "white")

    # image on the main window
    path = "Images/iiitkalayani.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = Label(window1, image=img)
    panel.place(x=80, y=20)

    # top label
    start1 = Label(text="STUDENT  &  COURSE\nMANAGEMENT  SYSTEM", font=("Arial", 45, "underline","bold","italic"),fg="magenta", bg = "white")  # same way bg
    start1.place(x=400, y=55)

    # function defined to start the main application
    def start_fun():
        window1.destroy()

    # created a start button
    # Button(window1, text="▶ START", command=start_fun, font=("Arial", 25), bg="orange", fg="blue", cursor="hand2",
    #        borderwidth=3, relief="raised").place(x=940, y=350)



    ## student login window
    def student_loginsignup_fun():
        window1.destroy()

        window2 = Tk()
        window2.title("Student Login")
        window2.iconbitmap('Images/icon.ico')
        window2.geometry('1200x750')
        window2.configure(bg="white")

        Label(window2, text="LOGIN", font=("Arial", 40, "bold"), fg="brown",bg="white").place(x=500, y=55)

        # login user name
        Label(window2, text='Student ID', font=("Arial", 30), fg="black", bg = "white").place(x=400, y=160)
        # login username entry
        sid_entry = Entry(window2, font=("Arial", 25), fg='black', bg="light gray", borderwidth=3, width=22)
        sid_entry.place(x=400, y=210)
        # login password
        Label(window2, text='Password', font=("Arial", 30), fg="black", bg = "white").place(x=400, y=270)
        # login password entry
        studp_entry = Entry(window2, font=("Arial", 25), show = '*', fg='black', bg="light gray", borderwidth=3, width=22)
        studp_entry.place(x=400, y=320)

        def login_fun():
            global stud_id, exit1
            def student_view():
                window4 = Tk()
                window4.title("Student")
                window4.iconbitmap('Images/icon.ico')
                window4.geometry('1440x760')
                window4.configure(bg="white")

                path41 = "Images/kalyani.jpg"
                img41 = ImageTk.PhotoImage(Image.open(path41))
                panel41 = Label(window4, image=img41, bg = "white")
                panel41.place(x=60, y=50)

                path42 = "Images/book.jpg"
                img42 = ImageTk.PhotoImage(Image.open(path42))
                panel42 = Label(window4, image=img42, bg = "white")
                panel42.place(x=20, y=350)

                path43 = "Images/line.jpg"
                img43 = ImageTk.PhotoImage(Image.open(path43))
                panel43 = Label(window4, image=img43)
                panel43.place(x=350, y=100)

                path44 = "Images/line.jpg"
                img44 = ImageTk.PhotoImage(Image.open(path44))
                panel44 = Label(window4, image=img44)
                panel44.place(x=1050, y=100)


                db = mysql.connector.connect(host="localhost", username="root", password="blanklogin!1",database="dbms_project")
                my_db = db.cursor()
                query = f"select * from students where sid={stud_id}"
                my_db.execute(query)
                x = my_db.fetchall()

                Label(window4, text='SID : ' +str (x[0][4]), font=("Arial", 25, "bold"), fg="black", bg="white").place(x=680, y=20)
                Label(window4, text='Name', font=("Arial", 20), fg="black", bg="white").place(x=400, y=120)
                Label(window4, text='Reg No.', font=("Arial", 20), fg="black", bg="white").place(x=400, y=165)
                Label(window4, text='Roll No.', font=("Arial", 20), fg="black", bg="white").place(x=400, y=210)
                Label(window4, text='Gender', font=("Arial", 20), fg="black", bg="white").place(x=400, y=255)
                Label(window4, text='D.O.B.', font=("Arial", 20), fg="black", bg="white").place(x=400, y=300)
                Label(window4, text='Department', font=("Arial", 20), fg="black", bg="white").place(x=400, y=345)
                Label(window4, text='Course', font=("Arial", 20), fg="black", bg="white").place(x=400, y=390)
                # Label(window4, text='Sem', font=("Arial", 20), fg="black", bg="white").place(x=400, y=400)
                # Label(window4, text='Year', font=("Arial", 20), fg="black", bg="white").place(x=400, y=445)
                Label(window4, text='Address', font=("Arial", 20), fg="black", bg="white").place(x=400, y=435)
                Label(window4, text='Email ID', font=("Arial", 20), fg="black", bg="white").place(x=400, y=480)
                Label(window4, text='Ph No.', font=("Arial", 20), fg="black", bg="white").place(x=400, y=525)
                Label(window4, text='Batch Mentor', font=("Arial", 20), fg="black", bg="white").place(x=400, y=570)

                Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=120)
                Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=165)
                Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=210)
                Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=255)
                Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=300)
                Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=345)
                Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=390)
                # Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=400)
                # Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=445)
                Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=435)
                Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=480)
                Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=525)
                Label(window4, text=':', font=("Arial", 20), fg="black", bg="white").place(x=590, y=570)

                Label(window4, text=str(x[0][5]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=120)
                Label(window4, text=str(x[0][6]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=165)
                Label(window4, text=str(x[0][7]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=210)
                Label(window4, text=str(x[0][8]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=255)
                Label(window4, text=str(x[0][9]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=300)
                Label(window4, text=str(x[0][0]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=345)
                Label(window4, text=str(x[0][1]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=390)
                # Label(window4, text=str(x[0][3]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=400)
                # Label(window4, text=str(x[0][2]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=445)
                Label(window4, text=str(x[0][12]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=435)
                Label(window4, text=str(x[0][10]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=480)
                Label(window4, text=str(x[0][11]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=525)
                Label(window4, text=str(x[0][13]), font=("Arial", 20), fg="black", bg="white").place(x=630, y=570)

                Label(window4, text='SEM - 1   :', font=("Arial", 20, "bold"), fg="black", bg="white").place(x=1100, y=110)
                Label(window4, text='SEM - 2   :', font=("Arial", 20, "bold"), fg="black", bg="white").place(x=1100, y=170)
                Label(window4, text='SEM - 3   :', font=("Arial", 20, "bold"), fg="black", bg="white").place(x=1100, y=230)
                Label(window4, text='SEM - 4   :', font=("Arial", 20, "bold"), fg="black", bg="white").place(x=1100, y=290)
                Label(window4, text='SEM - 5   :', font=("Arial", 20, "bold"), fg="black", bg="white").place(x=1100, y=350)
                Label(window4, text='SEM - 6   :', font=("Arial", 20, "bold"), fg="black", bg="white").place(x=1100, y=410)
                Label(window4, text='SEM - 7   :', font=("Arial", 20, "bold"), fg="black", bg="white").place(x=1100, y=470)
                Label(window4, text='SEM - 8   :', font=("Arial", 20, "bold"), fg="black", bg="white").place(x=1100, y=530)
                Label(window4, text='CGPA   :', font=("Arial", 20, "bold"), fg="black", bg="white").place(x=1150,y=600)

                sgpa_lis = []
                v = 0.0
                c = 0
                # print(x)
                for i in range(0,8):
                    if(i<len(x) and x[i][14]!="0.0"):
                        sgpa_lis.append(x[i][14])
                        v = v + float(x[i][14])
                        c = c + 1
                    else:
                        sgpa_lis.append("")
                v /= c
                v = round(v, 2)
                cgpa = str(v)

                Label(window4, text=sgpa_lis[0], font=("Arial", 20), fg="black", bg="white").place(x=1260,y=110)
                Label(window4, text=sgpa_lis[1], font=("Arial", 20), fg="black", bg="white").place(x=1260,y=170)
                Label(window4, text=sgpa_lis[2], font=("Arial", 20), fg="black", bg="white").place(x=1260,y=230)
                Label(window4, text=sgpa_lis[3], font=("Arial", 20), fg="black", bg="white").place(x=1260,y=290)
                Label(window4, text=sgpa_lis[4], font=("Arial", 20), fg="black", bg="white").place(x=1260,y=350)
                Label(window4, text=sgpa_lis[5], font=("Arial", 20), fg="black", bg="white").place(x=1260,y=410)
                Label(window4, text=sgpa_lis[6], font=("Arial", 20), fg="black", bg="white").place(x=1260,y=470)
                Label(window4, text=sgpa_lis[7], font=("Arial", 20), fg="black", bg="white").place(x=1260,y=530)
                Label(window4, text=cgpa, font=("Arial", 20, "bold"), fg="black", bg="white").place(x=1290, y=600)

                def grade_sheet():
                    pdf = FPDF(orientation='P', unit='mm', format='A4')
                    pdf.add_page()
                    pdf.set_font("Arial", "", 21)
                    pdf.set_text_color(0, 0, 0)
                    pdf.image('Images/Grade_Sheet.png', x=0, y=0, w=210, h=297)

                    if(len(x)>0):
                        pdf.text(60, 84, str(x[0][5]))
                        pdf.text(50, 98.5, str(x[0][4]))
                        pdf.text(130, 98.5, str(x[0][1]) + " - " + str(x[0][0]))
                        pdf.text(70, 128, sgpa_lis[0])
                        pdf.text(150, 128, sgpa_lis[1])
                        pdf.text(70, 143, sgpa_lis[2])
                        pdf.text(150, 143, sgpa_lis[3])
                        pdf.text(70, 159, sgpa_lis[4])
                        pdf.text(150, 159, sgpa_lis[5])
                        pdf.text(70, 175, sgpa_lis[6])
                        pdf.text(150, 175, sgpa_lis[7])
                        pdf.text(70, 205, cgpa)
                        if(c==8):
                            pdf.text(83, 220, "Course Completed")
                        else:
                            pdf.text(83, 220, "Promoted to Sem - " + str(c+1))


                    pdf.output('Grade_Sheet.pdf')
                    messagebox.showinfo("Status", "Grade Sheet Generated.", parent=window4)

                    # sending gradesheet to student email id
                    # instance of MIMEMultipart
                    msg = MIMEMultipart()
                    # storing the senders email address
                    msg['From'] = "aakashrajak02@gmail.com"
                    # storing the receivers email address
                    msg['To'] = str(x[0][10])
                    # storing the subject
                    msg['Subject'] = "Grade Sheet"
                    # string to store the body of the mail
                    body = "Below is the attached grade sheet for course taken."
                    # attach the body with the msg instance
                    msg.attach(MIMEText(body, 'plain'))
                    # open the file to be sent
                    filename = "Grade_Sheet.pdf"
                    attachment = open("Grade_Sheet.pdf", "rb")
                    # instance of MIMEBase and named as p
                    p = MIMEBase('application', 'octet-stream')
                    # To change the payload into encoded form
                    p.set_payload((attachment).read())
                    # encode into base64
                    encoders.encode_base64(p)
                    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                    # attach the instance 'p' to instance 'msg'
                    msg.attach(p)
                    # creates SMTP session
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    # start TLS for security
                    s.starttls()
                    # Authentication
                    s.login("aakashrajak02@gmail.com", "blanklogin!1")
                    # Converts the Multipart msg into a string
                    text = msg.as_string()
                    # sending the mail
                    s.sendmail("aakashrajak02@gmail.com", str(x[0][10]), text)
                    # terminating the session
                    s.quit()
                    messagebox.showinfo("Status", "Grade Sheet emailed successfully.", parent=window4)

                Button(window4, text="Grade Sheet", command=grade_sheet, font=("Arial", 17), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=1170, y=655)

                def exit_win4():
                    if messagebox.askokcancel("Exit", "Do you want to exit?"):
                        window4.destroy()
                window4.protocol("WM_DELETE_WINDOW", exit_win4)
                window4.mainloop()

            stud_id = sid_entry.get()
            stud_password = studp_entry.get()

            if stud_id == "" or stud_password == "":
                messagebox.showerror("Error", "All fields are Required", parent=window2)
            else:
                try:
                    db = mysql.connector.connect(host="localhost", username="root", password="blanklogin!1",database="dbms_project")
                    my_db = db.cursor()
                    # str1 = "\""
                    query = f"select stud_password from student1 where stud_id={stud_id}"
                    my_db.execute(query)
                    x = my_db.fetchall()
                    if(x[0][0]==stud_password):
                        messagebox.showinfo("Success", "Login Successfull", parent=window2)
                        db.close()
                        window2.destroy()

                        exit1 = True
                        # student class window starts
                        student_view()
                    else:
                        messagebox.showerror("Error", "Wrong Credentials")
                except Exception as es:
                    messagebox.showerror("Error", f"Error : {str(es)}")

        def forgot_password_fun():
            window3 = Tk()
            window3.title("Forgot Password")
            window3.iconbitmap('Images/icon.ico')
            window3.geometry('500x200')
            window3.configure(bg="white")

            # email
            Label(window3, text='Email ID', font=("Arial", 25), fg="black", bg="white").place(x=170, y=20)
            # email entry
            eentry = Entry(window3, font=("Arial", 20), fg='black', bg="light gray", borderwidth=3, width=25)
            eentry.place(x=50, y=70)

            def submit_fun():
                em = eentry.get()

                db = mysql.connector.connect(host="localhost", username="root", password="blanklogin!1",database="dbms_project")
                my_db = db.cursor()
                str1 = "\""
                query = f"select stud_id, stud_password from student1 where email1={str1 + em + str1}"
                my_db.execute(query)
                x = my_db.fetchall()

                if(len(x)>0):
                    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
                    smtpserver.ehlo()
                    smtpserver.starttls()
                    smtpserver.ehlo()
                    smtpserver.login('aakashrajak02@gmail.com', 'blanklogin!1')
                    subject = "Password Recovery for DBMS Project"
                    email_body = "Your Student ID is : " + str(x[0][0]) + "\nYour password is : " + str(x[0][1])
                    finalMessage = 'Subject: {}\n\n{} '.format(subject, email_body)
                    smtpserver.sendmail("aakashrajak02@gmail.com", em, finalMessage)
                    db.close()
                    window3.destroy()
                    messagebox.showinfo("Success", "Email Sent Successfully.\nCheck your email.")
                else:
                    messagebox.showerror("Error", "Enter correct email.")

            Button(window3, text="Submit", command=submit_fun, font=("Arial", 15), bg="light green", fg="blue",
                   cursor="hand2", borderwidth=3, relief="raised").place(x=200, y=120)

            window3.mainloop()

        Button(window2, text="Forgot Password?", command=forgot_password_fun, font=("Arial", 12), bg="white", fg="blue", cursor="hand2",borderwidth=0, relief="raised").place(x=670, y=370)
        Button(window2, text="Login", command=login_fun, font=("Arial", 20), bg="orange", fg="blue", cursor="hand2",borderwidth=3, relief="raised").place(x=550, y=440)

        # function created for exiting from window
        def exit_win2():
            global exit1
            if messagebox.askokcancel("Exit", "Do you want to exit?"):
                exit1 = True
                window2.destroy()

        # exit button created
        Button(window2, text="❌ EXIT", command=exit_win2, font=("Arial", 20), bg="red", fg="blue", cursor="hand2",borderwidth=3, relief="raised").place(x=530, y=620)

        window2.protocol("WM_DELETE_WINDOW", exit_win2)
        window2.mainloop()


    ## faculty login window
    def faculty_loginsignup_fun():
        window1.destroy()

        window2 = Tk()
        window2.title("Faculty Login & Signup")
        window2.iconbitmap('Images/icon.ico')
        window2.geometry('1200x750')
        window2.configure(bg="white")

        Label(text="LOGIN", font=("Arial", 40, "bold"), fg="brown",bg="white").place(x=200, y=55)
        Label(text="SIGNUP", font=("Arial", 40, "bold"), fg="brown", bg="white").place(x=780, y=55)

        # line image
        path2 = "Images/line.jpg"
        img2 = ImageTk.PhotoImage(Image.open(path2))
        panel2 = Label(window2, image=img2)
        panel2.place(x=590, y=20)

        # login user name
        Label(window2, text='Username', font=("Arial", 30), fg="black", bg = "white").place(x=100, y=160)
        # login username entry
        lu_entry = Entry(window2, font=("Arial", 25), fg='black', bg="light gray", borderwidth=3, width=22)
        lu_entry.place(x=100, y=210)
        # login password
        Label(window2, text='Password', font=("Arial", 30), fg="black", bg = "white").place(x=100, y=270)
        # login password entry
        lp_entry = Entry(window2, font=("Arial", 25), show = '*', fg='black', bg="light gray", borderwidth=3, width=22)
        lp_entry.place(x=100, y=320)

        # signup user name
        Label(window2, text='Username', font=("Arial", 30), fg="black", bg="white").place(x=680, y=160)
        # signup username entry
        su_entry = Entry(window2, font=("Arial", 25), fg='black', bg="light gray", borderwidth=3, width=22)
        su_entry.place(x=680, y=210)
        # signup email
        Label(window2, text='Email ID', font=("Arial", 30), fg="black", bg="white").place(x=680, y=270)
        # signup email entry
        se_entry = Entry(window2, font=("Arial", 25), fg='black', bg="light gray", borderwidth=3, width=22)
        se_entry.place(x=680, y=320)
        # signup password
        Label(window2, text='Password', font=("Arial", 30), fg="black", bg="white").place(x=680, y=380)
        # signup password entry
        sp_entry = Entry(window2, font=("Arial", 25), show = '*', fg='black', bg="light gray", borderwidth=3, width=22)
        sp_entry.place(x=680, y=430)

        def login_fun():
            global lusername,susername
            lusername = lu_entry.get()
            lpassword = lp_entry.get()

            if lusername == "" or lpassword == "":
                messagebox.showerror("Error", "All fields are Required", parent=window2)
            else:
                try:
                    db = mysql.connector.connect(host="localhost", username="root", password="blanklogin!1",database="dbms_project")
                    my_db = db.cursor()
                    str1 = "\""
                    query = f"select pass_word from admin1 where user_name={str1 + lusername + str1}"
                    my_db.execute(query)
                    x = my_db.fetchall()
                    if(x[0][0]==lpassword):
                        messagebox.showinfo("Success", "Login Successfull", parent=window2)
                        window2.destroy()
                    else:
                        messagebox.showerror("Error", "Wrong Credentials", parent=window2)

                    db.close()
                except Exception as es:
                    messagebox.showerror("Error", f"Error : {str(es)}", parent=window2)


        def signup_fun():
            global lusername, susername
            susername = su_entry.get()
            spassword = sp_entry.get()
            semail = se_entry.get()

            if susername == "" or spassword == "":
                messagebox.showerror("Error", "All fields are Required", parent=window2)
            else:
                try:
                    db = mysql.connector.connect(host="localhost", username="root", password="blanklogin!1",database="dbms_project")
                    my_db = db.cursor()
                    my_db.execute("insert into admin1 values(%s,%s,%s)", (susername,spassword,semail))
                    db.commit()
                    db.close()
                    messagebox.showinfo("Success", "Account Created Successfully", parent=window2)
                    window2.destroy()
                except Exception as es:
                    messagebox.showerror("Error", f"Error : {str(es)}", parent=window2)

        def forgot_password_fun():
            window3 = Tk()
            window3.title("Forgot Password")
            window3.iconbitmap('Images/icon.ico')
            window3.geometry('500x200')
            window3.configure(bg="white")

            # email
            Label(window3, text='Email ID', font=("Arial", 25), fg="black", bg="white").place(x=170, y=20)
            # email entry
            eentry = Entry(window3, font=("Arial", 20), fg='black', bg="light gray", borderwidth=3, width=25)
            eentry.place(x=50, y=70)

            def submit_fun():
                em = eentry.get()

                db = mysql.connector.connect(host="localhost", username="root", password="blanklogin!1",database="dbms_project")
                my_db = db.cursor()
                str1 = "\""
                query = f"select user_name, pass_word from admin1 where email1={str1 + em + str1}"
                my_db.execute(query)
                x = my_db.fetchall()

                smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
                smtpserver.ehlo()
                smtpserver.starttls()
                smtpserver.ehlo()
                smtpserver.login('aakashrajak02@gmail.com', 'blanklogin!1')
                subject = "Password Recovery for DBMS Project"
                email_body = "Your Username is : " + str(x[0][0]) + "\nYour password is : " + str(x[0][1])
                finalMessage = 'Subject: {}\n\n{} '.format(subject, email_body)
                smtpserver.sendmail("aakashrajak02@gmail.com", em, finalMessage)
                db.close()
                window3.destroy()
                messagebox.showinfo("Success", "Email Sent Successfully.\nCheck your email.")

            Button(window3, text="Submit", command=submit_fun, font=("Arial", 15), bg="light green", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=200, y=120)

            window3.mainloop()

        Button(window2, text="Forgot Password?", command=forgot_password_fun, font=("Arial", 12), bg="white", fg="blue", cursor="hand2",borderwidth=0, relief="raised").place(x=370, y=370)
        Button(window2, text="Login", command=login_fun, font=("Arial", 20), bg="orange", fg="blue", cursor="hand2",borderwidth=3, relief="raised").place(x=250, y=440)
        Button(window2, text="Signup", command=signup_fun, font=("Arial", 20), bg="orange", fg="blue",cursor="hand2", borderwidth=3, relief="raised").place(x=830, y=500)

        # function created for exiting from window
        def exit_win2():
            global exit1
            if messagebox.askokcancel("Exit", "Do you want to exit?"):
                exit1 = True
                window2.destroy()

        # exit button created
        Button(window2, text="❌ EXIT", command=exit_win2, font=("Arial", 20), bg="red", fg="blue", cursor="hand2",borderwidth=3, relief="raised").place(x=530, y=620)

        window2.protocol("WM_DELETE_WINDOW", exit_win2)
        window2.mainloop()



    Button(window1, text="STUDENT", command=student_loginsignup_fun, font=("Arial", 20), bg="orange", fg="blue", cursor="hand2",borderwidth=3, relief="raised").place(x=930, y=350)
    Button(window1, text="FACULTY", command=faculty_loginsignup_fun, font=("Arial", 20), bg="orange", fg="blue",cursor="hand2",borderwidth=3, relief="raised").place(x=930, y=420)

    # image on the main window
    path1 = "Images/front.jpg"
    img1 = ImageTk.PhotoImage(Image.open(path1))
    panel1 = Label(window1, image=img1)
    panel1.place(x=80, y=270)

    # function created for exiting from window
    def exit_win1():
        global exit1
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            exit1 = True
            window1.destroy()

    # exit button created
    Button(window1, text="❌ EXIT", command=exit_win1, font=("Arial", 20), bg="red", fg="blue", cursor="hand2",borderwidth=3, relief="raised").place(x=940, y=600)

    window1.protocol("WM_DELETE_WINDOW", exit_win1)
    window1.mainloop()

    ###################
    if exit1==False:
        window = Tk()
        obj1 = faculty_class(window)

        def exit_win():
            if messagebox.askokcancel("Exit", "Do you want to exit?"):
                window.destroy()
        window.protocol("WM_DELETE_WINDOW", exit_win)
        window.mainloop()
