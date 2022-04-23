from flask import Flask
from flask import jsonify
from flask import render_template
import data

app = Flask(__name__)

@app.route("/")
def home():
	return "Nothing here"

@app.route("/api/word-information/<string:word>/")
def search_word(word:str):
	response = data.scrap_info_palavra(word)
	return jsonify(response)

@app.route("/api/ranking-most-searched/")
def get_ranking():
	response = data.scrap_mais_buscadas()
	return jsonify(response)