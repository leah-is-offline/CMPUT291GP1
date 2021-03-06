import sqlite3
import time
import hashlib
import os
import sys

connection = None
cursor = None
matches = None


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


def main(argv):
    global connection, cursor

    '''during demo DB will be passed through command line.
    Okay to connect this way FOR NOW (generates db in CWD)'''
    path="./GP1DB.db"
    if len(argv)>0:
        if os.path.isfile(argv[0]):
            path = argv[0]
    connect(path)

    '''dont need to run the three following commands every run
    just to instantiate the db and define the tables '''
    #dropTables() 
    #defineTables()
    #insertData()

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

    cursor.execute(' PRAGMA foreign_keys=OFF; ')
    connection.commit()

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

    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()


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

    #NOTE: because python is asynch --> when you insert blocks of data like this, you have
    #to turn of foreign key constraints until you satisfy the constraint, or insert into
    #both tables in the same query.

    
    insert_users =  '''
                        INSERT INTO users (uid, name, pwd, city, crdate) VALUES
                        ('u100', 'Davood Rafiei' , 'totallyapassword123', 'Edmonton'  , '2020-01-10'),
                        ('u200', 'Joe Smith'     , 'password789'        , 'Vancouver' , '2020-08-15'),
                        ('u300', 'Mary Brown'    , 'CatsBirthdayPswrd'  , 'Edmonton'  , '2020-06-04'),
                        ('u400', 'Rick James'    , 'rickjamespassword'  , 'Edmonton'  , '2020-02-12'),
                        ('u500', 'uncle bill'    , 'qwertypass'         , 'Vancouver' , '2019-03-10'),
                        ('u600', 'Leah Copeland' , 'password'           , 'Edmonton'  , '2020-10-31');
                    '''
    
    insert_privileged = '''
                            INSERT INTO privileged (uid) VALUES
                            ('u500'),
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
                        ('p001' , date('now','-2 days') , 'how many bytes of data exist in all sqlite databases?' , 'someone else do the math', 'u600'),
                        ('p002' , date('now','-2 days') , 'has anyone seen my wallet?'  ,  'I CANT FIND IT ANYWHERE please I have so many stamp cards', 'u500'),
                        ('p003' , date('now','-2 days') , 'Why are you guys doubting im Rick James?', 'Seriously its me', 'u400'),
                        ('p004' , date('now','-2 days') , 'I have your wallet' , 'I am using your stamp cards','u100'),
                        ('p005' , date('now','-2 days') , 'No, I have not seen your wallet', null , 'u200'),
                        ('p006' , date('now','-2 days') , 'I doubt this guy is actually rick james' , 'prove that you are rick james then', 'u300'),
                        ('p100' , date('now','-30 days'), 'What is a relational database?' , 'What is the term referred to and what are the benefits?','u200'),
                        ('p200' , date('now','-29 days'), 'introduction to relational databases' , 'This is a post that introduce the relational databases including SQL','u100');
                   '''
    
    insert_tags = '''
                        INSERT INTO tags (pid, tag) VALUES
                        ('p100', 'relational'),
                        ('p100', 'database'),
                        ('p200', 'relational'),
                        ('p200', 'sql'),
                        ('p001', 'sql'),
                        ('p001', 'database'),
                        ('p001', 'cool'),
                        ('p001', 'big number'),
                        ('p001', 'relational'),
                        ('p002', 'controversial'),
                        ('p002', 'Wallet'),
                        ('p003', 'controversial'),
                        ('p003', 'rick james'),
                        ('p003', 'cOOl'),
                        ('p004', 'Wall      et'),
                        ('p005', 'Wallet'),
                        ('p006', 'Rick James');
                  '''

    
    insert_votes = '''
                        INSERT INTO votes (pid, vno, vdate, uid) VALUES
                        ('p200',1,date('now','-20 days'),'u200'),
                        ('p003',1,date('now'),'u400'),
                        ('p006',1,date('now'),'u400'),
                        ('p006',2,date('now'),'u600'),
                        ('p006',3,date('now'),'u300');
                   '''

    insert_questions = '''
                           INSERT INTO questions (pid, theaid) VALUES
                           ('p100' , null),
                           ('p002', null),
                           ('p003', null),
                           ('p001', null);
                       '''

    
    insert_answers = '''
                        INSERT INTO answers (pid,qid) VALUES
                        ('p200','p100'),
                        ('p004','p002'),
                        ('p005','p002'),
                        ('p006','p003');
                     '''


    cursor.execute(insert_users)
    cursor.execute(insert_privileged)
    cursor.execute(insert_badges)
    cursor.execute(insert_ubadges)
    cursor.execute(insert_posts)
    cursor.execute(insert_tags)
    cursor.execute(insert_votes)
    cursor.execute(insert_questions)
    cursor.execute(insert_answers)
    connection.commit()


    #we have to update accepted answers after the questions have been entered into the DB
    #because of the bi-directional REFERENCE/dependency between questions and answers table. 
    cursor.execute("UPDATE questions SET theaid = 'p004' WHERE pid='p002';")
    cursor.execute("UPDATE questions SET theaid = 'p006' WHERE pid='p003';")


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


    cursor.execute('SELECT name FROM users WHERE uid=?;',(uid,))
    name = cursor.fetchone()[0]
    
    print("Successfully logged in!\nWelcome back {uname}".format(uname = name))

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
    #function to display menu for all users

    header = "| # | Option\n"
    op1 = "| 1 | Post a question\n" 
    op2 = "| 2 | Search for posts\n"
    op3 = "| 3 | Logout\n"
    op4 = "| 4 | Exit\n"
    b1 =  "______________________________________\n"
    b2 = "\n************************************************"
    print(b2 + "\nTo perform post actions, search for posts first" + b2)
    
    print("\n",header,op1,op2,op3,op4,b1)
    
    selection = input("Make a selection from the menu by entering the option number: ")


    while selection not in ['1','2','3','4']:
        print("Please enter a valid selection !")
        selection = input("Make a selection from the menu by entering the option number: ")
        
    if selection == '1':
        PostAQuestion(currUser)
    elif selection == '2':
        SearchForPosts(currUser)
    elif selection == '3':
        logout(currUser)
    else:
        #when selection == 4
        exitProgram(currUser)
        

