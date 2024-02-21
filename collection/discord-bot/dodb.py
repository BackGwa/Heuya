from datetime import datetime as dt

class Dodb:
    def __init__(self, name, path, data_format):
        self.name = name
        self.path = path
        self.data_format = data_format
        self.session = 0

    def file_register(self):
        """
        새로운 데이터셋 파일을 생성합니다. (데이터셋 인덱스 값이 증가됩니다.)
        """
        try:
            self.session += 1
            new_path = self.path + f"/{self.name}_{self.gen_now()[1]}_{self.session}.csv"
            file = open(new_path, encoding="UTF-8", mode="w")

            for i in range(len(self.data_format)):
                if (len(self.data_format) - 1) == i:
                    file.write(self.data_format[i])
                else:
                    file.write(self.data_format[i] + ",")

            file.close()

            return new_path
        except Exception as e:
            self.runtime_error("새로운 파일을 등록하는 과정에서 오류가 발생했습니다.", e)
            return -1

    def register(self, path, data):
        """
        데이터셋에 데이터를 추가합니다.
        """
        file = open(path, encoding="UTF-8", mode="a")
        file.write("\n")

        for i in range(len(self.data_format)):
                if (len(self.data_format) - 1) == i:
                    file.write(str(data[i]))
                else:
                    file.write(str(data[i]) + ",")

        file.close()

    def gen_now(self):
        """
        현재 날짜와 시간을 반환합니다.
        """
        now = dt.now()
        return [now, now.strftime("%Y%m%d%H%M%S")]

    def runtime_error(self, title, message):
        """
        에러를 출력합니다.
        """
        print("\n\033[1m\033[31m[DoDB : RuntimeError]\033[0m")
        print(f"\033[1m{title}\n> \033[0m\033[31m{message}\033[0m")

    def log(self, title, message):
        """
        로그를 출력합니다.
        """
        print(f"\n\033[1m{title}\n> \033[0m\033[36m{message}\033[0m")