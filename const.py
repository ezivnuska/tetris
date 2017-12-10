# -*- coding: utf-8 -*-
import pygame

SCR_W = 300
SCR_H = 500

WELL_W = 10
WELL_H = 20

BLOCK_SIZE = 20
WELL_PX_W = WELL_W * BLOCK_SIZE
WELL_PX_H = WELL_H * BLOCK_SIZE

MARGIN_LEFT = 50
MARGIN_TOP  = 50

C_BLACK = (  0,   0,   0)
C_DGRAY = ( 20,  20,  20)
C_LGRAY = (125, 125, 125)
C_WHITE = (255, 255, 255)

C_CYAN   = (  0, 255, 255)
C_BLUE   = (  0,   0, 255)
C_ORANGE = (255, 128,   0)
C_YELLOW = (255, 255,   0)
C_GREEN  = (  0, 255,   0)
C_PURPLE = (200,   0, 200)
C_RED    = (255,   0,   0)

C_LIST = [C_BLACK,
          C_CYAN,
          C_BLUE,
          C_ORANGE,
          C_YELLOW,
          C_GREEN,
          C_PURPLE,
          C_RED,]

MOVE_DOWN = pygame.USEREVENT + 1

SHAPES = [
    [
        [
            [1, 1],
            [1, 1]
        ]
    ],
    [
        [
            [2, 2, 2],
            [2, 0, 0]
        ],
        [
            [2, 2],
            [0, 2],
            [0, 2]
        ],
        [
            [0, 0, 2],
            [2, 2, 2]
        ],
        [
            [2, 0],
            [2, 0],
            [2, 2]
        ]
    ],
    [
        [
            [3, 3],
            [3, 0],
            [3, 0]
        ],
        [
            [3, 3, 3],
            [0, 0, 3]
        ],
        [
            [0, 3],
            [0, 3],
            [3, 3]
        ],
        [
            [3, 0, 0],
            [3, 3, 3]
        ]
    ],
    [
        [
            [4, 0],
            [4, 4],
            [0, 4]
        ],
        [
            [0, 4, 4],
            [4, 4, 0]
        ]
    ],
    [
        [
            [0, 5],
            [5, 5],
            [5, 0]
        ],
        [
            [5, 5, 0],
            [0, 5, 5]
        ]
    ],
    [
        [
            [6, 6, 6, 6]
        ],
        [
            [6],
            [6],
            [6],
            [6]
        ]
    ],
    [
        [
            [3, 3, 3],
            [0, 3, 0]
        ],
        [
            [0, 3],
            [3, 3],
            [0, 3]
        ],
        [
            [0, 3, 0],
            [3, 3, 3]
        ],
        [
            [3, 0],
            [3, 3],
            [3, 0]
        ]
    ]
]
