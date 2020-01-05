import sqlite3

conn = sqlite3.connect("CareAll_Data.db")
c = conn.cursor()


class Elder:

    def create(self, id, init_ct = 0, init_rat=0.0, init_req=0):
        self.id = id
        self.name = input("\tEnter your name : ")
        self.rating = init_rat
        self.care_taker = init_ct
        self.no_of_req = init_req
        c.execute("INSERT INTO ELDER VALUES(?,?,?,?,?)", (id, self.name, 0.0, 0, 0))

    def gen_id(self):
        c.execute("SELECT MAX(ID) FROM ELDER")
        result = c.fetchone()
        if result[0]:
            id = result[0] + 1
        else:
            id = 101
        return id

    def dislay(self, id):
        c.execute("SELECT * FROM ELDER WHERE ID = (?)", (id,))
        data = c.fetchone()
        print("\tID : {0}  Name : {1}  Rating : {2}".format(data[0], data[1], data[2]))


    def get_care_ta_id(self, id):
        c.execute("SELECT CARE_TAKER FROM ELDER WHERE ID = (?)", (id,))
        data = c.fetchone()
        return data[0]

    def get_no_of_req(self,id):
        c.execute("SELECT NO_OF_REQ FROM ELDER WHERE ID = (?)",(id,))
        data = c.fetchone()
        return data[0]

    def update_care_taker(self,id,y_id):
        c.execute("UPDATE ELDER SET CARE_TAKER = (?) WHERE ID = (?)", (y_id, id))


    def e_id_check(self,id):
        c.execute("SELECT * FROM ELDER WHERE ID = (?)",(id,))
        data = c.fetchone()
        return data

    def check_avail(self):
        c.execute("SELECT ID FROM ELDER WHERE CARE_TAKER = 0 ")
        data = c.fetchall()
        return data

    def update_rating(self,id,rating):
        c.execute("UPDATE ELDER SET RATING = (?) WHERE ID = (?)", (rating,id))


class Young:

    def create(self,id,init_rat=0, init_eld=0, init_req=0):
        self.id = id
        self.name = input("\tEnter your name : ")
        self.fees = int(input("\tEnter your fees : "))
        self.rating = init_rat
        self.no_of_eld = init_eld
        self.no_of_req = init_req
        c.execute("INSERT INTO YOUNG VALUES(?,?,?,?,?,?)", (id, self.name, self.fees, 0.0, 0, 0))

    def gen_id(self):
        c.execute("SELECT MAX(ID) FROM YOUNG")
        result = c.fetchone()
        if result[0]:
            id = result[0] + 1
        else:
            id = 201
        return id


    def get_no_of_eld(self,id):
        c.execute("SELECT NO_OF_ELD FROM YOUNG WHERE ID = (?)",(id,))
        data = c.fetchone()
        return data[0]

    def dislay(self,id):
        c.execute("SELECT * FROM YOUNG WHERE ID = (?)",(id,))
        data = c.fetchone()
        print("\n\tID : {0}  Name : {1}  Fees : {2}  Rating : {3}".format(data[0],data[1],data[2],data[3]))

    def check_avail(self):
        c.execute("SELECT ID FROM YOUNG WHERE NO_OF_ELD < 4")
        data = c.fetchall()
        return data

    def update_no_of_eld(self,id, val):
        c.execute("UPDATE YOUNG SET NO_OF_ELD = (NO_OF_ELD+(?)) WHERE ID =(?)",(val,id))

    def y_id_check(self,id):
        c.execute("SELECT * FROM YOUNG WHERE ID = (?)",(id,))
        data = c.fetchone()
        return data

    def update_rating(self,id,rating):
        c.execute("UPDATE YOUNG SET RATING = (?) WHERE ID = (?)", (rating,id))

    def get_no_of_req(self,id):
        c.execute("SELECT NO_OF_REQ FROM YOUNG WHERE ID = (?)",(id,))
        data = c.fetchone()
        return data[0]


