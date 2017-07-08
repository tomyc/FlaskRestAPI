from app import app
from db import db

dc.init_app(app)


@app.before_first_request # przeniesione z app.py
def create_tables():
    db.create_all()
