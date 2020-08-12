import sys
import time
import random

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

import qemu
import game
import image
import ransac

margin_top = 128
margin_bottom = 128

min_grid_size = 30
max_grid_size = 40

pollen_box_top = 3
pollen_box_left = 572

history = []
random_count = 0

def find_grid_size(img, y, grid_size):
    strip = img[y:y+grid_size, :]
    scan = np.sum(strip, axis=0) / grid_size
    fft = np.absolute(np.fft.fft(scan))

    freq_min = image.width//max_grid_size
    freq_max = image.width//min_grid_size
    max_idx = np.argmax(fft[freq_min:freq_max+1])
    max_idx += freq_min

    return image.width//max_idx, fft[max_idx], (scan, strip)

def find_grids(img):
    grids = []
    weights = []
    scans = dict()

    y = margin_top
    grid_size = min_grid_size

    while y < image.height - margin_bottom:
        grid_size, weight, scan = find_grid_size(img, y, grid_size)
        grids.append((y, grid_size))
        weights.append(weight)
        scans[y] = scan
        y += grid_size

    return grids, weights, scans

def filter_grids(grids, weights):
    model = ransac.ransac(grids, weights, ransac.LinearFit, 10, 3, 0.6)
    if model is None:
        return []
    return sorted(model.points)

def find_flower_locations(grids, scans):
    locations = []

    for (y, grid_size) in grids:
        (scan, strip) = scans[y]
        scan = gaussian_filter1d(scan, 3)
        peaks, p = find_peaks(scan, prominence=10, distance=grid_size-3)

        good_peaks = set()
        for i in range(1, len(peaks)-1):
            if peaks[i] - peaks[i-1] < grid_size + 10:
                good_peaks.add(peaks[i])
                good_peaks.add(peaks[i-1])
                continue
            if peaks[i+1] - peaks[i] < grid_size + 10:
                good_peaks.add(peaks[i])
                good_peaks.add(peaks[i+1])

        # plt.subplot(211), plt.plot(scan)
        # plt.plot(peaks, scan[peaks], "x")
        # plt.subplot(212), plt.imshow(strip)
        # plt.show()

        for x in good_peaks:
            locations.append((y, x))

    return locations

def get_best_move(locations):
    global history
    global random_count

    dirs = ["w", "s", "a", "d"]
    inverse_dirs = {
        "w": "s",
        "s": "w",
        "a": "d",
        "d": "a",
    }

    if len(locations) < 10:
        if len(history) > 0:
            print("poping history")
            return inverse_dirs[history.pop()]
        else:
            random_count += 1
            if random_count >= 20:
                print("giving up")
                return None
            print("random move")
            return random.choice(dirs)

    oy, ox = image.height//2, image.width//2
    up_count = 0
    down_count = 0
    left_count = 0
    right_count = 0

    for (y, x) in locations:
        if y <= oy:
            up_count += 1
        else:
            down_count += 1
        if x >= ox:
            right_count += 1
        else:
            left_count += 1

    counts = [up_count, down_count, left_count, right_count]

    # print(counts)

    index = np.argmax(counts)
    move = dirs[index]
    history.append(move)
    if len(history) > 5:
        history = history[-5:]
    return move

def get_farm_move(img):
    img = image.convert_to_gray(img)
    grids, weights, scans = find_grids(img)
    grids = filter_grids(grids, weights)
    locations = find_flower_locations(grids, scans)
    return get_best_move(locations)

def pollen_full(img):
    return image.pollen_full_clip.match(img)

def farm():
    while True:
        img = image.get_screen_image()
        if pollen_full(img):
            print("pollen full")
            break
        game.reset_collect()
        move = get_farm_move(img)
        if move is None:
            break
        qemu.send_key(move, 0.5)

if __name__ == "__main__":
    image_file = "bee_swarm.ppm"
    img = image.load_image(image_file)
    # img = image.convert_to_gray(img)
    # move = get_farm_move(img)
    # print(move)
    pollen_full(img)
