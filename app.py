import sys, pygame, random, time
import const, classes
from pygame.locals import *

class App(object):
    def __init__(self):
        print('app initialized')

        # state
        self.timeLastKeyPressed = 0
        self.timeBetweenKeyPresses = 200
        self.gravity = 500
        # ...

        self.score = 0
        self.level = 1

        self.well = classes.Well()
        self.currentShape = None
        self.nextShape = None
        self.shapeRotation = 0

        self.init()

    def init(self):
        pygame.init()
        pygame.key.set_repeat(200, 100)
        pygame.time.set_timer(const.MOVE_DOWN, self.gravity)

        self.screen = pygame.display.set_mode((const.SCR_W, const.SCR_H))
        self.font = pygame.font.Font('Blackout3plus1.otf', 30)

        self.addTiles()

        while True:
            for event in pygame.event.get():
                self.handleEvent(event)

            self.loop()
            self.render()

    def handleEvent(self, event):
        if event.type == QUIT:
            self.terminate()

        if event.type is const.MOVE_DOWN:
            # print('-------')
            # print('MOVE_DOWN')
            self.moveDown()


        if event.type is pygame.KEYDOWN:
            if event.key is pygame.K_q:
                self.terminate()
            # if event.key is pygame.K_LEFT:
            #     if self.getTime() > self.timeLastKeyPressed + self.timeBetweenKeyPresses:
            #         self.moveLeft()
            # if event.key is pygame.K_RIGHT:
            #     if self.getTime() > self.timeLastKeyPressed + self.timeBetweenKeyPresses:
            #         self.moveRight()
            # if event.key is pygame.K_SPACE:
            #     self.moveToBottom()

    def moveDown(self):
        # print('canMoveDown: ' + str(self.currentShape.canMoveDown(self.well)))
        if self.currentShape.canMoveDown(self.well):
            print('moving down from app')
            # print('moving down')
            self.currentShape.moveDown(self.well)

        self.well.printWell()


    def addTiles(self):
        print('adding tiles')
        row = 0
        while row < const.WELL_H:
            tiles = []
            col = 0
            while col < const.WELL_W:
                tile = classes.Tile(row, col)
                tiles.append(tile)
                col += 1
            self.well.addRowOfTiles(tiles)
            row += 1

    def loop(self):
        if not self.currentShape:
            self.spawnShape()

    def getShape(self):
        randomInt = random.randint(0, len(const.SHAPES) - 1)
        return classes.Shape(randomInt, const.SHAPES[randomInt])

    def spawnShape(self):
        if not self.nextShape:
            self.nextShape = self.getShape()

        self.currentShape = self.nextShape
        self.nextShape = self.getShape()

        self.addShapeToWell()

    def addShapeToWell(self):
        shape = self.currentShape
        tiles = shape.getTiles()
        t = 0
        while t < len(tiles):
            tile = tiles[t]
            if tile.getValue() is not 0:
                self.well.setTile(tile.getY(), tile.getX(), tile.getValue())
            # newTile = self.well.getTile(tile.getY(), tile.getX())
            t += 1
        print('added shape')
        self.well.printWell()
        print('^^^^^^^^^^^^^^^^^^')


    def render(self):
        self.screen.fill(const.C_BLACK)

        # draw scoreboard
        self.scoreboardText = self.font.render('Score: ' + str(self.score), 1, (255, 255, 255))
        rect = self.scoreboardText.get_rect()
        rect.bottomleft = (const.MARGIN_LEFT, 495)
        self.screen.blit(self.scoreboardText, rect)

        # draw level
        self.levelText = self.font.render('Level: ' + str(self.level), 1, (255, 255, 255))
        rect = self.levelText.get_rect()
        rect.bottomright = (const.SCR_W - const.MARGIN_LEFT, 495)
        self.screen.blit(self.levelText, rect)

        pygame.draw.rect(self.screen, const.C_LGRAY, (const.MARGIN_LEFT - 5, const.MARGIN_TOP - 5,
                                                  const.WELL_PX_W + 10, const.WELL_PX_H + 10))
        pygame.draw.rect(self.screen, const.C_DGRAY, (const.MARGIN_LEFT, const.MARGIN_TOP,
                                                  const.WELL_PX_W, const.WELL_PX_H))

        row = 0
        while row < const.WELL_H:
            # print('getting tile: ' + str(row))
            col = 0
            while col < const.WELL_W:
                currentTile = self.well.getTile(row, col)
                if currentTile.getValue() is not 0:
                    pygame.draw.rect(self.screen, const.C_LIST[currentTile.getValue()],
                                    (const.MARGIN_LEFT + col * const.BLOCK_SIZE,
                                    const.MARGIN_TOP + row * const.BLOCK_SIZE,
                                    const.BLOCK_SIZE, const.BLOCK_SIZE))
                col += 1
            row += 1

        pygame.display.flip()

    def terminate(error = 0):
        pygame.quit()
        sys.exit(error)

app = App()
