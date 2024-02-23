import os
import pickle
from colorama import Fore, init, Back, Style
from os import system
from time import sleep

init(autoreset=True)

# 输入函数
choice_option = {"choosing": False, "choice": None}


def on_press(event):
    global choice_option
    if choice_option.get("choosing"):
        choice_option["choice"] = event.name
    return


def get_keys(*values):
    """get_keys()接受多种输入包括int,range,list,str"""
    global choice_option
    choice_option["choosing"] = True

    def change2list(*arg):
        l = []
        for i in arg:
            if isinstance(i, list):
                l.extend(change2list(*i))
            elif isinstance(i, range):
                l.extend(list(i))
            else:  # 字符/数字
                l.append(i)
        return l

    def get_key(value_type):
        if value_type == "any":
            while True:
                choice = choice_option["choice"]
                if choice is not None:
                    return choice
        if isinstance(value_type, list):
            while True:
                choice = choice_option["choice"]
                if choice in value_type:
                    return choice
                elif (
                    choice is not None
                    and choice.isdigit()
                    and int(choice) in value_type
                ):
                    return int(choice)

    if values[0] == "any":
        key = get_key("any")
    else:
        key = get_key(change2list(*values))
    choice_option = {"choosing": False, "choice": None}
    return key


def get_choice(ele_list: list, *arg, command_info='',num=8):
    """选择列表中的选项和*arg中的按键\ncommand_info是命令提示"""
    select = 0
    page = 0
    splitted_list = [ele_list[i : i + num] for i in range(0, len(ele_list), num)]
    while True:
        system("cls")
        for i in range(len(splitted_list[page])):
            if i==select:
                print(Back.CYAN+ str(i + num * page) + "." + str(splitted_list[page][i]))
            else:
                print(str(i + num * page) + "." + str(splitted_list[page][i]))
        print("\n" * (num - 1 - len(splitted_list[page])))
        print(Fore.RED + "---------------")
        print(command_info)
        key = get_keys(*arg, ["up", "down", "left", "right"])
        if key in ["up", "down", "left", "right"]:
            if key == "up":
                if select == 0 and page != 0:
                    select = num - 1
                    page -= 1
                elif select != 0 or page != 0:
                    select -= 1
            elif key == "down":
                if select + page * num == len(ele_list) - 1:
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
            else:
                if page != len(splitted_list) - 1:
                    page += 1
                    select = 0
            continue
        return page * num + select, key


# 信息输出
def print_time(game: object):
    """以年月日 时分的形式输出当前game board的时间"""
    print(
        "已进行时间：第%d年 %02d月 %02d日\t%02d:%02d"
        % (game.year + 2024, game.month, game.day, game.hour, game.minute)
    )


def show_saves(path='word_game/saves/'):
    system("cls")
    for i in range(1, 7):
        if os.path.exists(path + "save%d.save" % i):
            print(Fore.LIGHTCYAN_EX + "save-%d" % i)
        else:
            print(Fore.LIGHTCYAN_EX + "save-%d-empty" % i)


