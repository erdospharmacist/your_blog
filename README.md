This was a project I recently completed in an effort to better understand API's in Python and Flask to better my python webdev/front-end skills.
The project has been stripped back to barebones for anyone who wants to  use it, if this is you please make sure you do the following to ensure it works.
In your terminal in your project root directory enter the following:<br />
$ flask db init<br />
$ flask db migrate -m "Name of this migration"<br />
$ flask db upgrade<br />
Next we need to set you as an admin, to do this register an account on the webpage, then open up a flask shell and enter the following<br />
from app import db<br />
from app.models import User<br />

#replace this portion with your email<br />
admin_user = User.query.filter_by(email='your_email@example.com').first()<br />
admin_user.is_admin = True<br />
db.session.commit()
