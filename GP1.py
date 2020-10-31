import sqlite3
import time
import hashlib
import os
import sys

connection = None
cursor = None


#this class will be used to reference the singleton user and get their uid.
class CurrentUser: 
    def __init__(self, uid = None): 
         self._uid = uid
      
    # getter method 
    def get_uid(self): 
        return self._uid 
      
    # setter method 
    def set_uid(self, uid): 
        self._uid = uid


def main():
    global connection, cursor

    path="./GP1DB.db"
    connect(path)

    '''dont need to run the three following commands every run
    just to instantiate the db and define the tables '''
    dropTables() 
    defineTables()
    insertData()

    currUser = CurrentUser() 
    homeScreen(currUser)

    #connection.close()
    #return
    

def connect(path):
    #function to connect to sqlite3 db
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    
    return


def dropTables():
    #function to drop tables if they exist.
    global connection, cursor

    drop_answers_table = "drop table if exists answers; "
    drop_questions_table = "drop table if exists questions; "
    drop_votes_table = "drop table if exists votes; "
    drop_tags_table = "drop table if exists tags; "
    drop_posts_table = "drop table if exists posts; "
    drop_ubadges_table = "drop table if exists ubadges; "
    drop_badges_table = "drop table if exists badges; "
    drop_privileged_table = "drop table if exists privileged; "
    drop_users_table = "drop table if exists users; "

    cursor.execute(drop_answers_table)
    cursor.execute(drop_questions_table)
    cursor.execute(drop_votes_table)
    cursor.execute(drop_tags_table)
    cursor.execute(drop_posts_table)
    cursor.execute(drop_ubadges_table)
    cursor.execute(drop_badges_table)
    cursor.execute(drop_privileged_table)
    cursor.execute(drop_users_table)


def defineTables():
    #function to define table schema in db
    global connection, cursor

    ct_users=      '''
                        CREATE TABLE users (
                                      uid	char(4),
                                      name  	text,
                                      pwd	text,
                                      city	text,
                                      crdate	date,
                                      primary key (uid)
                                    );
                    '''
    
    ct_privileged=  '''
                        CREATE TABLE privileged (
                                      uid	char(4),
                                      primary key (uid),
                                      foreign key (uid) references users
                                    );
                    '''
    
    ct_badges=      '''
                    CREATE TABLE badges (
                                      bname	text,
                                      type  	text,
                                      primary key (bname)
                                    );
                    '''
    
    ct_ubadges=     '''
                    CREATE TABLE ubadges (
                                      uid	char(4),
                                      bdate	date,
                                      bname	text,
                                      primary key (uid,bdate),
                                      foreign key (uid) references users,
                                      foreign key (bname) references badges
                                    );
                    '''
    
    ct_posts=       '''
                    CREATE TABLE posts (
                                      pid	char(4),
                                      pdate	date,
                                      title	text,
                                      body	text,
                                      poster	char(4),
                                      primary key (pid),
                                      foreign key (poster) references users
                                    );
                    '''
    
    ct_tags=        '''
                    CREATE TABLE tags (
                                  pid		char(4),
                                  tag		text,
                                  primary key (pid,tag),
                                  foreign key (pid) references posts
                                );
                    '''
    
    ct_votes=       '''
                    CREATE TABLE votes (
                                  pid		char(4),
                                  vno		int,
                                  vdate		text,
                                  uid		char(4),
                                  primary key (pid,vno),
                                  foreign key (pid) references posts,
                                  foreign key (uid) references users
                                );
                    '''

    ct_questions=   '''
                    CREATE TABLE questions (
                                  pid		char(4),
                                  theaid	char(4),
                                  primary key (pid),
                                  foreign key (theaid) references answers
                                );
                    '''

    ct_answers=     '''
                    CREATE TABLE answers (
                                  pid		char(4),
                                  qid		char(4),
                                  primary key (pid),
                                  foreign key (qid) references questions
                                );
                    '''

    

    cursor.execute(ct_users)
    cursor.execute(ct_privileged)
    cursor.execute(ct_badges)
    cursor.execute(ct_ubadges)
    cursor.execute(ct_posts)
    cursor.execute(ct_tags)
    cursor.execute(ct_votes)
    cursor.execute(ct_questions)
    cursor.execute(ct_answers)
    
    connection.commit()
    return


