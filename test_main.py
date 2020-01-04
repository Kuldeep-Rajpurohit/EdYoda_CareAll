import  sqlite3

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON;")


c.execute("""CREATE TABLE ELDER(
    "ID" INTEGER,
    "NAME" TEXT,
    "RATING" REAL,
    "CARE_TAKER" INTEGER,
    PRIMARY KEY("ID")
    )""")


c.execute("""CREATE TABLE YOUNG(
    "ID" INTEGER,
    "NAME" TEXT,
    "RATING" REAL,
    "LOOKING_AFTER" INTEGER,
    PRIMARY KEY(ID)
    )""")


c.execute("""CREATE TABLE E_RATING(
    "ID" INTEGER,
    "SUM" REAL,
    "TOTAL" INTEGER,
    PRIMARY KEY("ID"),
    FOREIGN KEY(ID) REFERENCES ELDER(ID)
    )""")


c.execute("""CREATE TABLE Y_RATING(
    "ID" INTEGER,
    "SUM" REAL,
    "TOTAL" INTEGER,
    PRIMARY KEY("ID"),
    FOREIGN KEY(ID) REFERENCES YOUNG(ID)
    )""")


c.execute("""CREATE TABLE UNDER_Y(
    "ID" INTEGER,
    "E_ID" INTEGER
    )""")


c.execute("""CREATE TABLE REQUESTS_TO_E(
    "E_ID" INTEGER,
    "Y_ID" INTEGER,
    FOREIGN KEY(E_ID) REFERENCES ELDER(ID)
    )""")


with conn:
    c.execute("INSERT INTO ELDER VALUES(?,?,?,?)", (101,'KULDEEP',0.0,0))
    c.execute("INSERT INTO ELDER VALUES(?,?,?,?)", (102,'KUNAL',0.0,202))
    c.execute("INSERT INTO ELDER VALUES(?,?,?,?)", (103,'REEMA', 0.0, 0))
    c.execute("INSERT INTO ELDER VALUES(?,?,?,?)", (104,'MUSSI', 0.0, 201))

    c.execute("INSERT INTO YOUNG VALUES(?,?,?,?)", (201, 'ROHAN', 0.0, 1))
    c.execute("INSERT INTO YOUNG VALUES(?,?,?,?)", (202, 'MAK', 0.0, 1))

    c.execute("INSERT INTO E_RATING VALUES(?,?,?)", (101, 0.0, 0))
    c.execute("INSERT INTO E_RATING VALUES(?,?,?)", (102, 0.0, 0))
    c.execute("INSERT INTO E_RATING VALUES(?,?,?)", (103, 0.0, 0))
    c.execute("INSERT INTO E_RATING VALUES(?,?,?)", (104, 0.0, 0))


    c.execute("INSERT INTO Y_RATING VALUES(?,?,?)", (201, 0.0, 0))
    c.execute("INSERT INTO Y_RATING VALUES(?,?,?)", (202, 0.0, 0))

    c.execute("INSERT INTO UNDER_Y VALUES(?,?)", (202, 102))
    c.execute("INSERT INTO UNDER_Y VALUES(?,?)", (201, 104))

    c.execute("INSERT INTO REQUESTS_TO_E VALUES(?,?)",(101,202))
    c.execute("INSERT INTO REQUESTS_TO_E VALUES(?,?)",(101,201))


class Account:

    def create(self, id):
        self.id = id
        self.name = input("\tEnter your name : ")
        self.rating = 0.0
        self.partner = 0
        return (self.id,self.name,self.rating,self.partner)


def create_E():
    acc = Account()
    c.execute("SELECT MAX(ID) FROM ELDER")
    result = c.fetchone()
    id = result[0]+1
    data = acc.create(id)
    c.execute("INSERT INTO ELDER VALUES(?,?,?,?)", (acc.id,acc.name,acc.rating,acc.partner))
    c.execute("INSERT INTO E_RATING VALUES(?,?,?)", (acc.id,0.0,0))
    print("\tAccount created successful. Remember your ID")
    c.execute("SELECT * FROM ELDER WHERE ID = (?)", (id,))
    data = c.fetchone()
    print("\t",data,"\n")
    disp_E_Menu(id,data[3])


