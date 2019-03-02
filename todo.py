import web
import json
from web import form
import model
import requests


### Url mappings

urls = (
    '/', 'Index',
    '/db', 'Db',
    '/del/(\d+)', 'Delete'
)


### Templates
render = web.template.render('templates', base='base')
class Db:
    data= {"todos": [{"id":1, "name": "need to learn python", "when":"12th feb"}, {"id":2, "name": "need to submit project", "when":"16th march"}] } 
    def GET(self):
        """ Show page """
        return json.dumps(self.data) 

class Index:    
    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull, 
            description="I need to:"),
        web.form.Button('Add todo'),
    )

    def GET(self):

        resp = model.get_tasks()
        todos= resp.json()
        form = self.form()
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /todos/ {}'.format(resp.status_code))
        return render.index(todos[u'todos'], form)


    def POST(self):
        form = self.form()
        form.validates()
        task=form.d.title
        date="2nd March"
        resp = model.add_task(task,date)
        if resp.status_code != 201:
            raise ApiError('Cannot create task: {}'.format(resp.status_code))
        raise web.seeother('/')



class Delete:

    def POST(self, id):
        """ Delete based on ID """
        id = int(id)
        resp = model.task_done(id)
        if resp.status_code != 201:
            raise ApiError('Cannot create task: {}'.format(resp.status_code))
        raise web.seeother('/')
    


       

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
