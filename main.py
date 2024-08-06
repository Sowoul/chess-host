from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, join_room, leave_room, send
from chess import Board, Pawn, Rook, Knight, Bishop, Queen, King
from string import ascii_uppercase
from random import choice

app = Flask(__name__)
socket = SocketIO(app=app)
app.config["SECRET_KEY"] = "IDK123"
rooms = {}







def get_random_room(ln):
    return ''.join(choice(ascii_uppercase) for _ in range(ln))

def make_board(arr):
    piece_map = {
        'p': Pawn,
        'r': Rook,
        'n': Knight,
        'b': Bishop,
        'q': Queen,
        'k': King
    }
    temp = Board()
    for i, row in enumerate(arr):
        for j, elem in enumerate(row):
            if elem:
                piece_class = piece_map.get(elem['alias'])
                if piece_class:
                    temp.board[i][j] = piece_class(elem['color'])
                else:
                    raise ValueError(f"Unknown piece alias: {elem['alias']}")
    return temp





@app.route('/', methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        room = request.form.get("room")
        if name == "NoName":
            return render_template("login.html")
        if room != "" and room not in rooms:
            return render_template('login.html')
        session["turn"]="b"
        if room == "":
            room = get_random_room(8)
            newb = Board()
            newb.setup()
            rooms[room] = {"members": 0, "board": newb.to_dict(), "undo": [], "redo": [], "turn":"w"}
            session["turn"]="w"
        if rooms[room]["members"]==2:
            return redirect(url_for('login'))
        rooms[room]["members"]+=1
        session["room"] = room
        session["name"] = name  
        return redirect(url_for('index'))
    return render_template('login.html')





@app.route('/chess')
def index():
    code = session.get("room" , "Invalid")
    if code=="Invalid":
        return redirect(url_for('login'))
    return render_template("index.html", code = session.get("room","Invalid"))





@app.route('/getSide', methods=["GET"])
def side():
    return "0" if  "w"==session.get("turn") else "1"





@socket.on('connect')
def _connect():
    room = session.get('room')
    if not room or room not in rooms:
        return
    session["undo"] = rooms[room]["undo"]
    session["redo"] = rooms[room]["redo"]
    session["board"] = rooms[room]["board"]
    join_room(room)
    if len(session["undo"]) > 0:
        socket.emit('getboard', {'board': session["undo"][-1]}, room=room)
    else:
        socket.emit('getboard', {'board': session["board"]}, room=room)





@socket.on('move')
def handle_move(msg):
    room = session.get('room')
    if not room or room not in rooms:
        return
    if session["turn"]!=rooms[room]["turn"]:
        socket.emit('failure', {'reason' : 'Not your Turn'}, room=room)
        return
    temp = make_board(msg["board"])
    if not temp.getpiece(msg["start"]):
        socket.emit('failure', {'reason': 'No Piece Selected'}, room=room)
        return
    try:
        temp.move(msg["start"], msg["to"])
    except ValueError as e:
        socket.emit('failure', {'reason': str(e).lstrip("Error -")}, room=room)
        return
    rooms[room]["turn"]="w" if rooms[room]["turn"]=='b' else 'b'
    store = temp.to_dict()
    session["undo"].append(store)
    session["redo"] = []
    rooms[room]["undo"] = session["undo"]
    rooms[room]["redo"] = session["redo"]
    socket.emit('getboard', {"board": store}, room=room)





@socket.on('resetboard')
def handle_reset():
    room = session.get('room')
    if not room or room not in rooms:
        return

    board = Board()
    session["undo"] = []
    session["redo"] = []
    board.setup()
    store = board.to_dict()
    session["board"] = store
    rooms[room]["board"] = store
    rooms[room]["undo"] = session["undo"]
    rooms[room]["redo"] = session["redo"]
    rooms[room]["turn"]="w"
    socket.emit('getboard', {'board': store}, room=room)





@socket.on('undo')
def handle_undo():
    room = session.get('room')
    if not room or room not in rooms:
        return

    if len(session["undo"]) <= 1:
        if len(session["undo"]) == 1:
            session["redo"].append(session["undo"].pop())
        board = Board()
        board.setup()
        store = board.to_dict()
        session["board"] = store
    else:
        session["redo"].append(session["undo"].pop())
        board = make_board(session["undo"][-1])
        store = session["undo"][-1]
    rooms[room]["undo"] = session["undo"]
    rooms[room]["redo"] = session["redo"]
    rooms[room]["turn"]="w" if rooms[room]["turn"]=='b' else 'b'
    socket.emit('getboard', {'board': store}, room=room)





@socket.on('redo')
def handle_redo():
    room = session.get('room')
    if not room or room not in rooms:
        return

    if len(session["redo"]) == 0:
        return
    session["undo"].append(session["redo"].pop())
    board = make_board(session["undo"][-1])
    rooms[room]["undo"] = session["undo"]
    rooms[room]["redo"] = session["redo"]
    rooms[room]["turn"]="w" if rooms[room]["turn"]=='b' else 'b'
    socket.emit('getboard', {'board': session["undo"][-1]}, room=room)









if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=5000, debug=True)
