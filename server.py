from flask import Flask, render_template, redirect, url_for, request
from graphs import run_entire_process_graphs
from graphs import get_graph
import pdb

app = Flask(__name__)

@app.route("/")
def home():
    username = {"ADI", "APPL"}
    return render_template('index.html')

@app.route("/<ticker>")
def subpage(ticker):
    png_data = run_entire_process_graphs(ticker)
    print(png_data)
    return render_template("subpage.html", ticker=ticker, graph=png_data[0].decode('utf8'), graph1=png_data[1].decode('utf8'), graph2=png_data[2].decode('utf8'), graph3=png_data[3].decode('utf8'))
    
@app.route("/about")
def aboutMe():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
