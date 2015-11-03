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
    email = db.Column(db.String(64), nullable=False)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s firstname = %s lastname = %s email=%s>" % (
            self.user_id, self.firstname, self.lastname, self.email)


class Userreport(db.Model):
    """User report on Alerts website."""

    __tablename__ = "userreports"

    urep_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    # firstname = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64))
    latitude = db.Column(db.String(64), nullable=False)
    longitude = db.Column(db.String(64), nullable=False)
    report = db.Column(db.String(200), nullable=False)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("userreports", order_by=urep_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Userreport report=%s>" % (self.report)


class Reportsymptom(db.Model):
    """Provides a way to connect the userreports and symptoms tables"""

    __tablename__ = "reportsymptoms"

    reportsym_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    urep_id = db.Column(db.Integer, db.ForeignKey('userreports.urep_id'))
    sym_id = db.Column(db.Integer, db.ForeignKey('symptoms.sym_id'))

    # Define relationship to userreport
    userreport = db.relationship("Userreport",
                                 backref=db.backref("reportsymptoms",
                                                    order_by=reportsym_id))

    # Define relationship to symptom
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
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """Providesde helpful representation when printed."""

        return "<Symptom sym_id=%s sym_name=%s description=%s>" % (
            self.sym_id, self.sym_name, self.description)


class State(db.Model):
    """States on Alerts website."""

    __tablename__ = "states"

    state_id = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.String(64), nullable=False)
    longitude = db.Column(db.String(64), nullable=False)

    def __repr__(self):

        return "<State state_id=%s name=%s>" % (
            self.state_id, self.name)


class Staterecall(db.Model):
    """Provides a way to connect the states table to the fdarecalls table."""

    __tablename__ = "statesrecalls"

    state_recallid = db.Column(db.String(20), autoincrement=True, primary_key=True)
    state_id = db.Column(db.String(2), db.ForeignKey('states.state_id'))
    fdarep_id = db.Column(db.String(2), db.ForeignKey('fdarecalls.recall_id'))

    # Define relationship to state
    state = db.relationship("State",
                            backref=db.backref("statesrecalls",
                                               order_by=state_recallid))

    # Define relationship to fdarecall
    fdarecall = db.relationship("Fdarecall",
                                backref=db.backref("staterecalls",
                                                   order_by=state_recallid))

    def __repr__(self):

        return "<State state_recallid=%s state_id=%s fdarep_id=%s>" % (
            self.state_recallid, self.state_id, self.fdarep_id)


class Fdarecall(db.Model):
    """Provides a way to connect the states table to the fdarecalls table."""

    __tablename__ = "fdarecalls"

    recall_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    recall_date = db.Column(db.DateTime, nullable=False)
    recall_firm = db.Column(db.String(50), nullable=False)
    prod_type = db.Column(db.String(20), nullable=False)
    prod_desc = db.Column(db.String(200), nullable=False)
    dist_pattern = db.Column(db.String(200), nullable=False)
    recall_city = db.Column(db.String(50), nullable=False)
    recall_state = db.Column(db.String(2), nullable=False)
    recall_country = db.Column(db.String(2), nullable=False)
    recall_reason = db.Column(db.String(200), nullable=False)
    date_reported = db.Column(db.DateTime, nullable=False)

    def __repr__(self):

        return """<FDArecall recall_id=%s status=%s recall_date=%s recall_firm =%s
                    prod_type=%s prod_desc=%s dist_pattern=%s recall_city=%s
                    recall_state=%s recall_country=%s recall_reason=%s
                    date_reported=%s>""" % (
            self.recall_id, self.status, self.recall_date,
            self.recall_firm, self.prod_type, self.prod_desc,
            self.dist_pattern, self.recall_city, self.recall_state,
            self.recall_country, self.recall_reason, self.date_reported)


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
