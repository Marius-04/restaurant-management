class Order:
    def __init__(self):
        self._items = []

    def add_item(self, item):
        self._items.append(item)

    def calculate_total(self):
        return sum(item.price for item in self._items)

    def show_order(self):
        for item in self._items:
            print(item.get_details())
        print(f"Total: {self.calculate_total()}$")
