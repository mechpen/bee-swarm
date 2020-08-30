import time

import qemu
import image

def in_browser(img):
    check_connection_error(img)
    return image.browser_clip.match(img)

def check_connection_error(img):
    if image.disconnected_clip.match(img):
        qemu.send_key("alt-f4")
        raise Exception("disconnected")

    if image.idle_timeout_clip.match(img):
        qemu.send_key("alt-f4")
        raise Exception("idle timeout")

def in_game(img):
    check_connection_error(img)
    return image.help_clip.match(img)

def reset_collect():
    qemu.mouse_button(2)
    qemu.mouse_button(1)

def leave():
    qemu.send_key("esc")
    qemu.send_key("l")
    qemu.send_key("ret")

def start():
    while True:
        img = image.get_screen_image()
        if in_browser(img):
            break
        time.sleep(1)

    while True:
        # document.getElementById("MultiplayerVisitButton").click()
        qemu.send_key("up")
        qemu.send_key("ret")
        time.sleep(25)

        qemu.send_key("alt-tab")
        time.sleep(5)
        img = image.get_screen_image()
        if not in_browser(img):
            break

    while True:
        img = image.get_screen_image()
        if in_game(img):
            break
        time.sleep(3)

def init_view():
    qemu.mouse_move(300, 300)
    for _ in range(5):
        qemu.send_key("pgup", 0.5)
    for _ in range(5):
        qemu.send_key("o", 0.5)

inverse_keys = {
    "a": "d",
    "d": "a",
    "w": "s",
    "s": "w",
}

def rollback(steps):
    for key, dur in reversed(steps):
        key = inverse_keys.get(key, key)
        qemu.send_key(key, dur)

dandelion_steps = [
    ("s", 1.5),
    ("a", 1.5),
    ("a", 1.5),
]

sunflower_steps = [
    ("s", 1.5),
    ("s", 1.5),
    ("d", 1.5),
    ("d", 1.5),
]

mushroom_steps = [
    ("s", 1.5),
    ("s", 1.5),
    ("s", 1.5),
    ("a", 1.5),
]

clover_steps = [
    ("s", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("spc", 0.2),
    ("a", 1.5),
    ("spc", 0.2),
    ("a", 1.5),
]

spider_level = [
    ("s", 1.5),
    ("s", 1.5),
    ("s", 1.5),
    ("s", 1.5),
    ("s", 1.5),
    ("s", 1.5),
    ("spc", 0.2),
    ("s", 1.5),
]

spider_steps = spider_level + [
    ("a", 1.5),
]

strawberry_steps = spider_level + [
    ("d", 1.5),
]

banboo_steps = spider_level + [
    ("s", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("a", 1.5),
]

blueflower_steps = spider_level + [
    ("s", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("a", 1.5),
    ("w", 1.5),
    ("w", 1.5),
    ("w", 1.5),
    ("d", 1.5),
]

field_steps = {
    "dandeline"  : dandelion_steps,
    "sunflower"  : sunflower_steps,
    "mushroom"   : mushroom_steps,
    "clover"     : clover_steps,
    "spider"     : spider_steps,
    "strawberry" : strawberry_steps,
    "banboo"     : banboo_steps,
    "blueflower" : blueflower_steps,
}

def walk_to_field(field):
    for key, dur in field_steps[field]:
        qemu.send_key(key, dur)

if __name__ == "__main__":
    image.load_clips()
    img = image.load_image("hive.ppm")
    print(in_game(img))
