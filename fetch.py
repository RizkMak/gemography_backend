from flask import Flask, jsonify
from marshmallow import Schema, fields
import requests
import datetime
import json

#Initialization
app = Flask(__name__)

# defining a class for grouping the language attributes 
class LanguageList:
	def __init__(self, language, numberOfRepos, listOfRepos):
		self.language = language
		self.numberOfRepos = numberOfRepos
		self.listOfRepos = listOfRepos

# for serialization
class ResultSchema(Schema):
	language = fields.Str()
	numberOfRepos = fields.Int()
	listOfRepos = fields.List(fields.Str())


@app.route('/list')
def getList():
	output = [] # variable for stocking all the objects 
	date = datetime.date.today()- datetime.timedelta(days=1)
	r = requests.get('https://api.github.com/search/repositories?q=created:>'+str(date)+'&sort=stars&order=desc&per_page=100')
	if r.status_code != 200 : # checking the HTTP status code 
		return 'Oops! Something went wrong.'
	# if there is no exception, time to work on those attributes 
	response = r.json()['items']

	#first, getall the occurences of the languages from the trending repositories (will help with calculating the number of repositories that use each language )
	l = []
	for i in range(len(response)):
		if response[i]['language'] != None:
			l.append(response[i]['language'])

	# deleting all occurences for a language but one, to simplify iteration
	languages = []
	for j in range(len(l)):
		if l[j] not in languages:
			languages.append(l[j])

	# Assembling the output 
	for item in languages:
		repos = []
		number = l.count(item)
		for k in range(len(response)):
			if response[k]['language'] == item:
				repos.append(response[k]['owner']['repos_url'])
		element = LanguageList(item,number,repos)
		output.append(element)
	schema = ResultSchema(many=True)
	result = schema.dump(output)
	return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)



		




