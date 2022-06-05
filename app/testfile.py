from database import QuestionSetTable


db_file = "data.db"

table = QuestionSetTable("data.db", "decks")

table.insert("Test1", "Test2","Dec" ,"Content")
table.insert("Test2", "Test2", "D","Content21")
table.insert("Test3", "Test2", "D","Content2")
table.insert("Test4", "Test2", "D","Content233")
table.insert("Test5", "Test2", "D","Content33")

print(table.getRandomEntries(3))