def login_E():
    id = int(input("\tEnter your ID : "))
    c.execute("SELECT * FROM ELDER WHERE ID = (?)", (id,))
    temp = c.fetchone()
    if temp == None:
        print("\tInvalid ID")
    else:
        disp_E_Menu(id, temp[3])


def disp_E_Menu(id, ct_id):
    print("\n\tELDER MENU")
    print("\t1. Show the details of your care taker")
    print("\t2. Search for new care taker")
    print("\t3. Give rating to your care taker")
    print("\t4. See requests")
    ch = int(input("\tSelect your option : "))
    if ch == 1:
        dis_ct(ct_id)
    elif ch == 2:
        search_young(id)
    elif ch == 3:
        rate_young(id, ct_id)
    elif ch == 4:
        see_req(id)


def dis_ct(ct_id):
    if ct_id > 0:
        with conn:
            c.execute("SELECT * FROM YOUNG WHERE ID = (?)", (ct_id,))
            data = c.fetchone()
            print("\tID:", data[0], "\n\tName :", data[1], "\n\tRating :", data[2], "\n\tTaking care of :", data[3],
                  "people.\n")
    else:
        print("Oops..  You don't have a care taker\n")


def search_young(id):
    print("\n\nAvailable Care takers ")
    c.execute("SELECT * FROM YOUNG WHERE LOOKING_AFTER < 4")
    data = c.fetchall()
    for each in data:
        print("\t",each)
    new = int(input("Enter ID you want to select or 0 to skip"))
    if new != 0:
        with conn:
            c.execute("UPDATE ELDER SET CARE_TAKER = (?) WHERE ID=(?)", (new, id))
            c.execute("UPDATE YOUNG SET LOOKING_AFTER = (LOOKING_AFTER+1) WHERE ID = (?)", (new,))
            c.execute("INSERT INTO UNDER_Y VALUES(?,?)", (new,id))
        print("\tYour new Care Taker is : ",new)


def rate_young(id, ct_id):
    if ct_id == 0:
        print("You do not have a care taker")
    else:
        rating = int(input("Enter rating : (from 0 - 5)"))
        if rating <= 5.0:
            c.execute("SELECT * FROM Y_RATING WHERE ID=(?)", (ct_id,))
            temp = c.fetchone()
            sum = temp[1] + rating
            total = temp[2]+1
            new_rat = sum / total
            with conn:
                c.execute("UPDATE YOUNG SET RATING = (?) WHERE ID = (?)", (new_rat,ct_id))
                c.execute("UPDATE Y_RATING SET SUM = (?), TOTAL = (?) WHERE ID = (?)", (sum,total,ct_id))
        else:
            print("Invalid rating")


def see_req(id):
    with conn:
        c.execute("SELECT Y_ID FROM REQUESTS_TO_E WHERE E_ID = (?)", (id,))
        data = c.fetchall()
        if len(data):
            for i in range(len(data)):
                with conn:
                    c.execute("SELECT * FROM YOUNG WHERE ID = (?)", (data[i][0],))
                    print(next(c))
            new = int(input("Enter the ID you want to select or 0 to skip : "))
            if new != 0:
                with conn:
                    c.execute("UPDATE ELDER SET CARE_TAKER = (?) WHERE ID = (?)",(new,id))
                    c.execute("UPDATE YOUNG SET LOOKING_AFTER = (LOOKING_AFTER+1) WHERE ID = (?)",(new,))
                    c.execute("INSERT INTO UNDER_Y VALUES(?,?)",(new,id))
                print("Your new Care taker is : ")
                c.execute("SELECT ID, NAME FROM YOUNG WHERE ID = (?)",(new,))
                data = c.fetchone()
                print("\tID : ",data[0],"\tName : ",data[1],"\n")
        else:
            print("Currently no requests")


# -----------------------------------------------------------------------------------


def create_Y():
    acc = Account()
    c.execute("SELECT MAX(ID) FROM YOUNG")
    result = c.fetchone()
    Y_id = result[0]+1
    data = acc.create(Y_id)
    with conn:
        c.execute("INSERT INTO YOUNG VALUES(?,?,?,?)", (acc.id,acc.name,acc.rating,acc.partner))
        c.execute("INSERT INTO Y_RATING VALUES(?,?,?)", (acc.id,0.0,0))
    print("Acount created successful. Remember your ID")
    c.execute("SELECT * FROM YOUNG WHERE ID = (?)", (Y_id,))
    print(next(c))
    disp_Y_Menu(Y_id)


