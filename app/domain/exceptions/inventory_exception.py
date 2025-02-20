

class InventoryException(Exception):
    pass

class ZeroQuantityException(InventoryException):
    def __init__(self, message='Quantity must be greater than zero'):
        self.message = message
        super().__init__(message)


class InventoryOutOfStockException(InventoryException):
    def __init__(self, message='Not enough stock available'):
        self.message = message
        super().__init__(message)


class InventoryNotFoundException(InventoryException):
    def __init__(self, message="This inventory was not found please contact our customer service"):
        self.message = message
        super().__init__(self.message)