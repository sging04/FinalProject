from database import UsernamePasswordTable, QuestionSetTable  # using database classes
import json
DB_FILE = 'data.db'

'''
	If it seems the db is empty, use this file to add in some dummy rounds for html purposes
	DELETE LATER!
'''


userpass = UsernamePasswordTable(DB_FILE, 'userpass')
decks = QuestionSetTable(DB_FILE, 'decks')


print(decks.search("asa"))