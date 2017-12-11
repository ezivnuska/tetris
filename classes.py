import const

class Shape(object):
    def __init__(self, type, tileList, posX = 4, posY = 0):
        self.type = type
        self.tileList = tileList
        self.posX = posX
        self.posY = posY
        self.rotation = 0

        self.createTilesFromData()

    def createTilesFromData(self):
        self.tiles = []
        # tileList: a list, containing rows in nested lists
        tileList = self.getTileList()
        row = 0
        # for each row in list
        while row < len(tileList):
            col = 0
            # for each column in row
            while col < len(tileList[row]):
                # add tile to tiles
                tile = Tile(self.posY + row, self.posX + col, tileList[row][col])
                self.tiles.append(tile)
                col += 1
            row += 1

    def getNextTileList(self, rotation):
        tiles = []
        # tileList: a list, containing rows in nested lists
        tileList = self.getTileListAtRotation(rotation)
        row = 0
        # for each row in list
        while row < len(tileList):
            col = 0
            # for each column in row
            while col < len(tileList[row]):
                # add tile to tiles
                tile = Tile(self.posY + row, self.posX + col, tileList[row][col])
                tiles.append(tile)
                col += 1
            row += 1
        return tiles

    def clearShapeTiles(self, well):
        tiles = self.getTiles()
        t = 0
        while t < len(tiles):
            tile = tiles[t]
            tileY = tile.getY()
            tileX = tile.getX()
            well.setTile(tileY, tileX, 0)
            t += 1


    def getHeight(self):
        return len(self.getTileList())

    def getWidth(self):
        return len(self.getTileList()[0])

    def getX(self):
        return self.posX

    def setX(self, posX):
        self.posX = posX

    def getY(self):
        return self.posY

    def setY(self, posY):
        self.posY = posY

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getTileList(self):
        return self.tileList[self.rotation]

    def getTileListAtRotation(self, rotation):
        return self.tileList[rotation]

    def getTiles(self):
        return self.tiles

    def getListOfTiles(self):
        list = []
        row = 0
        tiles = self.getTileList()
        while row < len(tiles):
            col = 0
            while col < len(tiles[row]):
                list.append(tiles[row][col])
                col += 1
            row += 1
        return list

    def setTile(self, row, col, newY, newX):
        tiles = self.getTiles()
        t = 0
        while t < len(tiles):
            tile = tiles[t]
            if tile.getY() is row and tile.getX() is col:
                tile.setY(newY)
                tile.setX(newX)
            t += 1

    def isAtBottom(self, well):
        if self.posY + self.getHeight() == const.WELL_H:
            return True
        return False

    def canMoveDown(self, well):
        if self.isAtBottom(well):
            return False
        tiles = self.getBottomTiles(well)
        t = 0
        while t < len(tiles):
            tile = tiles[t]
            if not tile.isEmpty() and not tile.tileBelowIsEmpty(well):
                print('cannot move down')
                return False
            t += 1

        return True

    def canMoveRight(self, well):
        tiles = self.getRightTiles(well)
        t = 0
        while t < len(tiles):
            tile = tiles[t]
            if not tile.isEmpty() and not tile.tileToRightIsEmpty(well):
                print('cannot move right')
                return False
            t += 1

        return True

    def canMoveLeft(self, well):
        tiles = self.getLeftTiles(well)
        t = 0
        while t < len(tiles):
            tile = tiles[t]
            if not tile.isEmpty() and not tile.tileToLeftIsEmpty(well):
                print('cannot move left')
                return False
            t += 1

        return True

    def getRightTiles(self, well):
        rightTiles =[]
        tileList = self.getTileList()
        checkedRows = []
        row = 0
        while row < len(tileList):
            col = len(tileList[row]) - 1
            while col >= 0:
                currentColumn = tileList[row][col]
                if currentColumn is not 0:
                    if col is len(tileList[row]) - 1:
                        rightTiles.append(well.getTile(self.posY + row, self.posX + col))
                        checkedRows.append(row)
                    elif row not in checkedRows:
                        rightTiles.append(well.getTile(self.posY + row, self.posX + col))
                        checkedRows.append(row)
                col -= 1
            row += 1
        return rightTiles

    def getLeftTiles(self, well):
        leftTiles =[]
        tileList = self.getTileList()
        checkedRows = []
        row = 0
        while row < len(tileList):
            currentRow = tileList[row]
            col =  0
            while col < len(tileList[row]):
                currentColumn = tileList[row][col]
                if currentColumn is not 0:
                    if col is 0:
                        leftTiles.append(well.getTile(self.posY + row, self.posX + col))
                        checkedRows.append(row)
                    elif row not in checkedRows:
                        leftTiles.append(well.getTile(self.posY + row, self.posX + col))
                        checkedRows.append(row)
                col += 1
            row += 1
        return leftTiles

    def getBottomTiles(self, well):
        bottomTiles = []
        tileList = self.getTileList()
        checkedColumns = []
        row = len(tileList) - 1
        while row >= 0:
            col = 0
            while col < len(tileList[row]):
                currentColumn = tileList[row][col]
                if currentColumn is not 0:
                    if row is len(tileList) - 1:
                        bottomTile = well.getTile(self.posY + row, self.posX + col)
                        bottomTiles.append(bottomTile)
                        checkedColumns.append(col)
                    elif col not in checkedColumns:
                        bottomTile = well.getTile(self.posY + row, self.posX + col)
                        bottomTiles.append(bottomTile)
                        checkedColumns.append(col)
                col += 1
            row -= 1
        return bottomTiles

    def getTopTiles(self, well):
        topTiles = []
        tileList = self.getTileList()
        checkedColumns = []
        row = 0
        while row < len(tileList):
            col = 0
            while col < len(tileList[row]):
                currentColumn = tileList[row][col]
                if currentColumn is not 0:
                    if row is 0:
                        topTiles.append(well.getTile(self.posY + row, self.posX + col))
                        checkedColumns.append(col)
                    elif col not in checkedColumns:
                        topTiles.append(well.getTile(self.posY + row, self.posX + col))
                        checkedColumns.append(col)
                col += 1
            row += 1
        return topTiles

    def getFilledTiles(self):
        filledTiles = []
        t = 0
        tiles = self.getTiles()
        while t < len(tiles):
            tile = tiles[t]
            if tile.getValue() is not 0:
                filledTiles.append(tile)
            t += 1
        return filledTiles

    def moveRight(self, well):
        print('MOVING RIGHT')
        tiles = self.getFilledTiles()
        t = len(tiles) - 1
        while t >= 0:
            tile = tiles[t]
            tileY = tile.getY()
            tileX = tile.getX()
            well.setTile(tileY, tileX + 1, tile.getValue())
            self.setTile(tileY, tileX, tileY, tileX + 1)
            well.setTile(tileY, tileX, 0)
            t -= 1

        leftTiles = self.getLeftTiles(well)
        lt = 0
        while lt < len(leftTiles):
            tile = leftTiles[lt]
            y = tile.getY()
            x = tile.getX()
            well.setTile(y, x, 0)
            lt += 1

        # if self.posX + self.getWidth() < const.WELL_W - 1:
        self.posX += 1

    def moveLeft(self, well):
        print('MOVING LEFT')
        tiles = self.getFilledTiles()
        t = 0
        while t < len(tiles):
            tile = tiles[t]
            tileY = tile.getY()
            tileX = tile.getX()
            well.setTile(tileY, tileX - 1, tile.getValue())
            self.setTile(tileY, tileX, tileY, tileX - 1)
            well.setTile(tileY, tileX, 0)
            t += 1

        rightTiles = self.getRightTiles(well)
        rt = 0
        while rt < len(rightTiles):
            tile = rightTiles[rt]
            y = tile.getY()
            x = tile.getX()
            well.setTile(y, x, 0)
            rt += 1

        if self.posX > 0:
            self.posX -= 1

    def moveDown(self, well):
        print('MOVING DOWN')
        # get list of tiles in shape
        tiles = self.getFilledTiles()
        topTiles = self.getTopTiles(well)
        t = len(tiles) - 1
        # for each tile
        while t >= 0:
            tile = tiles[t]
            tileY = tile.getY()
            tileX = tile.getX()
            well.setTile(tileY + 1, tileX, tile.getValue())
            self.setTile(tileY, tileX, tileY + 1, tileX)
            well.setTile(tileY, tileX, 0)
            t -= 1

        tt = 0
        while tt < len(topTiles):
            topTile = topTiles[tt]
            y = topTile.getY()
            x = topTile.getX()
            well.setTile(y, x, 0)
            tt += 1

        if self.posY < const.WELL_H - 1:
            self.posY += 1

    def getNextRotationRight(self):
        if len(self.tileList) is 1:
            return 0
        if self.rotation + 1 < len(self.tileList):
            return self.rotation + 1
        return 0

    def getNextRotationLeft(self):
        if len(self.tileList) is 1:
            return 0
        if self.rotation - 1 >= 0:
            return self.rotation - 1
        return len(self.tileList) - 1

    def getHeightAfterRotationRight(self):
        nextRotation = self.getNextRotationRight()
        return len(self.tileList[nextRotation])

    def getHeightAfterRotationLeft(self):
        nextRotation = self.getNextRotationLeft()
        return len(self.tileList[nextRotation])

    def getWidthAfterRotationRight(self):
        nextRotation = self.getNextRotationRight()
        return len(self.tileList[nextRotation][0])

    def getWidthAfterRotationLeft(self):
        nextRotation = self.getNextRotationLeft()
        return len(self.tileList[nextRotation][0])

    def canRotateRight(self, well):
        # check new position at right edge
        newWidth = self.getWidthAfterRotationRight()
        newHeight = self.getHeightAfterRotationRight()
        if self.posX + newWidth >= const.WELL_W:
            return False
        if self.posY + newHeight >= const.WELL_H:
            return False

        # check new position relative to other tiles
        tileListAtRotation = self.getNextTileList(self.getNextRotationRight())
        t = 0
        while t < len(tileListAtRotation):
            currentTile = tileListAtRotation[t]
            posY = currentTile.getY()
            posX = currentTile.getX()
            tile = well.getTile(posY, posX)
            if not self.tileIsInShape(posY, posX):
                tile = well.getTile(posY, posX)
                if tile.getValue() is not 0:
                    return False
            t += 1
        return True

    def canRotateLeft(self, well):
        # check new position at left edge
        newWidth = self.getWidthAfterRotationLeft()
        newHeight = self.getHeightAfterRotationLeft()
        if self.posX < 0:
            return False
        if self.posY + newHeight >= const.WELL_H:
            return False

        # check new position relative to other tiles
        tileListAtRotation = self.getNextTileList(self.getNextRotationLeft())
        row = 0
        while row < len(tileListAtRotation):
            col = 0
            while col < len(tileListAtRotation[row]):
                posY = row
                posX = col
                if not self.tileIsInShape(posY, posX):
                    tile = well.getTile(posY, posX)
                    if tile.getValue() is not 0:
                        return False
                col += 1
            row += 1
        return True

    def rotateRight(self, well):
        if not self.canRotateRight(well):
            return None
        self.clearShapeTiles(well)
        self.rotation = self.getNextRotationRight()
        self.createTilesFromData()
        self.updateShape(well)

    def rotateLeft(self, well):
        if not self.canRotateLeft(well):
            return None
        self.clearShapeTiles(well)
        self.rotation = self.getNextRotationLeft()
        self.createTilesFromData()
        self.updateShape(well)

    def updateShape(self, well):
        tiles = self.getTiles()
        t = 0
        while t < len(tiles):
            tile = tiles[t]
            well.setTile(tile.getY(), tile.getX(), 0)
            if not tile.isEmpty():
                well.setTile(tile.getY(), tile.getX(), tile.getValue())
            t += 1

    def tileIsInShape(self, posY, posX):
        inShape = False
        tiles = self.getTiles()
        t = 0
        while t < len(tiles):
            tile = tiles[t]
            tileY = tile.getY()
            tileX = tile.getX()
            if tileY == posY and tileX == posX:
                inShape = True
            t += 1
        return inShape

