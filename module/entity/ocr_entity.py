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
        self.string = ""

    def is_except(self):
        print(self.string == self.except_result)
        return self.string == self.except_result

    def set_res(self, result):
        self.result = result
        self.string = result[0]["words"]
