# christmas_list.py
import os.path
import pickle

class ChristmasList:

    def __init__(self, filename):
        self.fname = filename
        if not os.path.isfile(self.fname):
            self.saveItems([])

    def loadItems(self):
        with open(self.fname, "rb") as f:
            items = pickle.load(f)
        return items

    def saveItems(self, items):
        with open(self.fname, "wb") as f:
            pickle.dump(items, f)

    def add(self, name):
        # each item is a dict: {"name": str, "purchased": bool}
        items = self.loadItems()
        items.append({"name": name, "purchased": False})
        self.saveItems(items)

    def check_off(self, name):
        items = self.loadItems()
        for item in items:
            if item["name"] == name:
                item["purchased"] = True
        self.saveItems(items)

    def remove(self, name):
        items = self.loadItems()
        items = [item for item in items if item["name"] != name]
        self.saveItems(items)

    def print_list(self):
        items = self.loadItems()
        for item in items:
            mark = "x" if item["purchased"] else "_"
            print(f"[{mark}] {item['name']}")
