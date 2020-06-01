from app import create_app

def init_db(sql_db='default'):
    from app.models.Users import User
    from app import db
    app=create_app(sql_db)
    app.app_context().push()
    db.drop_all()
    db.create_all()
    db.session.commit()

init_db()