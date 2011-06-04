from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
import wsgiref.handlers
import models
import re



class MainHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render("templates/link.html",{}))

		
class FavoriteHandler(webapp.RequestHandler):
	def post(self):
		action = self.request.get("action")
		func = mapping[action];
		func(self)


def get_link(handler):
	url = handler.request.get('link')
	link_content = urlfetch.fetch(url=url).content
	link_title = get_link_title(link_content)
	favorite = models.Favorite(link=url,title=link_title)
	handler.response.out.write(template.render("templates/save_link.html",{"favorite":favorite}))

def get_link_title(link_content):
	
	titlePattern = re.compile("<title>(.*)</title>",re.IGNORECASE)
	foundPatterns = titlePattern.findall(link_content)
	title = ""
	if len(foundPatterns) > 0:
		title = foundPatterns[0]
	return title
			


def save_link(handler):
	link = handler.request.get("link")
	title = handler.request.get("title")
	
	favorite = models.Favorite(link = link, title = title)
	favorite.put()
	handler.redirect("/")
	

mapping ={
	"link" : get_link,
	"save_link": save_link
}
			
def main():
	application = webapp.WSGIApplication([('/', MainHandler),
	('/link', FavoriteHandler),
	('/save_link', FavoriteHandler)
	], 
	debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
	main()