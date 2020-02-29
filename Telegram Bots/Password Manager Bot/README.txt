Introduction
Password Manager Bot is a Telegram Bot is a bot that allows you to store your username and passwords in a database, then retrieve it whenever you need it.
The purpose of this bot is to mainly as a platform where I can apply new coding knowledge to. 




29th February 2020
Password Manager Bot is now hosted live on a free PythonAnywhere account.
You may test Password Manager Bot at the following URL https://t.me/PasswordManageBot.

Please be gentle with the bot as there is an extremely limited amount of available compute time on a free PythonAnywhere account.
If the bot is down, do drop me a message at https://t.me/fridaynite to restart the bot. 


Version 0

Dependencies:
1. Google Sheets API to be enabled on Google Develop Console
2. pip install telepot
3. Various Google Sheets API libraries
4. Telegram 

Future improvements/Work in progress:
1. Dynamic buttons
2. Read/write functionality to an actual database like AWS DynamoDB
3. Better presentation of information retrieved from Google Sheets
4. Error handling with Try-Except
5. Multi-user functionality [Completed]


Version 0.1

Dependencies:
1. pip install telepot
2. pip install pandas
3. pip install numpy
4. Telegram

Updates:
- Shift from Google Sheets to Sqlite for databse
- Added a user log in verfication process
- Added a log out function
- Added a delete user function
- Some form of try-except error handling
- Support for multi-user concurrency
- User's records are now separated - Each user will have their own table in database
- Cleaner presentation of data to user

Future improvements/Work in progress:
1. Reduce the amount of hardcoding - Shift general variables to a system configuration database
2. Create a script that automatically installs all the dependencies
3. Telegram buttons
4. Implement some form of encryption algorithm
5. Implement some form of NLP engine
6. Modularize code
