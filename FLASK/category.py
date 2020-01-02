from database import DB
from attraction import Attraction


class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM categories').fetchall()
            return [Category(*row) for row in rows]

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute('SELECT * FROM categories WHERE id = ?', (id,)) \
                .fetchone()
            if not row:
                return Category(0, "All attractions")
            return Category(*row)

    def create(self):
        with DB() as db:
            values = (self.name,)
            db.execute('''
                INSERT INTO categories (name)
                VALUES (?)''', values)
            return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM categories WHERE id = ?', (self.id,))
            db.execute(
                '''
                UPDATE attractions
                SET category_id = 0 WHERE category_id = ?
                ''',
                (self.id,)
            )

    def attractions(self):
        return Attraction.find_by_category(self)