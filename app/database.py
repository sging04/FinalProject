import sqlite3

class QuestionSetTable:
	'''
	QuestionSetTable Class

	For question sets:

	DB design:
		id int
		title TEXT
		author TEXT
		content TEXT (but really JSON)
	'''

	def __init__ (self,fileName, name):
		'''
		__init__
		Args
		    filename: database file name
			name: name of table
		Returns
			instance of QuestionSetTable
		Class attributes
			self._db : the file our database comes from. uses fileName Check_same_thread
			was set to false, if you want us to change it, let us know. PRIVATE,
			do not use.
			self._cursor is the cursor for that database. PRIVATE, do not use.
			self._name is the name of the table, used to aid in writing methods for
			this class; private, do not use!
		'''
		self._db = sqlite3.connect(fileName, check_same_thread=False)
		self._cursor = self._db.cursor()
		self._name = name
		self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {self._name}(title TEXT, author TEXT, content TEXT, unique(title, content));")

	def insert(self,title, author, content):
		'''
		insert
		insert username and password. DOES NOT CHECK if it is duplicate.
		will throw error if duplicate! please use userExists method below!
		returns nothing
		Args
			title : title
			author : author
			content : content
		Returns
			boolean : success or faulure
		'''
		#insert vales & committing them

		try:
			self._cursor.execute(f"INSERT INTO {self._name} VALUES(\"{title}\", \"{author}\", \"{content}\");")
			self._db.commit()
			return True
		except:
			return False


	def getDeckByID(self, id):
		'''

		getDeckByID

		will return a deck with the rowid of id

		Args
			id : rowid

		returns
			json of the rowid, title, author, content
		'''

		self._cursor.execute(f"SELECT rowid, * FROM {self._name} WHERE rowid = {id};")
		return self._cursor.fetchone()


	def search(self, query):
		'''

		searchByTitle

		will return a decs with matches of title and content

		Args
			query : query

		returns
			list of json of the rowid, title, author, content

		'''

		self._cursor.execute(f"SELECT rowid, * FROM {self._name} WHERE (title LIKE \"%{query}%\") OR (content LIKE \"%{query}%\");")
		return self._cursor.fetchall()




class UsernamePasswordTable:

	'''
		UsernamePasswordTable Class
		A table inside of a database NOT  a database. Specifically
		designed for the username, password
		Ensures username IS UNIQUE
		Just wanted to make interacting w tables easier
		DB design:
			username TEXT
			password TEXT
	'''
	def __init__ (self,fileName, name):
		'''
		__init__
		Args
		    filename: database file name
			name: name of table
		Returns
			instance of UsernamePasswordTable
		Class attributes
			self._db : the file our database comes from. uses fileName Check_same_thread
			was set to false, if you want us to change it, let us know. PRIVATE,
			do not use.
			self._cursor is the cursor for that database. PRIVATE, do not use.
			self._name is the name of the table, used to aid in writing methods for
			this class; private, do not use!
		'''
		self._db = sqlite3.connect(fileName, check_same_thread=False)
		self._cursor = self._db.cursor()
		self._name = name
		self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {self._name}(username TEXT, password TEXT, unique(username));")

	def insert(self,username, password):
		'''
		insert
		insert username and password. DOES NOT CHECK if it is duplicate.
		will throw error if duplicate! please use userExists method below!
		returns nothing
		Args
			username : username
			password : password
		Returns
			Nothing
		'''
		#insert vales & committing them
		self._cursor.execute(f"INSERT INTO {self._name} VALUES(\"{username}\", \"{password}\");")
		self._db.commit()



	def userExists(self,username):
		'''
		userExists
		Will return true if user name exists in table will throw false otherwise.
		@params
			username : usernamebeing checked
		Returns
			boolean t/f
		'''
		#executing query
		self._cursor.execute(f"SELECT * FROM {self._name} where username=\"{username}\";")

		if self._cursor.fetchone() is not None: #if there was an entry returned
			return True #meaning we had a match
		else:
			return False

	def passMatch(self,username, password):
		'''
		passMatch
		Will return true if user name and pass exists in table will throw false otherwise.
		@params
			username : username being checked
			password : password being checked
		Returns
			boolean t/f
		'''
		#executing query
		self._cursor.execute(f"SELECT * FROM {self._name} where username=\"{username}\" AND password=\"{password}\";")

		if self._cursor.fetchone() is not None: #if there was an entry returned
			return True #meaning we had a match
		else:
			return False