def displayPostActionMenu(currUser,pid):
        #function display the appropriate menu depending on privelege

    privilege = checkPrivilege(currUser)

    header = "| # | Option\n"
    op1 = "| 1 | Post action-Answer\n"
    op2 = "| 2 | Post action-Vote\n"
    op3 = "| 3 | Post action-Mark as the accepted\n"
    op4 = "| 4 | Post action-Give a badge\n"
    op5 = "| 5 | Post action-Add a tag\n"
    op6 = "| 6 | Post Action-Edit\n"
    op7 = "| 7 | Logout\n"
    op8 = "| 8 | Exit\n"
    b1 =  "______________________________________\n"
    

    if privilege is True:
        print("\n",header,op1,op2,op3,op4,op5,op6,op7,op8,b1)
    else:   
        print("\n",header,op1,op2,op7,op8,b1)
        

    selection = input("Make a selection from the menu by entering the option number: ")

    if privilege is True:
        while selection not in ['1','2','3','4','5','6','7','8']:
            print("Please enter a valid selection !")
            selection = input("Make a selection from the menu by entering the option number: ")
    else:
        while selection not in ['1','2','7','8']:
            print("Please enter a valid selection !")
            selection = input("Make a selection from the menu by entering the option number: ")

        
    if selection == '1':
        PostActionAnswer(currUser,pid)
    elif selection == '2':
        PostActionVote(currUser,pid)
    elif selection == '3' and privilege is True:
        PostActionMarkAsTheAccepted(currUser,pid)
    elif selection == '4' and privilege is True:
        PostActionGiveABadge(currUser,pid)
    elif selection == '5' and privilege is True:
        PostActionAddATag(currUser,pid)
    elif selection == '6'and privilege is True:
        PostActionEdit(currUser,pid)
    elif selection == '7':
        logout(currUser)
    else:
        #if selection == 8
        exitProgram(currUser)


def generatePid():
    #function to generates a unique pid
    global connection, cursor, pidNum

    #normally post id should increase in chronological order
    cursor.execute('SELECT COUNT(pid) FROM posts;') #how many posts are there
    pidNum = (cursor.fetchone()[0] + 1) #increase that value by 1
    pid = ('p' + str(pidNum).zfill(3)) #python zfill pads the left with zeros until reaching the specified length(3). (operates on strings)

    #BUT the test data could have completely random pids (not chronological) so increase pid value until pid is UNIQUE 
    cursor.execute('SELECT pid FROM posts p WHERE p.pid =?', (pid,))
    while cursor.fetchone() is not None:
        pidNum += 1
        pid = ('p' + str(pidNum).zfill(3))
        print("pid was in DB. assigning new pid = ", pid)
        cursor.execute('SELECT pid FROM posts p WHERE p.pid =?', (pid,))

    return pid


