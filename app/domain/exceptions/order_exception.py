

class OrderException(Exception):
    pass

class InvalidOrderStatusException(OrderException):
    def __init__(self, message='Invalid order status'):
        self.message = message
        super().__init__(self.message)

class OrderNotFoundException(OrderException):
    def __init__(self, message="This order was not found please contact our customer service"):
        self.message = message
        super().__init__(self.message)