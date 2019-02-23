import pymysql
import subprocess
import os
from queries import Queries

class Database(Queries):

	def __init__(self, username,password):
		self.db_name = "igscrape"

		self.user =username
		self.password = password

	def run():
		end_early = self.connection_mysql(self.db_name)
		if end_early is None:
			print('auth details were incorrectly entered')
			return False

		# self.init_database()

	# function to make a connection to mysql (no specific database)
	def connection_mysql(self,connect_type='mysql'):
		try:
			# will make a connection to mysql by default but if specified will
			# make a connection to a specif databse to insert / select data
			if connect_type == 'mysql':
				conn = pymysql.connect(host='localhost', user=self.user, password=self.password)			## TODO : Wrap this in a decorator
			else:
				conn = pymysql.connect(host='localhost', user=self.user, password=self.password, database=connect_type)
			cursor = conn.cursor()
		except Exception as e:
			print('there was an exception {} when making the databse. initializing a new database'.format(e))
			return None

		self.conn, self.cursor = conn, cursor
		return conn, cursor

	def init_database(self):

		shell = subprocess.Popen(['mysql','-u',self.user, '-p"{}"'.format(self.password)],
								 shell=True,
								 stdin=subprocess.PIPE,
								 cwd = './pycode/database/')

		shell.communicate('source igscrape.sql')



if __name__ == "__main__":
	# x = database('root', 'pass')
	# x.init_database()
