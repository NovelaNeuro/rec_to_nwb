import math
import struct
import re
import time
import random
import numpy as np
import pyaudio
import wave
from itertools import compress

# V8pre_forage
# visits to incorrect wells cause 5s lockout
# exception is repeat visit to prior well (is ok, no lockout)
# can go to any outer well, any number of times
# lockout from getting rip/wait wells wrong is also 5s


# decide what type of up trigger was just recieved; act accordingly
# only for home and outer, center well defined in statescript
def pokeIn(dio):
	global homeWell
	global centerWell
	global outerWells
	global currWell
 
	currWell = int(dio[1])
	# no home: not using
	if currWell == homeWell: 
		doHome()

	# how do we start???
	# for testing we could start with an outer well visit

	for num in range(len(outerWells)):
		if currWell == outerWells[num]:
			doOuter(num)

# decide what type of down trigger was just recieved; act accordingly
def pokeOut(dio):
	global homeWell
	global centerWell
	global outerWells
	global currWell
	global lastWell
 
	currWell = int(dio[1])
	# no home: not using
	if currWell == homeWell: 
		endHome()

	# MEC commented out - moved to callback section
	#if currWell == centerWell: 
	#	endWait()    
	for num in range(len(outerWells)):
		if currWell == outerWells[num]:
			endOuter()
	lastWell = currWell

# NOTE: currently NOT calling this function
# instead use endOuter to start new trial
#home poke: decide trial type and upcoming wait length; turn on lights accordingly
# def doHome():
# 	global trialtype  # 0 go to home,1 go to center, 2 go to outer, 3 lockout
# 	global homePump
# 	global lastWell
# 	global currWell
# 	global goalWell
# 	global outerWells

# 	if trialtype == 0:	
# 		trialtype = 1
# 		print("SCQTMESSAGE: trialtype = "+str(trialtype)+";\n")
# 		# this line set the variable delaytime and then writes the variable to statescript  
# 		delaytime = chooseDelay()
# 		print("SCQTMESSAGE: waittime = "+str(delaytime)+";\n")

# 		# set goal well to 1 arm for this trial - get line from old script
# 		# set goal well based on replay content from spykshrk after enough visits to each arm

# 		# yes this is wrong for content rewared wells, but content information will reset
# 		# goalWell in beep function
# 		# this is where cued trials are set and we want to control disrubiton 
# 		#goalWell = np.random.choice(outerWells,1,replace=False)
# 		print("SCQTMESSAGE: homeCount = homeCount + 1;\n") # update homecount in SC
# 		print("SCQTMESSAGE: rewardWell = "+str(homePump)+";\n")
# 		print("SCQTMESSAGE: trigger(1);\n")   # deliver reward
# 	#check for home poke out of sequence, start lockout 1
# 	elif trialtype > 0 and trialtype < 3 and lastWell != currWell:
# 		lockout([0,1])

def chooseDelay():
    global trialtype
    global centercount
    global waitdist
    global startwaitdist

    #print(centercount)

    if centercount<3:  #first 3 trials of of each type should be short
        return startwaitdist[centercount]

    else:
        if centercount<=10:  #trials 4-10 of each type will be avg of startwaitdist and normal waitdist
            return int(round(np.mean([int(np.random.choice(startwaitdist,1)), int(np.random.choice(waitdist,1))])))

        else: # all trial 10 and later
            return int(np.random.choice(waitdist,1))

# NOTE: currently NOT calling this function
# def endHome():
# 	global trialtype
# 	global lastWell
# 	global homeWell
# 	global centerWell

# 	if trialtype == 1:
# 		print("SCQTMESSAGE: dio = "+str(centerWell)+";\n")   # turn on light in center well
# 		print("SCQTMESSAGE: trigger(3);\n")
# 		print("SCQTMESSAGE: dio = "+str(homeWell)+";\n")
# 		print("SCQTMESSAGE: trigger(4);\n")
# 		print("SCQTMESSAGE: trigger(5);\n")   # display stats

