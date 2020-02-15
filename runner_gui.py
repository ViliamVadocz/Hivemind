import sys
import os.path
sys.path.insert(0, os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/framework/python/'))

if __name__ == '__main__':

    from rlbot.gui.qt_root import RLBotQTGui

    RLBotQTGui.main()