from database import DB
from comment import Comment

class Attraction:
    def __init__(self, id, name, location, image, description, category):
        self.id = id
        self.name = name
        self.location = location
        self.image = image
        self.description = description
        self.category = category

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM attractions').fetchall()
            return [Attraction(*row) for row in rows]

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute(
                'SELECT * FROM attractions WHERE id = ?',
                (id,)
            ).fetchone()
            return Attraction(*row)

    @staticmethod
    def find_by_name(name):
        with DB() as db:
            row = db.execute(
                'SELECT * FROM attractions WHERE name = ?',
                (name,)
            ).fetchone()
            return Attraction(*row)

    @staticmethod
    def find_by_category(category):
        with DB() as db:
            rows = db.execute(
                'SELECT * FROM attractions WHERE category_id = ?',
                (category.id,)
            ).fetchall()
            return [Attraction(*row) for row in rows]

    def create(self):
        with DB() as db:
            values = (self.name, self.location, self.image, self.description, self.category.id)
            db.execute('''
                INSERT INTO attractions (name, location, image, description, category_id)
                VALUES (?, ?, ?, ?, ?)''', values)
            return self

    def save(self):
        with DB() as db:
            values = (
                self.name,
                self.location,
                self.image,
                self.description,
                self.category.id,
                self.id
            )
            db.execute(
                '''UPDATE attractions
                SET name = ?, location = ?, image = ?, description = ?, category_id = ?
                WHERE id = ?''', values)
            return self

    def rate(self):
        with DB() as db:
            values = (
                self.description,
                self.id
            )
            db.execute(
                '''UPDATE attractions
                SET description = ?
                WHERE id = ?''', values)
            return self


    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM attractions WHERE id = ?', (self.id,))

    def comments(self):
        return Comment.find_by_attraction(self)