class Rating:

    def e_create(self, id):
        self.id = id
        self.tot_sum = 0.0
        self.tot_raters = 0
        c.execute("INSERT INTO E_RATING VALUES(?,?,?)",(id, 0.0, 0))

    def y_create(self, id):
        self.id = id
        self.tot_sum = 0.0
        self.tot_raters = 0
        c.execute("INSERT INTO Y_RATING VALUES(?,?,?)", (id, 0.0, 0))


    def get_e_data(self, e_id):
        c.execute("SELECT SUM, TOTAL FROM E_RATING WHERE ID = (?)", (e_id,))
        data = c.fetchone()
        return (data[0], data[1])

    def get_y_data(self, y_id):
        c.execute("SELECT * FROM Y_RATING WHERE ID = (?)", (y_id,))
        data = c.fetchone()
        print(data)
        return (data[1], data[2])


    def upd_rating_of_y(self, id,rating, tot_sum, tot_raters):
        c.execute("UPDATE YOUNG SET RATING = (?) WHERE ID = (?)",(rating,id))
        c.execute("UPDATE Y_RATING SET SUM=(?),TOTAL=(?) WHERE ID = (?)", (tot_sum, tot_raters, id))


    def upd_rating_of_e(self, id, rating, tot_sum, tot_raters):
        c.execute("UPDATE ELDER SET RATING = (?) WHERE ID = (?)", (rating, id))
        c.execute("UPDATE E_RATING SET SUM=(?),TOTAL=(?) WHERE ID = (?)", (tot_sum, tot_raters, id))


class Request:

    def e_send(self, e_id, y_id):
        c.execute("INSERT INTO REQUESTS_TO_Y VALUES(?,?)", (e_id, y_id))
        c.execute("UPDATE YOUNG SET NO_OF_REQ = (NO_OF_REQ+1) WHERE ID = (?)", (y_id,))

    def e_accept(self, e_id, y_id):
        c.execute("DELETE FROM REQUESTS_TO_E WHERE E_ID = (?) AND Y_ID = (?)", (e_id, y_id))

    def y_send(self, e_id, y_id):
        c.execute("INSERT INTO REQUESTS_TO_E VALUES(?,?)", (e_id, y_id))
        c.execute("UPDATE ELDER SET NO_OF_REQ = (NO_OF_REQ+1) WHERE ID = (?)", (e_id,))

    def y_accept(self, e_id, y_id):
        c.execute("DELETE FROM REQUESTS_TO_Y WHERE E_ID = (?) AND Y_ID = (?)", (e_id, y_id))

    def get_req_to_e(self, e_id):
        c.execute("SELECT Y_ID FROM REQUESTS_TO_E WHERE ID=(?)", (e_id))
        data = c.fetchall()
        return data

    def get_req_to_y(self, y_id):
        c.execute("SELECT E_ID FROM REQUESTS_TO_Y WHERE ID=(?)", (y_id))
        data = c.fetchall()
        return data


class under_Y:

    def create(self,y_id,e_id):
        self.y_id = e_id
        self.e_id = y_id
        c.execute("INSERT INTO UNDER_Y VALUES(?,?)", (y_id,e_id))


    def delete(self,y_id,e_id):
        c.execute("DELETE FROM UNDER_Y WHERE Y_ID = (?) AND E_ID = (?)", (y_id,e_id))


    def get_id_of_elds(self,y_id):
        c.execute("SELECT E_ID FROM UNDER_Y WHERE Y_ID=(?)", (y_id,))
        data = c.fetchall()
        return data


def new_acc(ch):
    if ch == 1:
        new = Elder()
        id = new.gen_id()
        new.create(id)
        print("\n")
        new.dislay(id)
        rate = Rating()
        rate.e_create(id)
        e_menu(id)

    elif ch == 2:
        new = Young()
        id = new.gen_id()
        new.create(id)
        print("\n")
        new.dislay(id)
        rate = Rating()
        rate.y_create(id)
        y_menu(id)


