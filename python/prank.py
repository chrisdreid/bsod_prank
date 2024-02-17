"""
    Disclaimer:
        By engaging with this script in any manner be it invoking, executing, perusing, or modifying, you hereby recognize that its creators, 
        despite their seemingly boundless coding acumen, shall be absolved of all responsibility for any ensuing chaos. 
        This includes, but is not limited to: the metamorphosis of computing devices into culinary appliances, peripheral devices 
        staging a coup and demanding collective bargaining rights, or pregnancy either through conception or lack of.

        This script is graciously conferred upon you 'as is', devoid of any assurance that it will not, on a whim, forsake its 
        intended functions in favor of pursuing a career in digital arts. Should you opt to venture forth on this quixotic escapade, 
        you do so entirely at your own risk, equipped solely with your intellect and, potentially, an unaccountable zest for adventure.

        In the face of unanticipated digital maelstroms, take solace in the thought that the script's progenitors will be ensconced on 
        an enigmatic shoreline, leisurely sipping tea whilst pondering over existential conundrums, blissfully detached from the digital 
        havoc you might instigate.

        Tread lightly, for the moment you actuate this script, 
        its fate—and potentially the fate of your digital dominion—becomes irrevocably intertwined with your own.
"""


import sys, time
from PyQt5 import QtWidgets, QtCore, QtGui
import argparse

_LOOPS              = 99999
_START_TIME_DELAY   = 3000
_DELAY              = 0
_SPEED              = 1000

_FPATH_BG           = './images/BSOD_april_fools.jpg'
_FPATH_IMAGE        = './images/BSOD_april_fools_queen.pngx'
_COLOR              = '#121186'  

QUEEN_WIDTH         = 1035
QUEEN_HEIGHT        = 678


class AprilFools(QtWidgets.QMainWindow):
    def __init__(self, color=None, image=None, bg=None, loops=_LOOPS, delay=_DELAY, anim_delay=_START_TIME_DELAY, padding=0, speed=_SPEED):
        super(AprilFools, self).__init__(None, QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

        self._bgColor = color or _COLOR
        self._bgImage = bg or _FPATH_BG
        self._image = image or _FPATH_IMAGE
        self._loops = loops or _LOOPS
        self._delay = int(delay) or _DELAY
        self._anim_delay = anim_delay or _START_TIME_DELAY
        self._padding = int(padding) or 0
        self._speed = speed or _SPEED

        self.bg = QtWidgets.QLabel(self)
        self.setCentralWidget(self.bg)
        self.queen = QtWidgets.QLabel(self)
        
        self.queen.setVisible(False)
        
        # we can add these are variables as well
        self.setStyleSheet('QMainWindow {background: %s}'%self._bgColor)
        self._animating = True
        self._animDir = 1
        self._xMin = 0
        self._xMax = 10
        self._yPos = 0
        self._xINC = 5
        self._timeStep = 100
        self._cnt = 0

        
        self._desktop = QtWidgets.QApplication.desktop()
        self._desktopGeom = self._desktop.geometry()

        self.setGeometry(self._desktopGeom)


        self.setBGImage(self._bgImage)
        self.setImage(self._image)

        time.sleep(self._delay/1000)
        self.show()


    def setBGImage(self, imagePath):
        self.bg.setPixmap(QtGui.QPixmap(imagePath))
        
    def setImage(self, imagePath):

        self._imagePxmap = QtGui.QPixmap(imagePath)
        self.queen.setPixmap(self._imagePxmap)
        
        self._xMin = self._padding
        self._xMax = self._desktopGeom.width() - self._imagePxmap.width() - self._padding
        self._yPos = self._desktopGeom.height() - self._imagePxmap.height() - 100
        
        self.queen.setGeometry(QtCore.QRect(self._xMin, self._yPos, self._imagePxmap.width()+self._padding, self._imagePxmap.height()))
        QtCore.QTimer.singleShot(self._anim_delay, self.animate)
    
    def animate(self):
        self.queen.setVisible(True)
        self.queen.update()
        
        self.animGroup = QtCore.QSequentialAnimationGroup()
        
        anim = QtCore.QPropertyAnimation(self.queen, b"geometry")
        anim.setDuration(self._anim_delay // 2)
        anim.setStartValue(QtCore.QRect(-((self._imagePxmap.width()+self._padding) * 2), self._yPos, (self._imagePxmap.width()+self._padding), self._imagePxmap.height()))
        anim.setEndValue(QtCore.QRect(self._xMin, self._yPos, (self._imagePxmap.width()+self._padding), self._imagePxmap.height()))
        anim.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
    
        self.animGroup.addAnimation(anim)
        t0 = time.time()
        for i in range(self._loops):
            anim = QtCore.QPropertyAnimation(self.queen, b"geometry")
            anim.setDuration(self._speed)
            anim.setStartValue(QtCore.QRect(self._xMax if i % 2 else self._xMin, self._yPos, (self._imagePxmap.width()+self._padding), self._imagePxmap.height()))
            anim.setEndValue(QtCore.QRect(self._xMin if i % 2 else self._xMax, self._yPos, (self._imagePxmap.width()+self._padding), self._imagePxmap.height()))
            anim.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        
            self.animGroup.addAnimation(anim)
        print('%.2f (sec)' % (time.time() - t0))
        self.animGroup.start()
        
def getCLI():
    parser = argparse.ArgumentParser(description="Add command line arguments for the application")
    parser.add_argument('--color', type=str, help='Background color hex code')
    parser.add_argument('--bg', type=str, help='Background image path')
    parser.add_argument('--image', type=str, help='Image path')
    parser.add_argument('--loops', type=int, default=0, help='Number of loops')
    parser.add_argument('--delay', type=int, default=100, help='Delay before bsod (ms)')
    parser.add_argument('--anim_delay', type=int, default=0, help='Animation delay (ms)')
    parser.add_argument('--padding', type=int, default=0, help='Padding around the image')
    parser.add_argument('--speed', type=int, help='time in (ms) of slide from one side of screen to the other in animation. DEFAULT=%s'%_SPEED)

    return parser


def main(args=None):

    
    options = getCLI().parse_args(args)

    app = QtWidgets.QApplication(args)
    # Hide the cursor
    QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
    mywindow = AprilFools(color=options.color, image=options.image, bg=options.bg, loops=options.loops, delay=options.delay, anim_delay=options.anim_delay, padding=options.padding, speed=options.speed)

    mywindow.show()

    app.exec()


if __name__ == '__main__':
    args = sys.argv[1:]+[
        # test args go here
    ]
    sys.exit(main(args))