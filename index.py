import csv
from gazeplotter import *
import time


def FS(fix, x, y, t):
    fix.append([x, y, 0])
    return fix, True
 
def DF(fix, x, y, t):
    print(fix)
    fix[0][2] = fix[0][2] + 1
    return fix, True

def FE(fix, x, y, t):
     fix.append([x, y, None])
     return fix, True
 
def TIME(fix, x, y, t):
    #fix.append([x, y, t])
    return fix, False

def photo(fix, x, y, t):
    return fix, None

def switch_type(fix, row):
    switcher = {
        "FS"   : FS,
        "DF"   : DF,
        "FE"   : FE,
        "TIME" : TIME
    }
    tipe, x, y, t = row
    # Get the function from switcher dictionary
    func = switcher.get(str(tipe), photo)
    # Execute the function
    return func(fix, x, y, t)

"""
    Expextation is:

    photos = [
        fixations : [
            "fix" : [
                "FS"    : [ X = 405.165776696316, Y = 686.591209327296, t = - ],
                "FE"    : [ X = 405.165776696316, Y = 686.591209327296, t = - ],
                "TIME"  : [ X = -,                Y = -, t = 00:00:00.1429167 ]
            ],
            "fix" : [ ... ],
            "fix" : [ ... ],
            "fix" : [ ... ],
                .    : [  .  ],
        ],

        "fixations" : [ ... ],
        "fixations" : [ ... ],
            .     : [  .  ],
            .     : [  .  ],
            .     : [  .  ]    
    ]
"""
#fine fix, fixation -> inizializzo nuovo fix, fixation
def finalize_photo(fix, fixations, photos):
    print('end fixation')
    fixations.append(fix)
    photos.append(fixations)
    fixations = []
    fix       = []
    return  fix, fixations, photos

photos = []
with open('fixationStream.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    fixations = []
    fix       = []
    prev_row = next(csv_reader)
    for row in csv_reader:
        fix, end = switch_type(fix, row)
        # PHOTO_ occures
        if(end == None):
            print(len(fix))
            if len(fix) == 0:
                fix, fixations, photos = finalize_photo(fix, fixations, photos)
                print('chiusura normale')
            #forse cnsiderare in modo diverso se c'è solo FS o se ci sono sia FS che FE, ma non TIME
            elif len(fix) == 2:
                fix.append(['-', '-', False])
                fix, fixations, photos = finalize_photo(fix, fixations, photos)
                #inizializzo nuovo fix (come se avessi letto un FS)
                fix.append([prev_row[1], prev_row[2], 0])
            elif len(fix) == 1:
                fix.append([prev_row[1], prev_row[2], '-'])
                fix.append(['-', '-', False])
                fix, fixations, photos = finalize_photo(fix, fixations, photos)
                next_row = next(csv_reader)
                fix.append([next_row[1], next_row[2], 0])
            

        # TIME occures
        elif(not end):
            if len(fixations)>=1 and fixations[-1][2][2] is False:
                final_time = row[3]
                count_1 = fixations[-1][0][2]
                count_2 = fix[0][2]
                fixations[-1][2][3] == final_time*count_1/(count_1+count_2)
                fix.append(['-','-', final_time*count_2/(count_1+count_2)])
            else:
                fix.append(['-','-', row[3]])

            fixations.append(fix)
            fix = []
        
        prev_row = row
        
# print(photos)
photo_0 = [
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

photo_0 = {	'x'  :numpy.asarray([ int((float(x[0][0]) + float(x[1][0]))/2) for x in photo_0]),
        'y'  :numpy.asarray([ int((float(x[0][1]) + float(x[1][1]))/2) for x in photo_0]),
        'dur':numpy.asarray([ float(x[2][2].split(":")[-1])*1500 for x in photo_0 ])}

# print(fix)

draw_fixations_new(photo_0, (800, 800), imagefile="base.png", durationsize=True, durationcolour=True, alpha=1, savefilename="ciao_fix.png")
draw_heatmap_new(photo_0, (800, 800), imagefile="base.png",  durationweight=True, alpha=1, savefilename="ciao_heat.png")