from models import User, db
from app import app

db.drop_all()
db.create_all()

daniel = User(
    first_name='Daniel',
    last_name='Beyon',
    image_url='anything'
)
michael = User(
    first_name='Michael',
    last_name='Bocim',
    image_url='something'
)


db.session.add(daniel)
db.session.add(michael)

db.session.commit()
