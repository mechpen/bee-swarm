# Objective: make honey automatically
#
# Automation
#
#   1. reconnect
#   2. claim hive
#   3. walk to a field
#   4. farm in a field

import sys
import time
import traceback

import game
import hive
import farm
import image

image.load_clips()

#farm.farm()
#sys.exit(0)

while True:
    try:
        print(">>> starting game")
        game.start()
        print(">>> initing view")
        game.init_view()
        print(">>> finding hive")
        steps = hive.find_and_claim()
        print(">>> making honey")
        hive.make_honey()
        print(">>> walking back to origin")
        game.rollback(steps)
        print(">>> walking to field")
        game.walk_to_field()
        print(">>> start farming")
        farm.farm()
        print(">>> leaving game")
        game.leave()
        time.sleep(3)
    except Exception as e:
        print(e)
        time.sleep(3)
