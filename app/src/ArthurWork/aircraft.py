from ..ArthurWork.cabin_layout import CabinLayout

class Aircraft:

    def __init__(self, model, type, cabin):
        self.__model = model
        self.__type = type
        self.__cabin = [CabinLayout]

    def get_seat_layout(self):
        pass

    def get_all_seat(self):
        pass


    #getter
    def get_model(self):
        return self.__model