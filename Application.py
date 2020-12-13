import sys,os,time,math
import keyboard
import cv2
import argparse
import numpy as np
import matplotlib.pyplot as plt
import sampleViewer
import config

# image processing kernel
class MyExperimenting(sampleViewer.SampleViewer):

    def __init__(self, imagesPerCol = 3):
        super().__init__(imagesPerCol)

    # inherit the abstract methode kernel is mandatory
    def kernel(self):
        sampleViewer.SampleViewer.kernel(self) # call the parent first
        
        # open a image and transform it to the YCRCB color space
        self.image_read()

        # demo case 
        # pot your own code here
        YCRImg = cv2.cvtColor(self.imOrigin, cv2.COLOR_BGR2YCR_CB)
        Y, CR, CB = cv2.split(YCRImg)

        self.append("Y {}", Y) 
        self.append("CR {}", CR)
        self.append("CB {}", CB)

def main():
    viewer = sampleViewer.SampleViewer()

    # argument handler
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--data", required=False,
        help="sample images to be processed",
        default=config.DATA_PATH)
    args = vars(ap.parse_args())
        
    # viewer to show image samples
    viewer = MyExperimenting(imagesPerCol = 4) # rapace that with your class
    data_path = os.path.join(viewer.get_application_path(), args["data"])
    if os.path.isdir(data_path) == True:
        print('Data path: ', data_path)
    else:
        print('Could not open or find the data directory:', args["data"])
        exit(0)
    viewer.set_sample_path(data_path)
    viewer.print_samples()
    viewer.show_first()
    keyboard.on_press(viewer.menu, suppress=False) # Simple user interface
    loop(viewer, os.path.join(viewer.get_application_path(), config.DEBUG_PATH))

def loop(viewer, debuggPath = None):
    
    # main loop
    # WARNING: The viewer MUST run in the main(). 
    # Do NOT change anything. It might result in asynchronous program flow, with lost of images in the results list
    while(viewer.run):
        #if viewer.changed and viewer.results.len() > 0:
        if viewer.changed:
            viewer.changed = False
            if debuggPath != None:
                viewer.results.delete_images(debuggPath)
            viewer.kernel()
            viewer.results.show(viewer.get_current_info()) # this must be called out of the main tread
            viewer.print_watch()
            if debuggPath != None:
                viewer.results.save(debuggPath)
        plt.pause(0.1) # Must be called every loop otherwise the plots get hanged !!!
          
    # derminate application
    cv2.destroyAllWindows()
    plt.close('all')
    print('buy buy')
    sys.exit()

if __name__ == "__main__":
    main()
