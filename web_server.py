from bottle import route, run, template, static_file


@route('/')
def get_homepage():
	return template('index')

run(host='localhost', port=8080)