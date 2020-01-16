from flask import Flask
import logging
from flask import render_template, request, redirect, url_for
from datetime import datetime

from attraction import Attraction
from comment import Comment
from category import Category
from rating import Rating

app = Flask(__name__)

logging.basicConfig(filename='logs.log', level=logging.DEBUG)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True


def info_log(message):
    current_time = datetime.now()
    date = current_time.strftime("%d/%m/%Y %H:%M:%S")
    logging.info(message + date)


def error_log(message):
    current_time = datetime.now()
    date = current_time.strftime("%d/%m/%Y %H:%M:%S")
    logging.error(message + date)


@app.route('/')
def main_menu():
    info_log("Main menu")
    return redirect("/categories")


@app.route('/attractions')
def list_attractions():
    info_log("Listing all attractions")
    return render_template('attractions.html', attractions=Attraction.all())


@app.route('/attractions/<int:id>', methods=['GET', 'POST'])
def show_attraction(id):
    attraction = Attraction.find(id)  
    message = "Showing attraction with name - " + attraction.name
    info_log(message)
    return render_template('attraction.html', attraction=attraction)


@app.route('/attractions/<string:name>')
def show_attraction_by_name(name):
    attraction = Attraction.find_by_name(name)   
    message = "Showing attraction with name - " + attraction.name
    info_log(message)
    return render_template('attraction.html', attraction=attraction)


@app.route('/attractions/<int:id>/edit', methods=['GET', 'POST'])
def edit_attraction(id):
    attraction = Attraction.find(id)
    if request.method == 'GET':
        message = "Editing attraction with name - " + attraction.name 
        info_log(message)
        return render_template(
            'edit_attraction.html',
            attraction=attraction,
            categories=Category.all()
        )
    elif request.method == 'POST':
        message = "Saving attraction with name - " + attraction.name 
        info_log(message)
        attraction.name = request.form['name']
        attraction.location = request.form['location']
        attraction.image = request.form['image']
        attraction.description = request.form['description']
        attraction.rating = None
        attraction.category = Category.find(request.form['category_id'])
        attraction.save()
        return redirect(url_for('show_attraction', id=attraction.id))


@app.route('/attractions/<int:id>/rate', methods=['GET', 'POST'])
def rate_attraction(id):
    attraction = Attraction.find(id)
    if request.method == 'GET':
        message = "Rating attraction with name - " + attraction.name 
        info_log(message)
        return render_template('rate_attraction.html', attraction = attraction)
    elif request.method == 'POST':
        message = "Average rating on attraction with name - " + attraction.name + "set"
        info_log(message)
        arch = 0
        inter = 0
        hist = 0
        req = request.form.getlist('architecture rate')
        if req == [u'One']:  
            arch = 1
        elif req == [u'One', u'Two']:
            arch = 2
        elif req == [u'One', u'Two', u'Three']:
            arch = 3
        elif req == [u'One', u'Two', u'Three', u'Four']:
            arch = 4

        req = request.form.getlist('interior rate')
        if req == [u'One']:  
            inter = 1
        elif req == [u'One', u'Two']:
            inter = 2
        elif req == [u'One', u'Two', u'Three']:
            inter = 3
        elif req == [u'One', u'Two', u'Three', u'Four']:
            inter = 4

        req = request.form.getlist('historical value rate')
        if req == [u'One']:  
            hist = 1
        elif req == [u'One', u'Two']: 
            hist = 2
        elif req == [u'One', u'Two', u'Three']:
            hist = 3
        elif req == [u'One', u'Two', u'Three', u'Four']:
            hist = 4
        values = (None, attraction, arch, inter, hist, (arch + inter + hist) / 3)
        rating = Rating(*values).create()
        attraction.rating = (arch + inter + hist) / 3
        attraction.set_rating()
        return render_template('attraction.html', attraction=attraction)
            


@app.route('/attractions/new', methods=['GET', 'POST'])
def new_attraction():
    if request.method == 'GET':
        info_log("Creating new attraction")
        return render_template('new_attraction.html', categories=Category.all())
    elif request.method == 'POST':
        message = "Created attraction with name - " + request.form['name']
        info_log(message)
        categ = Category.find(request.form['category_id'])
        values = (
            None,
            request.form['name'],
            request.form['location'],
            request.form['image'],
            request.form['description'],
            None,
            categ
        )
        Attraction(*values).create()

        return redirect('/')


@app.route('/attractions/<int:id>/delete', methods=['POST'])
def delete_attraction(id):
    attraction = Attraction.find(id)
    message = "Deleting attraction with name - " + attraction.name
    info_log(message)
    attraction.delete()

    return redirect('/')


@app.route('/comments/new', methods=['POST'])
def new_comment():
    if request.method == 'POST':
        attraction = Attraction.find(request.form['attraction_id'])
        message = "Creating comment on attraction with name - " + attraction.name
        info_log(message)
        values = (None, attraction, request.form['message'])
        Comment(*values).create()

        return redirect(url_for('show_attraction', id=attraction.id))


@app.route('/categories', methods=['GET', 'POST'])
def get_categories():
    if request.method == 'POST':
        info_log("Listing all categories")
        if request.form.get('name'):
            attraction = Attraction.find_by_name(request.form.get('name'))
            if(attraction): 
                message = "Attraction with name - " + attraction.name + "successfully found"
                info_log(message)
                return redirect(url_for('show_attraction_by_name', name = request.form.get('name')))
            else:
                error_log("Attraction not found")
        elif request.form.get('rate'):
            message = "Searching attractions by rate " + request.form.get('rate')
            info_log(message)
            return render_template('attractions.html', attractions=Attraction.find_by_rating(request.form.get('rate'))) 
    return render_template("categories.html", categories=Category.all())


@app.route('/categories/new', methods=["GET", "POST"])
def new_category():
    if request.method == "GET":
        info_log("Creating new category")
        return render_template("new_category.html")
    elif request.method == "POST":
        info_log("Successfully created new category")
        category = Category(None, request.form["name"])
        category.create()
        return redirect("/categories")


@app.route('/categories/<int:id>')
def get_category(id):
    category = Category.find(id)
    message = "Finding category with name - " + category.name
    info_log(message)
    return render_template("category.html", category=category)


@app.route('/categories/<int:id>/delete')
def delete_category(id):
    category = Category.find(id)
    category.delete()
    message = "Deleting category with name - " + category.name
    info_log(message)
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
