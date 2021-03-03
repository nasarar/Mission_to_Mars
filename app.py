#importing dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

#Uses flask_pymongo to setup mongo connection
app.config['MONGO_URI'] = 'mongo://localhost:27017/mars_app'
mongo = PyMongo(app)

#creates homepage for the webpage
@app.route('/')
def index():
    #finds the 'mars' collection from Mongo
    mars = mongo.db.find_one()
    return render_template('index.html', mars = mars)


#creates the scraping route
@app.route('/scrape')
def scrape():
    mars = mongo.db.mars 
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert = True)
    return redirect('/', code = 302) #after adding data to db redirect back to '/' 

if __name__ == '__main__':
    app.run()