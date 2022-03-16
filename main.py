import mysql.connector
from tabulate import tabulate

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Password@123",
    auth_plugin='mysql_native_password',
)
mycursor = mydb.cursor()
try:
    mycursor.execute("CREATE DATABASE library")
except:
    print("Already Exists")

mycursor.execute("use library")

try:
    mycursor.execute("create table books(id int primary key,title varchar(50),author varchar(50),publisher varchar(50),"
                     "edition varchar(50), cost FLOAT, category varchar(50), member_id int, is_active boolean)")
    mycursor.execute("create table members(id int primary key,name varchar(50),phone varchar(50),number_of_books_issued int, is_active boolean)")
except:
    print("Already Exists")



print("Welcoen to yhe Library")

def addNewBook():
    bookId = int (input ("Enter a book id: "))
    title = input ("Enter book title: ")
    author = input ("Enter author of the book : ")
    publisher = input ("Enter book publisher: ")
    edition = input ("Enter edition of book: ")
    cost = float (input ("Enter cost of the book: "))
    category = input ("Enter category of book : ")
    member_id = None
    active = bool(True)
    mycursor = mydb.cursor()
    mycursor.execute ("INSERT INTO books VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9)",
                      (bookId, title, author, publisher, edition, cost, category,member_id,active))

def searchBook():
    title = input ("Enter a book name: ")
    mycursor.execute("select * from books where title=:title",{'title':title})
    res=mycursor.fetchall()
    if res:
        print(tabulate(res))
    else:
        print ("Not Found")

def deleteBook():
    bookId = int (input ("Enter a book id: "))
    mycursor.execute("select * from books where id=:bookId",{'bookId':bookId})

def showBooks():
    mycursor.execute("select * from books where is_active")
    res=mycursor.fetchall()
    if res:
        print(tabulate(res))
    else:
        print ("Not Found")

def addNewMember():
    id = int (input ("Enter a member id : "))
    name = input ("Enter member name: ")
    phoneno = int (input ("Enter phone number : "))
    mycursor.execute ("INSERT INTO members VALUES (:1,:2,:3,:4,:5)",(id, name, phoneno, 0,True))


def searchMember():
    name = input ("Enter a member name: ")
    mycursor.execute("select * from members where name=:name",{'name':name})
    res=mycursor.fetchall()
    if res:
        print ("Member Details are :\n")
        print(tabulate(res))
    else:
        print ("Not Found")


def deleteMember():
    mid= int (input ("Enter a member id : "))
    mycursor.execute("update members set is-active = 0 where id=:mid",{'mid':mid})
    print ("Member Deleted Successfully")

def showMembers():
    mycursor.execute("select * from members where is_active")
    res=mycursor.fetchall()
    if res:
        print(tabulate(res))
    else:
        print ("Not Found")

def issueBooks ():
    book_name = input ("Enter book name :")
    mycursor.execute("select * from books where name=:name",{'name':book_name})
    res=mycursor.fetchall()
    if res:
        m_name = input ("Enter member name: ")
        mycursor.execute("select * from members where name=:name",{'name':m_name})
        res2=mycursor.fetchall()
        if res2:
            member_id = res2[0][0]
            number_of_books = res2[0][3]

            # update the books table as book has been issued
            mycursor.execute("update books set member_id =: mid where name=:name",{'name':book_name, 'mid': member_id})
            #update the members table as number of books issued has changed
            number_of_books += 1
            mycursor.execute("update members set number_of_books_issued =:number_of_books where id=:mid",{'mid':member_id, 'number_of_books':number_of_books})
            print ("Book issued successfully")
        else:
            print("No such Member Found")
    else:
        print ("No Book Found in the Library")
        return

def returnBook():
    m_id=input ("Enter a member id : ")
    book_name = input ("Enter book name : ")
    mycursor.execute("select * from books where name=:name and member_id =:m_id",{'name':book_name, 'm_id':m_id})
    res=mycursor.fetchall()
    if res:
        ans = input ("Are you sure you want to return")
        if ans.lower () == "yes":
            mycursor.execute("select number_of_books_issued from members where id=:id",{'id':m_id})
            res2=mycursor.fetchall()
            number_of_books = res2[0][0]

            # update the books table as book has been issued
            mycursor.execute("update books set member_id = null where name=:name and member_id =:mid",{'name':book_name, 'mid': m_id})
            #update the members table as number of books issued has changed
            number_of_books -= 1
            mycursor.execute("update members set number_of_books_issued =:number_of_books where id=:mid",{'mid':m_id, 'number_of_books':number_of_books})
            print ("Book returned successfully")

        else:
            print ("Return operation cancelled")

    else:
        print ("The book is not issued to the member")
        return


def showissuedBooks ():
    mycursor.execute("select * from books where member_id is not null")
    res=mycursor.fetchall()
    if res:
        print(tabulate(res))
    else:
        print ("Not Found")

def deleteissuedBooks ():
    book_name = input ("Enter a book name: ")
    mycursor.execute("update books set is_active = 0 where name=:name",{'name':book_name})
    print("Deleted Issuied Book Successfully")

def showMenu():
    print ("-------------------------------------------------------------------------------")
    print ("                          NATIONAL DIGITAL LIBRARY                             ")
    print ("-------------------------------------------------------------------------------")
    print ("Press 1  - Add a New Book")
    print ("Press 2  - Search for a Book")
    print ("Press 3  - Delete & Book")
    print ("Press 4  - Show All Books")
    print ("Press 5  - Add a New Member")
    print ("Press 6  - Search for a Member")
    print ("Press 7  - Delete a Member")
    print ("Press 8  - Show All Members")
    print ("Press 9  - Issue a Book")
    print ("Press 10 - Return a Book")
    print ("Press 11 - Show All Issued Books")
    print ("Press 12 - Delete a Issue a Book")
    print ("Press 13 - To view Charts")
    print ("Press 14 - To exit")

    choice = int (input ("Enter your choice : "))
    return choice



# def showCharts():
#
#     print("Press 1 - Books and their Cost") print ("Press 2 - Number of Books issued by members
#
#     ch int (input ("Enter your choice : "))
#
#     =
#
#     if ch ==== 1:
#
#         df pd. read_csv (r"D:\\IP LIBRARY\\EXEL FILES\\
#
#     df = df [["title", "cost"]]
#
#     df.plot("title", "cost", kind='bar')
#
#     plt.xlabel ('title-->')
#
#     plt.ylabel('cost-->') plt.show()
#
#     if ch== 2:
#
#         df pd. read_csv (r"D:\\IP LIBRARY\\EXEL FILES\\\
#
#     df = df [ ["numberofbookissued", "m_name"]]
#
#     df.plot (kind='bar', color="red")
#
#     plt.show()

def login():
    while True:
        ch = showMenu()
        if ch == 1:
            addNewBook()
        elif ch == 2:
            searchBook()
        elif ch == 3:
            deleteBook()
        elif ch == 4:
            showBooks()
        elif ch == 5:
            addNewMember()
        elif ch == 6:
            searchMember()
        elif ch == 7:
            deleteMember()
        elif ch == 8:
            showMembers()
        elif ch == 9:
            issueBooks()
        elif ch == 10:
            returnBook()
        elif ch == 11:
            showIssuedBooks()
        elif ch == 12:
            DeleteIssuedBooks()
        elif ch == 13:
            showCharts()
        elif ch == 14:
            break;
        else:
            print("Wrong Choice")
    print("Thank You")

login()