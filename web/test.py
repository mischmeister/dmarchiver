import os
import sqlite3
import re
from flask import Flask
from flask import render_template

app = Flask(__name__, static_folder=os.path.dirname(os.path.realpath(__file__)) + "/static")

colors = [
	"#FF0029","#377EB8","#66A61E","#984EA2",
	"#00D2D5","#FF7F00","#AF8D00","#7F80CD",
	"#B3E900","#C42E60","#A65628","#F781BF",
	"#8DD3C7","#BEBADA","#FB8072","#80B1D3",
	"#FDB462","#FCCDE5","#BC80BD","#FFED6F"]

DATABASE="/usr/local/bin/dmarchiver/dmarchiver.sqlite"

@app.route("/")
def hello():

	labels = []
	values = []
	pub_domain = []
	pub_domain_count = []

	conn = sqlite3.connect(DATABASE)
	cur = conn.cursor()
	cur.execute("SELECT org_name, COUNT(*) FROM dmarc_reports GROUP BY org_name")
	conn.commit()

	rows = cur.fetchall();

	for i in rows:
		labels.append(i[0])
		values.append(i[1])

	str_labels = ""
	str_values = ""
	str_pub_domain_count = ""

	for i in values:
		str_values = str(str_values) + str(i) + ","

	cur.execute("SELECT pub_domain, COUNT(*) FROM dmarc_reports GROUP BY pub_domain")
	conn.commit()

	rows = cur.fetchall();

	for i in rows:
		pub_domain.append(i[0])
		pub_domain_count.append(i[1])

	for i in pub_domain_count:
		str_pub_domain_count = str(str_pub_domain_count) + str(i) + ","


	return render_template("test.html",title='DMARC Report Overview', max=100, values=str_values, labels=labels, colors=colors, pub_domain=pub_domain, pub_domain_count=str_pub_domain_count)


@app.route('/alignment')
def algiment():
	return render_template("alignment.html",title='DMARC Alignment Overview', max=100, colors=colors)




#@app.route("/")


