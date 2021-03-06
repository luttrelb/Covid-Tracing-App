import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Canvas, Frame, BOTH
import time as tm
import datetime as dt
import re
from getpass import getpass
from sqlalchemy import Column, Date, Integer, String
import urllib.request
import sys

class Application(tk.Frame):
    """
    COVID-19 Contact Tracing Desktop Application

    A program for a COVID-19 contact tracing desktop application that allows a
    user to make an account; upon doing so, they have access to various features,
    such as reading news and getting the latest data on COVID-19 as well as
    submitting contact tracting information.
    """

    # initializing the application
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """
        Creating the welcome page

        A function that creates all of the widgets for the welcome page and
        assigns commands to corresponding buttons to perform various actions.
        """

        # Greeting the user and requesting login credentials
        self.title = tk.Label(self, text="Welcome to MegaTrace",
        font=("Helvetica", 24))
        self.title.grid(row=0, column=1, pady=25)
        self.title = tk.Label(self, text="Please sign in to continue:",
        font=("Helvetica", 16))
        self.title.grid(row=1, column=1, pady=0)

        # Creating the login button that will open the login page
        self.login = tk.Button(self)
        self.login["text"] = "Login"
        self.login["font"] = ("Helvetica", 12, "bold")
        self.login["command"] = self.loginpage
        self.login.grid(row=2, column=1, pady=5)
        self.login.config(width=35, height=3)

        # Creating the sign up button that prompts the sign up page
        self.signUp = tk.Button(self)
        self.signUp["text"] = "Sign Up"
        self.signUp["font"] = ("Helvetica", 12, "bold")
        self.signUp["command"] = self.signUpPage2
        self.signUp.grid(row=3, column=1, pady=5)
        self.signUp.config(width=35, height=3)

        # Creating the quit button that exits the application
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=4, column=1, pady=5)
        self.quit.config(width=35, height=3)
        self.quit["font"] = ("Helvetica", 12, "bold")

    def signUpPage2(self):
        """
        Collecting new user information and creating a new account

        A function that creates the second sign up page where the user enters
        their information, including their first and last name, birthday, email,
        and phone number.  This information is not only necessary for account
        creation, but contact tracing as well.  The information is stored in a
        database, user_info_db.
        """

        signUpWindow2 = tk.Toplevel(root)
        signUpWindow2.title("Sign Up")
        signUpWindow2.geometry("450x400")

        conn = sqlite3.connect('sqlite:///C:\\Users\\Desktop\\user_info_db.db')

        # Creating the cursor to manipulate the database
        c = conn.cursor()

        # Creating the table for
        c.execute("""CREATE TABLE user_info (
                first_name text,
                last_name text,
                address text,
                city text,
                state text,
                zipcode integer,
                username text,
                password text
                )""")

        def submit_info():
            """
            Inserting the user's information to the database
            
            A function that will connect to the existing database and insert
            a user's information to the corresponding rows.  This information
            is collected from a user's entries into the text boxes in the 
            signup window.
            """
            
            # Create the user info DB
            conn = sqlite3.connect('sqlite:///user_info_db.db')

            # Create the cursor
            c = conn.cursor()

            # Insert information into the user_info table
            c.execute("""INSERT INTO user_info VALUES (:f_name, :l_name,
            :address, :city, :state, :zipcode, :u_name, :p_word)""",
                    {
                        'f_name': f_name.get(),
                        'l_name': l_name.get(),
                        'address': address.get(),
                        'city': city.get(),
                        'state': state.get(),
                        'zipcode': zipcode.get(),
                        'u_name': u_name.get(),
                        'p_word': p_word.get()
                    }

                    )

            conn.commit()
            conn.close()

            f_name.delete(0, tk.END)
            l_name.delete(0, tk.END)
            address.delete(0, tk.END)
            city.delete(0, tk.END)
            state.delete(0, tk.END)
            zipcode.delete(0, tk.END)
            u_name.delete(0, tk.END)
            p_word.delete(0, tk.END)

        def output_records():
            """
            Creating the querying function
            
            A function that will print the records of all users within
            the database.  
            """
            
            conn = sqlite3.connect('sqlite:///user_info_db.db')

            c = conn.cursor()

            c.execute("SELECT *, oid FROM user_info") # OID is primary key
            records = c.fetchall() # get all records

            print_records = ''
            for r in records:
                print_records += str(r) + "\n"

            query_label = tk.Label(signUpWindow2, text = print_records)
            query_label.grid(row = 10, column = 0, columnspan = 2)

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

        # Create text boxes
        f_name = tk.Entry(signUpWindow2, width = 30)
        f_name.grid(row = 0, column = 1, padx = 20)

        l_name = tk.Entry(signUpWindow2, width = 30)
        l_name.grid(row = 1, column = 1)

        address = tk.Entry(signUpWindow2, width = 30)
        address.grid(row = 2, column = 1)

        city = tk.Entry(signUpWindow2, width = 30)
        city.grid(row = 3, column = 1)

        state = tk.Entry(signUpWindow2, width = 30)
        state.grid(row = 4, column = 1)

        zipcode = tk.Entry(signUpWindow2, width = 30)
        zipcode.grid(row = 5, column = 1)

        u_name = tk.Entry(signUpWindow2, width = 30)
        u_name.grid(row = 6, column = 1)

        p_word = tk.Entry(signUpWindow2, show="*", width = 30)
        p_word.grid(row = 7, column = 1)

        # Create text box labels

        f_name_label = tk.Label(signUpWindow2, text = "First name")
        f_name_label.grid(row = 0, column = 0)

        l_name_label = tk.Label(signUpWindow2, text = "Last name")
        l_name_label.grid(row = 1, column = 0)

        address_label = tk.Label(signUpWindow2, text = "Address")
        address_label.grid(row = 2, column = 0)

        city_label = tk.Label(signUpWindow2, text = "City")
        city_label.grid(row = 3, column = 0)

        state_label = tk.Label(signUpWindow2, text = "State")
        state_label.grid(row = 4, column = 0)

        zipcode_label = tk.Label(signUpWindow2, text = "Zipcode")
        zipcode_label.grid(row = 5, column = 0)

        u_name_label = tk.Label(signUpWindow2, text = "Username")
        u_name_label.grid(row = 6, column = 0)

        p_word_label = tk.Label(signUpWindow2, text = "Password")
        p_word_label.grid(row = 7, column = 0)

        # Create submit button
        submit_btn = tk.Button(signUpWindow2, text = "Save",
        command = submit_info)
        submit_btn.grid(row = 8, column = 0, columnspan = 2, pady = 10,
        padx = 10, ipadx = 60)

        # Create query button
        query_btn = tk.Button(signUpWindow2, text = """Show records (for
        developemnt purposes)""", command = output_records)
        query_btn.grid(row = 9, column = 0, columnspan = 2, pady = 10,
        padx = 10, ipadx = 140)

    def loginpage(self):
        """
        Letting existing users log in
        
        A function to allow a returning user to log in to the application.
        If they forgot their password, they are prompted with a new window
        to enter either their phone number or email associated with the 
        account to start the password recovery process.
        """
        
        loginWindow = tk.Toplevel(root)
        loginWindow.title("Login Window")
        loginWindow.geometry("450x400")

        tk.Label(loginWindow, text="Username: ",
        font=("Helvetica", 16)).grid(row=0, pady=5)
        tk.Label(loginWindow, text="Password: ",
        font=("Helvetica", 16)).grid(row=1)

        tk.Entry(loginWindow, width=50).grid(row=0, column=1)
        tk.Entry(loginWindow, show="*", width=50).grid(row=1, column=1)

        #This button closes the login screen
        loginQuit = tk.Button(loginWindow, width=30, height=3)
        loginQuit["text"] = "Back"
        loginQuit["command"] = loginWindow.destroy
        loginQuit["font"] = ("Helvetica", 12, "bold")
        loginQuit.grid(row=4, column=1, pady=15)

        #Forgot password button
        forPas = tk.Button(loginWindow, width=30, height=3)
        forPas["text"] = "Forgot Password"
        forPas["command"] = self.forgotPass
        forPas["font"] = ("Helvetica", 12, "bold")
        forPas.grid(row=3, column=1, pady=15)

        # #Login button
        logBut = tk.Button(loginWindow, width=30, height=3)
        logBut["text"] = "Login"
        logBut["command"] = self.appPage
        logBut["font"] = ("Helvetica", 12, "bold")
        logBut.grid(row=2, column=1, pady=15)

    def appPage(self):
        """
        Creating the home screen
        
        A function that displays the home screen of MegaTrace with which
        the user can navigate the rest of the application, such as reading
        COVID-19 related news, fill out an exposure survey, check and/or
        update their personal information, or log out of the application.
        """
        
        appPage = tk.Toplevel(root)
        appPage.title("Application")
        appPage.geometry("450x400")

        label = tk.Label(appPage, text="Home Screen", font=("Helvetica", 24))
        label.grid(row=0, column=1)

        appQuit = tk.Button(appPage, width=42, height=3)
        appQuit["text"] = "Log Out"
        appQuit["command"] = appPage.destroy
        appQuit["font"] = ("Helvetica", 12, "bold")
        appQuit.grid(row=4, column=1, pady=10)

        survey = tk.Button(appPage, width=42, height=3)
        survey["text"] = "Survey"
        survey["command"] = self.survey
        survey["font"] = ("Helvetica", 12, "bold")
        survey.grid(row=3, column=1, padx=10, pady=10)

        UserInfo = tk.Button(appPage, width=42, height=3)
        UserInfo["text"] = "User Info"
        UserInfo["command"] = self.userPage
        UserInfo["font"] = ("Helvetica", 12, "bold")
        UserInfo.grid(row=2, column=1, padx=10, pady=10)

        news = tk.Button(appPage, width=42, height=3)
        news["text"] = "News"
        news["command"] = self.newsPage
        news["font"] = ("Helvetica", 12, "bold")
        news.grid(row=1, column=1, padx=10, pady=10)

    def forgotPass(self):
        """
        Starting the password reset process
        
        A function that prompts the user for an email address or phone 
        number to receive a password reset link in the event that they
        have forgotten their current one.
        """
        
        forPass = tk.Toplevel(root)
        forPass.title("Forgot Password")
        forPass.geometry("450x400")

        tk.Label(forPass, text="Enter Email: ",
        font=("Helvetica", 12)).grid(row=0,column=0, pady=5)
        tk.Label(forPass, text="Enter Phone Number:",
        font=("Helvetica", 12)).grid(row=1, column=0, pady=5)

        tk.Entry(forPass, width=40).grid(row=0, column=1, pady=5)
        tk.Entry(forPass, show="???", width=40).grid(row=1, column=1, pady=5)

        forLink = tk.Button(forPass, width=15, height=3)
        forLink["text"] = "Send Reset Link"
        forLink["command"] = self.destroy
        forLink["font"] = ("Helvetica", 10, "bold")
        forLink.grid(row=2, column=1, padx=10, pady=10)

        # BackPage button
        back = tk.Button(forPass, width=15, height=3)
        back["text"] = "Back"
        back["command"] = forPass.destroy
        back["font"] = ("Helvetica", 10, "bold")
        back.grid(row=2, column=0, pady=5)
        back.config(width=10, height=3)

    def editUsr(self):
        """
        Creating or editing user information
        
        A function to allow a new user to enter or an exisiting user to
        edit their name, date of birth, email address, and phone number.
        """
        
        editPge = tk.Toplevel(root)
        editPge.title("Sign Up")
        editPge.geometry("450x450")

        tk.Label(editPge, text="First Name: ",
        font=("Helvetica", 16)).grid(row=0,column=1, pady=5)
        tk.Label(editPge, text="Last Name: ",
        font=("Helvetica", 16)).grid(row=2, column=1, pady=5)
        tk.Label(editPge, text="Date of Birth (MM/DD/YYYY): ",
        font=("Helvetica", 16)).grid(row=4,column=1, pady=5)
        tk.Label(editPge, text="Email: ",
        font=("Helvetica", 16)).grid(row=6,column=1, pady=5)
        tk.Label(editPge, text="Phone Number: ",
        font=("Helvetica", 16)).grid(row=8, column=1, pady=5)

        tk.Entry(editPge, width=50).grid(row=1, column=1, pady=5)
        tk.Entry(editPge, show="???", width=50).grid(row=3, column=1, pady=5)
        tk.Entry(editPge, show="???", width=50).grid(row=5, column=1, pady=5)
        tk.Entry(editPge, show="???", width=50).grid(row=7, column=1, pady=5)
        tk.Entry(editPge, show="???", width=50).grid(row=9, column=1, pady=5)

        # #NextPage button
        save = tk.Button(editPge, width=30, height=3)
        save["text"] = "Save Changes"
        save["command"] = self.userPage
        save["font"] = ("Helvetica", 12, "bold")
        save.grid(row=10, column=1, pady=5)
        save.config(width=35, height=3)

    def userPage(self):
        """
        Showing the user's personal information
        
        A function to create the user profile page that allows a user to 
        view as well as update their personal information, including:
        first and last name, birthday, email address, phone number, and
        exposure date, if relevant.  If they choose to update the 
        information, the edit user window is opened.
        """
        
        usrInfo = tk.Toplevel(root)
        usrInfo.title("User Profile")
        usrInfo.geometry("450x400")

        #canvas = Canvas(usrInfo)
        #canvas.create_rectangle(170, 20, 280, 120)
        tk.Label(usrInfo, text="First Name: ",
        font=("Helvetica", 16)).grid(row=5,column=0, pady=5)
        tk.Label(usrInfo, text="Last Name: ",
        font=("Helvetica", 16)).grid(row=6, column=0, pady=5)
        tk.Label(usrInfo, text="Date of Birth (MM/DD/YYYY): ",
        font=("Helvetica", 16)).grid(row=7,column=0, pady=5)
        tk.Label(usrInfo, text="Email: ",
        font=("Helvetica", 16)).grid(row=8,column=0, pady=5)
        tk.Label(usrInfo, text="Phone Number: ",
        font=("Helvetica", 16)).grid(row=9, column=0, pady=5)
        tk.Label(usrInfo, text="Address: ",
        font=("Helvetica", 16)).grid(row=10,column=0, pady=5)
        tk.Label(usrInfo, text="Exposure Date: ",
        font=("Helvetica", 16)).grid(row=11,column=0, pady=5)

        # #NextPage button
        edit = tk.Button(usrInfo, width=30, height=3)
        edit["text"] = "Edit User Profile"
        edit["command"] = self.editUsr
        edit["font"] = ("Helvetica", 12, "bold")
        edit.grid(row=11, column=0, pady=5)
        edit.config(width=35, height=3)

    def newsPage(self):
        """
        Displaying recent and relevant headlines
        
        A function to show the user recent headlines related to 
        COVID-19 by using a webscraper parse news websites for 
        headlines related to COVID-19, searching for relevant
        keywords.
        """
        
        newsPage = tk.Toplevel(root)
        newsPage.title("COVID-19 NEWS")
        newsPage.geometry("450x400")

        """ url = 'https://www.mlive.com/#section__news'
        html = urllib.request.urlopen(url).read()
        parsed = bs4.BeautifulSoup(html, "html.parser")
        data = parsed.find_all("h3")
        headline = ""
        for item in data:
            if("COVID-19" in str(item) or "Coronavirus" in str(item) or "COVID" in str(item)):
                headline = str(item.text.strip())
                break

        tk.Label(newsPage, text="Most Recent Michigan Covid Headline: ", font=("Helvetica", 16)).grid(row=0,column=1, pady=5)
        tk.Label(newsPage, text=str(headline), font=("Helvetica", 12), wraplength=400).grid(row=1,column=1, pady=5)

        url = 'https://news.yahoo.com/'
        html = urllib.request.urlopen(url).read()
        parsed = bs4.BeautifulSoup(html, "html.parser")
        data = parsed.find_all("h3")
        headline = ""
        for item in data:
            if("COVID-19" in str(item) or "Coronavirus" in str(item) or "COVID" in str(item)):
                headline = str(item.text.strip()) """

        tk.Label(newsPage, text="Most Recent National Covid Headline: ",
        font=("Helvetica", 16)).grid(row=2,column=1, pady=5)
        #tk.Label(newsPage, text=str(headline), font=("Helvetica", 12), wraplength=400).grid(row=3,column=1, pady=5)

        appQuit = tk.Button(newsPage, width=42, height=3)
        appQuit["text"] = "Back"
        appQuit["command"] = newsPage.destroy
        appQuit["font"] = ("Helvetica", 12, "bold")
        appQuit.grid(row=4, column=1, padx=2, pady=1)

        local_time = tm.strftime('%I:%M %p')
        clk_lbl = tk.Label(newsPage, font = 'Helvetica', bg = 'white',
        fg = 'black', text = local_time)
        clk_lbl.grid(row = 6, column = 1)

    def tracePge(self):
        """
        Entering exposed contacts
        
        A function that prompts the user to enter contact information
        in the contact tracing information window for people that they 
        have potentially exposed to COVID-19.
        """
        
        conTrace = tk.Toplevel(root)
        conTrace.title("Contact Tracing Information")
        conTrace.geometry("450x200")
        tk.Label(conTrace, text="Enter First Name: ",
        font=("Helvetica", 12)).grid(row=0,column=0, pady=5)
        tk.Label(conTrace, text="Enter Email: ",
        font=("Helvetica", 12)).grid(row=1,column=0, pady=5)
        tk.Label(conTrace, text="Enter Phone Number:",
        font=("Helvetica", 12)).grid(row=2, column=0, pady=5)

        tk.Entry(conTrace, width=30).grid(row=0, column=1, pady=5)
        tk.Entry(conTrace, width=30).grid(row=1, column=1, pady=5)
        tk.Entry(conTrace, width=30).grid(row=2, column=1, pady=5)

         # #NextPage button
        addContact = tk.Button(conTrace, width=10, height=3)
        addContact["text"] = "Add"
        addContact["command"] = self.editUsr
        addContact["font"] = ("Helvetica", 12, "bold")
        addContact.grid(row=3, column=0)
        addContact.config(width=10, height=3)

         # #NextPage button
        newContact = tk.Button(conTrace, width=10, height=3)
        newContact["text"] = "New Contact"
        newContact["command"] = self.tracePge
        newContact["font"] = ("Helvetica", 12, "bold")
        newContact.grid(row=3, column=1)
        newContact.config(width=10, height=3)

         # #NextPage button
        doneButton = tk.Button(conTrace, width=10, height=3)
        doneButton["text"] = "Done"
        doneButton["command"] = self.destroy
        doneButton["font"] = ("Helvetica", 12, "bold")
        doneButton.grid(row=3, column=2)
        doneButton.config(width=10, height=3)

    def exposure(self):
        """
        Defining the exposure date
        
        A function to allow the user to select, from a calendar, a 
        date that indicates when they were exposed to COVID-19.
        """
        
        exPage = tk.Toplevel(root)
        exPage.title("COVID-19 Survey")
        exPage.geometry("400x150")

        cal = Calendar(exPage, selectmode = "day", year = 2020, month = 12, day = 8)
        cal.grid(row = 2, column = 1, pady = 10)

        def grab_date():
            date_label.config(text = cal.get_date())

        date_label = tk.Label(exPage, text="Possible Exposure Date: ",
        font=("Helvetica", 12)).grid(row=0, column=1, pady=5)
        # tk.Entry(exPage, width=40).grid(row=1, column=0, pady=5)
        cal_button = tk.Button(exPage, text='Save', command=grab_date)
        cal_button.grid(row = 3, column = 1, pady = 10)


        trace = tk.Button(exPage, width=30, height=3)
        trace["text"] = "Start Contact Tracing"
        trace["command"] = self.tracePge
        trace["font"] = ("Helvetica", 12, "bold")
        trace.grid(row=11, column=1, pady=5)
        trace.config(width=35, height=3)

    def survey(self):
        """
        Creating the exposure survey
        
        A function to allow the user to indicate whether they have
        had possible exposure to COVID-19.  If they have, the 
        application initiates the process of entering the user's 
        friends and family's contact information.
        """
        
        surPage = tk.Toplevel(root)
        surPage.title("COVID-19 Survey")
        surPage.geometry("250x120")

        tk.Label(surPage, text="Have You Been Exposed to Covid-19? ",
        font=("Helvetica", 16)).grid(row=0, column=1, pady=5)

        yes = tk.Button(surPage)
        yes["text"] = "YES"
        yes["command"] = self.exposure
        yes.grid(row=1, column=1, pady=5)

        no = tk.Button(surPage)
        no["text"] = "NO"
        no["command"] = surPage.destroy
        no.grid(row=2, column=1, pady=5)

def is_valid_pass(password):
    """
    Verifying a new user's password
    
    A function to check if a user making a new account has created a
    password matching the criteria.  The password must be an 
    8-character mixture of uppercase and lowercase letters as well as
    numeric values.
    """
    
    while True:
        password = getpass()
        if len(password) < 8:
            print("Password must be 8 characters.")
        elif re.search('[0-9]', password) is None:
            print("Password must have a number")
        elif re.search('[A-Z]', password) is None:
            print("Password must have one uppercase letter")
        else:
            break

root = tk.Tk()
root.geometry("450x400")
#root.configure(bg='#8cdbed')
root.title("MegaTrace")
app = Application(master=root)
app.mainloop()