#function: add time to wait dist. 
def addtime(newtime):
	global count
	global waitdist

	count+=1
	# % means mod (reaminder) function
	waitdist[count%8] = int(newtime[1])  #new time 1 will be timediff, not timestamp
	print(waitdist)

def beep():
	global centerPump
	global centerWell
	global trialtype
	global currWell
	global centercount

	centercount+=1
	# begin outer arm trial section of task
	trialtype = 2                   # ready for outer visit
	print("SCQTMESSAGE: trialtype = "+str(trialtype)+";\n")
	#deliver reward
	if currWell == centerWell:
		print("SCQTMESSAGE: rewardWell = "+str(centerPump)+";\n")
	print("SCQTMESSAGE: trigger(1);\n")
	print("SCQTMESSAGE: centerCount = centerCount + 1;\n") # update centercount in SC

# define goalWell
def chooseGoal():
	global taskState
	global replay_arm
	global outerarm_required_rewards
	global arm1_Goal
	global arm2_Goal
	global arm3_Goal
	global arm4_Goal
	global goalWell
	global outerWells

	# taskstate ==1 is cued visits to each outer arm
	if taskState == 1:
		# this is boolean way of setting this to 1 or 0
		# valid+_goals is not global just local to this funciton
		valid_goals = [arm1_Goal<outerarm_required_rewards,
					   arm2_Goal<outerarm_required_rewards,
					   arm3_Goal<outerarm_required_rewards,
					   arm4_Goal<outerarm_required_rewards]
		print(valid_goals)
		# this line doesnt work
		#print(outerWells[valid_goals])
		# try this:
		print(list(compress(outerWells,valid_goals)))

		# now only choose from list of outerwells where valid_goals == 1
		goalWell = np.random.choice(list(compress(outerWells,valid_goals)),1,replace=False)
		print('cued goalWell is: ',goalWell)
		print("SCQTMESSAGE: disp('CUED ARM VISITS "+str(outerarm_required_rewards)+"');\n")

	# for return to cued visits used 2*outerarm_required_rewards as cutoff
	elif taskState == 3:
		# this is boolean way of setting this to 1 or 0
		# valid+_goals is not global just local to this funciton
		valid_goals = [arm1_Goal<2*outerarm_required_rewards,
					   arm2_Goal<2*outerarm_required_rewards,
					   arm3_Goal<2*outerarm_required_rewards,
					   arm4_Goal<2*outerarm_required_rewards]
		print(valid_goals)
		# this line doesnt work
		#print(outerWells[valid_goals])
		# try this:
		print(list(compress(outerWells,valid_goals)))

		# now only choose from list of outerwells where valid_goals == 1
		goalWell = np.random.choice(list(compress(outerWells,valid_goals)),1,replace=False)
		print('cued goalWell is: ',goalWell)
		print("SCQTMESSAGE: disp('CUED ARM VISITS "+str(outerarm_required_rewards)+"');\n")

		#goalWell = np.random.choice(outerWells[valid_goals],1,replace=False)


	# if taskState == 2, content trials
	# define goalWell as outerwell matching replay arm
	# replay_arm - 1 to make 0 based becuase it is used an an index into outerWells
	# if replay arm not updated will index to -1 and error out
	# NEW: no goalwell if content trials
	else:
		#goalWell = [outerWells[replay_arm-1]]
		#print('content goalWell is: ',goalWell)
		#print('replay arm is: ',replay_arm)
		print('content trial - no outer arm goals')



