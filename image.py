import os
import time

import cv2
import numpy as np

import qemu

image_path = "/tmp/bee_swarm.ppm"

width = 1024
height = 768
ox = width // 2
oy = height //2

def load_image(filename, clip=False):
    img = cv2.imread(filename)
    h, w, _ = img.shape
    if not clip:
        assert height == h and width == w, img.shape
    return img

def get_screen_image():
    qemu.dump_screen(image_path)
    time.sleep(0.5)
    return load_image(image_path)

def convert_to_gray(img):
    # remove green
    img[:,:,1] = 0
    # max of red and blue
    return np.amax(img, axis=2)

def show_image(img):
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_image(path, img):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    cv2.imwrite(path, img)

def diff_image(img1, img2):
    diff = img1.astype(int) - img2.astype(int)
    return np.sum(np.absolute(diff))

class Clip:
    def __init__(self, name, x=0, y=0, w=0, h=0, perr=10):
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.perr = perr
        self.img = None

    def path(self):
        name = "%s.ppm" % self.name
        return os.path.join(os.path.dirname(__file__), "clips", name)

    def clip(self, img):
        self.img = img[self.y:self.y+self.h, self.x:self.x+self.w]

    def load(self):
        self.img = load_image(self.path(), clip=True)

    def save(self):
        save_image(self.path(), self.img)

    def match(self, img):
        clip = Clip("tmp", self.x, self.y, self.w, self.h)
        clip.clip(img)
        diff = diff_image(self.img, clip.img)

        perr = diff/(self.w*self.h)
        return perr < self.perr

e_clip = Clip("e", x=338, y=71, w=62, h=25)
help_clip = Clip("help", x=975, y=71, w=19, h=27)
pollen_full_clip = Clip("pollen_full", x=787, y=7, w=4, h=22)
pollen_empty_clip = Clip("pollen_empty", x=573, y=7, w=4, h=22, perr=20)
claim_hive_clip = Clip("claim_hive", x=405, y=69, w=208, h=25, perr=40)
make_honey_clip = Clip("make_honey", x=405, y=69, w=208, h=25, perr=40)

browser_clip = Clip("browser", x=3, y=3, w=60, h=27)
disconnected_clip = Clip("disconnected", x=317, y=283, w=390, h=202)
idle_timeout_clip = Clip("idle_timeout", x=316, y=294, w=390, h=180)

def load_clips():
    e_clip.load()
    help_clip.load()
    pollen_full_clip.load()
    pollen_empty_clip.load()
    claim_hive_clip.load()
    make_honey_clip.load()

    browser_clip.load()
    disconnected_clip.load()
    idle_timeout_clip.load()

if __name__ == "__main__":
    img = load_image("/tmp/bee_swarm.ppm")
    make_honey_clip.clip(img)
    make_honey_clip.save()
