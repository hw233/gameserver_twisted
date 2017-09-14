import time

last_frame_start_time = time.time()
delta_time = None


def update():
    global last_frame_start_time, delta_time
    delta_time = time.time() - last_frame_start_time
    last_frame_start_time = time.time()
