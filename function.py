import os
import pickle
import sys
from colorama import Fore,init, Back, Style
from os import system
from time import sleep
init(autoreset=True)

#输入函数
def on_press(event):
    global choice_option
    if choice_option.get('choosing'):
        choice_option['choice']=event.name
    return
choice_option={'choosing':False,'choice':None}
def get_keys(*values):
    '''get_keys()接受多种输入包括int,range,list,str'''
    global choice_option
    choice_option['choosing']=True
    def change2list(*arg):
        l=[]
        for i in arg:
            if isinstance(i,list):
                l.extend(change2list(*i))
            elif isinstance(i,range):
                l.extend(list(i))
            else:#字符/数字
                l.append(i)
        return l
    def get_key(value_type):
        if value_type=='any':
            while True:
                choice=choice_option["choice"]
                if choice is not None:
                    return choice
        if isinstance(value_type,list):
            while True:
                choice=choice_option["choice"]
                if choice in value_type:
                    return choice
                elif choice is not None and choice.isdigit() and int(choice) in value_type:
                    return int(choice)
    if values[0]=='any':
        key=get_key('any')
    else:
        key=get_key(change2list(*values))
    choice_option={'choosing':False,'choice':None}
    return key
#信息输出
def print_time(game:object):
    '''以年月日 时分的形式输出当前game board的时间'''
    print('已进行时间：第%d年 %02d月 %02d日\t%02d:%02d'%(game.year+2024,game.month,game.day,game.hour,game.minute))

def show_saves():
    system('cls')
    for i in range(1,7):
        if os.path.exists('word_game/saves/save%d.save'%i):
            print(Fore.LIGHTCYAN_EX+"save-%d"%i)
        else :
            print(Fore.LIGHTCYAN_EX+"save-%d-empty"%i)
def print_player_info(game):
    system("cls")
    print('你是一个%d的%s孩'%(game.player.age,game.player.gender))
    if game.player.awareness==5:
        health_condition=['你疼到近乎昏迷','你感到剧痛','你感到疼痛','你感到些许不适','你感觉很好']
        print('状况：',health_condition[game.player.health//18-1])
    else :
        print('健康：',game.player.health)
        print('体表温度：',game.player.body_temperature)
        print('名次：',game.player.fame)
        print('荣誉：',game.player.ruse)
def rise_menu(game):
    while True:
        system("cls")
        print_time(game)
        menu_list=['游戏菜单','1.继续游戏','2.物品','3.状态','4.统计','5.保存游戏','0.退出游戏']
        print('\n'.join(menu_list))
        k=get_keys(range(6),'m')
        if k==1 or k=='m':
            break
        elif k==2:
            system("cls")
            if len(game.player.inventory)==0:
                print('背包为空')
            else:
                for i in range(len(game.player.inventory)):
                    print(game.player.inventory[i],end='\t' if i%2 else '\n')
            print('m键返回')
            get_keys('m')
            continue
        elif k==3:
            print_player_info(game)
            print('m键返回')
            get_keys('m')
        elif k==4:
            pass
        elif k==5:
            saveGame(game)
            continue
        else:
            print('退出游戏中......')
            sys.exit()
        pass

def saveGame(game,path='word_game/saves/'):
    show_saves()
    print('保存至存档几?按0取消')
    choose=get_keys(range(7))
    if choose==0:
        print('取消保存')
        sleep(1.5)
        return
    with open(f"{path}save{choose}.save","wb") as f:
        pickle.dump(game,f)
    print("存档成功,存档号",choose)
    sleep(2)