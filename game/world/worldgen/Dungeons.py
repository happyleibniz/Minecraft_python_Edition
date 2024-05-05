import random


class WorldGenDungeons:  # some translated mc gen dungeons thingy
    def generate(self, world, random, i, j, k):
        byte0 = 3
        l = random.randint(0, 1) + 2
        i1 = random.randint(0, 1) + 2
        j1 = 0

        for l1 in range(i - l - 1, i + l + 2):
            for k2 in range(j - 1, j + byte0 + 2):
                for k3 in range(k - i1 - 1, k + i1 + 2):
                    material = world.getBlockMaterial(l1, k2, k3)
                    if k2 == j - 1 and not material.func_878_a():
                        return False
                    if k2 == j + byte0 + 1 and not material.func_878_a():
                        return False
                    if (
                            l1 == i - l - 1 or l1 == i + l + 1 or k3 == k - i1 - 1 or k3 == k + i1 + 1) and k2 == j and world.getBlockId(
                            l1, k2, k3) == 0 and world.getBlockId(l1, k2 + 1, k3) == 0:
                        j1 += 1

        if 1 <= j1 <= 5:
            for l1 in range(i - l - 1, i + l + 2):
                for k2 in range(j + byte0, j - 2, -1):
                    for k3 in range(k - i1 - 1, k + i1 + 2):
                        if (
                                l1 != i - l - 1 and k2 != j - 1 and k3 != k - i1 - 1 and l1 != i + l + 1 and k2 != j + byte0 + 1 and k3 != k + i1 + 1):
                            world.setBlockWithNotify(l1, k2, k3, 0)
                        elif k2 >= 0 and not world.getBlockMaterial(l1, k2 - 1, k3).func_878_a():
                            world.setBlockWithNotify(l1, k2, k3, 0)
                        elif world.getBlockMaterial(l1, k2, k3).func_878_a():
                            if k2 == j - 1 and random.randint(0, 3) != 0:
                                world.setBlockWithNotify(l1, k2, k3, Block.cobblestoneMossy.blockID_00)
                            else:
                                world.setBlockWithNotify(l1, k2, k3, Block.cobblestone.blockID_00)

            for _ in range(2):
                for _ in range(3):
                    k3 = i + random.randint(-l, l)
                    i4 = k + random.randint(-i1, i1)
                    if world.getBlockId(k3, j, i4) == 0:
                        j4 = 0
                        if world.getBlockMaterial(k3 - 1, j, i4).func_878_a():
                            j4 += 1
                        if world.getBlockMaterial(k3 + 1, j, i4).func_878_a():
                            j4 += 1
                        if world.getBlockMaterial(k3, j, i4 - 1).func_878_a():
                            j4 += 1
                        if world.getBlockMaterial(k3, j, i4 + 1).func_878_a():
                            j4 += 1
                        if j4 == 1:
                            world.setBlockWithNotify(k3, j, i4, Block.crate.blockID_00)
                            tileentitychest = world.func_603_b(k3, j, i4)
                            k4 = 0
                            while k4 < 8:
                                itemstack = self.func_530_a(random)
                                if itemstack is not None:
                                    tileentitychest.setInventorySlotContents(
                                        random.randint(0, tileentitychest.getSizeInventory() - 1), itemstack)
                                k4 += 1

            world.setBlockWithNotify(i, j, k, Block.mobSpawner.blockID_00)
            tileentitymobspawner = world.func_603_b(i, j, k)
            tileentitymobspawner.entityID = self.func_531_b(random)
            return True
        else:
            return False

    def func_530_a(self, random):
        i = random.randint(0, 10)
        if i == 0:
            return ItemStack(Item.saddle)
        elif i == 1:
            return ItemStack(Item.ingotIron, random.randint(1, 4))
        elif i == 2:
            return ItemStack(Item.bread)
        elif i == 3:
            return ItemStack(Item.wheat, random.randint(1, 4))
        elif i == 4:
            return ItemStack(Item.gunpowder, random.randint(1, 4))
        elif i == 5:
            return ItemStack(Item.silk, random.randint(1, 4))
        elif i == 6:
            return ItemStack(Item.bucketEmpty)
        elif i == 7 and random.randint(0, 99) == 0:
            return ItemStack(Item.appleGold)
        elif i == 8 and random.randint(0, 1) == 0:
            return ItemStack(Item.redstone, random.randint(1, 4))
        elif i == 9 and random.randint(0, 9) == 0:
            return ItemStack(Item.itemsList[Item.record13.swiftedIndex + random.randint(0, 1)])
        else:
            return None

    def func_531_b(self, random):
        i = random.randint(0, 3)
        if i == 0:
            return "Skeleton"
        elif i == 1 or i == 2:
            return "Zombie"
        elif i == 3:
            return "Spider"
        else:
            return ""