def login_Y():
    Y_id = int(input("Enter your ID : "))
    c.execute("SELECT * FROM YOUNG WHERE ID = (?)", (Y_id,))
    temp = c.fetchone()
    if temp == None:
        print("\tInvalid ID")
    else:
        print(temp[3])
        disp_Y_Menu(Y_id, temp[3])


def disp_Y_Menu(Y_id, no_e_looking):
    print("\n\tYOUNG MENU")
    print("\t1. See the list of people you are currently taking care of")
    print("\t2. Look for an elder and send request")
    print("\t3. Give rating to the elder you take care of")
    ch = int(input("Select your option : "))
    if ch == 1:
        see_eld(Y_id, no_e_looking)
    elif ch == 2:
        check_4(Y_id, no_e_looking)
    elif ch == 3:
        rate_elder(Y_id, no_e_looking)


def see_eld(Y_id, no_e_looking):
    if no_e_looking > 0:
        with conn:
            c.execute("SELECT E_ID FROM UNDER_Y WHERE ID = (?)",(Y_id,))
            data = c.fetchall()
        for i in range(len(data)):
            c.execute("SELECT * FROM ELDER WHERE ID = (?)",(data[i][0],))
            print(next(c),"\n")
    else:
        print("\tOops.. Empty list\n")


def check_4(Y_id, no_e_looking):
    if no_e_looking < 4:
        send_req(Y_id)
    else:
        print("\tYou cannot look after more than 4 people.\n")


def send_req(Y_id):
    c.execute("SELECT ID FROM ELDER WHERE CARE_TAKER = 0")
    data = c.fetchall()
    if data:
        print("(ID, NAME, Rating, Taking care of)")
        for i in range(len(data)):
            c.execute("SELECT * FROM ELDER WHERE ID = (?)",(data[i][0],))
            print(next(c))
        req_id = int(input("Enter ID you want to send request or 0 to skip : "))
        if req_id:
            c.execute("IINSERT INTO REQUESTS_TO_E VALUES(?,?)",(req_id, Y_id))
            print("\tRequest send successfully\n")
    else:
        print("\tOops No elder is available\n")


def rate_elder(Y_id, no_e_looking):
    if no_e_looking:
        print("(ID, NAME, Rating, Taking care of)")
        c.execute("SELECT E_ID FROM UNDER_Y WHERE ID = (?)", (Y_id,))
        data = c.fetchall()
        for i in range(len(data)):
            c.execute("SELECT * FROM ELDER WHERE ID = (?)", (data[i][0],))
            print(next(c))
        e_id = print("Enter ID you want to rate : ")
        rating = int(input("Enter rating : (from 0 - 5)"))
        if rating <= 5.0:
            c.execute("SELECT * FROM E_RATING WHERE ID=(?)", (e_id,))
            temp = c.fetchone()
            sum = temp[1] + rating
            total = temp[2] + 1
            new_rat = sum / total
            c.execute("UPDATE ELDER SET RATING = (?) WHERE ID = (?)",(new_rat,e_id))
            c.execute("UPDATE E_RATING SET SUM = (?), TOTAL = (?) WHERE ID = (?)",(sum,total,e_id))

        else:
            print("\tRating out of range\n")


def intro():
    print("\t----------------------------------")
    print("\t      Welcome to CareALL          ")
    print("\t----------------------------------")


intro()

ch = 0
while ch != 9:
    print("\tMain Menu")
    print("\t1. CREATE ELDER ACCOUNT")
    print("\t2. CREATE YOUNG ACCOUNT")
    print("\t3. LOGIN FOR ELDER")
    print("\t4. LOGIN FOR YOUNG")
    print("\t9. EXIT")
    ch = int(input("\tSelect your choice : "))

    if ch == 1:
        create_E()
    elif ch == 2:
        create_Y()
    elif ch == 3:
        login_E()
    elif ch == 4:
        login_Y()
    elif ch == 9:
        print("\tThanks for using CareAll\n")
        break
    else:
        print("\tInvalid choice")

