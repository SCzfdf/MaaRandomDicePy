red_stone = 1


class RDContext:
    @staticmethod
    def set_red_stone_location(location: int):
        global red_stone
        red_stone = location

    @staticmethod
    def get_red_stone_location() -> int:
        global red_stone
        return red_stone