class Tile(object):
    def __init__(self, posY, posX, value = 0):
        self.posY = posY
        self.posX = posX
        self.value = value

    def getY(self):
        return self.posY

    def setY(self, posY):
        self.posY = posY

    def getX(self):
        return self.posX

    def setX(self, posX):
        self.posX = posX

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def isEmpty(self):
        return self.value is 0

    def tileToRightIsEmpty(self, well):
        rowInWell = well.getRowOfTilesByIndex(self.posY)
        if self.tileIsFlushRight(well):
            return False
        nextTileInRow = rowInWell[self.posX + 1]
        return nextTileInRow.getValue() is 0

    def tileToLeftIsEmpty(self, well):
        rowInWell = well.getRowOfTilesByIndex(self.posY)
        if self.tileIsFlushLeft(well):
            return False
        previousTileInRow = rowInWell[self.posX - 1]
        return previousTileInRow.getValue() is 0

    def tileBelowIsEmpty(self, well):
        rowInWell = well.getRowOfTilesByIndex(self.posY)
        if self.tileIsAtBottom(well):
            return False
        nextRowInWell = well.getRowOfTilesByIndex(self.posY + 1)
        tileInRow = well.getRowOfTilesByIndex(self.posY)[self.posX]
        tileInNextRow = nextRowInWell[self.posX]
        return tileInNextRow.getValue() is 0

    def tileAboveIsEmpty(self, well):
        rowInWell = well.getRowOfTilesByIndex(self.posY)
        rowAboveInWell = well.getRowOfTilesByIndex(self.posY - 1)
        tileInRow = rowAboveInWell[self.posX]
        # print('checking tile above: ' + str(tileInRow.getValue()))
        return tileInRow is 0

    def tileIsFlushLeft(self, well):
        return self.posX is 0

    def tileIsFlushRight(self, well):
        lastColumn = well.getColumns() - 1
        return self.posX is lastColumn

    def tileIsAtBottom(self, well):
        lastRow = well.getRows() - 1
        return self.posY is lastRow

