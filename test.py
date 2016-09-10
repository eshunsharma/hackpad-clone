import unittest
from mongo import Mongo
from sockets import Sockets

class TestCases(unittest.TestCase):
	"""Tests for `hackpad`."""

	def MongoInsert(self):
		"""Insert record in MongoDB and check"""
		db = Mongo(0)
		db_insert = db.insert({'session': 'MongoTest', 'data': 'Test data'})
		db_fetch = db.fetch({'session': 'MongoTest', 'data': 'Test data'})
		return self.assertEqual('MongoTest', db_fetch['session'])

	def MongoUpdate(self):
		"""Update record in MongoDB and check"""
		db = Mongo(0)
		db_insert = db.insert({'session': 'UpdateTest', 'data': 'Update Test data'})
		db_update = db.update({'session': 'UpdateTest', 'data': 'Test data Updated'})
		db_fetch = db.fetch({'session': 'UpdateTest', 'data': ''})
		return self.assertEqual('Test data Updated', db_fetch['data'])

	def FindInsert(self):
		"""Find and Insert record in MongoDB and check"""
		db = Mongo(0)
		db_insert = db.insert({'session': 'FindInsertTest', 'data': 'FindInsertTest Test data'})
		db_findinsert = db.find_insert({'session': 'FindInsertTest', 'data': 'FindInsertTest Test data'})
		return self.assertEqual('FindInsertTest', db_findinsert['data'])

	def CreateSocket(self):
		"""Create a new socket"""
		sock = Sockets('TestSession')
		res = sock.create_socket()
		return self.assertEqual('TestSession', res['session'])



if __name__ == '__main__':
	unittest.main()