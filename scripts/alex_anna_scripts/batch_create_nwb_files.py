from generate_day_nwb import generate_day_nwb
#define animal list
animal_list = ['montague','despereaux','jaq','roquefort']
#define sessions to analyze for each animal 
sess_ana = []
sess_ana.append([3,11])
sess_ana.append([6,7,8,9,10,11,12,13,14]) 
sess_ana.append([6,7,8,9,10,11,12,13,14,15,16,17,18])
sess_ana.append([13,14,15,16,17,18,19,20,21,22]) 
#loop over and generate the nwb files 
for animal, sess in zip(animal_list, sess_ana):
    for s in sess:
        print('starting ' + animal + ' session ' + str(s))
        generate_day_nwb(animal,s)