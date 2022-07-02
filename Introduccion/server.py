from re import template
from jinja2 import Environment, FileSystemLoader
from wsgiref.simple_server import make_server

def application(env, start_response):

    headers = [('Content-Type', 'text/html')]
    start_response('200 OK', headers)
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    html = template.render(
        {
            'title' : 'Servidor en Python',
            'name'  : 'Eduardo'
        }
    )
    return [bytes(html, 'utf-8')]

server = make_server('0.0.0.0', 8082, application)
print('Server UP!')
server.serve_forever()