This was a project I recently completed in an effort to better understand API's in Python and Flask to better my python webdev/front-end skills.
The project has been stripped back to barebones for anyone who wants to use it, if this is you please make sure you do the following to ensure it works.
In your terminal in your project root directory enter the following:
$ flask db init
$ flask db migrate -m "Name of this migration"
$ flask db upgrade
Next we need to set you as an admin, to do this register an account on the webpage, then open up a flask shell and enter the following 
from app import db
from app.models import User

#replace this portion with your email
admin_user = User.query.filter_by(email='your_email@example.com').first()
admin_user.is_admin = True
db.session.commit()
