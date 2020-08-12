import time

import numpy as np

import qemu
import image

def at_hive(img):
    return image.e_clip.match(img) and image.claim_hive_clip.match(img)

def can_make_honey(img):
    return image.e_clip.match(img) and image.make_honey_clip.match(img)

def pollen_empty(img):
    return image.pollen_empty_clip.match(img)

def count_red(img):
    count = 0
    height, width, _ = img.shape
    for i in range(height):
        for j in range(width):
            b, g, r = img[i,j]
            if r > b and r > g:
                count += 1
    return count

def find_hive_dir(img):
    left_count = count_red(img[image.oy-30:image.oy+30, :image.ox-100])
    right_count = count_red(img[image.oy-30:image.oy+30, image.ox+100:])
    print("left %d right %d" % (left_count, right_count))
    if left_count > right_count:
        return "a"
    else:
        return "d"

def find_and_claim():
    key_log = []
    qemu.send_key("w", 1.7, log=key_log)
    img = image.get_screen_image()
    dir = find_hive_dir(img)

    while True:
        img = image.get_screen_image()
        if at_hive(img):
            break
        qemu.send_key(dir, 0.2, log=key_log)

    qemu.send_key("e")
    while True:
        img = image.get_screen_image()
        if not at_hive(img):
            break
        time.sleep(1)

    return key_log

def make_honey():
    while True:
        img = image.get_screen_image()
        if can_make_honey(img):
            qemu.send_key("e")
        if pollen_empty(img):
            time.sleep(5)
            break
        time.sleep(1)

if __name__ == "__main__":
    img = image.load_image("hive.ppm")
    print(at_hive(img))
