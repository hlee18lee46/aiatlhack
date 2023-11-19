import mysql.connector
import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image
import pytesseract
import re
from mysql.connector import pooling

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'  # your path may be different

loginStatus = True

def verifyLoginStatus():
    return loginStatus

def verifyLogin(email: str, password: str):

    # Attempt connection to Oracle db.
    try: 
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DlGkS!2#4%",
        database="mydatabase"
        )
        print("Connected to database")
    except:
        print("Was not able to connect to database")
    print("debug1")
    cur = connection.cursor()
    print("debug2")
    # Check if the user even exists
    select_stmt = "select * from users where email = %(email)s"
    cur.execute(select_stmt, { 'email': email })
    print("debug3")
    number = cur.fetchall() 
    if (len(number) != 1):
        print("User with email does not exist")
        return None
    select_stmt = "select * from users where email = %s and password = %s"
    cur.execute(select_stmt, (email, password))
    user = cur.fetchall()
    cur.close()
    connection.close()
    if (len(user) != 1):
        print("Password does not match, try again")
        return None
    print("Successfully verified user")
    return user
def login(email, password):

    user = verifyLogin(email, password)

    if user is None:
        st.write("Your email and/or password are incorrect")

    else:

        user_email = user[0][0]

        st.experimental_set_query_params(user="user", email=user_email)

        st.write("You are logged in")

        loginStatus = True

def addUser(email: str, password: str) -> str:

    #hashedEmail = hashCode(email).hexdigest()
    #hashedPassword = hashCode(password).hexdigest()

    # Attempt connection to Oracle database.
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DlGkS!2#4%",
        database="mydb"
        )
        print("Connected to database")

    except:
        print("Was not able to connect to the database.")
    cur = connection.cursor()
    try:
        select_stmt = "INSERT INTO users (email, password) VALUES (%s, %s)"
        cur.execute(select_stmt, (email, password))
        connection.commit()
        output = "Added user into database"
    except:
        output = "Unsuccessful"  
    cur.close()  
    connection.close()
    return output
def imgToText(image_path):
    # Open the image using Pillow
    img = Image.open(image_path)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(img)

    return text

def insertData(image_path, email):
    # Replace 'path/to/your/receipt/image.jpg' with the actual path to your receipt image
    #image_path = 'wal5.jpg'

    # Perform receipt recognition
    result_text = imgToText(image_path)

    # Print the recognized text
    #print("Recognized Text:")
    #print(result_text)

    recog1 = 'WAL*MART'
    recog2 = 'ST#'
    recog3 = 'TR#'
    recog4 = 'SUBTOTAL'

    index1 = result_text.find('WAL*MART') + len(recog1)

    trimmedText = result_text[index1:]
    trimmedText = trimmedText.replace(' ','')
    #trimmedText = trimmedText.replace('\n','')

    #print('Trimmed Text: ', trimmedText)

    #print('Text: ', result_text)

    storeID = result_text[result_text.find(recog2)+4:]
    storeID = storeID[:storeID.find(' ')]

    #print('store substring:', store)

    indexSpace = result_text.find('\n')+1

    #print('indexSpace: ', indexSpace)

    ctst = trimmedText[0:indexSpace]

    ctst = ctst.replace('\n','')

    #print('city state:',ctst)

    commaIndex = ctst.find(',')

    #print('City commaIndex: ',commaIndex)

    city = ctst[:commaIndex]

    #print('city:', city)

    st = ctst[commaIndex+1:]

    #print('st:', st)

    trimmedText = result_text[result_text.find(recog3)+4:].replace('','')

    print('trimmedText',trimmedText)



    dateTimeText = trimmedText[trimmedText.find('# ITEMS SOLD')+len('# ITEMS SOLD')+1:]

    receiptID = dateTimeText[dateTimeText.find('TCH ')+4:dateTimeText.find('TCH ')+28]

    receiptID=receiptID.replace(' ','')

    print('TCH??',receiptID)

    if 'TC#' in receiptID:
        receiptID=receiptID[3:]

    receiptID = int(receiptID)

    month = dateTimeText[dateTimeText.find('/')-2:dateTimeText.find('/')]

    

    #print('\nmonth\n', month)
    #print('\nmonthLength\n', len(month))

    if len(month) == 2 and month[:1] == '0':
        month = month[1:]

    #print('\nmonth\n', month)
    #print('\nmonthLength\n', len(month))

    dateTimeText = dateTimeText[dateTimeText.find('/')+1:]

    #print('\nnew dateTimeText string\n', dateTimeText)

    day = dateTimeText[dateTimeText.find('/')-2:dateTimeText.find('/')]

    if len(day) == 2 and day[:1] == '0':
        day = day[1:]

    #print('\nday\n', day)

    dateTimeText = dateTimeText[dateTimeText.find('/')+1:]

    #print('\nnew dateTimeText string\n', dateTimeText)

    year = dateTimeText[:2]

    #print('\nyear\n', year)

    dateTimeText = dateTimeText[2:]

    hour = dateTimeText[dateTimeText.find(':')-2:dateTimeText.find(':')]

    minute = dateTimeText[dateTimeText.find(':')+1:dateTimeText.find(':')+3]

    dateTimeText = dateTimeText[4:]

    second = dateTimeText[dateTimeText.find(':')+1:dateTimeText.find(':')+3]

    #print('\nhour\n', hour)

    #print('\nminute\n', minute)

    #print('\nsecond\n', second)

    #print('\nnew dateTimeText string\n', dateTimeText)

    #print('trimmed text:\n',trimmedText)

    trimmedText = trimmedText[:trimmedText.find(recog4)]

    lines = trimmedText.splitlines()

    print('dateTimeText',dateTimeText)

    #print('print each line\n')
    # Print each line
    for line in lines:
        if not all(line.isspace() for char in line) and line.find('.') != -1:
            print(line)
            #price = line[line.rfind(' '):]
            numbers = re.findall(r'\d+\.\d+|\d+', line)
            itemID = numbers[0]
            price = numbers[1]
            itemDesc = line[:line.find(itemID)-1]
            itemID = int(itemID)
            price = float(price)
            print('price:',price)
            print('itemID:',itemID)
            print('itemDesc:',itemDesc)
            addTrans(receiptID, email, itemID, itemDesc, price)

def addTrans(receiptID: int, email: str, itemID: int, itemDesc: str, price: float) -> str:
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DlGkS!2#4%",
        database="mydb",
        autocommit=True
        )
        print("Connected to database")
    except:
        print("Was not able to connect to the database.")
    print("db1")
    cur = connection.cursor()
    print("db2")

    try:
        print("db3")
        select_stmt = "INSERT INTO trans (receiptID, email, itemID, itemDesc, price) VALUES (%s, %s, %s, %s, %s)"
        print("db4")
        print(type(receiptID), receiptID)
        print(type(email), email)
        print(type(itemID), itemID)
        print(type(itemDesc), itemDesc)
        print(type(price), price)
        receiptID=str(receiptID)
        email=str(email)
        itemID=str(itemID)
        itemDesc=str(itemDesc)
        price=str(price)
        cur.execute(select_stmt, (receiptID, email, itemID, itemDesc, price))
        print("db5")
        connection.commit()
        print("db6")
        output = "Added trans into database"
    except:
        output = "Unsuccessful"  
    cur.close()  
    connection.close()

