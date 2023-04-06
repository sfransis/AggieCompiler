from main import *

if __name__ == '__main__':
    db.create_all() # creates all of the db NOTE that if you want to make a change to the db, you need to replace create_all with drop_all so that current dbs are deleted and then change it back so that the changes are made
#     #db.session.query(Comment).delete()
    app.run(debug = True) #means that we won't have to rerun the server
    
    