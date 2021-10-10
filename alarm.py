import common
import re
import esi


class Alarm:
    ts: int
    speaker: str = 'EVE系统'
    solar_system: str = None
    solar_system_id: int = None
    route: list = None
    msg: str

    def __init__(self, txt: str, location: str = None) -> None:
        result = re.search(
            r'\[ (\d{4}.\d{2}.\d{2} \d{2}:\d{2}:\d{2}) \] (.*?) > (.*)', txt)
        if result:
            self.ts = common.str_to_ts(result.group(1))
            self.speaker = result.group(2)
            self.msg = result.group(3)

            # 读取星系星系
            for solar_system in esi.get_solar_system_name_list():
                if self.msg.find(solar_system) > -1:
                    self.solar_system = solar_system
                    self.solar_system_id = esi.get_solar_system_id(
                        solar_system)

                    # 计算距离
                    if location:
                        self.update_location(location)
                    break

    def __str__(self) -> str:
        time_str = common.ts_to_str_format(self.ts)
        s = f'{time_str} [{self.speaker}]\t{self.solar_system}'
        d = self.distance()
        if d < 0:
            return s
        elif d == 0:
            return f'{s}\t 杀到本地了'
        else:
            return f'{s}\t{self.distance()}跳 入口 {self.enter()}'

    @property
    def dt(self) -> int:
        return common.cal_dt(self.ts)

    def update_location(self, location: str):
        self.route = esi.cal_route(location, self.solar_system)
        return self.route

    def distance(self, location: str = None):
        if location:
            self.update_location(location)

        if self.route is None:
            return -1
        else:
            return len(self.route)-1

    def enter(self, location: str = None) -> str:
        if location:
            self.update_location(location)

        if self.distance() == 0:
            return location
        else:
            return esi.get_solar_system_name(self.route[1])


if __name__ == '__main__':
    a = Alarm('[ 2021.09.26 11:36:35 ] 欧阳疯锋 > R-P7KL  阡陌默', 'ZK-YQ3')
    print(a)
    print(a.route)
    print(a.distance())
    print(a.enter())
    a.update_location('I1-BE8')
    print(a)
    print(a.route)
    print(a.distance())
    print(a.enter())