def endWait():
	global trialtype
	global goalWell
	global currWell
	global outerWells
	global arm1_Goal
	global arm2_Goal
	global arm3_Goal
	global arm4_Goal

	if trialtype == 2:   # wait complete

		print("SCQTMESSAGE: dio = "+str(currWell)+";\n")     # turn off rip light
		print("SCQTMESSAGE: trigger(4);\n")	

		print("SCQTMESSAGE: trigger(5);\n")   # display stats
		print("SCQTMESSAGE: disp('CURRENTGOAL IS "+str(goalWell[0])+" TASK_STATE IS "+str(taskState)+"');\n") 
		
		# use taskState to determine whether this is a cued trial or content trial
		# only for which outer lights to turn on
		if taskState == 1:
			# turn on light for goalWell only
			# brackets required to get integer only for statescript
			print("SCQTMESSAGE: dio = "+str(goalWell[0])+";\n")
			print("SCQTMESSAGE: trigger(3);\n")

		elif taskState == 3:
			# turn on light for goalWell only
			# brackets required to get integer only for statescript
			print("SCQTMESSAGE: dio = "+str(goalWell[0])+";\n")
			print("SCQTMESSAGE: trigger(3);\n")


		# taskState = 2
		# this may or may not happen...
		#else:
			# NEW: no outer arms - so re-start wait here
			# we want this wait to have no light, turn on light after wait ends
			# function 16 turns on light and makes beep after wait
			
			#trialtype = 1
			#print('first content trial, in endWait')
			#print("SCQTMESSAGE: trigger(16);\n")

			# the statescript function for each arm now produces the beep after recieving the REPLAY_ARM message
			# so goalWell should be updated based on the message from spykshrk not the random number
			## turn on all outer lights
			#for num in range(len(outerWells)):
			#	print("SCQTMESSAGE: dio = "+str(outerWells[num])+";\n")
			#	print("SCQTMESSAGE: trigger(3);\n")
			#	print('current goal is ',str(goalWell[0]))

			#print("SCQTMESSAGE: dio = "+str(centerWell)+";\n")   # turn center light on
			#print("SCQTMESSAGE: trigger(3);\n")
			#print("SCQTMESSAGE: trigger(5);\n")   # display stats


		# save out current goal well to the text file
		#with open("/home/lorenlab/spykshrk_realtime/config/rewarded_arm_trodes.txt","a") as reward_arm_file:
		#		try:
	#				reward_arm_file.write(str(currWell-9)+' '+str(taskState)+' '+str(goalWell[0]-9)+'\n')
		#		finally: 
		#			reward_arm_file.close()


def doOuter(val):
	global outerPumps
	global trialtype
	global allGoal
	global goalWell 
	global currWell
	global lastWell
	global homeWell
	global waslock
	global arm1_Goal
	global arm2_Goal
	global arm3_Goal
	global arm4_Goal
	global taskState
	global outerarm_required_rewards

	if trialtype == 2:
		trialtype = 1      # outer satisfied, old: head home next (0). new: head to center (1)
		print("SCQTMESSAGE: trialtype = "+str(trialtype)+";\n")
		print('current well',currWell)
		print('goal well',goalWell)
		if currWell in goalWell :  # repeated; reward
			print("SCQTMESSAGE: rewardWell = "+str(outerPumps[val])+";\n")
			print("SCQTMESSAGE: trigger(2);\n")   # deliver reward
			allGoal+=1
			# create and add to counter for each of the 4 outer arms
			if currWell == outerWells[0]:
				arm1_Goal+=1
				#print('arm1',arm1_Goal)
			elif currWell == outerWells[1]:
				arm2_Goal+=1
				#print('arm2',arm2_Goal)
			elif currWell == outerWells[2]:
				arm3_Goal+=1
				#print('arm3',arm3_Goal)
			elif currWell == outerWells[3]:
				arm4_Goal+=1
				#print('arm4',arm4_Goal)
			print('arm1',arm1_Goal,'arm2',arm2_Goal,'arm3',arm3_Goal,'arm4',arm4_Goal)

			# write to a file that will record last rewarded arm so that spykshrk can read it
			# bug: at first content trial it writes all 4 wells, not sure why, after that it works
			# write (currWell - 9) to get back to arms 1-4
			print('current well',currWell)
			with open("/home/lorenlab/spykshrk_realtime/config/rewarded_arm_trodes.txt","a") as reward_arm_file:
				try:
					reward_arm_file.write(str(currWell-9)+' '+str(taskState)+' '+str(goalWell[0])+'\n')
				finally: 
					reward_arm_file.close()

			# use this info to update taskState
			# if required rewards met for all arms, switch to content trials (taskState=2)
			# could replace this with a vector with the visits for each arm
			# 4 arms
			#if arm1_Goal>=outerarm_required_rewards and arm2_Goal>=outerarm_required_rewards and arm3_Goal>=outerarm_required_rewards and arm4_Goal>=outerarm_required_rewards:

			# end of cued trials, two arm V track:
			if taskState == 1 and arm1_Goal>=outerarm_required_rewards and arm2_Goal>=outerarm_required_rewards:
				taskState = 2
				print("SCQTMESSAGE: taskstate = "+str(taskState)+";\n") # update taskstate in SC
				print('switched to content trials')
				
			print("SCQTMESSAGE: goalTotal = "+str(allGoal)+";\n") # update goaltotal in SC

		else:   # wrong well; add to forage record if newly visited
			print("SCQTMESSAGE: otherCount = otherCount + 1;\n") # update othercount in SC

	elif trialtype < 2 and waslock<1:
		lockout([0,1])

