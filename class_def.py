from enum import Enum
from os import system
from random import randint

from anyio import sleep
from colorama import Back, Fore
import numpy as np

from function import *

class Key:
    def __init__(self, key,name_zh='',describe='') -> None:
        self.key = key
        self.name_zh=name_zh
        self.describe=describe
    def __eq__(self, __value) -> bool:
        if not self.key:
            return True
        elif isinstance(__value, Key):
            return self.key == __value.key
        else:
            return False

class interactDialogue:
    def __init__(self,summery:str='',dialogue:list[str]=['']):
        """格式 List[list[
            summery:str,
            dialogue:list,
            reply:Dict{
                tuple[reply:str,summery:str]
                }
        ]]"""
        self.dialogue=[[summery,dialogue,{}]]
    def add_dialogue(self,summery:str,talking: list):
        """summery:总结\ntalking:对话\nindex:添加到哪个对话"""
        self.dialogue.append([summery,talking,{}])
    def add_word(self,summery,word):
        ind=(i for i,ele in enumerate(self.dialogue) if ele[0]==summery)
        if len(ind)==0:
            return False
        ind=ind[0]
        self.dialogue[ind][1].append(word)
    def del_word(self,summery,ind):
        ind=(i for i,ele in enumerate(self.dialogue) if ele[0]==summery)
        if len(ind)==0:
            return False
        ind=ind[0]
        del self.dialogue[ind][1][ind]

    def add_reply(self,dialogue:str,reply: list[tuple[str,str]]):
        """dialogue:对话名(总结)\n对话回复机制格式[(回复1，下一个对话),(回复2，下一个对话),(回复3，下一个对胡)]"""
        for i in self.dialogue:
            if i[0]==dialogue:
                i[2].update({i:j for i,j in reply})
        else:
            return None
    def trig(self):

        pass
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
        self.inventory = [Key(None,name_zh='信函',describe='一个空白的信函')]
        self.buffs = []
        self.de_buffs = []
        # 意识：5清醒，4朦胧，3无感觉，2几乎昏迷，1失去感知
        self.awareness = 5
        self.awareness_of_time = True
        self.awareness_of_pain = True
        self.awareness_of_sight = True
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
class page:
    def __init__(
        self,
        name_zh="Default Name",
        describe="Default describe",
        name_en='Default Name_en',
    ):
        self.name_zh = name_zh
        self.name_en=name_en
        self.describe = describe
        self.in_trigger = []
        self.out_trigger = []
        self.frame_options = []
        self.interaction_options=[]
        self.road_info={}#Key and time consumption
        self.leave_able = True
    #更改设置
    def change_frame_name_zh(self,new_name:str):
        self.name_zh=new_name
    def change_frame_describe(self,new_describe:str):
        self.new_describe=new_describe
    def clean_all_connect(self):
        for frame in self.frame_options:
            frame.frame_options.remove(self)
            del frame.road_info[self.name_en]
    # 场景设置
    def connect_frame(self, frame: object,time_spend=20):
        """连接两个场景"""
        if frame not in self.frame_options:
            self.frame_options.append(frame)
            self.road_info.update({frame.name_en:{'Key':Key(None),'time spend':time_spend}})
        if self not in frame.frame_options:
            frame.frame_options.append(self)
            frame.road_info.update({self.name_en:{'Key':Key(None),'time spend':time_spend}})
    
    def add_oneway_lock(self,Destination: object,password):
        """锁定某个场景"""
        self.road_info[Destination.name_en]['Key']=Key(password)
    def add_mutual_lock(self,site: object,password):
        """锁定某个路线"""
        self.road_info[site.name_en]['Key']=Key(password)
        site.road_info[self.name_en]['Key']=Key(password)
    def add_in_trigger(self, dialogue: list):
        """新增对话触发"""
        self.in_trigger.append(trigger.dialogue_trigger(dialogue))
    
    def show_frame_info(self):
        sleep(0.01)
        system("cls")
        sleep(0.01)
        print(self.name_zh)
        sleep(0.01)
        print(self.describe)
        sleep(0.01)
        print("")

    #路线交互
    def show_frame_options(self,only_show_option=False):
        if only_show_option:
            print(Fore.BLUE + "现在要去到哪里？")
        print(*["\t%d.%s\t-%2d分钟\n" % (i, option.name_zh,self.road_info[option.name_en]['time spend'])for i, option in enumerate(self.frame_options, 1)])
    def get_frame_options(self):
        return [(option.name_zh,self.road_info[option.name_en]['time spend']) for option in self.frame_options]
    #场景交互
    def add_interact_option(self,option):
        self.frame_options.append(option)
    def show_interact_options(self):
        """返回options个数"""
        # l=len(self.interaction_options)
        choose_list=['q','w','e','r','t','y','u','i','o','p']
        if self.interaction_options:
            print(f"{choose_list[i]:2<}{option.name}" for i,option in enumerate(self.interaction_options))
        return len(self.interaction_options)
    def get_interact_options(self):
        """返回options列表"""
        return [option.name for option in self.interaction_options]
