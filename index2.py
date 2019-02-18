import csv
from gazeplotter import *
import time
from PIL import Image

""" #adjust csv file:
def csv_preprocess(my_csv_file):
    with open(my_csv_file, "r") as csv_file:
        print(my_csv_file)
        csv_reader = csv.reader(csv_file, delimiter=',')
        removal_list = []
        n_right_rows = 0
        for row in csv_reader:
            if n_right_rows < 3:
                if len(row) != 4:
                    #remove row
                    #print(row)
                    removal_list.append(row)
                else:
                    n_right_rows = n_right_rows + 1
            else:
                break
    with open(my_csv_file, "w") as csv_file_w:
        csv_writer = csv.writer(csv_file, delimiter= ',')
        #row = next(csv_writer)
        curr_row = next(csv_writer)
        for row in     """ 

            

#csv_preprocess("prova.csv")

photo_01 = [
        [
        ['10', '10', '-'], 
        ['10', '10', '-'], 
        ['-', '-', '00:00:00.0929167']
    ],
    [
        ['100', '100', '-'], 
        ['100', '100', '-'], 
        ['-', '-', '00:00:00.1429167']
    ], 
    [
        ['500', '500', '-'], 
        ['500', '500', '-'], 
        ['-', '-', '00:00:00.3985144']
    ], 
    [
        ['1000', '1000', '-'], 
        ['1000', '1000', '-'], 
        ['-', '-', '00:00:00.99838385']
    ]
]

def create_fixation_file(photo_csv_file, photo_file, photo_index):
    with open(photo_csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        fixations = []
        for row in csv_reader:
            print(row)
            if len(row) == 4:
                type_, x, y, t = row
                if type_ == "PHOTO_"+str(photo_index):
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
    fig = draw_fixations_new(photo_0, (width, height), imagefile = photo_file, durationsize=True, durationcolour=True, alpha=1, savefilename="ciao_fix.png")
    heatmap = draw_heatmap_new(photo_0, (width, height), imagefile = photo_file, durationweight=True, alpha=1, savefilename="ciao_heat.png")

    return fig, heatmap
            
    

fig, heatmap = create_fixation_file('ff.csv','PHOTO_0.png', 2)

#print(fixationns, len(fixationns))
"""
photo_01 = [
    [
        ['405.165776696316', '686.591209327296', '-'], 
        ['428.997947426729', '697.831585372331', '-'], 
        ['-', '-', '00:00:00.1429167']
    ], 
    [
        ['472.486781260764', '713.751130594919', '-'], 
        ['513.801962608515', '730.369969991633', '-'], 
        ['-', '-', '00:00:00.0239851']
    ], 
    [
        ['562.998530230781', '726.870304686396', '-'], 
        ['553.236107177513', '731.559620129557', '-'], 
        ['-', '-', '00:00:00.2838385']
    ], 
    [
        ['454.734026997588', '730.669447524409', '-'], 
        ['408.531896857328', '739.06976657097', '-'], 
        ['-', '-', '00:00:00.5466836']
    ], 
    [
        ['92.773939650188', '123.830248438845', '-'], 
        ['150.006046117738', '84.6782544643225', '-'], 
        ['-', '-', '00:00:00.6656182']
    ], 
    [
        ['340.02710941226', '394.743915077244', '-'], 
        ['337.919537100681', '359.445814926453', '-'], 
        ['-', '-', '00:00:00.1399196']
    ], 
    [
        ['379.092131296794', '256.028891474935', '-'], 
        ['388.136299155479', '272.826325312745', '-'],
         ['-', '-', '00:00:00.1499147']
    ], 
    [
        ['419.560466954874', '285.831216003093', '-'], 
        ['428.556083279987', '278.302415780837', '-'],
         ['-', '-', '00:00:00.2188753']
    ]
]

# fix = [{	'x'  :numpy.asarray([ (float(x[0][0]) + float(x[1][0]))/2 for x in photo]),
#     'y'  :numpy.asarray([ (float(x[0][1]) + float(x[1][1]))/2 for x in photo]),
#     'dur':numpy.asarray([ x[2][2] for x in photo ])}  for photo in photos]

photo_0 = {	'x'  :numpy.asarray([ int((float(x[0][0]) + float(x[1][0]))/2) for x in fixationns]),
        'y'  :numpy.asarray([ int((float(x[0][1]) + float(x[1][1]))/2) for x in fixationns]),
        'dur':numpy.asarray([ float(x[2][2].split(":")[-1])*1500 for x in fixationns ])}

#print(photo_0)

fig = draw_fixations_new(photo_0, (800, 800), imagefile="base.png", durationsize=True, durationcolour=True, alpha=1, savefilename="ciao_fix.png")
heatmap = draw_heatmap_new(photo_0, (800, 800), imagefile="base.png",  durationweight=True, alpha=1, savefilename="ciao_heat.png")
"""