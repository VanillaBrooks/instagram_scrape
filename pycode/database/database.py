import pymysql
import subprocess

class database():

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

	# function to create a new database and initialize tables to hold scraped data
	def init_database(self):
		#
		# The following line was commented out of the database .sql file :
		# -- SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
		# becuase mysql thought that it would allow a null value
		#
		# If there is a big ass error at some point in the future it might be
		# becuase of this
		#
		# Note: mysqlworkbench forward engineered the script provided without issue
		#

		mysql_auth = 'mysql -u {} -p; {};'.format(self.user, self.password)

		# TODO : change this to use mysql connector
		try:
			conn, cursor = self.connection_mysql()
			with open('pycode\database\igscrape.sql' , 'r') as f:
				data = f.read().split(';')
				for i in data:
					query = i.strip('\n')
					if self.validate_query(query):
						try:
							cursor.execute(query)
						except Exception as e:
							print('!!!WARNING the command {} did not run')
				conn.commit()

		except Exception as e:
			print("there was an exception making the database {}".format(e))
			print('the line was %s' % query)

	# function to make sure that each line executed will be ok
	@staticmethod
	def validate_query(query):
		if type(query) != str:
			raise TypeError('should be string')

		if '-' in query[0:5]:
			return False
		vowel_in = False
		for vowel in 'aeiou=AEIOU':
			if vowel  in query:
				vowel_in = True
				break
		if not vowel_in:
			print("the query : %s was empty, %s" % (query, type(query)))
			return False

		return True

if __name__ == "__main__":
	x = database('root', 'pass')
	x.init_database()
