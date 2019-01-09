from app import db, evaluations

db.create_all()


test_rec = evaluations(
        'Marco Hemken',
        'Los Angeles'
        )


db.session.add(test_rec)
db.session.commit()
