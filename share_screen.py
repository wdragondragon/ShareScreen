import base64
import io
import sys
import time

from PIL import Image
from mss import mss
import socketio

SERVER_URL = "http://localhost:10551"  # 更新为你的服务器地址
sio = socketio.Client()


def capture_and_upload(room_id, frame_rate, screen_area):
    sio.connect(SERVER_URL)
    compute_time = time.time()
    screen_count = 0
    size_count = 0
    with mss() as sct:
        while True:
            screenshot = sct.grab(screen_area)
            pim = Image.new("RGB", screenshot.size)
            pim.frombytes(screenshot.rgb)
            img_byte_array = io.BytesIO()
            pim.save(img_byte_array, format='PNG', quality=95)
            img_bytes = img_byte_array.getvalue()
            img_data = base64.b64encode(img_bytes).decode('utf-8')

            payload = {
                'room_id': room_id,
                'frame_rate': frame_rate,
                'screen_area': screen_area,
                'image_data': img_data
            }
            size = sys.getsizeof(payload)
            sio.emit('upload_screen', payload)

            size_count += size
            screen_count += 1
            now = time.time()
            if now - compute_time > 1:
                print(f"上传图片速率：{screen_count}/s，宽带占用：{size_count / (1024 * 1024)}M/s")
                screen_count = 0
                size_count = 0
                compute_time = now
            time.sleep(1 / frame_rate)


if __name__ == '__main__':
    room_id = "1"  # 更新为实际的房间号
    frame_rate = 10  # 更新为实际的帧刷新率
    screen_area = {'left': 1280, 'top': 720, 'width': 640, 'height': 640}  # 更新为实际的屏幕区域
    capture_and_upload(room_id, frame_rate, screen_area)
