import sys, pygame, random, time
import const, classes
from pygame.locals import *

class App(object):
    def __init__(self):
        print('app initialized')

        # state
        self.timeLastKeyPressed = 0
        self.timeBetweenKeyPresses = 200
        self.lastSpeed = 500
        self.speed = 500
        # ...

        self.score = 0
        self.level = 1

        self.well = classes.Well()
        self.shape = None
        self.nextShape = None
        self.shapeRotation = 0

        self.showRules = False
        self.gameOver = False

        self.init()

    def init(self):
        pygame.init()
        pygame.key.set_repeat(200, 100)

        self.setSpeed(self.speed)

        self.screen = pygame.display.set_mode((const.SCR_W, const.SCR_H))
        self.font = pygame.font.Font('Blackout3plus1.otf', 30)

        self.addTiles()

        while True:
            for event in pygame.event.get():
                self.handleEvent(event)

            self.loop()
            self.render()

    def getTime(self):
        return int(round(time.time() * 1000))

    def handleEvent(self, event):
        if event.type == QUIT:
            self.terminate()

        if event.type is const.MOVE_DOWN:
            self.moveDown()

        if event.type == pygame.KEYDOWN:

            # Quit
            if event.key == pygame.K_q:
                self.terminate()
            # Move left
            if event.key == pygame.K_LEFT:
                if self.getTime() > self.timeLastKeyPressed + self.timeBetweenKeyPresses:
                    self.moveLeft()
            # Move right
            if event.key == pygame.K_RIGHT:
                if self.getTime() > self.timeLastKeyPressed + self.timeBetweenKeyPresses:
                    self.moveRight()
            # Move to bottom
            if event.key is pygame.K_SPACE:
                if self.gameOver is True:
                    self.resetGame()
                    self.gameOver = False
                else:
                    self.moveToBottom()
            # Rotate right
            if event.key == pygame.K_UP:
                if self.getTime() > self.timeLastKeyPressed + self.timeBetweenKeyPresses:
                    self.rotateRight()
            # Rotate left
            if event.key == pygame.K_DOWN:
                if self.getTime() > self.timeLastKeyPressed + self.timeBetweenKeyPresses:
                    self.rotateLeft()
            # Reduce speed (for development)
            if event.key == pygame.K_COMMA:
                if self.getTime() > self.timeLastKeyPressed + self.timeBetweenKeyPresses:
                    self.reduceSpeed()
            # Increase speed (for development)
            if event.key == pygame.K_PERIOD:
                if self.getTime() > self.timeLastKeyPressed + self.timeBetweenKeyPresses:
                    self.increaseSpeed()
            # Pause / Resume (for development)
            if event.key == pygame.K_p:
                if self.getTime() > self.timeLastKeyPressed + self.timeBetweenKeyPresses:
                    if self.speed is not 0:
                        self.pause()
                    else:
                        self.resume()
            if event.key == pygame.K_r:
                if self.getTime() > self.timeLastKeyPressed + self.timeBetweenKeyPresses:
                    self.toggleRules()

    def endGame(self):
        self.pause()
        self.gameOver = True

    def setSpeed(self, speed):
        self.lastSpeed = self.speed
        self.speed = speed
        pygame.time.set_timer(const.MOVE_DOWN, self.speed)

    def reduceSpeed(self):
        newSpeed = self.speed + 50
        self.setSpeed(newSpeed)

    def increaseSpeed(self):
        newSpeed = self.speed - 50
        if newSpeed < 50: newSpeed = 50
        self.setSpeed(newSpeed)

    def pause(self):
        self.setSpeed(0)

    def resume(self):
        self.setSpeed(self.lastSpeed)

    def moveToBottom(self):
        while self.shape.canMoveDown(self.well):
            self.moveDown()

    def moveDown(self):
        if self.shape.canMoveDown(self.well):
            self.shape.moveDown(self.well)
        else:
            if self.shape.getY() is 0:
                self.endGame()
            lastShape = self.shape
            self.shape = None
            numberOfFilledRows = len(self.well.getFilledRows())
            if numberOfFilledRows > 0:
                self.score += numberOfFilledRows
                self.well.removeFilledRows()

        self.well.printWell()

    def moveRight(self):
        if self.shape.canMoveRight(self.well):
            self.shape.moveRight(self.well)

        self.well.printWell()

    def moveLeft(self):
        if self.shape.canMoveLeft(self.well):
            self.shape.moveLeft(self.well)

        self.well.printWell()

    def rotateRight(self):
        self.shape.rotateRight(self.well)

    def rotateLeft(self):
        self.shape.rotateLeft(self.well)

    def resetGame(self):
        self.score = 0
        self.level = 1
        self.clearTiles()
        self.resume()

    def clearTiles(self):
        row = 0
        while row < const.WELL_H:
            col = 0
            while col < const.WELL_W:
                tile = self.well.setTile(row, col, 0)
                col += 1
            row += 1

    def addTiles(self):
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
        if not self.shape:
            self.spawnShape()

    def getShape(self):
        randomInt = random.randint(0, len(const.SHAPES) - 1)
        return classes.Shape(randomInt, const.SHAPES[randomInt])

    def spawnShape(self):
        if not self.nextShape:
            self.nextShape = self.getShape()

        self.shape = self.nextShape
        self.nextShape = self.getShape()

        self.addShapeToWell()

    def addShapeToWell(self):
        shape = self.shape
        tiles = shape.getTiles()
        t = 0
        while t < len(tiles):
            tile = tiles[t]
            if tile.getValue() is not 0:
                self.well.setTile(tile.getY(), tile.getX(), tile.getValue())
            t += 1

        self.well.printWell()

    def toggleRules(self):
        self.showRules = not self.showRules
        if self.showRules is True:
            self.pause()
        else:
            self.resume()

    def drawRules(self):
        posY = 50
        margin = 10
        r = 0
        while r < len(const.RULES):
            rule = const.RULES[r]
            ruleText = self.font.render(rule, 1, (255, 255, 255))
            rect = ruleText.get_rect()
            rect.centerx = self.screen.get_rect().centerx
            rect.centery = posY
            self.screen.blit(ruleText, rect)
            lineHeight = self.font.get_linesize() + margin
            posY += lineHeight
            r += 1

    def drawGameOver(self):
        gameOverText = self.font.render('Game Over', 1, (255, 255, 255))
        rect = gameOverText.get_rect()
        rect.centerx = self.screen.get_rect().centerx
        rect.centery = self.screen.get_rect().centery
        self.screen.blit(gameOverText, rect)

    def render(self):
        self.screen.fill(const.C_BLACK)

        if self.gameOver is True:
            self.drawGameOver()
        elif self.showRules is True:
            self.drawRules()
        else:
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
                col = 0
                while col < const.WELL_W:
                    currentTile = self.well.getTile(row, col)
                    if currentTile.getValue() is not 0:
                        # draw tile border
                        pygame.draw.rect(self.screen, (255, 255, 255),
                                        (const.MARGIN_LEFT + col * const.BLOCK_SIZE,
                                        const.MARGIN_TOP + row * const.BLOCK_SIZE,
                                        const.BLOCK_SIZE, const.BLOCK_SIZE))
                        # draw tile fill
                        pygame.draw.rect(self.screen, const.C_LIST[currentTile.getValue()],
                                        (const.MARGIN_LEFT + col * const.BLOCK_SIZE + 1,
                                        const.MARGIN_TOP + row * const.BLOCK_SIZE + 1,
                                        const.BLOCK_SIZE - 2, const.BLOCK_SIZE - 2))
                    col += 1
                row += 1

        pygame.display.flip()

    def terminate(error = 0):
        pygame.quit()
        sys.exit(error)

app = App()
