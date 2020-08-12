import time
import subprocess

def send_key(key, hold_s=0.5, log=None):
    qemu_cmd = "sendkey %s %d" % (key, int(hold_s*1000))
    cmd = "tmux send-keys -t qemu.0".split()
    cmd += [qemu_cmd, "ENTER"]
    subprocess.call(cmd)
    if log is not None:
        log.append((key, hold_s))
    time.sleep(hold_s+1)

def mouse_button(button):
    qemu_cmd = "mouse_button %d" % button
    cmd = "tmux send-keys -t qemu.0".split()
    cmd += [qemu_cmd, "ENTER"]
    subprocess.call(cmd)

def mouse_move(dx, dy):
    qemu_cmd = "mouse_move %d %d" % (dx, dy)
    cmd = "tmux send-keys -t qemu.0".split()
    cmd += [qemu_cmd, "ENTER"]
    subprocess.call(cmd)

def dump_screen(filename):
    qemu_cmd = "screendump %s" % filename
    cmd = "tmux send-keys -t qemu.0".split()
    cmd += [qemu_cmd, "ENTER"]
    subprocess.call(cmd)
