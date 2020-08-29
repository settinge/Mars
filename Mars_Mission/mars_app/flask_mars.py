from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)



# Connect to a database. Will create one if not already available.
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
mars_data = scrape_mars.scrape_info()

    
mongo.db.collection.update({}, mars_data, upsert=True)


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    final_data = mongo.db.collection.find_one()
    print(final_data)

    # Return template and data
    return render_template("index10.html", final_d=final_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)


