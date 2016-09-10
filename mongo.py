from pymongo import MongoClient, errors

class Mongo():

	UPTIME = 0

	def __init__(self, UPTIME):
		Mongo.UPTIME = UPTIME
		self.db = self.connect()

	def connect(self):
		'''Initial mongo connection, if it fails local store is used'''

		try:
			client = MongoClient(connectTimeoutMS=3000, serverSelectionTimeoutMS=3000)
			client.server_info()
			Mongo.UPTIME = 1
			return client.test
		except errors.PyMongoError:
			Mongo.UPTIME = 0
			print("Could not connect to test")


	def insert(self, data):
		'''Inserting a new session in mongo'''

		result = self.db.hackpad.insert(data)
		return result


	def update(self, data):
		'''Update a session in mongo'''

		result = self.db.hackpad.update_one({"session" : data["session"]}, {"$set": {"data":data["data"]}})
		return result.matched_count


	def fetch(self, data):
		'''Fetch data from mongo'''

		result = self.db.hackpad.find({"session":data["session"]}).limit(1)
		for res in result:
			data = {"session": res["session"], "data" : res["data"]}
		return data


	def find_insert(self, data):
		'''Find a record in table, if found insert data, else return data'''

		if Mongo.UPTIME == 1:
			result = self.db.hackpad.find({"session":data["session"]}).limit(1).count()
			if result < 1:
				self.insert(data)
				return data
			else:
				res = self.fetch(data)
				return result
		else:
			return 0