def endOuter():
	global trialtype
	global outerWells
	global homeWell
	global lastWell
	global currWell
	global centerWell
	global taskState
	global outer_count_content

	# note: this should run at the end of the last cued trial, right after switch to taskstate 2
	if trialtype == 1 and lastWell != currWell and taskState == 1:  # outer satisfied. old: 0, new: 1
		for num in range(len(outerWells)):			# turn off outer lights
			print("SCQTMESSAGE: dio = "+str(outerWells[num])+";\n")
			print("SCQTMESSAGE: trigger(4);\n")
		# now we need to run endHome - to start wait at center
		# original
		#print("SCQTMESSAGE: dio = "+str(homeWell)+";\n")   # turn homewell on
		#print("SCQTMESSAGE: trigger(3);\n")
		#print("SCQTMESSAGE: trigger(5);\n")   # display stats
		# no home
		print("SCQTMESSAGE: dio = "+str(centerWell)+";\n")   # turn center light on
		print("SCQTMESSAGE: trigger(3);\n")
		print("SCQTMESSAGE: trigger(5);\n")   # display stats

		# this line set the variable delaytime and then writes the variable to statescript  
		delaytime = chooseDelay()
		print("SCQTMESSAGE: waittime = "+str(delaytime)+";\n")

		# we may want to define a lockout type here

	# for first content trial, run trigger 16
	elif taskState == 2 and outer_count_content == 0:
		outer_count_content += 1
		for num in range(len(outerWells)):			# turn off outer lights
			print("SCQTMESSAGE: dio = "+str(outerWells[num])+";\n")
			print("SCQTMESSAGE: trigger(4);\n")
		print('first content trial',outer_count_content)
		print("SCQTMESSAGE: trigger(5);\n")   # display stats
		print("SCQTMESSAGE: trigger(16);\n")

	# return to cued trials
	elif trialtype == 1 and lastWell != currWell and taskState == 3:  # outer satisfied. old: 0, new: 1
		for num in range(len(outerWells)):			# turn off outer lights
			print("SCQTMESSAGE: dio = "+str(outerWells[num])+";\n")
			print("SCQTMESSAGE: trigger(4);\n")
		# now we need to run endHome - to start wait at center
		print("SCQTMESSAGE: dio = "+str(centerWell)+";\n")   # turn center light on
		print("SCQTMESSAGE: trigger(3);\n")
		print("SCQTMESSAGE: trigger(5);\n")   # display stats

		# this line set the variable delaytime and then writes the variable to statescript  
		delaytime = chooseDelay()
		print("SCQTMESSAGE: waittime = "+str(delaytime)+";\n")	

