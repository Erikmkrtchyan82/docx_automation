class Nums:
    @staticmethod
    def ones(num):
        return {
            "0": "",
            "1": "մեկ",
            "2": "երկու",
            "3": "երեք",
            "4": "չորս",
            "5": "հինգ",
            "6": "վեց",
            "7": "յոթ",
            "8": "ութ",
            "9": "ինը",
        }[num]

    @staticmethod
    def tens(num):
        return {
            "0": "",
            "1": "տասն",
            "2": "քսան",
            "3": "երեսուն",
            "4": "քառասուն",
            "5": "հիսուն",
            "6": "վաթսուն",
            "7": "յոթանասուն",
            "8": "ութսուն",
            "9": "իննսուն"
        }[num]

    @staticmethod
    def hundreds(num):
        return "" if num == "" else "հարյուր"

    @staticmethod
    def thousands(num):
        return "" if num == "" else "հազար"

    @staticmethod
    def milions(num):
        if num == "" or num == '000':
            return ""
        if len(num) == 1 and num[0] == "1":
            return "մեկ միլիոն"
        return "միլիոն"

    @staticmethod
    def bilions(num):
        if num == "" or num == '000':
            return ""
        if len(num) == 1 and num[0] == "1":
            return "մեկ միլիարդ"
        return "միլիարդ"

    @staticmethod
    def get_dec(num: str):
        if len(num) > 3:
            return "**?"

        res = []
        if len(num) == 3:
            if num[0] not in "01":
                res.append(Nums.ones(num[0]))
            if num[0] != "0":
                res.append(Nums.hundreds(num[0]))
            num = num[1:]

        if len(num) == 2:
            if num[0] != 0:
                if num[0] == "1" and num[1] == "0":
                    res.append(Nums.tens(num[0])[:-1])
                else:
                    res.append(Nums.tens(num[0]))
            num = num[1:]

        if len(num) == 1:
            res.append(Nums.ones(num))

        return " ".join([r for r in res if r])

    @staticmethod
    def empty(num):
        return ""

    @staticmethod
    def construct(num):
        num = round(float(num))
        if num is not str:
            num = str(num)

        if num == "1":
            return Nums.get_dec(num)

        num = num.replace('.', '').replace(',', '').replace(' ', '')
        num = split_num(num)
        result = []

        for i, (num_chunk, multiply) in enumerate(zip(num, [Nums.empty, Nums.thousands, Nums.milions, Nums.bilions])):
            dec = Nums.get_dec(num_chunk)
            if dec or i > 1:
                result.append(multiply(num_chunk))
                if num_chunk != "1":
                    result.append(dec)

        result = list(filter(lambda k: k, result))
        return " ".join(result[::-1])


def split_num(num: str):
    num_copy = num[::-1]
    num_copy = [num_copy[i:i + 3] for i in range(0, len(num_copy), 3)]
    return [x[::-1] for x in num_copy]
