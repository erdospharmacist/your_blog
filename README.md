This was a project I recently completed in an effort to better understand API's in Python and Flask to better my python webdev/front-end skills.
The project has been stripped back to barebones for anyone who wants to  use it, if this is you please make sure you do the following to ensure it works.
In your terminal in your project root directory enter the following: **Enter**
$ flask db init__
$ flask db migrate -m "Name of this migration"__
$ flask db upgrade__
Next we need to set you as an admin, to do this register an account on the webpage, then open up a flask shell and enter the following__
from app import db__
from app.models import User__

#replace this portion with your email__
admin_user = User.query.filter_by(email='your_email@example.com').first()__
admin_user.is_admin = True__
db.session.commit()__
