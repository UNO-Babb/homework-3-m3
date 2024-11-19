from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Game state: track the current turn and the board's state
board = {}
current_player = 1  # Player 1 starts (1 = red, 2 = blue)

# Directions to check for neighboring hex tiles
hex_neighbors = [
    (0, 1),   # Right
    (1, 0),   # Bottom-right
    (1, -1),  # Bottom-left
    (0, -1),  # Left
    (-1, 0),  # Top-left
    (-1, 1),  # Top-right
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_board', methods=['GET'])
def get_board():
    return jsonify({'board': board, 'current_player': current_player})

@app.route('/make_move', methods=['POST'])
def make_move():
    global current_player

    data = request.json
    x = data['x']
    y = data['y']

    # Check if this spot is already occupied
    if (x, y) in board:
        return jsonify({'success': False, 'message': 'Tile already occupied'})

    # Check if the move is next to a tile of the current player's color
    can_place = False
    for dx, dy in hex_neighbors:
        neighbor = (x + dx, y + dy)
        if neighbor in board and board[neighbor] == ('red' if current_player == 1 else 'blue'):
            can_place = True
            break

    if not can_place:
        return jsonify({'success': False, 'message': 'Tile must be placed next to a tile of your color'})

    # Place the tile
    board[(x, y)] = 'red' if current_player == 1 else 'blue'

    # Switch the turn
    current_player = 2 if current_player == 1 else 1
    return jsonify({'success': True, 'current_player': current_player})

if __name__ == '__main__':
    app.run(debug=True)
