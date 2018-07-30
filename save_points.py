import os
import glob
import json
import xml.etree.ElementTree as ET
import numpy as np
import cv2


class AnnotationsGenerator:
    def __init__(self, config_file):
        self.config = None
        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file) as config_buffer:
            config = json.load(config_buffer)
        self.image_folder = config['images_folder']
        self.points_label = config['labels']
        self.bbox_path = config['bbox_path']

    def init(self):
        self.load_images()
        self.show_image()
        self.load_json_file()


    def load_images(self):
        img_types = ('*jpg', '*.png')
        img_files = []
        for files in img_types:
            img_files.extend(glob.glob(files))
        if img_files == []:
            print("No Images found")
            return False
        else:
            self.image_files = img_files
            self.num_images = len(img_files)
            self.current_image_number = 0
            self.current_image_name = os.path.basename(img_files[self.current_image_number])
            return True

    def load_json_file(self):
        self.annotation = {
            "filename":"",
            "image_shape":"",
            "bbox_dimensions":"",
            "point_location":""
        }
        pass

    def save_json_file(self):
        self.get_bbox_dimensions()

    def get_bbox_dimensions(self):
        image_name = os.path.splitext(self.current_image_name)
        xml_filename = self.bbox_path + image_name +'.xml'
        tree = ET.parse(xml_filename)
        root = tree.getroot()
        for child in root:
            if child.tag == 'object':
                for elem in child:
                    if elem.tag == 'bndbox':
                        for prop in elem:
                            if prop.tag == 'xmin':
                                xmin = int(prop.text)
                            if prop.tag == 'xmax':
                                xmax = int(prop.text)
                            if prop.tag == 'ymin':
                                ymin = int(prop.text)
                            if prop.tag == 'ymax':
                                ymax = int(prop.text)


    def show_image(self):
            image = cv2.imread(self.image_files[self.current_image_name])
            cv2.namedWindow("Select Points")
            cv2.setMouseCallback("Select Points", self.select_points)
            cv2.imshow("Select Points", image)

    def select_points(self, event, x, y, flag, params):
        self.position = x, y
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(image, x, y, 5, (0, 255, 0), -1)







ix,iy = -1,-1
# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),100,(255,0,0),-1)
        ix,iy = x,y

# Create a black image, a window and bind the function to window
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(ix,iy)

cv2.destroyAllWindows()