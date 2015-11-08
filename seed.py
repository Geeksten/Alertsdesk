"""Utility file to alerts from fakedata file data in alert_data/"""

import datetime

from model import User, Userreport, Symptom, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    for i, row in enumerate(open("seed_data/u.user")):

        row = row.rstrip()
        # print row
        # print type(row)

        list_of_values = row.split("|")
        user_id, email, firstname, lastname, password = list_of_values

        user = User(user_id=user_id,
                    email=email,
                    firstname=firstname,
                    lastname=lastname,
                    password=password)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

        # provide some sense of progress
        if i % 100 == 0:
            print "records added is %s" % i

    # Once we're done, we should commit our work
    db.session.commit()

##########################################################################


def load_userreports():
    """Load userreports from u.userreport into database."""

    print "Userreports"

    for i, row in enumerate(open("seed_data/u.userreport")):

        row = row.rstrip()
        # print row
        # print type(row)

        list_of_values = row.split("|")
        urep_id, user_id, address, zipcode, latitude, longitude, report = list_of_values

        userreport = Userreport(urep_id=urep_id,
                                user_id=user_id,
                                address=address,
                                zipcode=zipcode,
                                latitude=latitude,
                                longitude=longitude,
                                report=report)

        # We need to add to the session or it won't ever be stored
        db.session.add(userreport)

        # provide some sense of progress
        if i % 100 == 0:
            print "records added is %s" % i

    # Once we're done, we should commit our work
    db.session.commit()
##########################################################################


def load_symptoms():
    """Load symptoms from u.symptom into database."""

    print "Symptoms"

    for i, row in enumerate(open("seed_data/u.symptom")):
        row = row.rstrip()

        # clever -- we can unpack part of the row!
        sym_id, sym_name, description = row.split("|")

        symptom = Symptom(sym_id=sym_id,
                          sym_name=sym_name,
                          description=description)

        # We need to add to the session or it won't ever be stored
        db.session.add(symptom)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    # Once we're done, we should commit our work
    db.session.commit()

##############################################################################

# def load_ratings():
#     """Load ratings from u.data into database."""

#     print "Ratings"

#     for i, row in enumerate(open("seed_data/u.data")):
#         row = row.rstrip()

#         user_id, movie_id, score, timestamp = row.split("\t")

#         user_id = int(user_id)
#         movie_id = int(movie_id)
#         score = int(score)

#         # We don't care about the timestamp, so we'll ignore this

#         rating = Rating(user_id=user_id,
#                         movie_id=movie_id,
#                         score=score)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(rating)

#         # provide some sense of progress
#         if i % 1000 == 0:
#             print i

#             # An optimization: if we commit after every add, the database
#             # will do a lot of work committing each record. However, if we
#             # wait until the end, on computers with smaller amounts of
#             # memory, it might thrash around. By committing every 1,000th
#             # add, we'll strike a good balance.

#             db.session.commit()

#     # Once we're done, we should commit our work
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_userreports()
    load_symptoms()

#     # Mimic what we did in the interpreter, and add the Eye and some ratings
#     eye = User(email="the-eye@of-judgment.com", password="evil")
#     db.session.add(eye)
#     db.session.commit()

#     # Toy Story
#     r = Rating(user_id=eye.user_id, movie_id=1, score=1)
#     db.session.add(r)

#     # Robocop 3
#     r = Rating(user_id=eye.user_id, movie_id=1274, score=5)
#     db.session.add(r)

#     # Judge Dredd
#     r = Rating(user_id=eye.user_id, movie_id=373, score=5)
#     db.session.add(r)

#     # 3 Ninjas
#     r = Rating(user_id=eye.user_id, movie_id=314, score=5)
#     db.session.add(r)

#     # Aladdin
#     r = Rating(user_id=eye.user_id, movie_id=95, score=1)
#     db.session.add(r)

#     # The Lion King
#     r = Rating(user_id=eye.user_id, movie_id=71, score=1)
#     db.session.add(r)

#     db.session.commit()

#     # Add our user
#     jessica = User(email="jessica@gmail.com",
#                    password="love",
#                    age=42,
#                    zipcode="94114")
#     db.session.add(jessica)
#     db.session.commit()

#     # Toy Story
#     r = Rating(user_id=jessica.user_id, movie_id=1, score=5)
#     db.session.add(r)

#     # Robocop 3
#     r = Rating(user_id=jessica.user_id, movie_id=1274, score=1)
#     db.session.add(r)

#     # Judge Dredd
#     r = Rating(user_id=jessica.user_id, movie_id=373, score=1)
#     db.session.add(r)

#     # 3 Ninjas
#     r = Rating(user_id=jessica.user_id, movie_id=314, score=1)
#     db.session.add(r)

#     # Aladdin
#     r = Rating(user_id=jessica.user_id, movie_id=95, score=5)
#     db.session.add(r)

#     # The Lion King
#     r = Rating(user_id=jessica.user_id, movie_id=71, score=5)
#     db.session.add(r)

#     db.session.commit()
