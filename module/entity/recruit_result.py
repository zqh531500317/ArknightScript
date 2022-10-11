class RecruitResult:
    def __init__(self):
        self.times = 0
        self.star4 = 0
        self.star5or6 = 0
        self.starlessthan4 = 0

    def add(self, star):
        self.times += 0
        if star == 6:
            self.star5or6 += 1
        elif star == 5:
            self.star5or6 += 1
        elif star == 4:
            self.star4 += 1
        elif star <= 3:
            self.starlessthan4 += 1

    def get_res(self):
        return "公招次数:{},三星及以下:{},四星:{},五星六星:{}".format(self.times, self.starlessthan4,
                                                       self.star4, self.star5or6)


recruit_result = RecruitResult()


def init():
    global recruit_result
    recruit_result = RecruitResult()
