"""
The exceptions module defines custom exception classes used in the application.

Classes:
    - UnknownTagError: An exception raised when encountering an unknown tag during parsing.

"""

class UnknownTagError(Exception):
   """Exception raised when an unknown tag is encountered during parsing.

   This exception is raised when the parser encounters a tag that is not recognized as
   a generic HTML tag or a custom component. It indicates that the tag is unknown and
   cannot be processed correctly.

   Attributes:
        message (str): A description of the error.
   """
   pass