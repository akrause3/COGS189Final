import mindwave, time, datetime, sys, keyboard, csv, os.path

Hz = 128
Event_Cooldown = 5
fields = ["Time","Raw_Wave","Attention","Meditation","Is_Event"]

def makeFile():
    directory = './data/'
    if not os.path.isdir(directory):
        os.mkdir(directory)

    ppt = input("Enter Participant Name and Trial(e.g. John1): ")
    filename = "{}.csv".format(ppt)
    truePath = os.path.join(directory,filename)

    if(os.path.isfile(truePath)):
        txt = input("File Already Exists, would you like to overwrite? (y/n)")
        if(txt=='y'):
            os.remove(truePath)

    while os.path.isfile(truePath):
        ppt = input("New Trial Name: ")
        filename = "{}.csv".format(ppt)
        truePath = os.path.join(directory,filename)

    return os.path.join(directory,filename)

def writeRow(dir,row):
    with open(dir, 'a',newline='') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(row)

def ConnectHeadset():
    print("Connecting")
    headset = mindwave.Headset('COM3')
    time.sleep(4.1)
    print("Connected!")
    return headset

def RunTest(headset):
    try:
        while (headset.poor_signal > 15):
            print("Noise =  %d. Adjust the headset and the earclip." % (headset.poor_signal))
            time.sleep(0.1)

        print("Noise OK, keep your head still and press 'Num-Pad 7' to begin and end recording")
        keyboard.wait('7')

        print("Begining Recording" )
        time.sleep(1)
        event_label = 0
        stime = time.time()
        last_event = -999999
        prevTime = 0
        while True:
            cycle_start_time = time.time()
            if headset.poor_signal > 15 :
                print("Noise =  %d. Adjust the headset and the earclip." % (headset.poor_signal))
                ## just give array of 0's
                data = [round(time.time()-stime,5),0,0,0,0]
                writeRow(path,data)
            else :
                if(keyboard.is_pressed('9') and (time.time()-last_event > Event_Cooldown)) :
                    print('Mark Timestamp')
                    last_event = time.time()
                    event_label = 1
                else:
                    event_label = 0
                ##print data to csv (time,rawwave,attent,medit,event_log)
                data = [round(time.time()-stime,5),headset.raw_value,headset.attention,headset.meditation,event_label]
                writeRow(path, data)
            timeDiff = int(time.time()-stime)
            if(timeDiff != prevTime) :
                print("seconds elapsed: " + str(timeDiff))
                prevTime = timeDiff


            time.sleep((1/Hz) - (time.time() - cycle_start_time + 0.0005))
            if(keyboard.is_pressed('7')):
                break

    finally:
        print("Closing!")
        headset.stop()

path = makeFile()
writeRow(path,fields)
h1 = ConnectHeadset()
RunTest(h1)