class Well(object):
    def __init__(self):
        self.rows = []
        self.shape = None

    def getFilledRows(self):
        rows = []
        row = 0
        while row < len(self.rows):
            if self.isRowFilled(row):
                rows.append(self.rows[row])
            row += 1
        return rows

    def getRowPosY(self, rowOfTiles):
        firstTile = rowOfTiles[0]
        return firstTile.getY()

    def removeFilledRows(self):
        filledRows = self.getFilledRows()
        if len(filledRows) > 0:
            row = len(filledRows) - 1
            while row >= 0:
                col = 0
                while col < len(filledRows[row]):
                    tile = filledRows[row][col]
                    tileY = tile.getY()
                    tileX = tile.getX()
                    self.setTile(tileY, tileX, 0)
                    col += 1
                row -= 1

        self.dropRows()

    def swapRow(self, topIndex, bottomIndex):
        topRow = self.getRowOfTilesByIndex(topIndex)
        bottomRow = self.getRowOfTilesByIndex(bottomIndex)
        self.assignNewYPositionToRow(topIndex, bottomIndex)
        self.assignNewYPositionToRow(bottomIndex, topIndex)
        self.rows[bottomIndex] = topRow
        self.rows[topIndex] = bottomRow

    def assignNewYPositionToRow(self, oldY, newY):
        oldRow = self.getRowOfTilesByIndex(oldY)
        col = 0
        while col < len(oldRow):
            currentTile = oldRow[col]
            currentTile.setY(newY)
            col += 1

    def isRowFilled(self, rowIndex):
        row = self.getRowOfTilesByIndex(rowIndex)
        col = 0
        while col < len(row):
            if row[col].getValue() is 0:
                return False
            col += 1
        return True

    def isRowEmpty(self, rowIndex):
        row = self.getRowOfTilesByIndex(rowIndex)
        rowIsEmpty = True
        col = 0
        while col < len(row):
            if row[col].getValue() is not 0:
                rowIsEmpty = False
            col += 1
        return rowIsEmpty

    def getLowestEmptyRowIndex(self):
        row = 0
        emptyRow = 0
        while row < const.WELL_H:
            if self.isRowEmpty(row):
                emptyRow = row
            else:
                return emptyRow
            row += 1
        return const.WELL_H - 1

    def getEmptyRowsBelow(self, rowIndex):
        emptyRows = []
        if rowIndex is const.WELL_H - 1:
            return emptyRows
        row = rowIndex
        while row < const.WELL_H:
            if self.isRowEmpty(row):
                emptyRows.append(row)
            row += 1
        return emptyRows

    def moveRow(self, rowIndex, newRowIndex):
        rowToMove = self.rows[rowIndex][:]
        self.rows = self.rows[:rowIndex] + self.rows[rowIndex + 1:]
        self.rows = self.rows[:newRowIndex] + [rowToMove] + self.rows[newRowIndex:]
        row = rowIndex
        while row < const.WELL_H:
            currentRow = self.getRowOfTilesByIndex(row)
            currentPosY = self.getRowPosY(currentRow)
            if currentPosY is not row:
                self.assignNewYPositionToRow(row, row)
            row += 1

    def dropRows(self):
        rowIndex = const.WELL_H - 1
        lowestEmptyRowIndex = self.getLowestEmptyRowIndex()
        while rowIndex > lowestEmptyRowIndex:
            emptyRows = self.getEmptyRowsBelow(rowIndex)
            # if row is not empty and cleared rows below
            if not self.isRowEmpty(rowIndex) and len(emptyRows) > 0:
                self.moveRow(rowIndex, rowIndex + len(emptyRows))
            rowIndex -= 1

    def addRowOfTiles(self, rowOfTiles):
        self.rows.append(rowOfTiles)

    def getRowOfTilesByIndex(self, index):
        return self.rows[index]

    def getTile(self, row, col):
        if row > const.WELL_H - 1:
            print('fail: ' + str(row))
        return self.rows[row][col]

    def setTile(self, row, col, value):
        tileAtRow = self.rows[row]
        tile = tileAtRow[col]
        tile.setValue(value)

    def clearTilesAtIndex(self, index):
        rowOfTiles = self.rows[index]
        tile = 0
        while tile < len(rowOfTiles):
            rowOfTiles[tile].value = 0
            tile += 1

    def getRows(self):
        return len(self.rows)

    def getColumns(self):
        return len(self.rows[0])

    def printWell(self):
        print('-----------------')
        row = 0
        while row < self.getRows():
            rowOfTiles = self.getRowOfTilesByIndex(row)
            col = 0
            currentRow = []
            while col < len(rowOfTiles):
                tile = rowOfTiles[col]
                # print('tile y: ' + str(tile.getY()) + ' and x: ' + str(tile.getX()) + ': ' + str(tile.getValue()))
                currentRow.append(tile.getValue())
                col += 1
            print(currentRow)
            row += 1

        print('-----------------')
