from mongo import Mongo

class Sockets():

	def __init__(self, session):
		self.session = session


	def create_socket(self):
		'''When a new session is created, insert in mongo if it doesnt already exist'''

		init = { "session" : self.session, "data" : "" }
		db = Mongo(0)
		data = db.find_insert(init)
		return data