def displayEndPostActionMenu(currUser):
    #function to display the menu that should appear everytime a post action is finished

    header = "| # | Option\n"
    op1 = "| 1 | Back to main menu\n"
    op2 = "| 2 | Logout\n"
    op3 = "| 3 | Exit\n"
    b1 =  "______________________________________\n"

    print("\n",header,op1,op2,op3,b1)
    selection = input("Make a selection from the menu by entering the option number: ")

    while selection not in ['1','2','3']:
        print("Please enter a valid selection !")
        selection = input("Make a selection from the menu by entering the option number: ")

    if selection == '1':
        displayMenu(currUser)
    elif selection == '2':
        logout(currUser)
    else:
        exitProgram(currUser)
    
        
def PostAQuestion(currUser):
    #function to let a user post a question
    global connection, cursor

    title = input("Enter a title for your question: ")
    #https://www.tiaztikt.nl/derek-parfit-on-empty-questions-from-reasons-and-persons-1984/
    while len(title) < 1:
        title = input("\"An empty question has no answer\" - Derek Parfit(1984).\nEnter a valid title for your question: ")

    if title[-1] != "?":
        title += "?"

    #ASSUMPTION - the body does not need text as the question title may provide enough information.
    body = input("Enter a body for your question(optional): ")
    if len(body) < 1:
        body = " "

    pid = generatePid()

    #Insert values into posts table first, then into questions table.
    cursor.execute("INSERT INTO posts(pid, pdate, title, body, poster) VALUES (?, date('now'),?,?,?);",(pid, title, body, currUser._uid))
    cursor.execute("INSERT INTO questions(pid, theaid) VALUES (?, null);", (pid,))

    connection.commit()
    print("Question successfully posted.")
    displayEndPostActionMenu(currUser)



def countMatches(keywords):
    #function that counts unique matches (in title,body,or post tag) per keyword provided by user. 
    global connection, cursor, matches

    matches = {}

    #initialize matches to 0 for all posts (integer so we can increase count)
    cursor.execute("SELECT pid FROM posts;")
    pids = cursor.fetchall()
    if pids is not None:
        for pid in pids:
            matches[pid[0]] = 0

    #increase count of matches per pid of keyword
    #keywords either in title, body, or tag fields as per spec
    for key in keywords:
        key = "%" + key + "%" #add wildcard operators to keyword
        cursor.execute("SELECT DISTINCT(p.pid) FROM posts p LEFT JOIN tags t ON p.pid = t.pid WHERE p.title LIKE ? OR p.body LIKE ? OR t.tag LIKE ?;",(key,key,key))
        pids = cursor.fetchall()
        if pids is not None:
            for pid in pids:
                matches[pid[0]] += 1


def getMatches(pid):
    #function to return how many matches a pid has in the list of provided keywords
    global matches
    
    return matches[pid]

def executeSearchQuery(displayLimit, currUser):
    #function to execute search query, provided with user defined limit
    #recall that cursor and connection are global in scope of program
    global connection, cursor, matches

    #initialize a list containing only pids that matched at least one keyword
    pidMatches = []
    for key in matches.keys():
        if matches[key] != 0:
            pidMatches.append(key)

    #CITATION: StackOverflow post by bobince https://stackoverflow.com/a/283801
    placeholder = '?'
    placeholders = ', '.join([placeholder] * len(pidMatches))


    #columns of posts table, number of votes, number of answers if post is a question(0 if no answers)
    #order based on the number of matching keywords (posts matching largest number of keywords on top
    #at most 5 matches shown at a time
    search_query = '''
                    SELECT  p.pid, p.pdate, p.title, p.body, p.poster, ifnull(COUNT(v.vno),0), COUNT(a.qid)
                    FROM posts p LEFT OUTER JOIN votes v ON v.pid = p.pid LEFT OUTER JOIN answers a ON p.pid = a.qid
                    LEFT OUTER JOIN (SELECT pid, getMatches(pid) as matches FROM posts) matchTbl ON matchTbl.pid = p.pid
                    WHERE p.pid IN (%s)
                    GROUP BY p.pid, p.pdate, p.title, p.body, p.poster
                    ORDER BY matches DESC
                    LIMIT ?;'''% placeholders
    
    pidMatches.append(displayLimit)
    cursor.execute(search_query, pidMatches) #when passing in a list of values, no brackets. 

    #display the results
    results = cursor.fetchall()
    if results is not None:
        for result in results:
            print('|'.join(str(val) for val in result))
    else:
        print("There were no matches for your keywords")


    displayEndSearchMenu(displayLimit, currUser)


