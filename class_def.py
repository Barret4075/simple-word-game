from enum import Enum
from os import system
from random import randint

from anyio import sleep
from colorama import Back, Fore
import numpy as np

from function import *

class Key:
    def __init__(self, key,describe='') -> None:
        self.key = key
        self.describe=describe
    def __eq__(self, __value) -> bool:
        if not self.key:
            return True
        elif isinstance(__value, Key):
            return self.key == __value.key
        else:
            return False
class boundCondition:
    def __init__(self, *condition) -> None:
        def init_bound_condition(self):
            self.eye_mask = None
            self.necklace = None
            self.ankle_shackles = None
            self.handcuffs = None
            self.finger_cuffs = None
            self.arm_restraint = None
            self.leg_restraint = None
            self.breast_cage = None
            self.pudendum_cage = None

        def init_toy(self):
            self.butt_plug = None
            self.ball_gag = None

        init_bound_condition(self)
        init_toy(self)
        if condition:
            self.condition = condition
        else:
            self.condition = None

class toy:
    def __init__(self, name="Default Name", describe="Default describe") -> None:
        self.name = name
        self.describe = describe
    class toys(Enum):
        rope = 0
class actors:
    def __init__(self, type="player", site=None) -> None:
        # 固定属性
        self.gender = "女"
        self.site = site
        # 量化属性
        self.age = 18

        self.health = 100
        # ['你疼到近乎昏迷','你感到剧痛','你感到疼痛','你感到些许不适','你感觉很好']
        self.body_temperature = 37.5
        self.fame = 0
        self.ruse = 0

        self.strength = randint(1, 5)
        self.cognition = randint(1, 5)
        self.agility = randint(1, 5)

        self.type = type
        self.hand_held = [None, None]
        # 状态/背包
        self.inventory = [Key(None,name='信函',describe='一个空白的信函')]
        self.buffs = []
        self.de_buffs = []
        # 意识：5清醒，4朦胧，3无感觉，2几乎昏迷，1失去感知
        self.awareness = 5
        self.awareness_of_time = True
        self.awareness_of_pain = True
        self.awareness_of_sight = True
        self.bounded_condition = boundCondition(None)

    def gain(self, name):
        self.inventory.append(name)

    class method(Enum):
        heal = 0
        attack = 1
        block_sight = 2
        remove_eye_mask = 3
    def influence(self, method: method, strength: int):
        if method == actors.method.heal:
            self.health += strength
        if method == actors.method.attack:
            self.health -= strength - self.strength
            if self.health <= 0:
                self.health = 0
                self.awareness = 2
            elif self.health > 18:
                self.awareness = 5
        if method == actors.method.block_sight:
            self.awareness_of_sight = False
            self.awareness_of_time = False
        if method == actors.method.remove_eye_mask:
            self.awareness_of_sight = True
            self.awareness_of_time = True
    def bound(self, bound_condition: boundCondition):
        self.bounded_condition = bound_condition
    def add_toy(self, toy: toy):
        self.bounded_condition.toy = toy



class page:
    def __init__(
        self,
        name="Default Name",
        describe="Default describe",
    ):
        self.name = name
        self.describe = describe
        self.in_trigger = []
        self.out_trigger = []
        self.frame_options = []
        self.road_info={}#Key and time consumption
        self.leave_able = True
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, page):
            return self.name == __value.name
        else:
            return False

    # 初始化设置
    def connect_frame(self, frame: object,time_spend=20):
        """连接两个场景"""
        if frame not in self.frame_options:
            self.frame_options.append(frame)
            self.road_info[frame.name]['Key']=Key(None)
            self.road_info[frame.name]['time spend']=time_spend
        if self not in frame.frame_options:
            frame.frame_options.append(self)
            frame.road_info[self.name]['Key']=Key(None)
            frame.road_info[self.name]['time spend']=time_spend
    def add_oneway_lock(self,Destination: object,password):
        """锁定某个场景"""
        self.road_info[Destination]['Key']=Key(password)
        
    def add_mutual_lock(self,site: object,password):
        """锁定某个路线"""
        self.road_info[site]['Key']=Key(password)
        site.road_info[self]['Key']=Key(password)

    def add_in_trigger(self, dialogue: list):
        """新增对话触发"""
        self.in_trigger.append(trigger.dialogue_trigger(dialogue))

    # 交互设置
    def show_frame_info(self):
        sleep(0.01)
        system("cls")
        sleep(0.01)
        print(self.name)
        sleep(0.01)
        print(self.describe)
        sleep(0.01)
        print("")

    def show_frame_options(self):
        print(Fore.BLUE + "现在要去到哪里？")
        print(*["\t%d.%s-耗时20分钟\n" % (i, option.name)for i, option in enumerate(self.frame_options, 1)])
class trigger:
    class dialogue_trigger:
        def __init__(self,dialogue: list):
            self.dialogue=dialogue
            self.dialogue[0]+='  '
        def trig(self):
            '''触发,返回值bool:是否跳过其他触发器'''
            for i in range(len(self.dialogue)-1):
                print(self.dialogue[i],'\t......')
                get_keys('any')
            print(self.dialogue[-1])
            print(Back.RED+'对话已结束')
            sleep(2)
            return False
    class unmovable_trigger:
        def __init__(self,can_leave=True,can_in=True) -> None:
            self.leave_able = can_leave
            self.get_in_able = can_in
        def trig(self):
            return 
    def __init__(self):
        self.trig_types={
            "dialogue":self.dialogue_trigger,
        }
        pass
    def trig(self):
        return True
