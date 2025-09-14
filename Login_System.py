import sqlite3

db = sqlite3.connect("resource/users.db")
cursor = db.cursor()
'''
cursor.execute("DROP TABLE USER")
db.commit()

cursor.execute(
    
    CREATE TABLE USER(
       Username  CHAR(20) PRIMARY KEY,
       Password  CHAR(20),
       Highest_Score  BIGINT
       );
    
)
db.commit()
'''
#Can't see records in notepad++
cursor.execute("PRAGMA secure_delete = ON")
db.commit()

def Register(username, password):
    cursor.execute("INSERT INTO USER (Username, Password, Highest_Score) VALUES (?,?,?)", (username, password, -1))
    db.commit()

def Repeate_Username(username):
    cursor.execute("SELECT * FROM USER WHERE Username =?", (username,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False

def Login(username, password):
    cursor.execute("SELECT * FROM USER WHERE Username =? AND Password =?", (username, password))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
    
def Delete_User(username):
    cursor.execute("DELETE FROM USER WHERE Username =?", (username,))
    db.commit()
    
def Show_All_User():
    cursor.execute("SELECT Username FROM USER ORDER BY Highest_Score DESC")
    result = cursor.fetchall()
    return result

def Find_User(key):
    cursor.execute("SELECT Username From USER WHERE Username LIKE '{}' ORDER BY Highest_Score DESC".format(key))
    result = cursor.fetchall()
    return result

def Get_User_Data(username):
    cursor.execute("SELECT * FROM USER WHERE Username =?", (username,))
    result = cursor.fetchone()
    return result

def Update_User_Data(username, new_username, new_password):
    cursor.execute("UPDATE USER SET Username =?, Password =? WHERE Username =?", (new_username, new_password, username))
    db.commit()

def Get_Highest_Score(username):
    cursor.execute("SELECT Highest_Score FROM USER WHERE Username =?", (username,))
    result = cursor.fetchone()
    return result[0]

def Update_Highest_Score(username, score):
    hi_score = Get_Highest_Score(username)
    if hi_score > score:
        return
    cursor.execute("UPDATE USER SET Highest_Score =? WHERE Username =?", (score, username))
    db.commit()
#cursor.execute("DELETE FROM USER")
#db.commit()
#cursor.execute("SELECT Username FROM USER")
#result = cursor.fetchall()
#print(*result[1])
