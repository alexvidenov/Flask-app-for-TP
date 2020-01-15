from database import DB

class Rating:
    def __init__(self, id, attraction, architecture_rating, interior_rating, historical_value_rating, rating):
        self.id = id
        self.attraction = attraction
        self.architecture_rating = architecture_rating
        self.interior_rating = interior_rating
        self.historical_value_rating = historical_value_rating
        self.rating = rating

    def create(self):
        with DB() as db:
            values = (self.id, self.attraction.id,  self.architecture_rating, self.interior_rating, self.historical_value_rating, self.rating)
            db.execute('''
                INSERT INTO ratings (id, attraction_id, architecture_rating, interior_rating, historical_value_rating, rating)
                VALUES (?,?,?,?,?,?)''', values)
            return self

    def update(self):
        with DB() as db:
            values = (self.id, self.attraction.id, self.rating)
            db.execute('''
                UPDATE ratings 
                SET attraction_id = ?, rating = ?
                WHERE id = ?''', values)
            return self

    def find_by_rating(rating):
         with DB() as db:
            row = db.execute(
                'SELECT * FROM ratings WHERE rating = ?',
                (rating,)
            ).fetchone()
            return Rating(*row)

    @staticmethod
    def attraction_rating(attraction):
        with DB() as db:
            rows = db.execute(
                'SELECT * FROM ratings WHERE attraction_id = ?',
                (attraction.id,)
            ).fetchall()
            return [Rating(*row) for row in rows]