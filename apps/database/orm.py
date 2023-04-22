from sqlalchemy.orm import Session

from apps.database.connect import engine

def add_user_to_db(user_id, class_user):
    session = Session(engine)

    user = class_user(
        tg_id = user_id
    )
    session.add(user)
    session.commit()

def is_user_in_db(user_id, class_user):
    session = Session(engine)

    result = session.query(class_user.tg_id).filter(user_id == class_user.tg_id).first()
    return result != None

def update_user_warning(user_id, class_user):
    session = Session(engine)

    user = session.query(class_user).filter(user_id == class_user.tg_id).first()
    
    user.warning_count += 1
    session.commit()    



def get_user_warnings_db(user_id, class_user):
    session = Session(engine)

    result = session.query(class_user.warning_count).filter(class_user.tg_id == user_id).first()

    return result[0]