from database import DB


class Comment:
    def __init__(self, id, attraction, message):
        self.id = id
        self.attraction = attraction
        self.message = message

    def create(self):
        with DB() as db:
            values = (self.attraction.id, self.message)
            db.execute(
                'INSERT INTO comments (attraction_id, message) VALUES (?, ?)',
                values
            )
            return self

    @staticmethod
    def find_by_attraction(attraction):
        with DB() as db:
            rows = db.execute(
                'SELECT * FROM comments WHERE attraction_id = ?',
                (attraction.id,)
            ).fetchall()
            return [Comment(*row) for row in rows]