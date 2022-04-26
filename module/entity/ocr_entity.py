class OcrEntity:
    def __init__(self, except_result="", input_img=None, x1=0, y1=0, x2=1280, y2=720, cand_alphabet=None):
        self.input_img = input_img
        self.except_result = except_result
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.cand_alphabet = cand_alphabet
        self.result = ""

    def is_except(self):
        return self.result == self.except_result
