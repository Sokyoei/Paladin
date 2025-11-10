from sqlalchemy.orm import Session

from fastapi_learn.models import User
from fastapi_learn.schemas import User as UserSchema


class UserCRUD(object):

    def create_user(db: Session, user: UserSchema):
        db_user = User(user.name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(db: Session):
        pass

    def update_user(db: Session):
        pass

    def search_user(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()
