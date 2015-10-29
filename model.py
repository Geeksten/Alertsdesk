"""Models and database functions for Alerts project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of Alerts website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(64), nullable=False)
    lname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.Varchar(15), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s fname = %s email=%s>" % (self.user_id, self.fname, self.email)


class Userreport(db.Model):
    """User report on Alerts website."""

    __tablename__ = "userreports"

    urep_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    fname = db.Column(db.String(64), nullable=False)
    address = db.Column(db.Sring(64))
    latitude = db.Column(db.String(64), nullable=False)
    longitude = db.Column(db.String(64), nullable=False)
    report = db.column(db.String(200), nullable=False)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("userreports", order_by=urep_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Userreport latitude=%s longitude=%s report=%s>" % (self.latitude, self.longitude, self.report)


class Reportsymptom(db.Model):
    """Provides a way to connect the userreports and symptoms tables"""
    __tablename__ = "reportsymptoms"

    reportsym_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    urep_id = db.Column(db.Integer, db.ForeignKey('userreports.urep_id'))
    sym_id = db.Column(db.Integer, db.ForeignKey('symptoms.sym_id'))

    # Define relationship to user
    userreport = db.relationship("Userreport",
                                 backref=db.backref("reportsymptoms",
                                                    order_by=reportsym_id))

    # Define relationship to sympyom
    symptom = db.relationship("Symptom",
                              backref=db.backref("reportsymptoms",
                                                 order_by=reportsym_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Reportsymptom reportsym_id=%s urep_id=%s sym_id=%s>" % (
            self.reportsym_id, self.urep_id, self.sym_id)


class Symptom(db.Model):
    """Symptoms on Alerts website."""

    __tablename__ = "symptoms"

    sym_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sym_name = db.Column(db.String(64), nullable=False)
    description = db.column(db.String(200), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Symptom sym_id=%s sym_name=%s description>" % (
            self.sym_id, self.sym_name, self.description)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alerts.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
