import sqlite3


# name of database file is : "CareAll_data"


conn = sqlite3.connect("CareAll_Data.db")

c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON;")

c.execute("""CREATE TABLE ELDER(
    "ID" INTEGER,
    "NAME" TEXT,
    "RATING" REAL,
    "CARE_TAKER" INTEGER,
    "NO_OF_REQ" INTEGER,
    PRIMARY KEY (ID)
    )""")


c.execute("""CREATE TABLE YOUNG(
    "ID" INTEGER,
    "NAME" TEXT,
    "FEES" INTEGER,
    "RATING" REAL,
    "NO_OF_ELD" INTEGER,
    "NO_OF_REQ" INTEGER,
    PRIMARY KEY (ID)
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
    "Y_ID" INTEGER,
    "E_ID" INTEGER,
    FOREIGN KEY (Y_ID) REFERENCES YOUNG(ID),
    FOREIGN KEY (E_ID) REFERENCES ELDER(ID)
    )""")


c.execute("""CREATE TABLE REQUESTS_TO_E(
    "E_ID" INTEGER,
    "Y_ID" INTEGER,
    FOREIGN KEY(E_ID) REFERENCES ELDER(ID)
    FOREIGN KEY(Y_ID) REFERENCES YOUNG(ID)
    )""")



c.execute("""CREATE TABLE REQUESTS_TO_Y(
    "E_ID" INTEGER,
    "Y_ID" INTEGER,
    FOREIGN KEY(Y_ID) REFERENCES YOUNG(ID),
    FOREIGN KEY(E_ID) REFERENCES ELDER(ID)
    )""")

conn.commit()
c.close()

