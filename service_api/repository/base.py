class BaseRepo:
    model = None

    def __init__(self, db):
        self.db = db