def lockout(val):   # turn off all lights for certain amount of time
	global centerWell
	global outerWells
	global lastWell
	global trialtype
	global waslock

	print("lockout val "+str(val)+"\n")
	locktype = int(val[1])
	trialtype = 3
	print("SCQTMESSAGE: trialtype = "+str(trialtype)+";\n")
	print("SCQTMESSAGE: trigger(6);\n")  # start lockout timer in SCQTMESSAGE
	#turn off all lights
	print("SCQTMESSAGE: dio = "+str(homeWell)+";\n") # turn off home well
	print("SCQTMESSAGE: trigger(4);\n")
	print("SCQTMESSAGE: dio = "+str(centerWell)+";\n")  #turn off all center and outer well lights
	print("SCQTMESSAGE: trigger(4);\n")
	for num in range(len(outerWells)):
		print("SCQTMESSAGE: dio = "+str(outerWells[num])+";\n")
		print("SCQTMESSAGE: trigger(4);\n")
	waslock=1
	print("SCQTMESSAGE: waslock = "+str(waslock)+";\n") # turn off home well
	if locktype == 1:
		print("SCQTMESSAGE: locktype1 = locktype1 + 1;\n") # type 1 = wrong well order
	if locktype == 2:
		print("SCQTMESSAGE: locktype2 = locktype2 + 1;\n") # type 2 = impatience at center well

def lockend():
	global trialtype
	global homeWell

	# no home: now reset trial type to 1 not 0, and tell statescript
	trialtype = 1
	print("SCQTMESSAGE: trialtype = "+str(trialtype)+";\n")
	# home well
	#print("SCQTMESSAGE: trialtype = "+str(trialtype)+";\n")
	#print("SCQTMESSAGE: dio = "+str(homeWell)+";\n") # turn on home well
	#rint("SCQTMESSAGE: trigger(3);\n")

	# no home
	print("SCQTMESSAGE: dio = "+str(centerWell)+";\n")   # turn center light on
	print("SCQTMESSAGE: trigger(3);\n")
	print("SCQTMESSAGE: trigger(5);\n")   # display stats

	# choose wait time, tell statescript
	delaytime = chooseDelay()
	print("SCQTMESSAGE: waittime = "+str(delaytime)+";\n")

	# set last well to 10 so that loop with center well timer will run
	print("SCQTMESSAGE: lastWell = "+str(10)+";\n")

def startContentTrial():
	global trialtype
	global content_trial_dist

	# no home: now reset trial type to 1 not 0, and tell statescript
	trialtype = 1
	print("SCQTMESSAGE: trialtype = "+str(trialtype)+";\n")
	print("SCQTMESSAGE: trigger(5);\n")   # display stats

	# choose time between trials
	#content_trial_time = int(np.random.choice(content_trial_dist,1))
	# sample from exponential distribution, mean 30 sec
	# note: 3 sec is added in statescript
	content_trial_time = int(1000*(1 + np.random.exponential(scale=30, size=None)))
	print("SCQTMESSAGE: content_trial_time = "+str(content_trial_time)+";\n")

	# start new content wait time
	print('start next content trial')
	print("SCQTMESSAGE: trigger(16);\n")

def returnToCued():
	global taskState

	print('return to cued trials')
	taskState = 3
	# use lockend to start new cued trial
	lockend()

def updateWaslock(val):
	global waslock

	waslock = int(val[1])
	print("SCQTMESSAGE: waslock = "+str(waslock)+";\n")

# Function: generate cowbell sound
def generate_beep():

	File='Beep.wav'
	#File='noise.wav'
	spf = wave.open(File, 'rb')
	signal = spf.readframes(-1)
	signal = np.fromstring(signal, 'Int16')
	p = pyaudio.PyAudio()
	stream = p.open(format =
				p.get_format_from_width(spf.getsampwidth()),
				channels = 1,
				rate = spf.getframerate(),
				output = True)
	#play 
	data = struct.pack("%dh"%(len(signal)), *list(signal))    
	stream.write(data)
	stream.close()
	p.terminate()

