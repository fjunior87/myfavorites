from google.appengine.ext import db

class Favorite(db.Model):
	user = db.UserProperty(auto_current_user_add=True)
	link = db.StringProperty(required=True)
	title = db.StringProperty(required=True)
	private = db.BooleanProperty(default=False)
	