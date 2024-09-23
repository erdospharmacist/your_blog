from flask import Blueprint, render_template, flash, request, redirect, url_for, abort
from flask_login import login_required, current_user, login_user, logout_user
# At the top of routes.py
from app.forms import LoginForm, RegistrationForm, PostForm, CommentForm

from app import db
from app.models import User, BlogPost, Comment
from app.decorators import admin_required
from werkzeug.security import check_password_hash

# Create a Blueprint to handle routing so we can avoid circular imports 
bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/index')
def index():
    return "Ethan Teicher's blog"


@bp.route('/contact')
def contact():
    return render_template('contact.html')


@bp.route('/learning')
def learning():
    return render_template('learningteaching.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  # Use 'main.home' since we're in a Blueprint

    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(email=email).first():
            flash('Email address already in use', 'danger')
            return redirect(url_for('main.register'))
        
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('main.login'))

    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


@bp.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)


@bp.route('/blog/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    comments = post.comments.order_by(Comment.created_at.desc()).all()
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You need to log in to comment.', 'danger')
            return redirect(url_for('main.login'))

        comment_content = form.content.data

        new_comment = Comment(content=comment_content, post_id=post.id, author_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()

        flash('Comment posted!', 'success')
        return redirect(url_for('main.view_post', post_id=post.id))

    return render_template('view_post.html', post=post, comments=comments, form=form)
@bp.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

#This is our admin route for posts
@bp.route('/create_post', methods=['GET', 'POST'])
@login_required
@admin_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_post = BlogPost(title=title, content=content, author_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        flash('Blog post created!', 'success')
        return redirect(url_for('main.blog'))

    return render_template('create_post.html', form=form)

# Error handler for 403 Forbidden
@bp.app_errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403