def makewhitenoise():  #play white noise for duration of lockout
	global locksoundlength

	soundlength = int(44100*locksoundlength/1000)
	p = pyaudio.PyAudio()
	stream = p.open(format = 8, channels = 1, rate = 44100, output = True)
	whitenoise = np.random.randint(700,size = soundlength)
	data = struct.pack("%dh"%(len(whitenoise)), *list(whitenoise))    
	stream.write(data)
	stream.close()
	p.terminate()


# This is the custom callback function. When events occur, addScQtEvent will
# call this function. This function MUST BE NAMED 'callback'!!!!
def callback(line):

	global waslock
	global goalWell
	global replay_arm 

	if line.find("UP") >= 0: #input triggered
		pokeIn(re.findall(r'\d+',line))
	if line.find("DOWN") >= 0: #input triggered
		pokeOut(re.findall(r'\d+',line))
	# add ripwait to holding vector
	if line.find("riptime") >=0:
		addtime(re.findall(r'\d+',line))
	if line.find("BEEP1") >= 0: # make a beep and deliver reward
		chooseGoal()
		#beep()
	# this is only called by cued trials, remove sound cue
	if line.find("BEEP2") >= 0: # make a beep and deliver reward
		beep()
		#generate_beep()
		#mec added to turn on outer lights at same time as beep
		endWait()
	# for content trials. beep sound
	if line.find("BEEP3") >= 0: # only deliver reward
		generate_beep()
	# for content trials. reward only no beep sound
	if line.find("BEEP4") >= 0: # only deliver reward
		beep()
	
	if line.find("LOCKOUT") >= 0: # lockout procedure
		lockout(re.findall(r'\d+',line))
	if line.find("LOCKEND") >= 0: # reset trialtype to 0
		lockend()
	if line.find("WHITENOISE") >= 0: # make noise during lockout
		makewhitenoise()
	if line.find("waslock") >= 0:  #update waslock value
		updateWaslock(re.findall(r'\d+',line))
	# function for reading specific arm output from spykshrk
	# note: had to reprint statescript variable replay_arm after it comes in, in order for python to see it
	if line.find("replay_arm") >= 0:
		replay_arm = re.findall(r'\d+',line)
		replay_arm = int(replay_arm[1])
		print('replay arm from callback', replay_arm)
	# to start next content trial based on function 18 in statescript
	if line.find("NEXT_TRIAL") >= 0:
		startContentTrial()
	# to switch back to cued trials (at begin of function 16 in statescript)
	if line.find("TASKSTATE3") >= 0:
		returnToCued()	


# all global variables are initialized
# all variables can be used anywhere in this script
# define wells, old outer: 10,11,12,13
homeWell = 1
centerWell = 2
outerWells = [10,13]

# define pumps
# old outer: 19,20,21,22
homePump = 25
centerPump = 26
outerPumps = [19,22]

#global variables 
lastWell = -1
currWell = -1

# no home: initiaze with trialtype 2 (was 0 before) and turn on one outer well light
trialtype = 2


allGoal = 0

# counters for each indivudal arm
arm1_Goal = 0
arm2_Goal = 0
arm3_Goal = 0
arm4_Goal = 0
outerarm_required_rewards = 6
outer_count_content = 0

# task state variable
# 1 = cued reward well
# 2 = content contigent rewrad well
taskState = 1
# should start at -1 so that it doesnt return a real arm
# this may require a check that replay-arm does not equal -1
replay_arm = 0

# choose one well at random of the 4
# no home - try to initalize with well 10 and a list (was 0 before)
goalWell = [10]

startwaitdist = [500, 500, 500]
waitdist = [500]
content_trial_dist = [5000]
count = 0

locksoundlength = 1000
print(goalWell)
waslock=0
centercount = 0
