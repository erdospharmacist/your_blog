#MAKE SURE YOU HAD YOUR OWN SECRET_KEY FILE FOR THIS PROJ ON YOUR COMPUTER OUTSIDE YOUR BLOG DIRECTORY TO ENSURE PROPER SITE SECURITY
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Optional, to disable overhead


