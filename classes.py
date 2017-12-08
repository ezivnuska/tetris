import const

class Shape(object):
    def __init__(self, type, tileList, posX = 4, posY = 0):
        self.type = type
        self.tileList = tileList
        self.posX = posX
        self.posY = posY
        self.rotation = 0

        self.startY = 0
        self.startX = 4

        self.tiles = []
        self.createTilesFromData()

    def createTilesFromData(self):
        # tileList: a list, containing rows in nested lists
        tileList = self.getTileList()
        row = 0
        # for each row in list
        while row < len(tileList):
            col = 0
            # for each column in row
            while col < len(tileList[row]):
                # add tile to tiles
                tile = Tile(self.startY + row, self.startX + col, tileList[row][col])
                self.tiles.append(tile)
                col += 1
            row += 1

    def updateTiles(self):
        # tiles must be updated after shape rotation
        tileList = self.getTiles()
        updatedTiles = []
        row = 0
        # for each row in
        while row < len(tileList):
            col = 0
            # for each column in row
            while col < len(tileList[row]):
                updatedTiles.append(Tile(row, col, type))
                col += 1
            row += 1
        self.tiles = updatedTiles

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

    def canMoveDown(self, well):
        tiles = self.getBottomTiles(well)
        # print('canMoveDown tile: ' + str(tiles))
        # for i in tiles:
        #     print('bottomTiles at y: ' + str(i.getY()) + ' and x: ' + str(i.getX()))
        t = 0
        while t < len(tiles):
            tile = tiles[t]
            # if tile is not empty and tile below is vacant
            # print('tile is empty: ' + str(tile.isEmpty()) + ' y: ' + str(tile.getY()) + ' x: ' + str(tile.getX()))
            # print('tile below is empty: ' + str(tile.tileBelowIsEmpty(well)) + ' y: ' + str(tile.getY()) + ' x: ' + str(tile.getX()) + ' value: ' + str(tile.getValue()))
            if not tile.isEmpty() and not tile.tileBelowIsEmpty(well):
                print('cannot move down')
                return False
            t += 1

        return True

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
                    # print('get tile called from getBottomTiles')
                    if row is len(tileList) - 1:
                        # print('bottomTile y:' + str(self.posY + row) + ' and x: ' + str(self.posX + col))
                        bottomTiles.append(well.getTile(self.posY + row, self.posX + col))
                        checkedColumns.append(col)
                    elif col not in checkedColumns:
                        # print('bottomTile y:' + str(self.posY + row) + ' and x: ' + str(self.posX + col))
                        bottomTiles.append(well.getTile(self.posY + row, self.posX + col))
                        checkedColumns.append(col)
                col += 1
            # print('tileBelowIsEmpty: ' + str(tile.tileBelowIsEmpty(well)))
            # if tile.tileBelowIsEmpty(well):
            #     bottomTiles.append(tile)
            row -= 1
        # print(str(len(bottomTiles)) + ' bottomTiles')
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
                    # print('get tile called from getTopTiles')
                    if row is 0:
                        # print('topTile y:' + str(self.posY + row) + ' and x: ' + str(self.posX + col))
                        topTiles.append(well.getTile(self.posY + row, self.posX + col))
                        checkedColumns.append(col)
                    elif col not in checkedColumns:
                        # print('topTile y:' + str(self.posY + row) + ' and x: ' + str(self.posX + col))
                        topTiles.append(well.getTile(self.posY + row, self.posX + col))
                        checkedColumns.append(col)
                col += 1
            row += 1
        # print(str(len(topTiles)) + ' topTiles')
        return topTiles

    def getFilledTiles(self):
        filledTiles = []
        t = 0
        tiles = self.getTiles()[:]
        while t < len(tiles):
            tile = tiles[t]
            if tile.getValue() is not 0:
                filledTiles.append(tile)
            t += 1
        # print('getFilledTiles():' + str(len(filledTiles)))
        return filledTiles

    def moveDown(self, well):
        print('MOVING DOWN ')
        # get list of tiles in shape
        tiles = self.getFilledTiles()
        topTiles = self.getTopTiles(well)
        # print('topTiles: ' + str(len(topTiles)))
        # print('number of tiles to move: ' + str(len(tiles)))
        t = len(tiles) - 1
        # for each tile
        while t >= 0:
            tile = tiles[t]
            tileY = tile.getY()
            tileX = tile.getX()
            # print('moving tile at y: ' + str(tile.getY()) + ' and x: ' + str(tile.getX()))
            # print('setTile from shape.moveDown: ' + str(tileY + 1))
            well.setTile(tileY + 1, tileX, tile.getValue())
            self.setTile(tileY, tileX, tileY + 1, tileX)
            well.setTile(tileY, tileX, 0)
            t -= 1

        tt = 0
        while tt < len(topTiles):
            topTile = topTiles[tt]
            y = topTile.getY()
            x = topTile.getX()
            # print('resetting topTile at y:' + str(x) + ' and x: ' + str(y))
            print('...setting top tile...' + str(y) + ', ' + str(x))
            well.setTile(y, x, 0)
            tt += 1

        if self.posY < const.WELL_H - 1:
            self.posY += 1

        # well.printWell()

    def rotateRight(self):
        if len(self.tiles) is 0:
            return
        if self.rotation + 1 < len(self.tiles):
            self.rotation += 1
        else: self.rotation = 0
        self.updateTiles()

    def rotateLeft(self):
        if len(self.tiles) is 0:
            return
        if self.rotation - 1 >= 0:
            self.rotation -= 1
        else: self.rotation = len(self.tiles) - 1
        self.updateTiles()

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
        tileInRow = rowInWell[self.posX + 1]
        return tileInRow is 0

    def tileToLeftIsEmpty(self, well):
        rowInWell = well.getRowOfTilesByIndex(self.posY)
        tileInRow = rowInWell[self.posX - 1]
        return tileInRow is 0

    def tileBelowIsEmpty(self, well):
        rowInWell = well.getRowOfTilesByIndex(self.posY)
        if self.tileIsAtBottom(well):
            return False
        nextRowInWell = well.getRowOfTilesByIndex(self.posY + 1)
        tileInRow = rowInWell[self.posX]
        tileInNextRow = nextRowInWell[self.posX]
        # print('tileInNextRow y: ' + str(tileInNextRow.getY()) + ' x: ' + str(tileInNextRow.getX()) + ' :' + str(tileInNextRow.getValue()))
        # print('checking tile below: ' + ' y: ' + str(tileInRow.getY()) + ' x: ' + str(tileInRow.getX()) + ': ' + str(tileInNextRow.getValue()))
        return tileInNextRow.getValue() is 0

    def tileAboveIsEmpty(self, well):
        rowInWell = well.getRowOfTilesByIndex(self.posY)
        rowAboveInWell = well.getRowOfTilesByIndex(self.posY - 1)
        tileInRow = rowAboveInWell[self.posX]
        # print('checking tile above: ' + str(tileInRow.getValue()))
        return tileInRow is 0

    def tileIsFlushLeft(self):
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

    def addRowOfTiles(self, rowOfTiles):
        self.rows.append(rowOfTiles)

    def getRowOfTilesByIndex(self, index):
        return self.rows[index]

    def getTile(self, row, col):
        # print('getting tile at y: ' + str(row) + ', x: ' + str(col))
        if row > const.WELL_H - 1:
            print('fail: ' + str(row))
        return self.rows[row][col]

    def setTile(self, row, col, value):
        tileAtRow = self.rows[row]
        if value is 0:
            print('WELL::setting tile to 0 at: row: ' + str(row) + ', col: ' + str(col) + ', val: ' + str(value))
        else: print('WELL::setting tile at: row: ' + str(row) + ', col: ' + str(col) + ', val: ' + str(value))
        col = tileAtRow[col]
        col.setValue(value)

    def clearTilesAtIndex(self, index):
        rowOfTiles = self.rows[index]
        tile = 0
        while tile < len(rowOfTiles):
            rowOfTiles[tile].value = 0
            tile += 1

    def getRows(self):
        return len(self.rows)

    def getColumns(self):
        return len(self.rows[0].tiles)

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