def SearchForPosts(currUser):
    #lets a user search for posts
    global connection, cursor, matches

    #default display limit
    displayLimit = 5 

    #get keywords from user
    keywords = input("Enter keywords to search for a post (or press enter to return all posts): ")
    while len(keywords) < 0:
        keywords = input("Please enter more than 0 keywords: ")
    keywords = list(keywords.split(" "))

    #initiliaze the GLOBAL dictionary containing pids and their corresponding matches to keywords
    countMatches(keywords)

    
    #initialize user defined function
    connection.create_function('getMatches', 1, getMatches)
    
    #execute searchy query
    executeSearchQuery(displayLimit, currUser)

    displayEndSearchMenu(displayLimit,currUser)
    

def displayEndSearchMenu(displayLimit, currUser):
    #funtion to diplay the menu after a search is performed
    global connection, cursor
    
    #letting the user select a post or see more matches.    
    header = "| # | Option\n"
    op1 = "| 1 | Display more posts\n"
    op2 = "| 2 | Perform a post action\n"
    op3 = "| 3 | Back to main menu\n"
    b1 =  "______________________________________\n"

    print("\n",header,op1,op2,op3,b1)
    selection = input("Make a selection from the menu by entering the option number: ")

    while selection not in ['1', '2','3']:
        print("Please enter a valid selection !")
        selection = input("Make a selection from the menu by entering the option number: ")
        
    if selection == '1':
        #display 5 more posts from the search query
        displayLimit += 5
        executeSearchQuery(displayLimit, currUser) 
    elif selection == '2':
        #navigate to post action menu after user provides post id
        pid = input("enter the post id you would like to perform an action on: ")
        cursor.execute('SELECT * FROM posts p WHERE p.pid=?', (pid,))
        while cursor.fetchone() is None:
            pid = input("Please enter a valid post id: ")
            cursor.execute('SELECT * FROM posts p WHERE p.pid=?', (pid,))
        displayPostActionMenu(currUser,pid)
    else:
        #back to main menu
        displayMenu(currUser)
    

def PostActionAnswer(currUser, pid):
    #function to let a user post an answer to a question, if the post selected is a question
    global connection, cursor

    cursor.execute('SELECT * FROM posts p, questions q WHERE q.pid = p.pid AND p.pid = ?;', (pid,))
    while cursor.fetchone() is None:
            print("The post you selected is not a question\n")
            pid = input("Please enter a valid post id of a question: ")
            cursor.execute('SELECT * FROM posts p, questions q WHERE q.pid = p.pid AND p.pid = ?;', (pid,))

    qid = pid
    pid = generatePid()

    title = input("Enter the title for your answer: ")
    while len(title) < 1:
        title = input("Your answer must have a title.\nEnter a valid title for your answer: ")

    #ASSUMPTION - the body does not need text as the answer title may provide enough information.
    body = input("Enter a body for your answer(optional): ")
    if len(body) < 1:
        body = " "

    #Insert values into posts table first, then into answers table.
    cursor.execute("INSERT INTO posts(pid, pdate, title, body, poster) VALUES (?, date('now'),?,?,?);",(pid, title, body, currUser._uid))
    cursor.execute("INSERT INTO answers(pid, qid) VALUES (?,?);", (pid,qid))

    connection.commit()
    print("Answer successfully posted.")
    displayEndPostActionMenu(currUser)

