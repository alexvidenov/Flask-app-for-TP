from flask import Flask
from flask import render_template, request, redirect, url_for

from attraction import Attraction
from comment import Comment
from category import Category

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
        attraction.category = Category.find(request.form['category_id'])
        attraction.save()
        return redirect(url_for('show_attraction', id=attraction.id))

@app.route('/attractions/<int:id>/rate', methods=['GET', 'POST'])
def rate_attraction(id):
    attraction = Attraction.find(id)
    if request.method == 'GET':
        return render_template(
            'rate_attraction.html',
            attraction=attraction,
        )
    elif request.method == 'POST':
        if request.form.get('one star rate'):
            attraction.description = attraction.description + "This attraction is rated with one star"
            attraction.rate()
            return redirect(url_for('show_attraction', id=attraction.id))
        elif request.form.get('two star rate'):
            attraction.description = attraction.description + "This attraction is rated with two stars" 
            attraction.rate()
            return redirect(url_for('show_attraction', id=attraction.id))
        elif request.form.get('three star rate'):
            attraction.description = attraction.description + "This attraction is rated with three stars" 
            attraction.rate()
            return redirect(url_for('show_attraction', id=attraction.id))
        elif request.form.get('four star rate'):
            attraction.description = attraction.description + "This attraction is rated with four stars" 
            attraction.rate()
            return redirect(url_for('show_attraction', id=attraction.id))


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
        return redirect(url_for('show_attraction_by_name', name = request.form.get('name')))
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
