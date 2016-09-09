from mongo import Mongo

class Sockets():

	def __init__(self, session):
		self.session = session

	def create_socket(self):
		init = { "session" : self.session, "data" : "" }
		db = Mongo(0)
		data = db.find_insert(init)
		return data
