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
    """New user sign in form."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration.
        Uses a redirect so user does not have to leave page after registration.
        Also uses flash messages to inform user that they have successfully registered
        and displays the username which is the email that was registered."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]

    user = User.query.filter_by(email=email).first()

    if user:
        flash("You're already a user. Please log in.")
        return redirect("/login")

    else:

        new_user = User(email=email, password=password, firstname=firstname, lastname=lastname)

    db.session.add(new_user)
    db.session.commit()

    flash("Thank you %s, you have been added as a user. Go ahead and log in" % email)
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
        flash("Sorry that email was not found on our system. Please check the email address or register as a new user")
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

    # user = User.query.get(user_id)

    user_id = session.get("user_id")

    if not user_id:
        return redirect('/login')

    else:
        user = User.query.get(user_id)
        return render_template("profile.html", user=user)

########################################################################


@app.route('/addnewreport', methods=['GET'])
def report_form():
    """Show add new report form."""

    # print session["user_id"]

    user_id = session.get("user_id")

    if not user_id:
        flash("Sorry log in required before adding a report.")
        return redirect('/login')

    else:
        return render_template("add_new_report_form.html")

#########################################################################


@app.route('/userreport', methods=['POST'])
def report_process():
    """Process new report."""

    # Get form variables

    address = request.form["address"]
    report = request.form["report"]
    user_id = session["user_id"]
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]

    new_userreport = Userreport(address=address, report=report, user_id=user_id, latitude=latitude, longitude=longitude)

    db.session.add(new_userreport)
    db.session.commit()

#     flash("Thank you %s, your report was added. Click the Search link to search for reports" % firstname)

    user_id = session.get("user_id")

    # user = User.query.filter_by(email=email).first()
    user = User.query.get(user_id)
    print "*********************** user is %s" % user
    userreport_list = Userreport.query.filter_by(user_id=user_id).all()

    print "*********************** userreport is %s" % userreport_list

    return render_template("userreport.html", userreport_list=userreport_list, user=user)

#########################################################################


@app.route('/alerts', methods=['GET'])
def alerts_signup_form():
    """Show alerts sign up form."""

    user_id = session.get("user_id")

    if not user_id:
        flash("Sorry log in required before signing up for alerts.")
        return redirect('/login')

    else:
        return render_template("alerts_signup.html")

#########################################################################


@app.route('/alerts', methods=['POST'])
# def alerts_process():
#     """Process alerts sign up."""

#     # Get form variables
#     email = request.form["email"]
#     password = request.form["password"]

#     user = User.query.filter_by(email=email).first()

#     if not user:
#         flash("Sorry that email was not found on our system. Please check the email address or register as a new user")
#         return redirect("/login")

#     if user.password != password:
#         flash("Incorrect password")
#         return redirect("/login")

#     session["user_id"] = user.user_id

#     flash("You logged in successfully")
#     return redirect("/profile/%s" % user.user_id)
##########################################################################


# @app.route('/search', methods=['POST'])
# def search():
#     """Process login."""

#     # Get form variables
#     email = request.form["email"]
#     password = request.form["password"]

#     user = User.query.filter_by(email=email).first()

#     if not user:
#         flash("Sorry that email was not found on our system. Please check the email address or register as a new user")
#         return redirect("/login")

#     if user.password != password:
#         flash("Incorrect password")
#         return redirect("/login")

#     session["user_id"] = user.user_id

#     flash("You logged in successfully")
#     return redirect("/profile/%s" % user.user_id)
#########################################################################


@app.route("/symptom/<int:sym_id>")
def show_symptoms(sym_id):
    """Return page showing more information about a given symtom.
    """
    # user = User.query.filter_by(email=email).first()
    symptom = Symptom.query.get(sym_id)
    print symptom
    return render_template("symptom_details.html",
                           symptom=symptom)
#########################################################################


@app.route('/map')
def show_map():
    return render_template("map.html")


#########################################################################

# @app.route('/alerts')
# def sign_up_for_alerts():
#     pass

##########################################################################


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("You have logged out successfully.")
    return redirect("/")


#########################################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
