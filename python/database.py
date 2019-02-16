import pymysql

class database():

	def __init__(self, username,password):
		self.db_name = "igscrape"

		end_early = self.connection_mysql(username, password)
		if end_early is False:
			return False

		self.init_database()

	# function to make a connection to mysql (no specific database)
	def connection_mysql(self,username, password, connect_type='mysql'):
		try:
			# will make a connection to mysql by default but if specified will
			# make a connection to a specif databse to insert / select data
			if connect_type == 'mysql':
				conn = pymysql.connect(host='localhost', user=username, password=password)
			else:
				conn = pymysql.connect(host='localhost', user=username, password=password, database=connect_type)
			cursor = conn.cursor()
		except Exception as e:
			print('there was an exception {} when making the databse. initializing a new database'.format(e))
			return None

		self.conn, self.cursor = conn, cursor
		return conn, cursor

	# function to create a new database and initialize tables to hold scraped data
	def init_database(self):
		try:
			create_db = "create database {}".format(self.db_name)

			#
			# TODO: create all tables / foreign keys / auto inc variables
			#       in mysql workbench and then export them to a format
			#       to automatically initialize a database here
			#
			tables = ["create table users"] # .. etc etc use mysql workbench for this

			self.cursor.execute(create_db)
			self.conn.commit()

			for table in tables:
				self.cursor.execute(table)

		except Exception as e:
			print("there was an exception making the database {}".format(e))

if __name__ == "__main__":
	x = database(1, 2)
