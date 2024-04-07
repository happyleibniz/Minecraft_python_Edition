from game.GUI.ModalWindow import ModalWindow
from settings import *
import pyglet

class CraftingTable:
    def __init__(self, plClass, blClass,glClass):
        # TODO: do crafting table
        self.draggingItem = []
        self.inventory = {}
        self.blocksLabel = {}
        self.pc = plClass
        self.bc = blClass
        self.gl = self.pc.gl
        
        self.window = ModalWindow(self.gl)
        self.window.setWindow(self.gl.gui.GUI_TEXTURES["crafting_table"])
        self.window.clickEvent = self.windowClickEvent
        self.window.updateFunctions.append(self.update)
        self.window.cellPositions = {0: [(20, 34), None], 1: [(96, 34), None], 2: [(132, 34), None],
                                     3: [(60, 70), None], 4: [(96, 70), None], 5: [(132, 70), None],
                                     6: [(60, 106), None], 7: [(96, 106), None], 8: [(132, 106), None],
                                     9: [(240, 62, 48, 48), None]}

        x = 16
        for i in range(9):
            self.window.cellPositions[i] = [(x, 284), None]
            x += 36

        x, y = 196, 36
        self.window.cellPositions[37] = [(x, y), None]
        x += 36
        self.window.cellPositions[38] = [(x, y), None]
        x = 196
        y += 36
        self.window.cellPositions[39] = [(x, y), None]
        x += 36
        self.window.cellPositions[40] = [(x, y), None]

        self.window.cellPositions[41] = [(308, 56), None]  # TODO: crafting table in inventory

        x, y = 16, 168
        for i in range(9 * 3, 0, -1):
            self.window.cellPositions[9 + i] = [(x, y), None]

            x += 36
            if x > 304:
                x = 16
                y += 36
        for i in range(9 * 5 + 1):
            self.inventory[i] = ["sand", 0]
            self.blocksLabel[i] = pyglet.text.Label("0",
                                                    font_name='Minecraft Rus',
                                                    color=(255, 255, 255, 255),
                                                    font_size=10,
                                                    x=self.gl.WIDTH // 2, y=60)
        self.inventory = plClass.inventory.get_inventory_blocks()
        print(self.inventory)
        self.window.show()

    def windowClickEvent(self, button, cell):
        print("thanks")
        if button[0]:
            print("yes!")
            if self.draggingItem:
                print("ooooooo")
                if self.inventory[cell][1] == 0:
                    print("soga")
                    self.inventory[cell] = self.draggingItem
                    self.draggingItem = []
                else:
                    print("huhuhuh")
                    safe = [self.inventory[cell][0], self.inventory[cell][1]]
                    print(safe)
                    print(self.draggingItem)
                    print(self.inventory)
                    self.inventory[cell] = self.draggingItem
                    self.draggingItem = safe
            else:
                print("you")
                if self.inventory[cell][1] != 0:
                    self.draggingItem = [self.inventory[cell][0], self.inventory[cell][1]]
                    self.inventory[cell][1] = 0
        if button[2]:
            print("huh")
            if self.draggingItem:
                print("yee")
                if self.inventory[cell][0] == self.draggingItem[0] and self.draggingItem[1]:
                    self.inventory[cell][1] += 1
                    self.draggingItem[1] -= 1
                elif self.inventory[cell][1] == 0 and self.draggingItem[1]:
                    self.inventory[cell][0] = self.draggingItem[0]
                    self.inventory[cell][1] += 1
                    self.draggingItem[1] -= 1

    def update(self, win, mousePos):
        by = 117
        for i in self.window.cellPositions.items():
            if i[0] <= 9:
                continue
            bid = 41 - i[0]
            xx, yy = self.window.cellPositions[bid + 1][0][0], self.window.cellPositions[bid + 10][0][1]

            self.window.cellPositions[bid + 9][1] = self.gl.player.inventory.inventory[bid]
            inv = self.gl.player.inventory.inventory[bid]

            if inv[1] == 0 or inv[0] == 0:
                continue
            self.gl.inventory_textures[inv[0]].blit((self.gl.WIDTH // 2 - (win.width // 2)) + xx + 5,
                                                    (self.gl.HEIGHT // 2 + (win.height // 2)) - yy + by - 27)
            if by == 117 and bid % 9 == 0:
                by -= 9
            if bid % 9 == 0:
                by -= 72
            if by == -108:
                by -= 9