def login(ch):
    if ch == 3:
        entered_id = int(input("\n\tEnter your ID : "))
        eld = Elder()
        exist = eld.e_id_check(entered_id)
        if exist:
            e_menu(entered_id)
        else:
            print("\tIncorrect ID\n")
    elif ch == 4:
        entered_id = int(input("\n\tEnter your ID : "))
        yng = Young()
        exist = yng.y_id_check(entered_id)
        if exist:
            y_menu(entered_id)
        else:
            print("\tIncorrect ID\n")


def e_menu(id):
    print("\n\tELDER MENU")
    print("\t1. Show the details of your care taker")
    print("\t2. Search for new care taker and send request")
    print("\t3. Give rating to your care taker")
    print("\t4. See requests")
    ch = int(input("\tSelect your option : "))

    if ch == 1:
        disp_ct(id)
    elif ch == 2:
        search_ct(id)
    elif ch == 3:
        e_rating(id)
    elif ch == 4:
        see_req_to_e(id)
    else:
        print("\tInvalid choice\n")


def disp_ct(id):
    new = Elder()
    ct_id = new.get_care_ta_id(id)
    if ct_id:
        ct = Young()
        print("\n\tYour care taker is : ")
        ct.dislay(ct_id)
        print(" ")
    else:
        print("\tOops..  You don't have a care taker\n")


def search_ct(id):
    new = Young()
    data = new.check_avail()
    eld = Elder()
    curr_ct = eld.get_care_ta_id(id)
    if len(data):
        for i in range(len(data)):
            if curr_ct != data[i][0]:
                new.dislay(data[i][0])
        req_id = int(input("\n\tEnter ID you want to send request or 0 to skip\n"))
        if req_id:
            send_req_to_y(id, req_id)
    else:
        print("\tOops currently no care taker available\n")


def send_req_to_y(e_id, y_id):
    req = Request()
    req.e_send(e_id, y_id)
    print("\tRequest sent successfully\n")


def e_rating(id):
    ct = Elder()
    ct_id = ct.get_care_ta_id(id)
    if ct_id:
        disp_ct(id)
        rate_got = float(input("\tEnter your rating (0 - 5) : "))
        if (rate_got>=0.0 and rate_got <= 5.0):
            data = Rating()
            tot_sum, tot_raters = data.get_y_data(ct_id)
            tot_sum = tot_sum + rate_got
            tot_raters += 1
            upd_rating = tot_sum / tot_raters
            new = Rating()
            new.upd_rating_of_y(ct_id,upd_rating,tot_sum,tot_raters)
            # yng = Young()
            # yng.update_rating(id,upd_rating)

        else:
            print("\tInvalid rating\n")
    else:
        print("\tYou don't have a care taker for now\n")


def see_req_to_e(id):
    data = Elder()
    requests =  data.get_no_of_req(id)
    old_ct = data.get_care_ta_id(id)
    if requests:
        temp = Request()
        req_ids = temp.get_req_to_e(id)
        for i in range(len(req_ids)):
            young = Young()
            young.dislay(req_ids[i][0])

        new_ct = int(input("\tEnter ID you want to select or 0 to skip : "))
        if new_ct:
            data.update_care_taker(id,new_ct)
            print("\tYour New Care Taker is ()")
            young = Young()
            young.update_no_of_eld(old_ct, -1)
            temp.e_accept(id,new_ct)
            und_y = under_Y()
            und_y.create(new_ct,id)
            und_y.delete(old_ct,id)

    else:
        print("\tOops.. You don't have any request\n")


