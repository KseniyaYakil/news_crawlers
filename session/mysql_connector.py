import torndb
from uuid import uuid4

class MySQLConnector:
	# TODO: read database name + host + user + pass from config
	def __init__(self):
		self.host = '127.0.0.1'
		self.user = 'session_user'
		self.password = 'secret987'
		self.database = 'session_db'
		self.cookie_expired_time = '60' # min

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

	def del_user_by_id(self, user_id):
		try:
			self.db.query("delete form user_role where id_user={}".format(user_id))
			self.db.query("delete from user where id={}".format(user_id))
			return True
		except:
			return False

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

		for of in other_fields:
			if of not in user_data.keys():
				continue
			str_mh += ', ' + of
			str_val += ', \'' + user_data[of] + '\''

		role_id = self.db.query("select * from roles where name='{}'".format(user_data['role']))
		if len(role_id) == 0:
			print "ERR: unable to insert user: no role '{}'".format(user_data['role'])
			return None

		try:
			query_str = "insert into user ({}) values ({})".format(str_mh, str_val)
			user_id = self.db.insert(query_str)
			query_str = "insert into user_roles (id_user, id_role) values ({}, {})".format(user_id, role_id[0]['id'])
			user_role_id = self.db.insert(query_str)
			return user_id
		except:
			print "INF: unable to insert user '" + user_data['username'] + "'"
			return None

	def insert_user_role(self, user_id, role_id):
		try:
			return user_role_id
		except:
			print "INF: can not add user_id ({}) ; user_role ({})".format(user_id, role_id)
			return None

	def __gen_cookie__(self):
		return uuid4().hex

	def create_cookie(self, user_data):
		if	'username' not in user_data.keys() or \
			'password' not in user_data.keys():
			return None

		q_str = "select * from user where username='{}' and password={}".format(user_data['username'], user_data['password'])
		try:
			user_info = self.db.query(q_str)
			if len(user_info) == 0:
				print 'INF: no user {} / incorrect password'.format(user_data['username'])
				return None

			q_str = "delete from cookie where user_id={}".format(user_info[0]['id'])
			self.db.execute(q_str)

			cookie = self.__gen_cookie__()
			q_str = "insert into cookie (cookie_token, user_id) values('{}', {})".format(cookie, user_info[0]['id'])
			cookie_id = self.db.insert(q_str)

			print 'DEB: cookie for user {} was created'.format(user_data['username'])
			return cookie
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None

	def get_user_by_cookie(self, user_cookie):
		try:
			user_id = self.db.query("select user_id from cookie where cookie_token='{}'".format(user_cookie))
			print user_id
			return user_id
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None

	def del_cookie(self, user_cookie):
		try:
			self.db.execute("delete from cookie where cookie_token='{}'".format(user_cookie))
		except Exception as ex:
			print 'ERR: {}'.format(ex)

	def role_by_cookie(self, user_cookie):
		try:
			role_info = self.db.query("select id_role from cookie as c join user_roles as ur on c.user_id=ur.id_user")
			print 'DEB: role_info=\'{}\' by cookie'.format(role_info)
			return role_info[0]['id_role']
		except Exception as ex:
			print 'ERR: {}'.format(ex)
			return None



