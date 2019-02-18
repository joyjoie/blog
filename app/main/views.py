from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from ..models import User, Posts
from .forms import PostsForm,UpdateProfile
from .. import db,photos
from flask_login import login_user, logout_user, login_required, current_user
import datetime




# Views
@main.route('/')
def index():

    posters=Posts.query.all()
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to Blog'

    form = PostsForm()
    return render_template('index.html',form = form,title=title, posts=posters)
    

@main.route('/new_post', methods = ['GET','POST'])

def new_post():
    form = PostsForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        add_post = Posts(title=title,content=content)
        add_post.save_posts()
        flash("Your post has been created!" ,"success")
        return redirect(url_for('main.index'))
    return render_template('new_post.html',form=form)


@main.route('/post/<int:post_id>', methods = ['GET','POST'])

def post(post_id):
    post =Posts.query.get(post_id)
    form = PostsForm()
    title = form.title.data
    
    return render_template('post.html',form=form, title=title , post=post)


@main.route('/post/<int:post_id/update>', methods = ['GET','POST'])
@login_required
def update_post(post_id):
    post =Posts.query.get(post_id)
    if post.author != current_user:
        abort(403)
        
    form = PostsForm()
    title = form.title.data
    
    return render_template('post.html',form=form, title=title , post=post)
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

# @main.route('/new_feedback', methods = ['GET','POST'])
# @login_required
# def new_feedback():
#     form = FeedbackForm()
#     pitch = Pitch.query.filter()
#     if form.validate_on_submit():

#         feedback = Feedback(title=form.title.data,feedback=form.feedback.data, pitch=pitch)
#         db.session.add(feedback)
#         db.session.commit()

#     feed_back = Feedback.query.filter_by(pitch=pitch).all()
#     return render_template('new_feedback.html',feed_back=feed_back,form=form)