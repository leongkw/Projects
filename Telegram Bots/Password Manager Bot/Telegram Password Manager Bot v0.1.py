import telepot, telepot.aio
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open

# -----------------------------------------------------------------------#
import sqlite3
import pandas as pd
import numpy as np
import time

# ------------------------------------------------------------------------#
# For PythonAnywhere
import urllib3
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, 
    								maxsize=10, retries=False, timeout=30),
					 }
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, 
															 maxsize=1, retries=False, timeout=30))

# -------------------------------------------------------------------------#



#  ___             _   _               _    _ _                      
# | __|  _ _ _  __| |_(_)___ _ _  ___ | |  (_) |__ _ _ __ _ _ _ _  _ 
# | _| || | ' \/ _|  _| / _ \ ' \(_-< | |__| | '_ \ '_/ _` | '_| || |
# |_| \_,_|_||_\__|\__|_\___/_||_/__/ |____|_|_.__/_| \__,_|_|  \_, |
#                                                               |__/ 

# Create new user
def create(username, db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
    
    except:
        resp = 'Unable to register username in database. Please try again later.'
        return resp
    
    query = '''CREATE TABLE ''' + str(username) + ''' (Website, Username, Password)'''
    cursor.execute(query)
    conn.commit()
    cursor.close()
    resp = 'Your username ' + username + ' has been registered on the database.'
    return resp

# Create new entry
def create_entry(website, uname, password, username, db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
    except:
        resp = 'Unable to create record in database. Please try again later.'
        return resp

    query = 'INSERT INTO ' + str(username) + ' VALUES' + " ('" + str(website) + "', '" + str(uname) + "', '" + str(password) + "');"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    resp = 'Ok, your entry has been saved in the database.'
    return resp

# Update username for one record
def update_uname(website, uname, username, db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
    except:
        resp = 'Unable to access record in database. Please try again later.'
        return resp

    query = 'UPDATE ' + str(username) + ' SET ' + 'Username = ' + "'" + uname + "' " + 'WHERE Website'  + ' =' + "'" + str(website) + "';"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    resp = 'Ok, your username for ' + str(website) + ' has been updated to ' + str(uname) + '.'
    return resp

# Update password for one record 
def update_password(website, password, username, db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
    except:
        resp = 'Unable to access record in database. Please try again later.'
        return resp

    query = 'UPDATE ' + str(username) + ' SET ' + 'Password = ' + "'" + password + "' " + 'WHERE Website'  + ' =' + "'" + str(website) + "';"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    resp = 'Ok, your password for ' + str(website) + ' has been updated.'
    return resp 

# List all records 
def showall(username, db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        query = 'SELECT * FROM ' + str(username)
        df = pd.read_sql_query(sql=query, con=conn)
        resp = 'Index' + ', ' + df.columns.values[0] + ', ' + df.columns.values[1] + ', ' + df.columns.values[2]
        for i in range(0, len(df.index), 1):
            resp += '\n'
            resp += str(i+1) + '. '
            resp += str(df.loc[i].values[0]) + ', ' + str(df.loc[i].values[1]) + ', ' + str(df.loc[i].values[2])
        cursor.close()
        return resp
    
    except:
        resp = 'Unable to access records in database. Please try again later.'
        return resp


    return resp

# Delete user account
def delete_user(username, db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
    except:
        resp = 'Unable to access records in database. Please try again later.'
        return resp

    query = 'DROP TABLE ' + username
    cursor.execute(query)
    conn.commit()
    cursor.close()
    resp = 'Ok ' + username + ', all your records have been wiped from the database.'
    return resp

# Delete one record 
def delete_entry(username, website, db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
    except:
        resp = 'Unable to access records in database. Please try again later.'
        return resp

    query = 'DELETE FROM ' + username + " WHERE Website = '" + website + "'"
    cursor.execute(query)
    conn.commit()
    resp = 'Ok, your records for ' + website + ' has been removed from the database.'
    return resp

# Show one record
def retrieve(username, website, db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
    except:
        resp = 'Unable to access records in database. Please try again later.'
        return resp

    query = 'SELECT * FROM ' + username + " WHERE Website = '" + website + "'"
    df = pd.read_sql_query(sql=query, con=conn)
    
    try:
        wsite = df['Website'][0]
        name = df['Username'][0]
        pword = df['Password'][0]
    except:
        error = 'Sorry, there are no records found for ' + website + '.'
        return error

    resp = 'Website: ' + wsite + '\n' + 'Username: ' + name + '\n' + 'Password: ' + pword
    return resp

# To check at log in stage if username entered is found in database
def verify_user(username, db):
    try:
        conn = sqlite3.connect(db)
        query = "SELECT * FROM " + username
        df = pd.read_sql_query(sql=query, con=conn)
        conn.close()
        
    except:
        resp = 'Sorry, the username that you entered is not found in the database.\nPlease ensure that you have entered the correct username.\n\nPlease type /start to try again.'
        return resp, False 
    
    output = username
    return output, True

# To check at account creation stage if chosen user name already exists in database
def similar_username(username, db):
    try:
        conn = sqlite3.connect(db)
        query = "SELECT * FROM " + username
        df = pd.read_sql_query(sql=query, con=conn)
        conn.close()
        
    except:
        resp = 'Username is available. Setting up records in database...'
        return resp, True 
    
    resp = 'Sorry, the username (' + username + ') that you chose is already taken.\n\nPlease try again with a new username.'
    output = resp
    return output, False

class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self.new_session = True
        
        # Value attributes
        self.login = ''
        self.website = ''
        self.username = ''
        self.password = ''
        self.uname = ''
        self.create = ''
        self.deletecheck = ''
        
        # Stage attributes - Used to track user state
        self.loginstage = 0
        self.createstage = 0
        self.newentrystage = 0
        self.menustage = 0
        self.uustage = 0
        self.upstage = 0
        self.delstage = 0
        self.delastage = 0
        self.findstage = 0
        
            
            
#   __  __                            _  _              _ _         
# |  \/  |___ ______ __ _ __ _ ___  | || |__ _ _ _  __| | |___ _ _ 
# | |\/| / -_|_-<_-</ _` / _` / -_) | __ / _` | ' \/ _` | / -_) '_|
# |_|  |_\___/__/__/\__,_\__, \___| |_||_\__,_|_||_\__,_|_\___|_|  
#                        |___/                                        
   
    def on_chat_message(self, message):
        content_type, chat_type, chat_id = telepot.glance(message)
        
        # State: /start entered
        # Bot welcomes user with welcome message
        # User enters menu, set menu stage = 1
        if message['text'] == '/start':
            bot.sendMessage(chat_id, 'Welcome to Password Manager Bot!\n\nPlease log in with your username.\n\nIf you have not registered, please enter /create to register a username in the database.')
            # Resetting everything except for menu stage
            self.login = ''
            self.website = ''
            self.username = ''
            self.password = ''
            self.uname = ''
            self.create = ''
            self.loginstage = 0
            self.createstage = 0
            self.newentrystage = 0
            self.menustage = 1
            
            
#----------------------------------- CREATE NEW USER ------------------------------------- 
        # State: menu stage = 1, user inputs /create
        # Set create stage = 1, as user enters /create mode
        # Bot prompts user for desired username, set create stage = 2 to proceed to next stage of /create 
        elif self.menustage == 1 and message['text'] == '/create':
            self.createstage = 1
            bot.sendMessage(chat_id, 'Welcome! To create a new user, please enter your desired username.')
            self.createstage = 2
        
        # State: create stage = 2
        # User inputed username saved as self.create
        # similar_username function used to check if user inputed username exists in database
        # checksum is either True/False
        # resp is the corresponding True/False reply
        elif self.createstage == 2:
            self.create = message['text']
            checksum = similar_username(self.create, database)[1]
            resp = similar_username(self.create, database)[0]
            
            # State: create stage = 2, checksum = False
            # False = User inputed username already exists in database
            # msg_out is the a message telling user to try another username for registration
            # self.create = '' to empty user input field
            # Set create stage = 2 to route back to checking part
            if checksum == False:
                msg_out = resp
                bot.sendMessage(chat_id, msg_out)
                self.create = ''
                self.createstage = 2
            
            # State: create stage = 2, checksum = True
            # True = User input username does not exists in database
            # msg_outs are messages telling user successful creation and to use /start to login with registered username
            # Set menu stage = 0, to reset menu state
            # Set create stage = 0 to reset create state
            # Set self.create = '', to reset user's input
            else:
                succ_resp = create(self.create, database)
                msg_out1 = resp + '\n\n' 
                msg_out2 = succ_resp + '\n\n' + 'Please enter /start to log in with your username.'
                bot.sendMessage(chat_id, msg_out1)
                bot.sendMessage(chat_id, msg_out2)
                self.menustage = 0
                self.createstage = 0
                self.create = ''

                
#----------------------------------- LOG IN -------------------------------------         
        # State: menu stage = 1, user input not a command, login stage = 0
        # Represents an attempt to log in
        # User input is saved as self.username
        # User input is processed by verify_user function
        # result is either True/False
        # True means user's input username can be found in database, therefore successful log in
        # False means user's input username cannot be found in database, therefore unsuccessful log in
        # resp is the corresponding response depending on True/False
        # msg is a welcome message sent to user upon successful log in
        elif self.menustage == 1 and self.loginstage == 0 and message['text'] not in commands and message['text'] != '/start':
            self.username = message['text']
            result = verify_user(self.username, database)[1]
            resp = verify_user(self.username, database)[0]
            msg = 'Welcome ' + self.username + ' !' + '\nTo see the commands available, please enter /help.'
            
            
            # State: menu stage = 1, result = True
            # True = Successful log in
            # Bot sends welcome message to user
            # Set login stage = 1, representing that user is logged in
            if result == True:
                bot.sendMessage(chat_id, msg)
                self.loginstage = 1
            
            # State: menu stage = 1, result = False
            # False = Unsuccessful log in
            # Bot tells user attempt to log in is not successful and to try again
            # Set menu stage = 1, reroute user to main menu
            # Set self.username = '', remove user input from self.username for clean slate
            elif result == False:
                bot.sendMessage(chat_id, resp)
                self.username = ''
                self.menustage = 1

                
#----------------------------------- LOG IN PROTECTION -------------------------------------                 
        # State: menu stage = 1, login stage = 0
        # Meant to catch people who are using bot commands but not logged in
        # No change in final state
        elif self.menustage == 1 and self.loginstage == 0 and message['text'] in commands:
            bot.sendMessage(chat_id, 'Please log in to use Password Manager Bot.\n\nEnter /start to navigate to the log in menu.')

            
#----------------------------------- ADD NEW RECORD -------------------------------------        
        # State: login stage = 1, menu stage = 1, user inputs /newentry as command        
        # Bot sends resp to prompt user to enter website
        # # Set newentry stage = 1, to move on to next step of /newentry
        elif self.loginstage == 1 and message['text'] == '/newentry':
            resp = 'Please enter the website which you will use the password.\n\nE.g. If storing password for Hotmail, enter Hotmail.'
            bot.sendMessage(chat_id, resp)
            self.newentrystage = 1
        
        # State: login stage = 1, newentry stage = 1, 
        # User input is saved as self.website
        # Bot sends resp to prompt user to input username
        # Set newentry stage = 2, representing move to next step of /newentry
        elif self.loginstage == 1 and self.newentrystage == 1:
            self.website = message['text']
            resp = 'Please enter your username for ' + self.website + '.'
            bot.sendMessage(chat_id, resp)
            self.newentrystage = 2
        
        # State: login stage = 1, newentry stage = 2
        # User input is saved as self.uname
        # Bot sends resp to prompt user to input password
        # Set newentry stage = 3, representing move to next step of /newentry
        elif self.loginstage == 1 and self.newentrystage == 2:
            self.uname = message['text']
            resp = 'Please enter your password for ' + self.website + '.'
            bot.sendMessage(chat_id, resp)
            self.newentrystage = 3
        
        # State: login stage = 3, newentry stage = 3
        # User input is saved as self.password
        # Bot sends resp1 to tell user that it has received all user's input
        # Try: Attempt to write user's data into database using create_entry function
        # Upon success, Bot sends resp2 to tell user it has successfully written saved input into database
        # Except: Bot sends resp3 to tell user there is an error
        # Set self.website, uname, password = '' regardless of failure/success to reset everything
        # Set newentrystage = 0 regardless of failure/success to reset /newentry process
        elif self.loginstage == 1 and self.newentrystage == 3:
            self.password = message['text']
            resp1 = 'Okay received your information. Writing information into database...'
            bot.sendMessage(chat_id, resp1)
            try:
                write = create_entry(self.website, self.uname, self.password, self.username, database)
                resp2 = 'Ok! The following information has been written into the database:\nWebsite: ' + self.website + '\n' 'Username: ' + self.uname + '\n' + 'Password: ' + self.password
                bot.sendMessage(chat_id, resp2)
            
            except:
                resp3 = 'There is an error creating your entry. Please try again later.'
                bot.sendMessage(chat_id, resp3)
            
            self.website = ''
            self.uname = ''
            self.password = ''
            self.newentrystage = 0

            
#----------------------------------- SHOW ALL RECORDS -------------------------------------            
        # State: login stage = 1, user inputs /listall as command
        # Bot sends user message telling user it has received user's request
        # showall function takes in user's username and retrieves all user's records from database
        # User's records are saved in resp, Bot sends resp to user
        elif self.loginstage == 1 and message['text'] == '/listall':
            bot.sendMessage(chat_id, 'Okay, displaying all records found under your username. Please give me a moment...')
            resp = showall(self.username, database)
            bot.sendMessage(chat_id, resp)

            
#----------------------------------- UPDATE USERNAME -------------------------------------  
        # State: login stage = 1, user inputs /updateusername as command
        # Bot prompts user for website
        # Set uustage = 1, to represent progression to next updateusername stage
        elif self.loginstage == 1 and message['text'] == '/updateusername':
            bot.sendMessage(chat_id, 'Please enter which website you would like to make an update for the username.\n\nE.g. If you would like to update your username for Hotmail, enter Hotmail.')
            self.uustage = 1
        
        # State: login stage = 1, uustage = 1
        # Bot stores user input as self.website
        # Bot tells user it is loading up records for user inputed website
        # Bot displays records for user inputed website for user's reference
        # Bot prompts user to enter new username
        # Set uustage = 2, representing progression to next updateusername stage
        elif self.loginstage == 1 and self.uustage == 1:
            self.website = message['text']
            resp1 = 'Ok, loading your records for ' + self.website + '...'
            bot.sendMessage(chat_id, resp1)
            resp2 = 'Your records for ' + self.website + ' are as follows:\n' + retrieve(self.username, self.website, database) +  '\n\nPlease enter your new username.'
            bot.sendMessage(chat_id, resp2)
            self.uustage = 2
        
        # State: login stage = 1, uustage = 2
        # Bot saves user inputed new username as self.uname
        # Bot acknowledges receipt
        # update_uname function is used to update username, generating a response depending on success/failure
        # Bot sends user response to indicate successful update/failure
        # Set self.uname = '', self.website = '', uustage = 0 to reset after update job is complete
        elif self.loginstage == 1 and self.uustage == 2:
            self.uname = message['text']
            bot.sendMessage(chat_id, 'Updating...')
            resp = update_uname(self.website, self.uname, self.username, database)
            bot.sendMessage(chat_id, resp)
            
            self.uname = ''
            self.website = ''
            self.uustage = 0
            

#----------------------------------- UPDATE PASSWORD -------------------------------------
        # State: login stage = 1, user inputs /updatepassword
        # Bot prompts user to enter website to update password
        # Set upstage = 1, to progress to next updatepassword stage
        elif self.loginstage == 1 and message['text'] == '/updatepassword':
            bot.sendMessage(chat_id, 'Please enter which website you would like to make an update for the password.\n\nE.g. If you would like to update your password for Hotmail, enter Hotmail.')
            self.upstage = 1
        
        # State: login stage = 1, upstage = 1
        # User inputed website is saved under self.website
        # Bot tells user it is loading up records for user inputed website
        # Bot displays records for user inputed website for user's reference
        # Bot prompts user to enter new password
        # Set upstage = 2, representing progression to next updatepassword stage 
        elif self.loginstage == 1 and self.upstage == 1:
            self.website = message['text']
            resp1 = 'Ok, loading your records for ' + self.website + '...'
            bot.sendMessage(chat_id, resp1)
            resp2 = 'Your records for ' + self.website + ' are as follows:\n' + retrieve(self.username, self.website, database) +  '\n\nPlease enter your new password.'
            bot.sendMessage(chat_id, resp2)
            self.upstage = 2
        
        # State: login stage = 1, upstage = 2
        # Bot saves user inputed new username as self.password
        # Bot acknowledges receipt
        # update_password function is used to update username, generating a response depending on success/failure
        # Bot sends user response to indicate successful update/failure
        # Set self.password = '', self.website = '', upstage = 0 to reset after update job is complete
        elif self.loginstage == 1 and self.upstage == 2:
            self.password = message['text']
            bot.sendMessage(chat_id, 'Updating...')
            resp = update_password(self.website, self.password, self.username, database)
            bot.sendMessage(chat_id, resp)
            
            self.password = ''
            self.website = ''
            self.upstage = 0
            
            
#----------------------------------- DELETE RECORD -------------------------------------
        # State: login stage = 1, user inputs /delete
        # Bot prompts user to enter website to delete records from
        # Set delstage = 1, to progress to next delete stage
        elif self.loginstage == 1 and message['text'] == '/delete':
            bot.sendMessage(chat_id, 'Please enter which website you would like to delete your record for.\n\nE.g. If you would like to delete your record for Hotmail, enter Hotmail.')
            self.delstage = 1
        
        # State: Login stage = 1, delstage = 1
        # User inputed website is saved under self.website
        # Bot sends message to ask user to confirm if user wants to delete record
        # /yes = confirm, /no = cancel
        # Set delstage = 2, to progress to next delete stage
        elif self.loginstage == 1 and self.delstage == 1:
            self.website = message['text']
            resp = 'Are you sure you want to delete your record for ' + self.website + ' ?\n\nEnter /yes to confirm. Enter /no to restart the process.'
            bot.sendMessage(chat_id, resp)
            self.delstage = 2
        
        # State: login stage = 1, delstage = 2, user inputs /yes for confirmation
        # delete_entry used to delete record for user inputed website, generating a response saved as resp
        # Bot sends user resp
        # Set self.website = '', delstage = 0 to reset process
        elif self.loginstage == 1 and self.delstage == 2 and message['text'] == '/yes':
            resp = delete_entry(self.username, self.website, database)
            bot.sendMessage(chat_id, resp)
            
            self.website = ''
            self.delstage = 0
        
        # State: login stage = 1, delstage = 2, user inputs /o
        # Bot sends acknowleges the 'no'
        # Set self.website = '' to blank out previously entered website
        # Bot prompts user again to restart deletion process
        # Set delstage = 1 to reset deletion process
        elif self.loginstage ==1 and self.delstage == 2 and message['text'] == '/no':
            bot.sendMessage(chat_id, 'Okay, restarting deletion process...')
            self.website = ''
            bot.sendMessage(chat_id, 'Please enter which website you would like to delete your record for.\n\nE.g. If you would like to delete your record for Hotmail, enter Hotmail.')
            
            self.delstage = 1

            
#----------------------------------- DELETE USER -------------------------------------
        # State: login stage = 1, user inputs /deleteaccount
        # Bot sends user message asking if user is sure user wants to do so. 
        # Bot informs user of consequences
        # Bot prompts user to enter user's username for verification
        # Set delastage = 1, to progress to next step
        elif self.loginstage == 1 and message['text'] == '/deleteaccount':
            bot.sendMessage(chat_id, 'Are you sure you want to delete your account? This will wipe off all records registered under your username from the database.\n\nTo proceed, please enter your username for verification.')
            self.delastage = 1
        
        # State: login stage = 1, delastage = 1
        # Bot saves user's input under self.deletecheck
        # If self.deletecheck matches user's username (self.username), bot proceeds with account deletion
        # delete_user used to delete account
        # Bot sends message to user informing user that account has been deleted
        # If self.deletecheck doesn't match, bot sends user failure message
        elif self.loginstage == 1 and self.delastage == 1:
            self.deletecheck = message['text']
            
            if self.deletecheck == self.username:
                resp1 = delete_user(self.username, database)
                resp2 = resp1 + '\n\nThank you for using Password Manager Bot.\nEnter /start if you would like to create a fresh account.'
                bot.sendMessage(chat_id, resp2)
                
                self.loginstage = 0
                self.delastage = 0
                self.menustage = 0
                self.deletecheck = ''
                self.username = ''
            
            else:
                resp = 'Verification process failed.\n\nPlease enter /deleteaccount if you wish to delete your account.\nOtherwise, please continue using other functions of Password Manager Bot.'
                bot.sendMessage(chat_id, resp)
                
                self.delastage = 0
                self.deletecheck = ''


#----------------------------------- GET ONE RECORD -------------------------------------
        # State: login stage = 1, user inputs /find
        # Bot prompts user for website which user wants to retrieve records from
        # Set findstage = 1, to progress to next step
        elif self.loginstage == 1 and message['text'] == '/find':
            bot.sendMessage(chat_id, 'Please enter the website that you wish to retrieve your records from.\n\nE.g. If you wish to get password for Hotmail, enter Hotmail.')
            self.findstage = 1
        
        # State: login stage = 1, find stage = 1
        # Bot saves user inputed website under self.website
        # Bot acknowledges receipt of user input, then retrieves records found under website for user
        # Bot sends user retrieved records
        # Bot prompts user to type /find if user wishes to retrieve another record
        # Set findstage = 0, self.website = '' to reset
        elif self.loginstage == 1 and self.findstage == 1:
            self.website = message['text']
            resp1 = 'Okay, retrieving records for ' + self.website + '...'
            bot.sendMessage(chat_id, resp1)
            resp2 = retrieve(self.username, self.website, database)
            bot.sendMessage(chat_id, resp2)
            resp3 = 'Enter /find if you would like to retrieve another record.'
            bot.sendMessage(chat_id, resp3)
            
            self.findstage = 0
            self.website = ''

            
#----------------------------------- LOG OUT ------------------------------------- 
        # User inputs /logout
        # Reset everything to base values
        # Bot sends message to inform user of successful logout
        elif self.loginstage == 1 and message['text'] == '/logout':
            bot.sendMessage(chat_id, 'Logging out...')

            self.login = ''
            self.website = ''
            self.username = ''
            self.password = ''
            self.uname = ''
            self.create = ''
            self.deletecheck = ''
            self.loginstage = 0
            self.createstage = 0
            self.newentrystage = 0
            self.menustage = 0
            self.uustage = 0
            self.upstage = 0
            self.delstage = 0
            self.delastage = 0
            self.findstage = 0
            
            bot.sendMessage(chat_id, 'Log out successful.\nThank you for using Password Manager Bot\n\nPlease enter /start to begin.')


#----------------------------------- HELP -------------------------------------
        # User types /help when logged in to display list of bot functions
        elif self.loginstage == 1 and message['text'] == '/help':
            bot.sendMessage(chat_id, help_text)


#----------------------------------- CATCH ALL -------------------------------------            
        # Purpose: Catch-all situation
        # If user is in limbo or types nothing that the bot recognizes, bot will reset user to start from log in page
        # Set all self.variables to nothing 
        else:
            bot.sendMessage(chat_id, 'Error! Please enter /start to log in.')
            # Resetting everything except for menu stage

            self.login = ''
            self.website = ''
            self.username = ''
            self.password = ''
            self.uname = ''
            self.create = ''
            self.deletecheck = ''
            self.loginstage = 0
            self.createstage = 0
            self.newentrystage = 0
            self.menustage = 1
            self.uustage = 0
            self.upstage = 0
            self.delstage = 0
            self.delastage = 0
            self.findstage = 0

            
#  __  __      _        ___                              
# |  \/  |__ _(_)_ _   | _ \_ _ ___  __ _ _ _ __ _ _ __  
# | |\/| / _` | | ' \  |  _/ '_/ _ \/ _` | '_/ _` | '  \ 
# |_|  |_\__,_|_|_||_| |_| |_| \___/\__, |_| \__,_|_|_|_|
#                                   |___/                

            
help_text = "/create - To create a new account.\n/newentry - To create a new record.\n/listall - To list all records stored in account.\n/find - To retrieve one record.\n/deleteaccount - To delete user's account.\n/delete - To delete one record.\n/updateusername - To update username of one record.\n/updatepassword - To update password of one record.\n/help - To print out a list of all commands for Password Manager Bot."
commands = ['/create', '/newentry', '/listall', '/logout', '/find', '/deleteaccount', '/delete', '/updatepassword', '/updateusername', '/help']

# Sqlite3 database
database = ''
# Telegram bot token
Token = ''           

        
# Timeout duration, bot will auto time out after 300 seconds of inactivity       
max_duration = 300



bot = telepot.DelegatorBot(Token, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=max_duration),
])



run_server = True
print('BOT IS ALIVE! WOOT WOOT!!')
MessageLoop(bot).run_as_thread()

                  
while run_server:
    time.sleep(3)