class trigger:
    class dialogue_trigger:
        def __init__(self,dialogue: list):
            self.dialogue=dialogue
            self.dialogue[0]+='  '
        def __bool__(self):
            return
        def trig(self):
            '''触发,返回值bool:是否跳过其他触发器'''
            for i in range(len(self.dialogue)-1):
                print(self.dialogue[i],'\t......')
                get_keys('any')
            print(self.dialogue[-1])
            print(Back.RED+'对话已结束,任意键继续')
            sleep(2)
            get_keys('any')
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

        big_map_zh = [
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
        self.big_map={en:page(name_zh=zh,describe=f'你正在{zh}',name_en=en) for en,zh in zip(big_map_en,big_map_zh)}
        #定义子场景
        North_resident_map=zip(['Roadside','Gateway','Home','Bathroom','Bedroom'],['路边','大门','客厅','浴室','卧室'])
        self.big_map.update({en:page(name_zh=zh,describe=f'你正在{zh}',name_en=en) for en,zh in North_resident_map})

        # init_frames()
        init_frame_interact()
        init_frame_trigger()

        self.time_min=0
        self.year=0
        self.month=1
        self.day=1
        self.hour=6
        self.minute=0

        self.player = actors(site=self.big_map['Roadside']) 
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
        '''游戏中读取按键，必要时唤起菜单，返回False时标记退出游戏板'''
        k=get_keys(*arg,'m')
        if k=='m':
            return rise_menu(self)
        else:
            return k
    def get_menu_choice(self,element:list[list],option:list[list],num=8):
        while [] in element:
            del option[element.index([])]
            element.remove([])
        while [] in option:
            del element[option.index([])]
            option.remove([])
        length_ele=list(map(len,element))
        length_opt=list(map(len,option))
        menu=0
        page=0
        select=0
        splitted_list = [[ele_list[i : i + num] for i in range(0, len(ele_list), num)]for ele_list in element]
        while True:
            system("cls")
            c_len=len(splitted_list[menu][page])
            for i in range(c_len):
                if i==select:
                    print(Back.CYAN+ str(i + num * page) + "." + str(splitted_list[menu][page][i]))
                else:
                    print(str(i + num * page) + "." + str(splitted_list[menu][page][i]))
            print("\n" * (num - 1 - len(splitted_list[menu][page])))
            print(Fore.RED + "---------------")
            print(*[f'{str(i):>2}.{str(ele)}' for i,ele in enumerate(option[menu],1)],sep='\n')
            key = get_keys(range(1,1+length_opt[menu]), ["up", "down", "left", "right",'q','e','m'])
            if key=='m':
                return rise_menu(self)
            elif key=='q':
                menu-=1
                if menu<0:
                    menu+=len(element)
                page=select=0
            elif key=='e':
                menu+=1
                if menu>=len(element):
                    menu-=len(element)
                page=select=0
            elif key == "up":
                if select == 0 and page != 0:
                    select = num - 1
                    page -= 1
                elif select != 0 or page != 0:
                    select -= 1
            elif key == "down":
                if select + page * num == length_ele[menu] - 1:
                    pass
                elif select == num - 1:
                    select = 0
                    page += 1
                else:
                    select += 1
            elif key == "left":
                if page == 0:
                    select = 0
                else:
                    page -= 1
                    select = 0
            elif key == "right":
                if page != len(splitted_list[menu]) - 1:
                    page += 1
                    select = 0
            if key in ["up", "down", "left", "right","q","e"]:
                continue
            return menu,page*num+select,key
    #编辑操作
    def del_frame(self,frame_name_en):
        if frame_name_en!='Roadside':
            del self.big_map[frame_name_en]
            print('删除完成')
        else:
            print('无法删除开局场景')
        sleep(1.2)
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
            # self.current_frame.show_frame_options()
            # length=self.current_frame.show_interact_options()

            # choose_list=['q','w','e','r','t','y','u','i','o','p']
            # frame_count=len(self.current_frame.frame_options)
            # num=self.getKey(range(1,frame_count+1),choose_list[:length])
            k=self.get_menu_choice(
                [[f'{e1:<7}\t{e2}分钟' for e1,e2 in self.current_frame.get_frame_options()],
                self.current_frame.get_interact_options()],
                [['前往'],
                ['交互']]
            )
            if k==False:
                break
            if k is None:
                continue
            menu,select,option=k
            if menu==0:
                #option=0
                self.goto_frame(select)
            elif menu==1:
                pass
            continue
            if num==False:
                break
            if num is None:
                continue
            if isinstance(num,int):
                self.goto_frame(num)
            elif isinstance(num,str):
                self.trig_interact_option(choose_list.index(num))
    def goto_frame(self, num):
        destination_frame=self.current_frame.frame_options[num-1]
        if not self.current_frame.leave_able:
            print('无法离开此地')
            sleep(1.3)
            return
        if self.current_frame.road_info.get(destination_frame.name_en).get('key',Key(None)) not in self.player.inventory:
            print('没有对应的钥匙')
            sleep(1.3)
            return
        if self.current_frame.out_trigger:
            leave_site=self.current_frame.out_trigger.pop().trig()
        else:
            leave_site = True
        if leave_site:
            self.addTime(self.current_frame.road_info[destination_frame.name_en]['time spend'])
            self.current_frame=destination_frame
    def trig_interact_option(self,num):
        self.current_frame.interaction_options[num].trig()