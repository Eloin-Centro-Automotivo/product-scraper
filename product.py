class Product:
    def __init__(self, code=None, description=None, image=None, application=None,
                 is_registered_vip=None, price=None):
        self.code = code
        self.description = description
        self.image = image
        self.application = application
        self.is_registered_vip = is_registered_vip,
        self.price = price

    def __repr__(self) -> str:
        return (f"Product(code={self.code!r}, price={self.price!r}, "
                f"description={self.description!r}, image={self.image!r}, "
                f"application={self.application!r}, "
                f"is_registered_vip={self.is_registered_vip!r})")
