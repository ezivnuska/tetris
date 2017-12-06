#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, pygame, random, time
from pygame.locals import *
import const

class GameState:
    def __init__(self):
        self.init_well()
        self.score = 0
        self.level = 1
        self.gravity = 400
        self.curr_piece = None
        self.next_piece = None
        self.piece_state = 0

    def init_well(self):
        self.well = []
        for y in range(const.WELL_H):
            row = []
            for x in range(const.WELL_W):
                row.append(0)
            self.well.append(row)

    def get_new_piece(self):
        # print('number of shapes: ' + str(len(const.SHAPES)))
        randomInt = random.randint(0, len(const.SHAPES) - 1)
        self.current_piece_color = randomInt
        # print('randomInt: ' + str(randomInt))
        newPiece = const.SHAPES[randomInt]
        # print('newPiece:', str(newPiece))
        return newPiece
        # return [[random.choice(range(1,8))]]

    def spawn_piece(self):
        if self.next_piece == None:
            self.next_piece = self.get_new_piece()

        self.curr_piece = self.next_piece
        self.next_piece = self.get_new_piece()

        # print('curr_piece:', self.curr_piece)
        # print('curr_piece.width:', self.getPieceWidth())
        # print('next_piece:', self.next_piece)

        self.piece_x = 4
        self.piece_y = 0

        self.addPieceToWell()

    def addPieceToWell(self):
        piece = self.curr_piece[self.piece_state]
        posX = self.piece_x
        posY = self.piece_y
        width = len(piece[0])
        height = len(piece)
        well = self.well

        wellRowStartIndex = posY
        wellRowEndIndex = posY + height
        wellColStartIndex = posX
        wellColEndIndex = posX + width

        pieceRowIndex = 0
        wellRowIndex = wellRowStartIndex

        while wellRowIndex < wellRowEndIndex:
            currentWellRow = well[wellRowIndex][:]
            # print('currentWellRow:' + str(currentWellRow))
            # print('wellRowIndex:' + str(wellRowIndex))
            # print('wellRowEndIndex:' + str(wellRowEndIndex))
            well[wellRowIndex] = currentWellRow[:wellColStartIndex] + piece[pieceRowIndex] + currentWellRow[wellColEndIndex:]

            wellRowIndex += 1
            pieceRowIndex += 1

        self.printWell()

    def pieceUnderneath(self):
        piece = self.curr_piece[self.piece_state]
        pieceY = self.piece_y
        pieceHeight = len(piece)
        if pieceY + pieceHeight == const.WELL_H:
            return True
        else: return False

    def moveDown(self):
        well = self.well
        piece = self.curr_piece[self.piece_state][:]
        pieceY = self.piece_y
        pieceHeight = len(piece)
        pieceX = self.piece_x
        pieceWidth = len(piece[0])
        startX = pieceX
        endX = pieceX + pieceWidth

        # start with bottom row first
        row = pieceY + pieceHeight - 1
        while row >= pieceY:

            currentRow = well[row][:]

            if row + 1 >= const.WELL_H:
                self.spawn_piece()
                return
            nextRow = well[row + 1][:]

            newRow = []

            col = 0
            while col < const.WELL_W:
                currentPiece = currentRow[col]
                nextPiece = nextRow[col]
                # if moving piece down
                if currentPiece is not 0 and nextPiece is 0:
                    newRow.append(currentPiece)
                # if piece below blank space
                elif currentPiece is 0 and nextPiece is not 0:
                    newRow.append(nextPiece)
                elif currentPiece is 0 and nextPiece is 0:
                    newRow.append(0)
                else:
                    self.spawn_piece()
                    return
                col += 1

            if len(newRow) == 10:
                well[row] = [0 for x in range(0, 10)]
                well[row + 1] = newRow
            else:
                self.spawn_piece()
                return

            self.printWell()

            row -= 1

        self.piece_y += 1

    def rowEmpty(self, row):
        empty = True
        currentRow = self.well[row]
        col = 0
        while col < len(currentRow):
            if currentRow[col] is not 0:
                empty = False
        return empty

    def movePiecesDown(self):
        well = self.well
        row = 0
        # for each row in well
        while row < const.WELL_H - 1:
            col = 0
            # for each column in row
            while col < const.WELL_W - 1:
                currentBlockValue = well[row][col]
                # print('currentBlockValue: ' + str(currentBlockValue))
                if not self.blockInCurrentPiece(row, col) and currentBlockValue is not 0:
                    # if current block is filled
                    # print('block in current piece: ' + str(self.blockInCurrentPiece(row, col)))
                    # if block is not in current piece and block below is empty
                    if well[row + 1][col] == 0:
                        well[row][col] = 0
                        well[row + 1][col] = currentBlockValue
                col += 1
            row += 1

    def blockInCurrentPiece(self, row, col):
        isCurrentPiece = False
        if row >= self.piece_y and row <= self.piece_y + self.getCurrentPieceWidth():
            isCurrentPiece = True
        if col >= self.piece_x and col <= self.piece_x + self.getCurrentPieceHeight():
            isCurrentPiece = True
        return isCurrentPiece

    def getCurrentPieceHeight(self):
        return len(self.curr_piece[self.piece_state])

    def getCurrentPieceWidth(self):
        return len(self.curr_piece[self.piece_state][0])

    def pieceCanMove(self):

        movable = True

        piece = self.curr_piece[self.piece_state]
        posX = self.piece_x
        posY = self.piece_y
        width = len(piece[0])
        height = len(piece)
        well = self.well

        wellRowEndIndex = posY + height
        wellColStartIndex = posX
        wellColEndIndex = posX + width

        # if piece will move beyond bottom of screen
        if wellRowEndIndex == const.WELL_H:
            return False

        col = wellColStartIndex
        while col < wellColEndIndex:
            currentBlock = well[wellRowEndIndex][col]
            if currentBlock is not 0:
                print('currentBlock: ' + str(currentBlock))
                nextBlock = well[wellRowEndIndex + 1][col]
                print('nextBlock: ' + str(nextBlock))
                if nextBlock is not 0:
                    movable = False
            col += 1
        return movable

    def printWell(self):
        y = 0
        print('--------------------')
        while y < len(self.well):
            print(self.well[y])
            y += 1
        print('--------------------')

