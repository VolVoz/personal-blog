from app import db
if db.create_all():
    print "Models updated!!!"
print "Oops!"