def y_menu(y_id):
    print("\n\tYOUNG MENU")
    print("\t1. See the list of people you are currently taking care of")
    print("\t2. Look for an elder and send request")
    print("\t3. Give rating to the elder you take care of")
    print("\t4. See requests")
    ch = int(input("\tSelect your option : "))

    if ch == 1:
        disp_eld(y_id)
    elif ch == 2:
        search_eld(y_id)
    elif ch == 3:
        y_rating(y_id)
    elif ch == 4:
        see_req_to_y(y_id)
    else:
        print("\tInvalid Choice\n")


def disp_eld(y_id):
    data = Young()
    no_of_eld = data.get_no_of_eld(y_id)
    if no_of_eld:
        und_y = under_Y()
        data = und_y.get_id_of_elds(y_id)
        print(" ")
        for i in range(no_of_eld):
            eld = Elder()
            eld.dislay(data[i][0])
        print(" ")
    else:
        print("\tOops.. No elders in your list\n")


def search_eld(y_id):
    yng = Young()
    takin_c_of = yng.get_no_of_eld(y_id)
    if takin_c_of < 4:
        eld = Elder()
        data = eld.check_avail()
        if len(data):
            print("\n\tThe elders available are : ")
            for i in range(len(data)):
                eld.dislay(data[i][0])
            req_id = int(input("\tEnter ID you want to send request or 0 to skip\n"))
            if req_id:
                send_req_to_y(req_id,y_id)
    else:
        print("\tOops.. Currently no elder available.\n")


def send_req_to_y(e_id, y_id):
    req = Request()
    req.y_send(e_id, y_id)
    print("\tRequest sent successfully")


def y_rating(y_id):
    yng = Young()
    eld_undr_y = yng.get_no_of_eld(y_id)
    if eld_undr_y:
        und_y = under_Y()
        elds_ids = und_y.get_id_of_elds(y_id)
        eld = Elder()
        for i in range(len(elds_ids)):
            eld.dislay(elds_ids[i])
        rat_id = int(input("\tEnter ID you want to rate : "))
        rate_got = int(input("\tEnter your rating (0 - 5) : "))
        if (rate_got >= 0.0 and rate_got <= 5.0):
            data = Rating()
            tot_sum, tot_raters = data.get_e_data(rat_id)
            tot_sum = tot_sum + rate_got
            tot_raters += 1
            upd_rating = tot_sum / tot_raters
            new = Rating()
            new.upd_rating_of_e(rat_id, tot_sum, tot_raters)
            eld.update_rating(rat_id,upd_rating)

        else:
            print("\tInvalid rating\n")
    else:
        print("\tOops.. You don't have any one in your list.\n")


def see_req_to_y(y_id):
    data = Young()
    takin_care_of = data.get_no_of_eld(y_id)
    requests = data.get_no_of_req(y_id)
    if requests:
        temp = Request()
        req_ids = temp.get_req_to_y(y_id)
        for i in range(len(req_ids)):
            elder = Elder()
            elder.dislay(req_ids[i][0])
        if takin_care_of < 4:
            new_eld = int(input("\tEnter ID you want to select or 0 to skip : "))
            if new_eld:
                elder.update_care_taker(new_eld, y_id)
                print("\tNow you have one more elder to look after\n")
                data.update_no_of_eld(y_id, +1)
                temp.y_accept(new_eld, y_id)
                und_y = under_Y()
                und_y.create(y_id,new_eld)

        else:
            print("\tCannot send request")
            print("\tYou cannot look after more than 4 people\n")

    else:
        print("\tOops.. Currently no requests\n")


def intro():
    print("\t\t\t\t**********************************")
    print("\t\t\t\t      Welcome to CareALL          ")
    print("\t\t\t\t**********************************\n\n\n")


#start of code

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
        new_acc(ch)
    elif ch == 2:
        new_acc(ch)
    elif ch == 3:
        login(ch)
    elif ch == 4:
        login(ch)
    elif ch == 9:
        print("\tThanks for using CareAll\n")
        break
    else:
        print("\tInvalid choice")

