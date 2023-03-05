from sqlalchemy import update


class BaseRepo:
    model = None

    def __init__(self, db):
        self.db = db

    def create(self, payload):
        entity = self.model(**payload)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def all(self, *args, **kwargs):
        return self.db.query(self.model).all()

    def get(self, entity_id):
        return self.db.get(self.model, entity_id)

    def update(self, entity_id, payload):
        stmt = update(
            self.model
        ).where(
            self.model.id == entity_id
        ).values(
            **payload
        ).returning(self.model)
        result = self.db.execute(stmt)
        self.db.commit()
        return result.scalar()

    def delete(self, entity_id, user_id):
        return self.db.query(self.model).where(
            self.model.id == entity_id,
            self.model.author_id == user_id,
            self.model.archive_id.is_not(None)).delete()
