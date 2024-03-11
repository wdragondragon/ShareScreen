from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# 存储屏幕共享状态的字典
screen_sharing_state = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/watch/<room_id>')
def watch(room_id):
    return render_template('watch.html', room_id=room_id)


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('join_room')
def handle_join_room(data):
    room_id = data['room_id']
    screen_sharing_state[room_id] = True
    socketio.emit('joined_room', {'room_id': room_id})


@socketio.on('leave_room')
def handle_leave_room(data):
    room_id = data['room_id']
    socketio.emit('left_room', {'room_id': room_id})


@socketio.on('upload_screen')
def upload_screen(data):
    room_id = data['room_id']
    image_data = data['image_data']
    if screen_sharing_state.get(room_id, False):
        # 将 base64 编码的图像数据转换为图像对象
        socketio.emit('update_screen', {'image_data': image_data})
    return {'success': True}


if __name__ == '__main__':
    socketio.run(app, use_reloader=False, allow_unsafe_werkzeug=True, log_output=True, port=10551, host='0.0.0.0')
