# Chess Web Application

This is a real-time multiplayer chess web application built using Flask and Flask-SocketIO. The application supports real-time updates and multi-sessions, leading to multiple rooms being created overall.

## Features

- Real-time multiplayer chess game.
- Supports undo and redo actions.
- Dynamic room creation with random room codes.
- Interactive chessboard interface with move validation.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python.
- **Flask-SocketIO**: Enables real-time communication between the server and clients.
- **eventlet**: Used for asynchronous task handling and long-polling fallback.

## Installation

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)

### Steps

1. **Clone the repository:**
```
git clone https://github.com/Sowoul/chess-host
cd chess-host
```

2.  Install the required packages:
```
pip install -r requirements.txt
```
3.  Run the application locally:
```
python3 main.py
```
4.  Visit the application:
Open your browser and navigate to `http://localhost:5000`.

## Usage

1. Access the application:
- Visit the pre-hosted webslite at [Koyeb](https://chess.koyeb.app/) or [Render](https://chess-host.onrender.com/)

2. Join or create a room:
- Enter a room name or leave it blank to create a new room with a random code.

3. Start playing:
- Once another player joins the room, the game will start.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Contributions are welcome!
