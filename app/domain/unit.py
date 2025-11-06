class Unit:
    def __init__(self, id: int, name: str, symbol: str):
        self.id = id
        self.name = name
        self.symbol = symbol

    def rename(self, new_name: str):
        if not new_name or len(new_name) < 1:
            raise ValueError("Unit name can not be empty")
        self.name = new_name

    def change_symbol(self, new_symbol: str):
        if not new_symbol or len(new_symbol) < 1:
            raise ValueError("Unit symbol can not be empty")
        self.symbol = new_symbol
