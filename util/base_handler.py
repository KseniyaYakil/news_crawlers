from session_agent import SessionAgent
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		cookie = self.get_cookie('user_cookie')
		if not cookie:
			return None
		print 'DEB: check cookie ' + cookie
		s_agent = SessionAgent()
		resp = s_agent.is_authorized({'user_cookie': cookie})
		if resp.status == 200:
			return cookie
		return None

