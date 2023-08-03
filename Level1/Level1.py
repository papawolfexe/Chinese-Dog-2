import math
import random
from time import perf_counter
import pygame.mixer
from GameObject import MovingObject


def lvl1_pregame(window):
    global pregame_bg
    pygame.mixer.music.load("./Level1/start-sfx.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1, start=1.5)

    pregame_bg = MovingObject(window,
                              "./Level1/start-bg.jpeg",
                              (0, 0),
                              False, (1280, 720), 0, False)


def pregame_loop(window):
    pregame_bg.draw()


def lvl1_start(window):
    global xp_sfx, move_angle, social_credit_emoji, credit_counter, click_counter, credit_count, lvl1_event_id, \
        update_credit_event, font, bg, time_to_finish, timer, update_timer_event, time_start

    # Music
    pygame.mixer.music.load("./Level1/MAO_ZEDONG_DRIP.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=0, start=1.5)

    xp_sfx = pygame.mixer.Sound("./Level1/xp-sfx.mp3")
    xp_sfx.set_volume(.25)

    bg = MovingObject(window,
                      "./Level1/china_bg.jpg",
                      (window.get_width() / 2, window.get_height() / 2),
                      False, (1280, 720), 0, True)

    move_angle = random.randint(20, 70)
    social_credit_emoji = MovingObject(window,
                                       "./Level1/social_credit_emoji.png",
                                       (window.get_width() / 2, window.get_height() / 2),
                                       True, 0.2, 5, True)

    lvl1_event_id = pygame.USEREVENT + 1

    credit_counter = 0
    click_counter = 0
    credit_count = "Social Credit: +0".rjust(3)
    update_credit_event = pygame.event.Event(lvl1_event_id, subtype="click")

    time_to_finish = 10
    time_start = round(perf_counter(), 2)
    timer = f"Time left {time_to_finish}"
    update_timer_event = pygame.event.Event(lvl1_event_id, subtype="time")

    font = pygame.font.SysFont('Consolas', 30)


def loop(window):
    global move_angle, time_remaining, timer, first_run
    # Render
    bg.draw()
    social_credit_emoji.move_at_angle(move_angle, 10)
    move_angle = social_credit_emoji.check_for_bounce(move_angle)
    social_credit_emoji.draw()

    credit_text = font.render(credit_count, True, "red")
    window.blit(credit_text, (32, 26))
    time_elapsed = round(perf_counter(), 2) - time_start
    time_remaining = round(time_to_finish - time_elapsed, 1)
    timer = f"Time Left {time_remaining}"
    check_timer()
    timer_text = font.render(timer, True, "red")
    window.blit(timer_text, (timer_text.get_rect(topright=(window.get_width() - 32, 26))))


def lvl1_event_loop(e):
    global credit_counter, click_counter, credit_count, lvl1_event_id, xp_sfx

    if e.type == pygame.MOUSEBUTTONDOWN:
        if e.button == 1 and social_credit_emoji.collides_with_mouse():
            pygame.event.post(update_credit_event)

    if e.type == lvl1_event_id:
        if e.subtype == "click":
            xp_sfx.play()
            click_counter += 1
            check_click_counter()
            credit_counter += random.randint(10000, 100000)
            credit_count = f'Social Credit: +{credit_counter}'.rjust(3)


def lvl1_music_stop():
    pygame.mixer.music.stop()


def check_click_counter():
    if click_counter == 100:
        fail()


def check_timer():
    if time_remaining == 0:
        fail()


def fail():
    lvl1_music_stop()
