from database import UsernamePasswordTable, QuestionSetTable  # using database classes
import json
DB_FILE = 'data.db'

'''
	If it seems the db is empty, use this file to add in some dummy rounds for html purposes
	DELETE LATER!
'''


userpass = UsernamePasswordTable(DB_FILE, 'userpass')
decks = QuestionSetTable(DB_FILE, 'decks')

userpass.insert("pat", "pat")
print(userpass.passMatch("pat", "pat"))

decks.insert("s", "a", "as", "as")

for i in range(10, 20):
	decks.insert(
		f'Title {i}',
		f'Author {i}',
		f'Description {i}',
		str([{"question" : "QUESTION {}".format(i), "answer" : "ANSWER 1"},
			 {"question" : "question 2 ", "answer": "answer 2"}])
		)
