
import sys
import os
import keyboard
import cv2
from timeit import default_timer as timer
import imagelist


class SampleViewer():
    def __init__(self, imagesPerCol=3):
        self._files = []            # images to experiment with
        self._index = 0             # index of _files
        self.changed = False        # results has changed. New images to be shown.
        self.run = True             # controlls the main() while loop
        self.results = imagelist.ImageList(imagesPerCol)  # images to be shown.
        self._applicationPath = ""   # application path
        self._applicationRunningMode = ""
        self.imOrigin = None        # image without any manipulation
        self.imOriginSmall = None   # some processing can be donne in a small image
        self.smallSize = 200        # small image is a reactangle image with dimesion smallSize * smallSize

        self._startWatch = 0         # execution timer
        self.enableStopWatch = True   # enable te stop watch
        self._timeStatistics = []    # liste to hold the stopwatch statistics
        self.clear_watch()

        self._keys = ""  # buffer for numerical key string

        # construct the argument parse and parse the arguments
        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            self._applicationPath = os.path.dirname(sys.executable)
            self._applicationRunningMode = 'Frozen/executable'
        else:
            try:
                app_full_path = os.path.realpath(__file__)
                self._applicationPath = os.path.dirname(app_full_path)
                self._applicationRunningMode = "Non-interactive (e.g. 'python myapp.py')"
            except NameError:
                self._applicationPath = os.getcwd()
                self._applicationRunningMode = 'Interactive'
        print("[INFO] Application running mode: ", self._applicationRunningMode)
        print("[INFO] Application path: ", self._applicationPath)

    def get_application_path(self):
        return self._applicationPath

    def image_read(self):
        # read the image
        self.imOrigin = cv2.imread(self._files[self._index], cv2.COLOR_BGR2RGB)
        if self.imOrigin is None:
            print('[ERR] Could not open or find the image:', _files[self._index])
            return
        else:
            self.append(os.path.basename(self._files[self._index]), self.imOrigin)

        # for texture analyses it can be done on as smaller image with constat size
        # masks can be scaled up to the original zize
        self.imOriginSmall = cv2.resize(self.imOrigin, (self.smallSize, self.smallSize), interpolation=cv2.INTER_LINEAR)

    def scale_to_origin(self, mask):
        return cv2.resize(mask, (self.imOrigin.shape[1], self.imOrigin.shape[0]), interpolation=cv2.INTER_LINEAR)

    # abstract method. Hast to be overwritten
    def kernel(self):
        self.clear()
        print('[INFO] Show file [{}] {} '.format(self._index, self._files[self._index]))

    def set_sample_path(self, path):
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                self._files.append(os.path.join(r, file))

    def print_samples(self):
        for f in self._files:
            print(f)

    def show_first(self):
        self.set_index(0)

    def clear(self):
        self.results.clear()

    def append(self, text, image):
        self.results.append(text, image)

    def im_show(self, text, image, file=True):
        if file:
            self.imSave(text, image)
        cv2.imshow("text", image)
        cv2.waitKey(0)

    def im_save(self, text, image):
        path = os.path.join(self._applicationPath, "debugg")
        # make dir if not existing
        if not os.path.exists(path):
            os.makedirs(path)

        # save file
        sufix = ".jpg"
        fileName = text
        fileName = fileName.replace(sufix, "")
        fileName = fileName.replace('.', '_')
        fullPath = os.path.join(path, text + sufix)
        cv2.imwrite(fullPath, image)

    def len(self):
        return self.results.len()

    def get_current_info(self):
        return '[INFO] Show file [{}]'.format(self._index)

    def set_index(self, index):
        if index >= 0 and index < len(self._files):
            self._index = index
            self.changed = True
            self.clear_watch()

    def menu(self, key):
        if keyboard.is_pressed('esc'):
            self.run = False

        if keyboard.is_pressed('q') or keyboard.is_pressed('Q'):
            self.run = False

        if keyboard.is_pressed('x') or keyboard.is_pressed('X'):
            self.run = False

        if keyboard.is_pressed('c') or keyboard.is_pressed('C'):
            self.run = False

        if keyboard.is_pressed('h') or keyboard.is_pressed('H'):
            print('[INFO] Valid keys')
            print('  Exit: q Q x X c C')

        if keyboard.is_pressed('space'):
            print('space')

        if keyboard.is_pressed('enter'):
            index = int(self._keys)
            if index >= 0 and index < len(self._files):
                self.set_index(index)
            else:
                print('[ERR] Invalid command {}'.format(index))
            self._keys = ""

        if keyboard.is_pressed('home'):
            self.set_index(0)
            # print('home: ', self._index)

        if keyboard.is_pressed('end'):
            self.set_index(len(self._files) - 1)
            # print('end: ', self._index)

        if keyboard.is_pressed('left'):
            # print('left1: ', self._index)
            if self._index > 0:
                self.set_index(self._index - 1)
            else:
                self.set_index(len(self._files) - 1)
            # print('left2: ', self._index)

        if keyboard.is_pressed('right'):
            if self._index < len(self._files) - 1:
                self.set_index(self._index + 1)
            else:
                self.set_index(0)

        if key.name in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self._keys = self._keys + key.name

    def start_watch(self):
        if self.enableStopWatch:
            self.stopWatch = timer()

    def stop_watch(self, message=""):
        if self.enableStopWatch:
            delta = timer()-self.stopWatch
            self._timeStatistics.append(("init", delta))
            print("[INFO] applying " + message + " took {:.3f} seconds".format(delta))

    def clear_watch(self):
        self._timeStatistics.clear()

    def print_watch(self):
        total = 0
        for t in self._timeStatistics:
            total = total + t[1]
        print("[INFO] total {:.3f} seconds".format(total))
