import sys
import os
import shutil
import matplotlib.pyplot as plt
import matplotlib
import math
import cv2


class ImageList():
    def __init__(self, imagesPerCol=3):
        self._textList = []
        self._imageList = []
        self._imagesPerCol = imagesPerCol

        plt.close('all')
        plt.show(block=False)

    def clear(self):
        self._textList.clear()
        self._imageList.clear()

    def append(self, text, image):
        try:
            self._textList.append(text)
            self._imageList.append(image.copy())
        except Exception as e:
            print("[ERR] Failed to append imageList: "+str(e))

    def len(self):
        return len(self._textList)

    def delete_images(self, path):
        sufix = ".jpg"
        if os.path.exists(path):
            # delete all pictures
            for filename in os.listdir(path):
                # delete *.jpg only
                if sufix in filename:
                    filepath = os.path.join(path, filename)
                    try:
                        shutil.rmtree(filepath)
                    except OSError:
                        os.remove(filepath)

    def save(self, path):
        # make dir if not existing
        if not os.path.exists(path):
            os.makedirs(path)

        # save files
        sufix = ".jpg"
        for index in range(len(self._textList)):
            fileName = self._textList[index]
            fileName = fileName.replace(sufix, "")
            fileName = fileName.replace('.', '_')

            fullPath = os.path.join(path, fileName + sufix)
            cv2.imwrite(fullPath, self._imageList[index])

    def show(self, title=""):
        plt.close('all')
        

        # clculate layout: max 3 images per column
        if len(self._textList) > self._imagesPerCol:
            cols = self._imagesPerCol
            rows = math.ceil(len(self._textList) / self._imagesPerCol)
        elif len(self._textList) > 0:
            cols = len(self._textList)
            rows = 1
        fig, axs = plt.subplots(rows, cols, constrained_layout=True)
        fig.canvas.set_window_title(title)
        # show images in the list
        ri = 0
        ci = 0
        for index in range(len(self._textList)):
            if len(self._textList) > 1:
                if rows > 1:
                    axs[ri][ci].set_title(self._textList[index], fontsize=16)
                    axs[ri][ci].imshow(cv2.cvtColor(self._imageList[index], cv2.COLOR_BGR2RGB))
                else:
                    axs[ci].set_title(self._textList[index], fontsize=16)
                    axs[ci].imshow(cv2.cvtColor(self._imageList[index], cv2.COLOR_BGR2RGB))
                # increment subplot indexes
                if ci < cols - 1:
                    ci = ci + 1
                else:
                    ci = 0
                    if ri < rows - 1:
                        ri = ri + 1
            elif len(self._textList) == 1:
                axs.set_title(self._textList[index], fontsize=16)
                axs.imshow(cv2.cvtColor(self._imageList[index], cv2.COLOR_BGR2RGB))
            plt.draw()
        plt.pause(0.1)  # Must be called every loop otherwise the plots get hanged !!!

    #def move_figure(self, x, y):
    #    """Move figure's upper left corner to pixel (x, y)"""
    #    backend = matplotlib.get_backend()
    #    if backend == 'TkAgg':
    #        plt.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    #    elif backend == 'WXAgg':
    #        plt.canvas.manager.window.SetPosition((x, y))
    #    else:
    #        # This works for QT and GTK
    #        # You can also use window.setGeometry
    #        plt.canvas.manager.window.move(x, y)
