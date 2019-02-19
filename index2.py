import csv
from gazeplotter import *
import time
from PIL import Image
import os

photo_path = 'C:\\Users\\lello\\source\\repos\\ClientCs_ServerPy\\ClientCs_ServerPy\\images\\'
csv_path = 'C:\\Users\\lello\\source\\repos\\ClientCs_ServerPy\\ClientCs_ServerPy\\csvs\\'
save_path = 'C:\\Users\\lello\\source\\repos\\Gaze-plot\\gaze_analysis\\'
csv_names = os.listdir(csv_path)
print(csv_names)

def create_fixation_file(photo_csv_file, photo_file):
    photo_name = photo_file.split('\\')[-1].split('.')[0]
    print(photo_name)

    with open(photo_csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        fixations = []
        for row in csv_reader:
            print(row)
            if len(row) == 4:
                type_, x, y, t = row
                if type_ == photo_file.split('\\')[-1].split('.')[0]:
                    fix = []
                if type_ == "FS":
                    fix.append([x, y, 0])
                elif type_ == "DF":
                    if len(fix) == 0:
                        fix.append([x,y,0])
                    #do nothing or:
                    #fix[0][2] = fix[0][2] + 1
                elif type_ == "FE":
                    if len(fix) == 1 and x != 'NaN':
                        fix.append([x, y, None])
                elif type_ == "TIME":
                    if len(fix) == 2:
                        fix.append([x, y, t])
                        fixations.append(fix)
                        fix = []
                elif type_ == "END_":
                    #finalize_photo(fix, fixations)
                    #se non ho trovato FE prima di trovare END, forse si puo' evitare questo controllo.. ?! 
                    if len(fix) == 1:
                        fix = []

    photo_0 = {	'x'  :numpy.asarray([ int((float(x[0][0]) + float(x[1][0]))/2) for x in fixations]),
        'y'  :numpy.asarray([ int((float(x[0][1]) + float(x[1][1]))/2) for x in fixations]),
        'dur':numpy.asarray([ float(x[2][2].split(":")[-1])*1500 for x in fixations ])}
    print('.................')
    print(photo_0)
    im = Image.open(photo_file)
    width, height = im.size
    print(width, height)
    fig = draw_fixations_new(photo_0, (width, height), imagefile = photo_file, durationsize=True, durationcolour=True, alpha=1, savefilename=save_path+photo_name+'_fixs.png')
    heatmap = draw_heatmap_new(photo_0, (width, height), imagefile = photo_file, durationweight=True, alpha=1, savefilename=save_path+photo_name+"_heat.png")

    return fig, heatmap

for file_name in csv_names:
    photo_name = file_name.split('.')[0]+'.png'
    create_fixation_file(csv_path + file_name, photo_path + photo_name)