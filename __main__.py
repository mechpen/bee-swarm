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
import utils

image.load_clips()

if len(sys.argv) == 1:
    farm.farm()
    sys.exit(0)

field = sys.argv[1]

while True:
    try:
        utils.log(">>> starting game")
        game.start()
        utils.log(">>> initing view")
        game.init_view()
        utils.log(">>> finding hive")
        steps = hive.find_and_claim()
        utils.log(">>> making honey")
        hive.make_honey()
        utils.log(">>> walking to origin")
        game.rollback(steps)
        utils.log(">>> walking to field")
        game.walk_to_field(field)
        utils.log(">>> start farming")
        farm.farm()
        utils.log(">>> leaving game")
        game.leave()
        time.sleep(3)
    except Exception as e:
        utils.log(e)
        time.sleep(3)