def print_player_info(game):#未完成
    system("cls")
    print("你是一个%d的%s孩" % (game.player.age, game.player.gender))
    if game.player.awareness == 5:
        health_condition = [
            "你疼到近乎昏迷",
            "你感到剧痛",
            "你感到疼痛",
            "你感到些许不适",
            "你感觉很好",
        ]
        print("状况：", health_condition[game.player.health // 18 - 1])
    else:
        print("健康：", game.player.health)
        print("体表温度：", game.player.body_temperature)
        print("名次：", game.player.fame)
        print("荣誉：", game.player.ruse)


def rise_menu(game):
    """唤起菜单，当要结束进行的游戏时return False，否则return None"""
    while True:
        system("cls")
        print_time(game)
        menu_list = [
            "游戏菜单",
            "1.继续游戏",
            "2.物品",
            "3.状态",
            "4.统计(未完成功能)",
            "5.保存游戏",
            "6.保存并返回主菜单",
            "0.返回主菜单",
        ]
        print("\n".join(menu_list))
        k = get_keys(range(7), "m")
        if k == 1 or k == "m":
            break
        elif k == 2:
            system("cls")
            for i in range(len(game.player.inventory)):
                print(i,game.player.inventory[i].name_zh,game.player.inventory[i].describe)
            print("\nm键返回")
            get_keys("m")
            continue
        elif k == 3:
            print_player_info(game)
            print("\nm键返回")
            get_keys("m")
        elif k == 4:
            pass
        elif k == 5:
            saveGame(game)
            continue
        elif k == 6:
            saveGame(game)
            return False
        else:
            print("退出游戏中 ... ...")
            return False
        return None


def saveGame(game, path="word_game/saves/"):
    show_saves()
    print("保存至存档几?\t按0取消")
    choose = get_keys(range(7))
    if choose == 0:
        print("取消保存")
        sleep(1.5)
        return
    with open(f"{path}save{choose}.save", "wb") as f:
        pickle.dump(game, f)
    print("存档成功,存档号", choose)
    sleep(2)


#内置编辑器
def raise_editor(game):
    while True:
        system("cls")
        print(Fore.RED + "编辑面板")
        print("1.查看基础世界信息\n2.地图概览\n0.返回")
        key = get_keys(range(3))
        if key == 1:
            print_time(game)
            print("Any key to continue")
            get_keys("any")
        # 已创建场景
        if key == 2:
            system("cls")
            print(*list(zip(game.big_map.keys(),list(map(lambda x: x.name_zh, game.big_map.values())),)),sep="\t")
            print("1.查看/修改场景信息/删除场景\n2.新增场景(功能未完成)")
            key1 = get_keys(1, 2)
            if key1 == 1:
                temp = frame_info(game)
                if temp:
                    game = temp
            elif key1 == 2:
                continue
                game = add_frame(game)
        if key == 0:
            break
    return game


def change_frame_info(game, frame_name):#未完成
    while True:
        choice,option=get_choice([f"修改内部名:\t{frame_name}",
                    f"修改场景名:\t{game.big_map[frame_name].name_zh}",
                    f"修改描述:\t{game.big_map[frame_name].describe}",
                    f"删除场景",],
                    [1,2],command_info="1.确认\n2.返回"
                    )
        if option==2:
            break
        if choice==0:
            print("无法修改内部名")
        elif choice==1:
            game.big_map[frame_name].change_frame_name_zh(input("请输入新的名字："))
            print("修改成功！")
            sleep(1.2)
        elif choice==2:
            game.big_map[frame_name].change_frame_describe(input("请输入新的名字："))
            print("修改成功！")
            sleep(1.2)
        elif choice==3:
            game.big_map[frame_name].clean_all_connect()
            game.del_frame(frame_name)
            print(Back.RED+'任意键继续')
            get_keys('any')
            break
    return game



def frame_info(game):

    while True:
        frame_list = list(
            zip(game.big_map.keys(), list(map(lambda x: x.name_zh, game.big_map.values())))
        )
        select_frame_index, key = get_choice(
            frame_list,
            range(5),
            command_info="1.查看场景信息\n2.修改场景信息(功能未完成)\n3.修改场景连接(功能未完成)\n4.删除此场景(功能未完成)\n0.返回",
        )
        select_frame_name = frame_list[select_frame_index][0]
        select_frame = game.big_map[select_frame_name]
        if key == 1:
            system("cls")
            print(select_frame.name_zh, select_frame.name_en)
            print(Fore.RED + "--------------")
            print(Fore.BLUE + "目的地")
            print(*[f"{i:<20}用时{select_frame.road_info[i].get('time spend')}"for i in select_frame.road_info.keys()],sep="\n")
            print(Fore.RED + "--------------")
            print(Back.RED + "Any key to continue")
            get_keys("any")
        elif key == 2:
            game = change_frame_info(game, select_frame_name)
        elif key == 3:
            pass
        elif key == 4:
            pass
        elif key == 0:
            return game
