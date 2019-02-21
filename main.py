import pyglet
import socket, sys
import random

from pyglet.window import key,mouse
from threading import Thread, RLock


from resources import Resources

class ElevatorServer():
    floor_positions = [70, 205, 342, 478]

    order_keys   = Resources.order_keys

    def __init__(self, index, x, y, parent):
        elev_y = random.randrange(self.floor_positions[0], self.floor_positions[-1])
        self.lock = RLock()
        self.batch = pyglet.graphics.Batch()

        self.hall_up_orders = []
        self.hall_down_orders = []
        self.cab_orders = []
        self.floors = []

        self.window = parent
        self.index = index
        self.active = True
        self.stopped = False

        # Create sprites for floors and orders
        for i in range(4):
            self.floors.append(pyglet.sprite.Sprite(Resources.floor_imgs[i],
                    x=x-30, y=self.floor_positions[i], batch=self.batch))
            self.floors[i].opacity = 80

        for i in range(3):
            self.hall_up_orders.append(pyglet.sprite.Sprite(Resources.arrow_img,
                    x=x-15, y=self.floor_positions[i]+14, batch=self.batch))
            self.hall_up_orders[i].opacity = 80

        for i in range(1, 4):
            self.hall_down_orders.append(pyglet.sprite.Sprite(Resources.arrow_down_img,
                    x=x-15, y=self.floor_positions[i]-6, batch=self.batch))
            self.hall_down_orders[i-1].opacity = 80

        for i in range(4):
            self.cab_orders.append(pyglet.sprite.Sprite(Resources.cab_order_imgs[i],
                    x=x-50, y=y - 20, batch=self.batch))
            self.cab_orders[i].opacity = 80

        # Create sprites for the elevator
        self.elevator = pyglet.sprite.Sprite(Resources.elevator_img, x, elev_y, batch=self.batch)
        self.elevator.dy = 0.0

        self.doors = pyglet.sprite.Sprite(Resources.doors_img,
                x=x + 5, y=elev_y + 5)

        self.stop_button = pyglet.sprite.Sprite(Resources.stop_img,
                x=x + 8, y=elev_y + 10)
        self.stop_button.visible = False

        self.signal = pyglet.sprite.Sprite(Resources.signal_img,
                x=x, y=elev_y, batch=self.batch)
        self.signal.visible = False

        # Start the networking thread
        self.thread = Thread(target=recv_on_port, args=(self, index,15657+index,))
        self.thread.start()

    def update(self, dt):
        self.elevator.y += self.elevator.dy * dt
        self.doors.y += self.elevator.dy * dt
        self.stop_button.y += self.elevator.dy * dt
        self.signal.y += self.elevator.dy * dt

        self.elevator.center = (self.elevator.x + self.elevator.width/2,
                                self.elevator.y + self.elevator.height/2 - 15)

    def set_motor_direction(self, direction):
        with self.lock:
            if direction == 1:
                self.elevator.dy = 30
            elif direction == 255:
                self.elevator.dy = -30
            else: # direction == 0
                self.elevator.dy = 0

    def set_stop_button_light(self, state):
        with self.lock:
            self.stop_button.visible = bool(state)

    def set_connected(self, state):
        with self.lock:
            self.signal.visible = bool(state)

    def get_floor(self):
        for i in range(4):
            if self.floors[i].y < self.elevator.center[1] < self.floors[i].y + self.floors[i].height:
                return i
        return -1

    def set_floor_indicator(self, floor):
        with self.lock:
            for i in range(4):
                if i == floor:
                    self.floors[i].opacity = 255
                else:
                    self.floors[i].opacity = 80

    def set_door_open_light(self, state):
        with self.lock:
            self.doors.visible = not bool(state)

    def set_order_light(self, order_type, floor, state):
        if order_type == 0:
            with self.lock:
                self.hall_up_orders[floor].opacity = 255 if state else 80
        elif order_type == 1:
            with self.lock:
                self.hall_down_orders[floor-1].opacity = 255 if state else 80
        elif order_type == 2:
            with self.lock:
                self.cab_orders[floor].opacity = 255 if state else 80

    def get_order(self, button_type, floor):
        return self.window.keys[self.order_keys[self.index][button_type][3-floor]]

def recv_on_port(parent, index, port):
    def serve(conn, addr):
        while parent.active:
            try:
                data = conn.recv(buf_size).strip()
                if not data:
                    break
                else:
                    if (data[0] == 1):
                        parent.set_motor_direction(data[1])
                    elif (data[0] == 2):
                        parent.set_order_light(data[1], data[2], data[3])
                    elif (data[0] == 3):
                        parent.set_floor_indicator(data[1])
                    elif (data[0] == 4):
                        parent.set_door_open_light(data[1])
                    elif (data[0] == 5):
                        parent.set_stop_button_light(data[1])
                    elif (data[0] == 6):
                        order_state = parent.get_order(data[1], data[2])
                        conn.send(bytes([6, order_state, 0, 0]))
                    elif (data[0] == 7):
                        floor = parent.get_floor()
                        if floor == -1:
                            conn.send(bytes([7, 0, 0, 0]))
                        else:
                            conn.send(bytes([7, 1, floor, 0]))
                    elif (data[0] == 8):
                        if parent.stopped():
                            conn.send(bytes([8, 1, 0, 0]))
                        else:
                            conn.send(bytes([8, 0, 0, 0]))
                    elif (data[0] == 9):
                        print("TODO: Implement obstruction")
                    else:
                        print("Unknown data received: {}".format(data[0]))

            except socket.timeout:
                continue
            except ConnectionResetError:
                print("Connection lost: " + str(addr))
                break

    localhost = '127.0.0.1'
    buf_size = 4

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(0.1)
    s.bind((localhost, port))
    s.listen(1)

    while parent.active:
        parent.set_connected(False)
        try:
            conn, addr = s.accept()
            conn.settimeout(0.1)
            print("New connection: " + str(addr))
            parent.set_connected(True)
            serve(conn, addr)
            conn.close()
        except socket.timeout:
            continue
        except e:
            print(str(e))

class Window(pyglet.window.Window):
    elevator_servers = []

    def __init__(self):
        super(Window, self).__init__(vsync = False, width=500, height=600)

        # self.keys will contain all currently pressed keys
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        pyglet.clock.schedule_interval(self.update, 1.0 / 60.0)
        pyglet.clock.set_fps_limit(60)

        self.background = pyglet.sprite.Sprite(Resources.background_img)

        for i in range(3):
            self.elevator_servers.append(ElevatorServer(i, 50+175*i, 50, self))

    def update(self, dt):
        for elev_serv in self.elevator_servers:
            elev_serv.update(dt)

    def on_draw(self):
        pyglet.clock.tick()
        self.clear()
        self.background.draw()
        for elev_serv in self.elevator_servers:
            elev_serv.batch.draw()
            elev_serv.doors.draw()
            elev_serv.stop_button.draw()

    def on_close(self):
        for elev_serv in self.elevator_servers:
            elev_serv.active = False
        self.close()

window = Window()
pyglet.app.run()
