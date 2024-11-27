from random import randint
from game_framework import change_mode
from stateMachine import StateMachine
from pico2d import *
import gameWorld
import game_framework
from gameWorld import game_width, game_height
from battle_state import *
from skill import Type, Status

other = None

class Battle:
    touchpad = None
    UI = None
    background = None
    font = None
    textbox = None
    meet_script = ('앗! 야생의 ', '(이)가 나타났다!', '가랏! ', '!')
    attack_script = ('의 ', '!')
    counter_script = ('효과가 굉장했다!', '효과가 별로인 듯 하다')
    status_script = ('상대의 몸에 독이 퍼졌다!', '은(는) 독에 의한 데미지를 입었다!',
                     '상대는 화상을 입었다!', '은(는) 화상 데미지를 입었다!',
                     '상대는 마비되어 기술이 나오기 어려워졌다!', '은(는) 몸이 저려서 움직일 수 없다!')


    def __init__(self):
        if Battle.touchpad == None:
            Battle.touchpad = load_image('resource/battleTouchpad.png')
        if Battle.UI == None:
            Battle.UI = load_image('resource/battleUI.png')
        if Battle.background == None:
            Battle.background = load_image('resource/battleBackground.png')
        if Battle.font == None:
            Battle.font = load_font('resource/font.ttf', 40)
        if Battle.textbox == None:
            Battle.textbox = load_image('resource/textbox.png')