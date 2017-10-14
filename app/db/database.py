from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()


class SerializableMixin:
    serializable_attrs = []

    def __repr__(self):
        attributes = list()
        # always add id to __repr__ (if present)
        if 'id' in self.__dict__:
            attributes.append('id={0}'.format(self.id))
        for attr in self.serializable_attrs:
            if attr == 'id':
                continue
            attributes.append("{attr_name}={attr_value}".format(
                attr_name=attr,
                attr_value=getattr(self, attr),
            ))
        return '<{class_name} {attributes}>'.format(
            class_name=self.__class__.__name__,
            attributes=', '.join(attributes),
        )

    def to_dict(self):
        result = dict()
        for attr in self.serializable_attrs:
            if attr == 'app_id':
                result['id'] = getattr(self, attr)
            else:
                result[attr] = getattr(self, attr)
        return result


class CRUDMixin:
    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def insert(cls, error_handler, commit=True, obj=None, **kwargs):
        new_obj = obj or cls.create(**kwargs)
        return new_obj.save(commit=commit, error_handler=error_handler)

    def update(self, commit=True, **kwargs):
        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)
        return self.save(commit=commit)

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    def save(self, commit=True, error_handler=None):
        try:
            with db.session.begin_nested():  # SAVEPOINT
                db.session.add(self)
        except IntegrityError:
            db.session.rollback()
            if error_handler is None:
                return self
            return error_handler(self)
        else:
            if commit:
                db.session.commit()
            return self


class BaseModel(SerializableMixin, CRUDMixin, db.Model):
        __abstract__ = True


db.BaseModel = BaseModel
