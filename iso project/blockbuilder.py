import numpy as np
from data import *

data = mapdata[1]
len = 1
rect_list = []
to_delete = []
rect_num = 0
start_new_rect = True
for y,row in enumerate(data):

    if not start_new_rect:
        rect = [rect_pt1, rect_pt2]
        rect_list.append(rect)
        rect_num += 1
        start_new_rect = True

    for x, tile in enumerate(row):
        if tile == 1 and start_new_rect:
            rect_pt1 = [x,y]
            rect_pt2 = [x + len, y + len]
            start_new_rect = False
        elif tile == 1 and not start_new_rect:
            rect_pt2 = [x + len, y + len]
        elif tile == 0 and not start_new_rect:
            rect = [rect_pt1, rect_pt2]
            rect_list.append(rect)
            rect_num += 1
            start_new_rect = True
if not start_new_rect:
    rect = [rect_pt1, rect_pt2]
    rect_list.append(rect)
    rect_num += 1
    start_new_rect = True

for rect in rect_list:
    if rect[0][1] > 0:
        for other_rect in rect_list:
            if other_rect[1][1] == (rect[0][1]) and other_rect[0][0] == rect[0][0] and other_rect[1][0] == rect[1][0]:
                other_rect[1] = rect[1]
                if not (rect_list.index(rect) in to_delete):
                    to_delete.append(rect_list.index(rect))

for i in reversed(to_delete):
    del rect_list[i]
