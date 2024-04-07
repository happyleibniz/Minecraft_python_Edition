def getCraftingItem(objects, tableType=False , numbers = None):
    if numbers is None:
        print("Warning: not provided a numbers")
    else:
        numbers = numbers
    item = ["wood", 0]
    print(objects)
    if tableType:  # 3x3
        pass
    else:  # 2x2
        if "['log_oak', '', '', '']" == str(objects):
            return ["planks_oak",numbers[0]]
        else:
            pass

        if "['planks_oak', 'planks_oak', 'planks_oak', 'planks_oak']" == str(objects):
            print("crafting table! lets go!")
            return ["crafting_table",numbers[0]]
        else:
            pass

    return item
