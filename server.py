"""Alerts."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Userreport, Reportsymptom
from model import Symptom, State, Staterecall, Fdarecall


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("index.html")

############################################################################


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration.
    Uses a redirect so user does not have to leave page after registartion.
        Also uses flash messages to inform user that they have successfully registered
        and displays the username which is the email that was registered."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    firstname = (request.form["firstname"])
    lastname = request.form["lastname"]

    new_user = User(email=email, password=password, firstname=firstname, lastname=lastname)

    db.session.add(new_user)
    db.session.commit()

    flash("Thank you %s, you have been added as a user. Click the Login link to search" % email)
    return redirect('/')

########################################################################


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Sorry no such user found on our system. Please check the email address or register as a new user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("You logged in successfully")
    return redirect("/profile/%s" % user.user_id)

#########################################################################


@app.route('/profile/<int:user_id>')
def user_profile(user_id):
    """Show logged in users profile"""

    user = User.query.get(user_id)

    return render_template("profile.html", user=user)

########################################################################


@app.route('/addnewreport', methods=['GET'])
def report_form():
    """Show add new report form."""

    # user = User.query.get(user_id)
    # session["user_id"] = user.user_id
    print session["user_id"]

    return render_template("add_new_report_form.html")


# @app.route('/addnewreport', methods=['POST'])
# def report_process():
#     """Process new report."""

#     # Get form variables

#     address = request.form["address"]
#     report = request.form["report"]
#     user_id = session["user_id"]
#     firstname = request.form["firstname"]
#     latitude = request.form["latitude"]
#     longitude = request.form["longitude"]

#     new_userreport = Userreport(address=address, report=report, user_id=user_id, firstname=firstname, latitude=latitude, longitude=longitude)

#     db.session.add(new_userreport)
#     db.session.commit()

#     flash("Thank you %s, your report was added. Click the Search link to search for reports" % firstname)

#     # user = Userreport.query.get(user_id)

#     userreport = Userreport.query.filter_by(user_id)
#     print userreport

#     # return render_template("profile.html", user=user)

#     # return redirect("/profile/%s/%s" % (user.user_id, userreport.urep_id))

#     return render_template("profile.html", userreport=userreport)
#     # return render_template("profile.html", user=user)

#########################################################################


@app.route('/profile/<int:user_id>/<int:urep_id>')
def user_report(urep_id, user_id):
    """Show logged in users reports"""

    user = User.query.get(user_id)

    userreport = Userreport.query.filter_by(user_id)

    session["user_id"] = user.user_id

    return render_template("profile.html", userreport=userreport, user=user)


# @app.route('/profile/<int:user_id>')
# def user_profile(user_id):
#     """Show logged in users profile"""

#     user = User.query.get(user_id)

#     session["user_id"] = user.user_id

#     return render_template("profile.html", user=user)
#########################################################################


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("You have logged out successfully.")
    return redirect("/")


#########################################################################


# @app.route("/users")
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)

########################################################################


# @app.route("/users/<int:user_id>")
# def user_detail(user_id):
#     """Show info about user."""

#     user = User.query.get(user_id)
#     return render_template("user.html", user=user)

#######################################################################


# @app.route("/movies")
# def movie_list():
#     """Show list of movies."""

#     movies = Movie.query.order_by('title').all()
#     return render_template("movie_list.html", movies=movies)

#####################################################################


# @app.route("/movies/<int:movie_id>", methods=['GET'])
# def movie_detail(movie_id):
#     """Show info about movie.

#     If a user is logged in, let them add/edit a rating.
#     """

#     movie = Movie.query.get(movie_id)

#     user_id = session.get("user_id")

#     if user_id:
#         user_rating = Rating.query.filter_by(
#             movie_id=movie_id, user_id=user_id).first()

#     else:
#         user_rating = None

#     return render_template("movie.html",
#                            movie=movie,
#                            user_rating=user_rating)

#######################################################################


# @app.route("/movies/<int:movie_id>", methods=['POST'])
# def movie_detail_process(movie_id):
#     """Add/edit a rating."""

#     # Get form variables
#     score = int(request.form["score"])

#     user_id = session.get("user_id")
#     if not user_id:
#         raise Exception("No user logged in.")

#     rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

#     if rating:
#         rating.score = score
#         flash("Rating updated.")

#     else:
#         rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
#         flash("Rating added.")
#         db.session.add(rating)

#     db.session.commit()

#     return redirect("/movies/%s" % movie_id)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
