import torndb

class MySQLConnector:
	# TODO: read database name + host + user + pass from config
	def __init__(self):
		self.host = '127.0.0.1'
		self.user = 'session_user'
		self.password = 'secret987'
		self.database = 'session_db'

		self.db = None
		self.__connect__()

	def __connect__(self):
		if self.db is not None:
			self.db.close()
		try:
			self.db = torndb.Connection(host=self.host, database=self.database,
										user=self.user, password=self.password)
			return 0
		except:
			print "ERR: unable to connect to db ('{}':{} for user {})".format(self.host, self.database, self.user)
			return -1

	def select_all_users(self):
		try:
			users = self.db.query("select * from user")
			return users
		except:
			print "ERR: unable to select users"
			return None

	def insert_user(self, user_data):
		must_have_fields = ('username', 'password')
		other_fields = ('name', 'surname', 'sex', 'email', 'position', 'phone_number')

		str_mh = ""
		str_val = ""
		for mh in must_have_fields:
			if mh not in user_data.keys():
				return None
			if str_mh != "":
				str_mh += ', '
			str_mh += mh
			if str_val != "":
				str_val += ', '
			str_val += '\'' + user_data[mh] + '\''

		user = self.db.query("select id from user where username='" + user_data['username'] + "'")
		if len(user) != 0:
			print "INF: user {} already exists".format(user_data['username'])
			return None

		for of in other_fields:
			if of not in user_data.keys():
				continue
			str_mh += ', ' + of
			str_val += ', \'' + user_data[of] + '\''

		query_str = "insert into user ({}) values ({})".format(str_mh, str_val)
		try:
			user_id = self.db.insert(query_str)
			return user_id
		except:
			print "ERR: unable to insert user '" + user_data['username'] + "'"
			return None

