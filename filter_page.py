from flask import Flask, render_template, request
import requests

app = Flask(__name__)

session = None
server_addr = 'http://django-service'

def saveFilters(user_id, filters):
	global session

	r = session.delete(url=server_addr + ':8000/app1/filters/?userID=' + str(user_id))

	for filtr in filters:
		jsondata = {
				"userID": user_id,
				"znamka": None if filtr['znamka'] == '' else filtr['znamka'],
				"model": None if filtr['model'] == '' else filtr['model'],
				"cena_od": None if filtr['cena_od'] == '' else filtr['cena_od'],
				"cena_do": None if filtr['cena_do'] == '' else filtr['cena_do'],
				"letnik_od": None if filtr['letnik_od'] == '' else filtr['letnik_od'],
				"letnik_do": None if filtr['letnik_do'] == '' else filtr['letnik_do']
		}
		r = session.post(url=server_addr + ':8000/app1/filters/', json=jsondata)

@app.route("/filter/<user_id>", methods=['GET', 'POST'])
def filter(user_id):
	global session
	print('user_id: ' + str(user_id))
	if request.method == 'POST':
		saveFilters(user_id, request.json)
		print(request.json)
		return 'POST called!'
	elif request.method == 'GET':
		filtersJSON = {"data": []}
		# TODO iz baze mora prejeti vse relevantne filtre
		r = session.get(url=server_addr + ':8000/app1/filters/?userID=' + str(user_id))
		filters = r.json()
		for filtr in filters:
			filtersJSON['data'].append({
				"znamka": "" if filtr['znamka'] is None else filtr['znamka'],
				"model": "" if filtr['model'] is None else filtr['model'],
				"cena_od": "" if filtr['cena_od'] is None else filtr['cena_od'],
				"cena_do": "" if filtr['cena_do'] is None else filtr['cena_do'],
				"letnik_od": "" if filtr['letnik_od'] is None else filtr['letnik_od'],
				"letnik_do": "" if filtr['letnik_do'] is None else filtr['letnik_do']})

		return filtersJSON	


	return 'Hello World!'



@app.route("/filterpage/<user_id>")
def filterpage(user_id):
	global session
	if session is None:
		session = requests.Session()
	return render_template("filter_page.html", url_root=request.url_root, user_id=user_id)

@app.route("/pozdrav/<name>")
def pozdrav(name):
	return "<h1>Hello " + name + "!</h1>"

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port='5000')
