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
        return "" if num == "" else "միլիոն"

    @staticmethod
    def bilions(num):
        return "" if num == "" else "միլիարդ"

    @staticmethod
    def _get_dec(num):
        if len(num) != 2:
            return ""
        # 12,000
        # 03,555
        # 40,555
        # 00,579
        if num[0] == num[1] == "0":
            return ""
        if num[0] == "0":
            return Nums.ones(num[1])
        if num[0] == "1" and num[1] == "0":
            return Nums.tens(num[0])[:-1]+Nums.ones(num[1])
        return Nums.tens(num[0])+Nums.ones(num[1])

    @staticmethod
    def empty(num):
        return ""

    def construct(num: any) -> str:
        num = round(float(num))
        if num is not str:
            num = str(num)

        num = num.replace('.', '').replace(',', '').replace(' ', '')
        result = []
        i = 0
        x = [Nums.empty, Nums.thousands, Nums.milions, Nums.bilions]
        while len(num) > 2:
            length = len(num)
            number = num[length - 3:]
            result.append(x[i](number[0]))

            result.append(Nums._get_dec(number[1:]))
            if number[0] != "0":
                result.append(Nums.hundreds(number[0]))
            if number[0] != "1":
                result.append(Nums.ones(number[0]))

            i += 1
            num = num[:length - 3]

        if len(num) != 0:
            result.append(x[i](num[0]))
            if len(num) == 1 and num[0] != '1':
                result.append(Nums.ones(num[0]))
            else:
                result.append(Nums._get_dec(num))

        result = list(filter(lambda k: k, result))
        return " ".join(result[::-1])
