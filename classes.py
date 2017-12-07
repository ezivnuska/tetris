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
        tiles = self.getTiles()
        while row < len(tiles):
            col = 0
            while col < len(tiles[row]):
                list.append(tiles[row][col])
                col += 1
            row += 1
        return list

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

    def tileToRightIsEmpty(self, well):
        rowInWell = well[self.posY]
        tileInRow = rowInWell[self.posX + 1]
        return tileInRow is 0

    def tileToLeftIsEmpty(self, well):
        rowInWell = well[self.posY]
        tileInRow = rowInWell[self.posX - 1]
        return tileInRow is 0

    def tileBelowIsEmpty(self, well):
        rowInWell = well[self.posY + 1]
        tileInRow = rowInWell[self.posX]
        return tileInRow is 0

    def tileIsFlushLeft(self):
        return self.posX is 0

    def tileIsFlushRight(self, well):
        lastColumn = len(well[0])
        return self.posX is lastColumn

    def tileIsAtBottom(self, well):
        lastRow = len(well)
        return self.posY is lastRow

class RowOfTiles(object):
    def __init__(self, tiles):
        self.tiles = tiles

    def getTiles(self):
        return self.tiles

    def getTile(self, col):
        return self.tiles[col]

    def rowIsFilled(self):
        tile = 0
        while tile < len(tiles):
            if tiles[tile] is 0:
                return False
            tile += 1
        return True

    def printTiles(self):
        tiles = []
        t = 0
        while t < len(self.tiles):
            tiles.append(self.getTile(t).getValue())
            t += 1
        print(tiles)

class Well(object):
    def __init__(self):
        self.rows = []
        self.shape = None

    def addRowOfTiles(self, rowOfTiles):
        self.rows.append(rowOfTiles)

    def getRowOfTilesByIndex(self, index):
        return self.rows[index]

    def getTile(self, row, col):
        return self.rows[row][col]

    def setTile(self, row, col, value):
        row = self.rows[row]
        col = row[col]
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
                currentRow.append(tile.getValue())
                col += 1
            print(currentRow)
            row += 1

        print('-----------------')
