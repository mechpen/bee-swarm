import time

import qemu
import image

def in_browser(img):
    return image.browser_clip.match(img)

def starting_err(img):
    return image.starting_err_clip.match(img)

def reset_collect():
    qemu.mouse_button(2)
    qemu.mouse_button(1)

def in_game(img):
    return image.help_clip.match(img)

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
        img = image.get_screen_image()
        if not starting_err(img):
            break

    qemu.send_key("alt-tab")
    while True:
        img = image.get_screen_image()
        if in_game(img):
            break
        time.sleep(3)

def init_view():
    for _ in range(5):
        qemu.send_key("pgup", 0.5)
    for _ in range(5):
        qemu.send_key("o", 0.5)
    qemu.mouse_move(600, 900)

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

def walk_to_field():
    steps = [
        ("s", 1.5),
        ("a", 2),
    ]
    for key, dur in steps:
        qemu.send_key(key, dur)

if __name__ == "__main__":
    image.load_clips()
    img = image.load_image("hive.ppm")
    print(in_game(img))
