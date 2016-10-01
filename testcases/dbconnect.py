import pymysql

class DBConnect():
	def __init__(self):
		pass		# here we dont do anything so we pass

	# for below, if double underscore, so its private method
	def __connect(self,db):
		# below its documentation
		'''

		:param endpoint:
		:param data:
		:return:
		'''
		host = '127.0.0.1'
		# below db means which db we want to connect to
		conn = pymysql.connect(host=host,port=3306,user='root',passwd='mysql',db=db)

		return conn

	def select(self,db,query):
		'''

		:param endpoint:
		:param data:
		:return:
		'''

		# for below, we call the method from above 
		# we do self coz its an instance of the class
		conn = self.__connect(db)
		cur = conn.cursor()
		cur.execute(query)
		result = cur.fetchall()

		# start with empty list
		all_rows = []
		for line in result:
			row = []
			for col in line:
				row.append(str(col))  #convert each value to string
			# row_list = list(row)
			all_rows.append(row) 

		conn.close()   # closing the db connection
		cur.close()    # clearing the cursor

		return all_rows

	def update(self,db,query):
		'''

		:param endpoint:
		:param data:
		:return:
		'''
		# create connection
		conn = self.__connect(db)
		cur = conn.cursor()

		# execute the query
		# we are writing to the database
		result = cur.execute(query)
		# below is saving the file
		conn.commit()
		conn.close()
		cur.close()

		return result
