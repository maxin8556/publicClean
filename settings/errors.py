



class CustomException(Exception):
   """Base class for other exceptions"""
   pass

class PackageNotFoundError(CustomException):
   """Raised when the input value is too small"""
   pass

# class PackageNotFoundError(CustomException):
#    """Raised when the input value is too large"""
#    pass
