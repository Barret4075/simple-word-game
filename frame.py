from os import system
import os
import sys
import pickle
from anyio import sleep
from colorama import Fore, Back, Style, init
import keyboard
from function import *
from class_def import *

init(autoreset=True)

#21
#                     外岛          礁石    悬崖
#                       \           /       /
#                        \         /       /
#
# 山脉   开发区 城北居民区  码头    沙滩     丘陵
#   口     口      口      口      口------口
#     \   /  \   /   \   /   \   /   \
#      \ /    \ /     \ /     \ /     \
#       口     口------口      口      口------口
#      村庄  自然公园  学校  酒吧会所  大农场   荒野
#        \    / \     / \     / \     / \     /
#         \  /   \   /   \   /   \   /   \   /
#          口      口------口      口      口
#         郊区 城南居民区  商业街   工业区    车站
#
#   公交：开发区-自然公园-城北居民区-学校-城南居民区-商业街-酒吧会所-码头-工业区
#   城南居民区-(楼下/居民区小卖部) 楼下-(电表/家门口)
map_zn = [
    # page 4
    "外岛","礁石","悬崖",
    # page 3
    "山脉","开发区","城北居民区","码头","沙滩","丘陵",
    # page 2
    "村庄","自然公园","学校","酒吧会所","大农场","荒野",
    # page 1
    "郊区","城南居民区","商业街","工业区","车站",]
map_en = [
    # page 4
    "Outer Island","Reef","Cliff",
    # page 3
    "Mountain Range","Development Zone","North Resident","Wharf","Beach","Hills",
    # page 2
    "Village","Natural Park","School","Bar Club","Big Farm","Wilderness",
    # page 1
    "Suburb","South Resident","Commercial Street","Industrial Zone","Station",]

#
game=None


def play():
    global game
    if not game:
        game=gameBoard()
    game.start_game()


def saves_interface():
    global game
    show_saves()
    print('0.返回主界面')
    key=get_keys(range(7))
    if key==0:
        print('返回')
        sleep(1)
        return None
    elif not os.path.exists('word_game/saves/save%d.save'%key):            
        print('无此存档')
        sleep(2)
        return None
    else:
        with open('word_game/saves/save%d.save'%key,'rb') as f:
            game=pickle.load(f)
    return game
def main_interface():
    global game
    while True:
        system('cls')
        print(Fore.LIGHTCYAN_EX+"欢迎来到Word Game\n1.游戏开始\n2.加载存档\n3.退出游戏")
        key=get_keys(1,2,3,'e')
        if key==1:
            play()
        elif key==2:
            game_saved=saves_interface()
            if game_saved:
                game_saved.continue_game()
        elif key==3:
            sys.exit()
        elif key=='e':
            game=raise_editor(game if game else gameBoard())
if __name__ == "__main__":
    if not os.path.exists('word_game'):
        os.mkdir('./word_game')
    if not os.path.exists('word_game/saves'):
        os.mkdir('./word_game/saves')
    keyboard.on_press(on_press)
    main_interface()
#e