class Dice:
    roi_x: int
    roi_y: int
    roi_w: int = 70
    roi_h: int = 70
    index: int
    type: str

    def __init__(self, roi_x, roi_y, index):
        self.roi_x = roi_x
        self.roi_y = roi_y
        self.index = index
        self.type = "*"