class gameBoard:
    def __init__(self) -> None:
        def init_frame_interact():
            # 大地图连接
            connect_info_of_big_map=[('Outer Island', 'Wharf'),
                ('Reef', 'Beach'),
                ('Cliff', 'Hills'),
                ('Mountain Range', 'Village'),
                ('Development Zone', 'Village'),
                ('Development Zone', 'Natural Park'),
                ('North Resident', 'Natural Park'),
                ('North Resident', 'School'),
                ('Wharf', 'School'),
                ('Wharf', 'Bar Club'),
                ('Beach', 'Bar Club'),
                ('Beach', 'Big Farm'),
                ('Beach', 'Hills'),
                ('Village', 'Suburb'),
                ('Natural Park', 'Suburb'),
                ('Natural Park', 'South Resident'),
                ('School', 'South Resident'),
                ('School', 'Commercial Street'),
                ('School', 'Natural Park'),
                ('Big Farm', 'Wilderness'),
                ('Commercial Street', 'Bar Club'),
                ('Commercial Street', 'South Resident'),
                ('Industrial Zone', 'Bar Club'),
                ('Industrial Zone', 'Big Farm'),
                ('Industrial Zone', 'Station'),
                ('Station', 'Big Farm'),
                ('Station', 'Wilderness')]
            # 场景连接
            connect_info_of_North_resident=[('Roadside','North Resident'),
                                            ('Roadside','Gateway'),
                                            ('Home','Gateway'),
                                            ('Home','Bathroom'),
                                            ('Home','Bedroom')]
            
            connect_info_of_big_map.extend(connect_info_of_North_resident)
            for i in connect_info_of_big_map:
                self.big_map[i[0]].connect_frame(self.big_map[i[1]])

        def init_frame_trigger():
            self.big_map['Home'].add_in_trigger(['some body say','some thing to u'])
        def init_world_info():
            self.time_min=0
            self.year=0
            self.month=1
            self.day=1
            self.hour=6
            self.minute=0

        big_map_zn = [
            # page 4
            "外岛","礁石","悬崖",
            # page 3
            "山脉","开发区","城北居民区","码头","沙滩","丘陵",
            # page 2
            "村庄","自然公园","学校","酒吧会所","大农场","荒野",
            # page 1
            "郊区","城南居民区","商业街","工业区","车站",]
        big_map_en = [
    # page 4
            "Outer Island","Reef","Cliff",
            # page 3
            "Mountain Range","Development Zone","North Resident","Wharf","Beach","Hills",
            # page 2
            "Village","Natural Park","School","Bar Club","Big Farm","Wilderness",
            # page 1
            "Suburb","South Resident","Commercial Street","Industrial Zone","Station",]
        # 定义大地图场景
        self.big_map={en:page(name=zn,describe=f'你正在{zn}') for en,zn in zip(big_map_en,big_map_zn)}
        #定义子场景
        North_resident_map=zip(['Roadside','Gateway','Home','Bathroom','Bedroom'],['路边','大门','客厅','浴室','卧室'])
        self.big_map.update({en:page(name=zn,describe=f'你正在{zn}') for en,zn in North_resident_map})

        # init_frames()
        init_frame_interact()
        init_frame_trigger()
        init_world_info()
        self.player = actors(site=self.big_map['Roadside']) 
        self.current_frame=self.big_map['Roadside']
    def addTime(self,minute):
        m=np.array([0,31, 60, 91, 121, 152, 182, 213, 243, 274, 304, 335, 365])
        self.time_min+=minute
        self.minute+=minute
        if self.minute>59:
            self.minute-=60
            self.hour+=1
        if self.hour>23:
            self.hour-=24
            self.day+=1
        if self.day>m[self.month]:
            self.day-=m[self.month]
            self.month+=1
        if self.month>12:
            self.month-=12
            self.year+=1
    def start_game(self):
        self.current_frame=self.big_map.get('Roadside')
        self.reach_frame(self.current_frame)
    def continue_game(self):
        self.reach_frame(self.current_frame)
    def getKey(self,*arg):
        '''游戏中读取按键，必要时唤起菜单'''
        while True:
            k=get_keys(*arg,'m')
            if k=='m':
                rise_menu(self)
                return None
            else:
                return k
    def reach_frame(self,frame):
        self.current_frame=frame
        self.player.site=frame
        self.current_frame.show_frame_info()
        while True:
            for _ in range(len(self.current_frame.in_trigger)):
                triggers=self.current_frame.in_trigger.pop()
                if triggers.trig():
                    break
            self.current_frame.show_frame_info()
            self.current_frame.show_frame_options()
            frame_count=len(self.current_frame.frame_options)
            num=self.getKey(range(1,frame_count+1))
            self.goto_frame(num)

    def goto_frame(self, num):
        if not num:
            return
        destination_frame=self.current_frame.frame_options[num-1]
        if not self.current_frame.leave_able:
            print('无法离开此地')
            sleep(1.3)
            return
        if self.current_frame.road_info.get(destination_frame.name).get('key',Key(None)) not  in self.player.inventory:
            print('没有对应的钥匙')
            sleep(1.3)
            return
        if self.current_frame.out_trigger:
            leave_site=self.current_frame.out_trigger.pop().trig()
        else:
            leave_site = True
        if leave_site:
            self.addTime(self.current_frame.road_info[destination_frame.name]['time spend'])
            self.current_frame=destination_frame