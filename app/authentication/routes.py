from forms import UserSignUpForm, UserSigninForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash


# imports for flask login
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

# from flask_oauth import OAuth

# oauth = OAuth()
# car_app = oauth.remote_app('car_app')
auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignUpForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            print(email, first_name, last_name, password)

            user = User(email, first_name, last_name, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'User-created')
            return redirect(url_for('site.home'))
            
            
            
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form=form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserSigninForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successful in your login. Congratulations, and welcome to the Car Inquiries Page.', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('You do not have access to this content bacause you do not have the proper authorization.', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form and Validate Your Information.')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))


