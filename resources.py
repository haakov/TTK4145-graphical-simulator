import pyglet
from pyglet.window import key

class Resources():
    elevator_img = pyglet.image.load("img/elevator.png")
    doors_img = pyglet.image.load("img/doors.png")
    stop_img = pyglet.image.load("img/stop.png")
    signal_img = pyglet.image.load("img/signal.png")
    arrow_img = pyglet.image.load("img/arrow.png")
    arrow_down_img = pyglet.image.load("img/arrow_down.png")
    background_img = pyglet.image.load("img/background.png")

    floor_imgs = [ pyglet.image.load("img/floor_%d.png" % i) for i in range(0,4) ]

    cab_order_imgs = [ pyglet.image.load("img/%d.png" % i) for i in range(0,4) ]

    f_button_imgs = [ pyglet.image.load("img/f%d.png" % i) for i in range(1,4) ]

    reset_keys = [ key.F1, key.F2, key.F3 ]

    order_keys   = [
                    # Elevator 1
                    [[ None, key.Q, key.A, key.Z        ],  # Hall up
                     [ key._2, key.W, key.S, None       ],  # Hall down
                     [ key._3, key.E, key.D, key.C      ]], # Cab

                    # Elevator 2
                    [[ None, key.R, key.F, key.V        ],
                     [ key._5, key.T, key.G, None       ],
                     [ key._6, key.Y, key.H, key.N      ]],

                    # Elevator 3
                    [[ None, key.U, key.J, key.M        ],
                     [ key._8, key.I, key.K, None       ],
                     [ key._9, key.O, key.L, key.PERIOD ]]
                    ]