def insertData():
    #function to insert some data
    global connection, cursor

    
    insert_users =  '''
                        INSERT INTO users (uid, name, pwd, city, crdate) VALUES
                        ('u100','Davood Rafiei', 'totallyapassword123', 'Edmonton','2020-01-10'),
                        ('u200','Joe Smith','password789','Vancouver','2020-08-15'),
                        ('u300','Mary Brown','CatsBirthdayPswrd', 'Edmonton','2020-06-04');
                    '''
    
    insert_privileged = '''
                            INSERT INTO privileged (uid) VALUES
                            ('u100'),
                            ('u300');
                        '''
    
    insert_badges = '''
                        INSERT INTO badges (bname, type) VALUES
                        ('socratic question','gold'),
                        ('stellar question', 'gold'),
                        ('great answer','gold'),
                        ('popular answer','gold'),
                        ('fanatic user','gold'),
                        ('legendary user','gold'),
                        ('good question','silver'),
                        ('good answer','silver'),
                        ('enthusiast user','silver'),
                        ('nice question','bronze'),
                        ('nice answer','bronze'),
                        ('commentator user','bronze');
                     '''

    insert_ubadges  = '''
                            INSERT INTO ubadges (uid, bdate, bname) VALUES
                            ('u200','2020-09-06','stellar question');
                      '''

    insert_posts = '''
                        INSERT INTO posts (pid, pdate, title, body, poster) VALUES
                        ('p100',date('now','-30 days'),'What is a relational database?','What is the term referred to and what are the benefits?','u200'),
                        ('p200',date('now','-29 days'),'introduction to relational databases','This is a post that introduce the relational databases including SQL','u100');
                   '''
    
    insert_tags = '''
                        INSERT INTO tags (pid, tag) VALUES
                        ('p100','relational'),
                        ('p100','database'),
                        ('p200','relational'),
                        ('p200','sql');
                  '''

    insert_votes = '''
                        INSERT INTO votes (pid, vno, vdate, uid) VALUES
                        ('p200',1,date('now','-20 days'),'u200');
                   '''

    insert_questions = '''
                            INSERT INTO questions (pid, theaid) VALUES
                            ('p100',null);
                       '''
                        
    insert_answers = '''
                            INSERT INTO answers (pid, qid) VALUES
                            ('p200','p100');
                     '''

    cursor.execute(insert_users)
    cursor.execute(insert_privileged)
    cursor.execute(insert_badges)
    cursor.execute(insert_ubadges)
    cursor.execute(insert_posts)
    cursor.execute(insert_tags)
    cursor.execute(insert_votes)
    cursor.execute(insert_questions)
    cursor.execute(insert_answers )
    connection.commit()
    return


def homeScreen(currUser):
    #function to displays homescreen for user
    val = str(input("Enter 1 to log in, or enter 2 to sign up: "))

    
    while val != '1' and val != '2':
        print("Please enter a valid input!")
        val = input("Enter 1 to log in, or enter 2 to sign up: ")

    if val == '1':
        login(currUser)
    else:
        signup(currUser)
        
    
def login(currUser):
    #function logs in a user
    global connection, cursor

    #ask for uid, ask for pwd, check db for uid, if not exists, notify them, go back to homeScreen
    uid = input("Enter your uid: ")
    pwd = input("Enter your password: ")

    #spec says password is case sensitive
    cursor.execute('SELECT * FROM users WHERE uid=? AND pwd=? ', (uid,pwd))
    
    while cursor.fetchone() is None:
        print("Your username or password is incorrect. Please try again.")
        uid = input("Enter your uid: ")
        pwd = input("Enter your password: ")
        cursor.execute('SELECT * FROM users WHERE uid=? AND pwd=? ', (uid,pwd))
  
    print("Successfully logged in!")
    currUser.set_uid(uid)
    displayMenu(currUser)


