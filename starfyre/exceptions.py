"""
The exceptions module defines custom exception classes used in the application.

Classes:
    - UnknownTagError: An exception raised when encountering an unknown tag during parsing.
    - InitFyreMissingError: An exception raised when the '__init__.fyre' file is missing.
    - IndexFileConflictError: An exception raised when there is an 'index.fyre' file in the pages folder.

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

class InitFyreMissingError(Exception):
    """
    Exception raised when the '__init__.fyre' file is missing.
    """
    def __init__(self, message="Error: '__init__.fyre' file is missing."):
        super().__init__(message)

class IndexFileConflictError(Exception):
    """Exception raised when there is an 'index.fyre' file in the pages folder.

    This exception is raised when the router encounters an 'index.fyre' file
    in the specified pages directory. Such a file is not allowed, as it would
    conflict with the generation of the main 'index.html' file that is produced
    from the transpilation of the '__init__.fyre' file.

    Using 'index.fyre' in the pages folder would result in an ambiguity between
    the manually provided 'index.fyre' and the automatically generated 'index.html'.

    Attributes:
        message (str): A description of the error.
    """

    def __init__(self, message="'index.fyre' is not allowed as it conflicts with 'index.html' generation. Please rename the file to avoid this conflict."):
        super().__init__(message)


