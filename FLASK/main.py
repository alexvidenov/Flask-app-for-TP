from flask import Flask
from flask import render_template, request, redirect, url_for

from attraction import Attraction
from comment import Comment
from category import Category
from rating import Rating

app = Flask(__name__)


@app.route('/')
def main_menu():
    return redirect("/categories")


@app.route('/attractions')
def list_attractions():
    return render_template('attractions.html', attractions=Attraction.all())


@app.route('/attractions/<int:id>', methods=['GET', 'POST'])
def show_attraction(id):
    attraction = Attraction.find(id)  
    return render_template('attraction.html', attraction=attraction)


@app.route('/attractions/<string:name>')
def show_attraction_by_name(name):
    attraction = Attraction.find_by_name(name)   
    return render_template('attraction.html', attraction=attraction)


@app.route('/attractions/<int:id>/edit', methods=['GET', 'POST'])
def edit_attraction(id):
    attraction = Attraction.find(id)
    if request.method == 'GET':
        return render_template(
            'edit_attraction.html',
            attraction=attraction,
            categories=Category.all()
        )
    elif request.method == 'POST':
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
        return render_template('rate_attraction.html', attraction = attraction)
    elif request.method == 'POST':
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
        return render_template('new_attraction.html', categories=Category.all())
    elif request.method == 'POST':
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
    attraction.delete()

    return redirect('/')


@app.route('/comments/new', methods=['POST'])
def new_comment():
    if request.method == 'POST':
        attraction = Attraction.find(request.form['attraction_id'])
        values = (None, attraction, request.form['message'])
        Comment(*values).create()

        return redirect(url_for('show_attraction', id=attraction.id))


@app.route('/categories', methods=['GET', 'POST'])
def get_categories():
    if request.method == 'POST':
        if request.form.get('name'):
            attraction = Attraction.find_by_name(request.form.get('name'))
            if(attraction):
                return redirect(url_for('show_attraction_by_name', name = request.form.get('name')))
            else:
                app.logger.error('The user inputted nonexistent atraction')
        elif request.form.get('rate'):
            return render_template('attractions.html', attractions=Attraction.find_by_rating(request.form.get('rate'))) 
    return render_template("categories.html", categories=Category.all())


@app.route('/categories/new', methods=["GET", "POST"])
def new_category():
    if request.method == "GET":
        return render_template("new_category.html")
    elif request.method == "POST":
        category = Category(None, request.form["name"])
        category.create()
        return redirect("/categories")


@app.route('/categories/<int:id>')
def get_category(id):
    return render_template("category.html", category=Category.find(id))


@app.route('/categories/<int:id>/delete')
def delete_category(id):
    Category.find(id).delete()
    return redirect("/")


if __name__ == '__main__':
    app.run()
