from main import *
from compiler import * 
from flask import Flask
from flask_socketio import SocketIO




@socketio.on('connect')
def handle_connect():
    emit('connect')

@socketio.on('code')
def handle_code(code):
    emit('code', code, broadcast=True)


# if __name__ == '__main__':
#     db.create_all() # creates all of the db NOTE that if you want to make a change to the db, you need to replace create_all with drop_all so that current dbs are deleted and then change it back so that the changes are made
# #     #db.session.query(Comment).delete()
#     app.run(debug = True) #means that we won't have to rerun the server
#     app = Flask(__name__)
#     socketio.run(beta)
    