def PostActionVote(currUser, pid):
    #function to let a user vote on a post, if they have not voted on it yet
    global connection, cursor
    cursor.execute('SELECT * FROM votes WHERE uid = ? AND pid = ?;', (currUser._uid, pid))
    while cursor.fetchone() is not None:
            print("You have already voted on this post\n")
            pid = input("Please enter a valid post id (one you have yet to vote on): ")
            cursor.execute('SELECT * FROM votes WHERE uid = ? AND pid = ?;', (currUser._uid, pid))


    "vno assigned by your system"
    #"All votes in the project are upvotes (downvotes are not considered)."
    cursor.execute('SELECT COUNT(vno) FROM votes WHERE pid = ?;',(pid,))
    vno = (cursor.fetchone()[0] + 1)

    #insert values into votes table
    cursor.execute("INSERT INTO votes (pid, vno, vdate, uid) VALUES (?,?,date('now'),?);",(pid,vno,currUser._uid))

    connection.commit()
    print("Post successfully voted on.")
    displayEndPostActionMenu(currUser)

def PostActionMarkAsTheAccepted(currUser, pid):
    #check the post is an answer
    cursor.execute("select * from answers where pid=?;", [pid])
    post = cursor.fetchone()
    while post is None:
        print("The post you selected is not an answer\n")
        pid = input("Please enter a valid post id of an answer (to be marked accepted): ")
        cursor.execute("select * from answers where pid=?;", [pid])
        post = cursor.fetchone()
    cursor.execute("select * from questions where pid=?;", [post[1]])
    question = cursor.fetchone()
    if question[1]:
        #if the question already has an answer prompt to overwrite
        choice = input("Question has accepted answer ("+question[1]+") Enter 1 to overwrite: ")
        if choice == '1':
            cursor.execute("update questions set theaid=? where pid=?;", [post[0], question[0]])
            connection.commit()
        else:
            print("Invalid input. Accepted answer not overwritten")
    else:
        cursor.execute("update questions set theaid=? where pid=?;", [post[0], question[0]])
        connection.commit()
    displayEndPostActionMenu(currUser)

def PostActionGiveABadge(currUser, pid):
    cursor.execute("select * from posts where pid=?;", [pid])
    post = cursor.fetchone()
    poster = post[4]
    cursor.execute("select distinct(bname) from badges;")
    badges = cursor.fetchall()
    bname = input("Enter a badge {bn}: ".format(bn=badges))
    #check that badge exists
    cursor.execute("select bname from badges where bname=?;", [bname])
    badge = cursor.fetchone()
    while badge is None:
        #prompt for valid badge or cancel
        bname = input("Enter a valid badge(blank to cancel): ")
        cursor.execute("select bname from badges where bname=?;", [bname])
        badge = cursor.fetchone()
        if not bname:
            break
    if bname:
        #check if the user got the badge today
        cursor.execute("select * from ubadges where uid=? and bdate=date('now') ", [poster])
        if cursor.fetchone() is None:
            cursor.execute("insert into ubadges (uid, bdate, bname) values (?, date('now'), ?);", [poster, bname])
            print("Badge successfully awarded.")
            connection.commit()
        else:
            print("User already has a badge\n")

    displayEndPostActionMenu(currUser)

def PostActionAddATag(currUser, pid):
    tagIn = input("Enter tag(s): ")
    #split tags into list
    tags = tagIn.split(" ")
    new_tag = False
    for tag in tags:
        #iterate over list and add non-duplicate tags
        cursor.execute("select * from tags where pid=? and tag=?;", [pid, tag])
        duplicate = cursor.fetchone()
        if not duplicate and (len(tag) > 0):
            cursor.execute("insert into tags (pid, tag) values (?, ?);", [pid, tag])
            
            new_tag = True
        elif len(tag) == 0:
            print("Your tag was empty and was not entered.")
        else:
            print("This post already has that tag. Your tag was not entered.")
    if new_tag:
        connection.commit()
    displayEndPostActionMenu(currUser)


def PostActionEdit(currUser, pid):
    #edit title and/or body
    title = input("Enter new title(blank for no change): ")
    body = input("Enter new body(blank for no change): ")
    if title and body:
        cursor.execute("update posts set title=?, body=? where pid=?;", [title, body, pid])
    elif title:
        cursor.execute("update posts set title=? where pid=?;", [title, pid])
    elif body:
        cursor.execute("update posts set body=? where pid=?;", [body, pid])
    else:
        displayEndPostActionMenu(currUser)
        return
    
    connection.commit()
    displayEndPostActionMenu(currUser)
    

if __name__ == "__main__":
    main(sys.argv[1:])
