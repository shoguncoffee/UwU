class Seat:

    def __init__(self, row, column, type, passenger, description):
        self.__row = row
        self.__column = column
        self.__type = type
        self.__passenger = []
        self.__description = description