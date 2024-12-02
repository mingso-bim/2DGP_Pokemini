from pico2d import *
import gameWorld

tmp_image = None

def b_blink():
    b_fade_out()
    b_fade_in()

def w_blink():
    w_fade_out()
    w_fade_in()

def b_fade_out(duration=0.2, color=(0, 0, 0)):
    steps = 255
    r, g, b = color
    elapsed_time = 0
    start_time = get_time()
    while elapsed_time < duration:
        alpha = int((elapsed_time / duration) * 255)  # 현재 진행도에 따라 alpha 값 계산
        clear_canvas()
        gameWorld.render()
        b_draw_rectangle_fill_with_alpha(0, 0, gameWorld.game_width, gameWorld.game_height, r, g, b, alpha)
        update_canvas()
        elapsed_time = get_time() - start_time

def b_fade_in(duration=0.2, color=(0, 0, 0)):
    steps = 255
    r, g, b = color
    elapsed_time = 0
    start_time = get_time()
    while elapsed_time < duration:
        alpha = 255 - int((elapsed_time / duration) * 255)  # 현재 진행도에 따라 alpha 값 계산
        clear_canvas()
        gameWorld.render()
        b_draw_rectangle_fill_with_alpha(0, 0, gameWorld.game_width, gameWorld.game_height, r, g, b, alpha)
        update_canvas()
        elapsed_time = get_time() - start_time

def b_draw_rectangle_fill_with_alpha(x1, y1, x2, y2, r, g, b, alpha):
    global tmp_image
    if tmp_image is None:
        tmp_image = load_image("resource/black_square.png")  # 검은 사각형 이미지를 준비
    tmp_image.opacify(alpha / 255)  # 투명도 조정
    tmp_image.clip_draw(0, 0, 10, 10, (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1)

def w_fade_out(duration=0.05, color=(255, 255, 255)):
    r, g, b = color
    elapsed_time = 0
    start_time = get_time()
    while elapsed_time < duration:
        alpha = int((elapsed_time / duration) * 255)  # 현재 진행도에 따라 alpha 값 계산
        clear_canvas()
        gameWorld.render()
        w_draw_rectangle_fill_with_alpha(0, 0, gameWorld.game_width, gameWorld.game_height, r, g, b, alpha)
        update_canvas()
        elapsed_time = get_time() - start_time

def w_fade_in(duration=0.05, color=(255, 255, 255)):
    r, g, b = color
    elapsed_time = 0
    start_time = get_time()
    while elapsed_time < duration:
        alpha = 255 - int((elapsed_time / duration) * 255)  # 현재 진행도에 따라 alpha 값 계산
        clear_canvas()
        gameWorld.render()
        w_draw_rectangle_fill_with_alpha(0, 0, gameWorld.game_width, gameWorld.game_height, r, g, b, alpha)
        update_canvas()
        elapsed_time = get_time() - start_time

def w_draw_rectangle_fill_with_alpha(x1, y1, x2, y2, r, g, b, alpha):
    global tmp_image
    if tmp_image is None:
        tmp_image = load_image("resource/black_square.png")  # 흰 사각형 이미지를 준비
    tmp_image.opacify(alpha / 255)  # 투명도 조정
    tmp_image.clip_draw(10, 0, 10, 10, (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1)
