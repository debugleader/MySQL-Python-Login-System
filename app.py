import mysql.connector
from pyfiglet import Figlet

database_connection = False
running = True
pass_weak = False
login_status = False
login_said = False

def database_connect(host_v,usr,password,datab):
    global database_connection, db, mycursor
    try:
        db = mysql.connector.connect(
            host=host_v,
            user=usr,
            passwd=password,
            database=datab
        )
        mycursor = db.cursor()
        if db:
            database_connection = True
            return "Connection to the database is working"
    except:
        return "Connection to the database wasn't successful"
    
def setup_database_connection():
    global database_connection
    host_v = input("Input the hostname (Type localhost if you're not sure): ")
    usr = input("Input the database user: ")
    password = input("Input the database password: ")
    datab = input("Input the database name: ")
    print(database_connect(host_v,usr,password,datab))
    if database_connection == False:
        exit() 

f = Figlet(font='slant')
print(f.renderText('Login System'))
print("Welcome to Login System v1.3 by debugleader!")
print("")
while running:
    if not database_connection:
        setup_database_connection()
    print("")
    print("1) Create a table (Mandatory before registering or logging in): ")
    print("2) Register")
    print("3) Login")
    print("4) Quit")
    print("")
    user_input = input("Input a number: ")
    if user_input == str(4):
        print("")
        print("Thank you for using our program!")
        exit()
    elif user_input == str(1):
        try:
            mycursor.execute("CREATE TABLE system_data (name VARCHAR(20), password VARCHAR(20), personID int PRIMARY KEY AUTO_INCREMENT)")
            print("Table created!")      
        except: 
            print("Table already created or something else went wrong!")
    elif user_input == str(2):
        register_name = input("Input your name: ")
        while not pass_weak:
            register_passwd = input("Input your password: ")
            if (any(x.isupper() for x in register_passwd) and any(x.islower() for x in register_passwd) and any(x.isdigit() for x in register_passwd) and len(register_passwd) >= 8):
                mycursor.execute(f"INSERT INTO system_data (name,password) VALUES ('{register_name}','{register_passwd}')")
                db.commit()
                pass_weak = True
                print("")
                print(f"Congratulations! Your name is {register_name} and your password is {register_passwd}!")
            else:
                print("Weak password, the password should contain at least an upper case letter, a lower case letter, a number and must be longer than 7 characters!")
        pass_weak = False
    elif user_input == str(3):

        mycursor.execute("SELECT * FROM system_data")
        credentials = []
        for x in mycursor:
            credentials.append(x)
        while not login_status:
            login_name = input("Input your name: ")
            login_passwd = input("Input your password: ")
            for counter in range(len(credentials)):
                if login_name == credentials[counter][0]:
                    if login_passwd == credentials[counter][1]:
                        print("")
                        print("You successfully logged in, thank you really much for using our system :)")
                        print("")
                        print(f'The account name is called "{credentials[counter][0]}" and the password is "{credentials[counter][1]}"')
                        print(f"This account was the number {credentials[counter][2]} registered account!")
                        print("")
                        exit()
                    else:
                        if login_said == False:
                            print("Sorry, wrong username or password!")
                            login_said = True
                elif login_said == False:
                            print("Sorry, wrong username or password!")
                            login_said = True
            login_said = False
