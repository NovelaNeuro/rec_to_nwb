from generate_day_yaml import generate_day_yaml

animal_list = ['montague','despereaux','jaq','roquefort']

sess_ana = []
sess_ana.append([3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
sess_ana.append([3,4,5,6,7,8,9,10,11,12,13,14])
sess_ana.append([6,7,8,9,10,11,12,13,14,15,16,17,18])
sess_ana.append([7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22])

for animal, sess in zip(animal_list, sess_ana):
    for s in sess:
        print('starting ' + animal + ' session ' + str(s))
        generate_day_yaml(animal,s)
        
       