class App:
    def __init__(self):
        self.timeKeyPressed = 0
        self.keyInterval = 1000

        self.init()

    def terminate(error=0):
        pygame.quit()
        sys.exit(error)

    def init(self):
        pygame.init()
        self.displaysurf = pygame.display.set_mode((const.SCR_W, const.SCR_H))
        self.game_state = GameState()

        # set font
        self.font = pygame.font.Font('Blackout3plus1.otf', 30)

        # set key repeat time: delay, interval
        pygame.key.set_repeat(200, 100)

        # set gravity
        pygame.time.set_timer(const.MOVE_DOWN, self.game_state.gravity)

        while True:
            for event in pygame.event.get():
                self.handleEvent(event)

            # Game Logic
            if self.getCurrentPiece() == None:
                self.game_state.spawn_piece()

            # Display
            self.draw_screen()

    def handleEvent(self, event):
        if event.type == QUIT:
            self.terminate()

        if event.type == const.MOVE_DOWN:
            self.game_state.moveDown()

        if event.type == pygame.KEYDOWN:
            # press 'q' to quit
            if event.key == pygame.K_q:
                self.terminate()
            # if event.key == pygame.K_LEFT:
            #     if self.getTime() > self.timeKeyPressed + self.keyInterval:
            #         self.movePieceLeft()
            # if event.key == pygame.K_RIGHT:
            #     if self.getTime() > self.timeKeyPressed + self.keyInterval:
            #         self.movePieceRight()
            # if event.key == pygame.K_SPACE:
            #     self.movePieceToBottom()

    def savePiece(self):
        posX = self.getPieceX()
        posY = self.getPieceY()
        width = self.getPieceWidth()
        height = self.getPieceHeight()
        well = self.getWell()
        piece = self.getCurrentPieceState()

        startRow = posY
        endRow = posY + height
        startCol = posX
        endCol = posX + width

        rowInPiece = 0
        rowInWell = startRow
        while rowInWell < endRow:
            well[rowInWell] = [well[rowInWell][:startCol] + piece[rowInPiece] + well[rowInWell][endCol:]]
            rowInWell += 1
        # well = self.getWell()
        # pieceY = self.getPieceY()
        # pieceX = self.getPieceX()
        # currentPiece = self.getCurrentPieceState()
        # print('currentPiece: ' + str(currentPiece))
        # print('pieceX: ' + str(pieceX))
        # print('pieceY: ' + str(pieceY))
        # rowInPiece = 0
        # # for each row in piece
        # while rowInPiece < len(currentPiece[rowInPiece]):
        #     currentRowOfPiece = currentPiece[rowInPiece]
        #     print('current row of piece: ' + str(currentRowOfPiece))
        #     print(well)
        #     colInPiece = 0
        #     # for each column in piece row
        #     while colInPiece < len(currentRowOfPiece):
        #         currentColumn = currentRowOfPiece[colInPiece]
        #         well[pieceY + rowInPiece][pieceX + colInPiece] = currentPiece[colInPiece][rowInPiece]
        #         colInPiece += 1
        #     rowInPiece += 1

        print(well)
        # self.getWell()[self.getPieceY()][self.getPieceX()] = self.getCurrentPiece()[0][0]
        self.checkForLines()
        self.game_state.spawn_piece()

    # def movePieceDown(self):
    #     posX = self.getPieceX()
    #     posY = self.getPieceY()
    #     width = self.getPieceWidth()
    #     height = self.getPieceHeight()
    #     well = self.getWell()
    #     piece = self.getCurrentPieceState()
    #
    #     startRow = posY
    #     endRow = posY + height
    #     startCol = posX
    #     endCol = posX + width
    #
    #     rowInPiece = 0
    #     rowInWell = startRow
    #     while rowInWell < endRow:
    #         well[rowInWell] = well[rowInWell][:startCol] + piece[rowInPiece] + well[rowInWell][endCol:]
        # pieceHeight = self.getCurrentPieceState
        # posX = self.getPieceX()
        # posY = self.getPieceY()
        # newPosY = self.getPieceY() + 1
        # if posY < const.WELL_H - 1 and self.getWell()[newPosY][posX] == 0:
        #     self.incrementY()
        # else:
        #     self.savePiece()

    def movePieceLeft(self):
        if self.getPieceX() > 0:
            self.decrementX()

    def movePieceRight(self):
        if self.getPieceX() + self.getPieceWidth() < const.WELL_W - 1:
            self.incrementX()

    def movePieceToBottom(self):
        col = self.getPieceX()
        while self.getPieceY() < const.WELL_H - 1 and self.getWell()[self.getPieceY() + 1][col] == 0:
            self.incrementY()

    def getTime(self):
        return int(round(time.time() * 1000))

    def checkForLines(self):
        completedLines = []
        for line in range(0, len(self.getWell())):
            print(self.getWell()[line])

            # if all spaces filled
            if not 0 in self.getWell()[line]:
                print('COMPLETE:', line)
                completedLines.append(line)

        if len(completedLines) > 0:
            self.handleCompletedLines(completedLines)

    def handleCompletedLines(self, completedLines):
        print('***** lines completed ******')
        for completedLine in completedLines:
            print('line ' + str(completedLine) + ' completed')
            print(str(self.getWell()[completedLine]) + ' completed')

            # remove completed lines (set each space in line to 0)
            for row in range(0, len(self.getWell()[completedLine])):
                self.getWell()[completedLine][row] = 0

        # move all other blocks down one line for each line removed
        for l in range(len(self.getWell()), 0, -1):
            line = l - 1
            print('moving incomplete lines down...')
            print('** ' + str(line) + ' **')
            if line not in completedLines:
                print('line ' + str(line) + ' is not completed, moving down')
                print(self.getWell()[line])
                for row in range(0, len(self.getWell()[line])):
                    print('moving row ' + str(row) + ' of line ' + str(line))

                    if self.getWell()[line + 1][row] == 0:
                        # save row state
                        rowState = self.getWell()[line][row]
                        # set row state to zero
                        self.getWell()[line][row] = 0
                        # set row state in next line
                        self.getWell()[line + 1][row] = rowState

        self.updateScore(len(completedLines))
        self.speedUp()

    def updateScore(self, numPoints):
        self.game_state.score += numPoints

    def speedUp(self):
        if self.game_state.gravity > 50:
            self.game_state.gravity -= 50
            pygame.time.set_timer(const.MOVE_DOWN, self.game_state.gravity)

    def draw_screen(self):
        self.displaysurf.fill(const.C_BLACK)

        # draw scoreboard
        self.scoreboardText = self.font.render('Score: ' + str(self.game_state.score), 1, (255, 255, 255))
        rect = self.scoreboardText.get_rect()
        rect.bottomleft = (const.MARGIN_LEFT, 495)
        self.displaysurf.blit(self.scoreboardText, rect)

        # draw level
        self.levelText = self.font.render('Level: ' + str(self.game_state.level), 1, (255, 255, 255))
        rect = self.levelText.get_rect()
        rect.bottomright = (const.SCR_W - const.MARGIN_LEFT, 495)
        self.displaysurf.blit(self.levelText, rect)

        # Draw well (with border)
        pygame.draw.rect(self.displaysurf, const.C_LGRAY, (const.MARGIN_LEFT - 5, const.MARGIN_TOP - 5,
                                                  const.WELL_PX_W + 10, const.WELL_PX_H + 10))
        pygame.draw.rect(self.displaysurf, const.C_DGRAY, (const.MARGIN_LEFT, const.MARGIN_TOP,
                                                  const.WELL_PX_W, const.WELL_PX_H))

        # Draw blocks:
        y = 0
        while y < const.WELL_H:
            x = 0
            while x < const.WELL_W:
                curr = self.getWell()[y][x]
                #   print(curr)
                if curr != 0:
                    pygame.draw.rect(self.displaysurf, const.C_LIST[curr],
                            (const.MARGIN_LEFT + x * const.BLOCK_SIZE,
                             const.MARGIN_TOP + y * const.BLOCK_SIZE,
                             const.BLOCK_SIZE, const.BLOCK_SIZE))
                x += 1
            y += 1

        curr_left = const.MARGIN_LEFT + (self.getPieceX() * const.BLOCK_SIZE)
        curr_top = const.MARGIN_TOP + (self.getPieceY() * const.BLOCK_SIZE)
        curr_color = const.C_LIST[curr]

        pygame.draw.rect(self.displaysurf, curr_color,
            (curr_left, curr_top, const.BLOCK_SIZE, const.BLOCK_SIZE))

        pygame.display.flip()

    def getCurrentPiece(self):
        return self.game_state.curr_piece

    def getCurrentPieceState(self):
        return self.game_state.curr_piece[self.game_state.piece_state]

    def getPieceState(self):
        return self.game_state.piece_state

    def getPieceWidth(self):
        currentPiece = self.getCurrentPieceState()
        return len(currentPiece[0])

    def getPieceHeight(self):
        currentPiece = self.getCurrentPieceState()
        return len(currentPiece)

    def rotateRight(self):
        pass

    def rotateLeft(self):
        pass

    def getWell(self):
        return self.game_state.well

    def getPieceY(self):
        return self.game_state.piece_y

    def incrementY(self):
        self.game_state.piece_y += 1

    def getPieceX(self):
        return self.game_state.piece_x

    def decrementX(self):
        self.game_state.piece_x -= 1

    def incrementX(self):
        self.game_state.piece_x += 1

app = App()
