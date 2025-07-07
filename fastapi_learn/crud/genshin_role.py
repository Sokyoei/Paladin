from sqlalchemy.orm import Session

from fastapi_learn.models import GenshinRole
from fastapi_learn.schema import GenshinRole as GenshinRoleSchema


class GenshinRoleCRUD(object):

    def create_genshin_role(db: Session, genshin_role: GenshinRoleSchema):
        db_genshin_role = GenshinRole(name=genshin_role.name)
        db.add(db_genshin_role)
        db.commit()
        db.refresh(db_genshin_role)
        return db_genshin_role

    def delete_genshin_role(db: Session, genshin_role_id: int):
        db_genshin_role = db.query(GenshinRole).filter(GenshinRole.id == genshin_role_id).first()
        db.delete(db_genshin_role)
        db.commit()
        return db_genshin_role

    def update_genshin_role(db: Session, genshin_role_id: int, genshin_role: GenshinRoleSchema):
        db_genshin_role = db.query(GenshinRole).filter(GenshinRole.id == genshin_role_id).first()
        db_genshin_role.name = genshin_role.name
        db.commit()
        db.refresh(db_genshin_role)
        return db_genshin_role

    def search_genshin_role(db: Session, genshin_role_id: int):
        return db.query(GenshinRole).filter(GenshinRole.id == genshin_role_id).first()