def signup(currUser):
    #function signs up a user
    global connection, cursor

    #check db for existing uid, if exists, notify user, call login(), if not, sign them up, notify them, log them in.
    #should be exactly 4 because no key should be a subset of another key. This is the only field that needs to be unique
    uid = input("Create a 4 character uid: ")

    name = input("Enter your name: ")
    pwd = input("Create a password: ") 
    city = input("Enter your city: ")

    #check if uid is unique
    cursor.execute('SELECT uid FROM users WHERE uid=?', (uid,))
    

    while cursor.fetchone() is not None or len(uid) != 4:
        print("That uid is already taken or is not 4 characters. Please Enter a new one.")
        uid = input("Create a 4 character uid: ")
        cursor.execute('SELECT uid FROM users WHERE uid=?', (uid,))


    cursor.execute("INSERT INTO users (uid, name, pwd, city, crdate) VALUES (?,?,?,?,date('now'))",(uid,name,pwd,city))
    connection.commit()

    print("Successfully signed up!")
    currUser.set_uid(uid)
    displayMenu(currUser)
    

def logout(currUser):
    #logs user out, navigates back to homescreen
    print("Successfully logged out")
    currUser.set_uid(None)
    homeScreen(currUser)


def exitProgram(currUser):
    #exits program
    currUser.set_uid(None) #redundant but wtv
    print("Goodbye!")
    sys.exit(0)
    

def checkPrivilege(currUser):
    #function returns bool of whether or not user is privileged
    global connection, cursor

    cursor.execute('SELECT * FROM privileged p, users u WHERE p.uid=?', (currUser._uid,))
    if cursor.fetchone() is None:
        privilege = False
    else:
        privilege = True
    
    return privilege
    

def displayMenu(currUser):
    #function display the appropriate menu depending on privelege

    privilege = checkPrivilege(currUser)

    header = "| # | Option\n"
    op1 = "| 1 | Post a question\n" 
    op2 = "| 2 | Search for posts\n"
    op3 = "| 3 | Post action-Answer\n"
    op4 = "| 4 | Post action-Vote\n"
    op5 = "| 5 | Post action-Mark as the accepted\n"
    op6 = "| 6 | Post action-Give a badge\n"
    op7 = "| 7 | Post action-Add a tag\n"
    op8 = "| 8 | Post Action-Edit\n"
    op9 = "| 9 | Logout\n"
    op10 ="| 10| Exit\n"
    b1 =  "______________________________________\n"
    

    if privilege is True:
        print("\n",header,op1,op2,op3,op4,op5,op6,op7,op8,op9,op10,b1)
    else:   
        print("\n",header,op1,op2,op3,op4,op9,op10,b1)
        

    selection = input("Make a selection from the menu by entering the option number: ")


    while selection not in ['1','2','3','4','5','6','7','8','9','10']:
        print("Please enter a valid selection !")
        selection = input("Make a selection from the menu by entering the option number: ")
        
    if selection == '1':
        PostAQuestion(currUser)
    elif selection == '2':
        SearchForPosts(currUser)
    elif selection == '3':
        PostActionAnswer(currUser)
    elif selection == '4':
        PostActionVote(currUser)
    elif selection == '5' and privilege is True:
        PostActionMarkAsTheAccepted(currUser)
    elif selection == '6' and privilege is True:
        PostActionGiveABadge(currUser)
    elif selection == '7' and privilege is True:
        PostActionAddATag(currUser)
    elif selection == '8' and privilege is True:
        PostActionEdit(currUser)
    elif selection == '9':
        logout(currUser)
    else:
        #when selection == 10
        exitProgram(currUser)
        
        
def PostAQuestion(currUser):
    pass

def SearchForPosts(currUser):
    pass

def PostActionAnswer(currUser):
    pass

def PostActionVote(currUser):
    pass

def PostActionMarkAsTheAccepted(currUser):
    pid = input("Enter an answer pid: ")
    cursor.execute("select * from answers where pid=?;",[pid])
    post = cursor.fetchone()
    cursor.execute("select * from questions where pid=?",[post[1]])
    question = cursor.fetchone()
    cursor.execute("update questions set theaid=:a where pid=:p",{"a":post[0],"p":question[0]})
    displayMenu(currUser)

def PostActionGiveABadge(currUser):
    pid = input("Enter a post pid: ")

    displayMenu(currUser)

def PostActionAddATag(currUser):
    pid = input("Enter a post pid: ")
    displayMenu(currUser)

def PostActionEdit(currUser):
    pid = input("Enter a post pid: ")
    displayMenu(currUser)

main()
