#!/usr/bin/env python3
import sys
import os as os
import subprocess
#from collections import defaultdict
import re
#import json
import pytz
import datetime
import pprint
import shlex
from pymongo import MongoClient
import uuid
import extarc_grainary_mod
from hashlib import md5

## Tools settings
#sys.stdout.reconfigure(encoding='utf-8')

all_hrv= []
hrv_ind = dict

pp = pprint.PrettyPrinter(indent=4)

ts = datetime.datetime.now().timestamp()
print(ts)

mongo = MongoClient()

db = mongo.mydb #prod grainery
collection_harvest = db.harvest
collection_container = db.container

## Def. of processes
def read_warctop(arg): #update also for unfinished warcs
    warcrex = dict()
    r = subprocess.Popen(arg, stdout=subprocess.PIPE, shell=True)  # be aware tu run LOCALLY!!
    while True:
        output = r.stdout.readline().decode('utf-8')
        if output == '' and r.poll() is not None:
            break
        if output:
            output = output.strip()# Empty str
            output = output
            # Reading lines
            if len(output) > 1:
                liner = output.split(": ", 1)  # Setting maxsplit 1+1
                if len(liner) == 1:  # Checking splitting  WARC/1 and " "
                    warcrex["format"] = liner[0]  # wrc rec head
                else:
                    warcrex[liner[0]] = liner[1]
    rc = r.poll()
    if not bool(warcrex):
        rc = 999
        warcrex2 = {}
    else:
        try:
            warcrex2 = grainarymod03.switch_wrc(warcrex)  # Updating semantics via dict switch
        except:
            print("Exception in user code:")
            print('-' * 30)
            traceback.print_exc(file=sys.stdout)
            print('-' * 30)
        #pp.pprint(warcrex2)
    return (rc, warcrex2)

def create_hash(arg): #update also for unfinished warcs
    argsl = shlex.split(arg)
    r = subprocess.Popen(argsl, stdout=subprocess.PIPE)  # be aware tu run LOCALLY!!
    output, err = r.communicate()
    print("MD5 : ", error)
    if error > 0:
        output = "NA"
    else:
        output = output.decode('ascii').rstrip()
        output = output.split(" ", 1)
        output = output[0]
    return (error, output)


##Running main
if __name__ == "__main__":
    for (dirname, dirs, files) in os.walk(grainarymod03.root):
        #setting root
        for filename in files:
            # os.listdir(directory):
            record = ""
            if filename.endswith(".warc.gz"):  ##TODO acc. also to unfinished warcs
                thefile = os.path.join(dirname, filename) #prefering absolute paths, cause od diff python pointers
                grainarymod03.n_wrc_abs+=1
                warc_name=filename
                print(filename)

                ## Generation of datas using shell commands
                print(thefile)
                print(filename)
                arg = "gunzip -c " + thefile + " | head -c 1K -n 22"
                (error, warcrec) = read_warctop(arg)
                arg = "md5sum " + thefile
                (error_h, hsh) = create_hash(arg)

                if error == 0:
                    # Outside measures
                    size= os.path.getsize(thefile)
                    print(filename, " : ", size)
                    # Init obj
                    timenow = grainarymod03.timnow(datetime.datetime.now())
                    timenow_raw = datetime.datetime.now() # TODO rozmysliet kde umiestnit
                    obj = grainarymod03.wrc(timenow)
                    objcon = grainarymod03.container()
                    objtyp = grainarymod03.type()
                    objpaths = grainarymod03.paths()
                    objrev = grainarymod03.revision()
                    #print(obj.__dict__.keys())
                    #print(dir(obj))
                    # este pridat kontrolu ci naozaj obsahuje deklarovany subset, inak try max
                    print(warcrec)

                    # Check harvest dict
                    iPO= warcrec["isPartOf"]
                    iPO= str(iPO)
                    if iPO not in grainarymod03.d_hrv:
                        hrv_ind.update({iPO: grainarymod03.n_hrv}) #going from zero ind
                        grainarymod03.n_hrv+=1
                        grainarymod03.n_wrc+=1
                        print("======== N E W : : : ", iPO ," : : : : H A R V E S T ========")
                        grainarymod03.d_hrv.update({iPO : 1})
                        grainarymod03.d_hrv_help.update({grainarymod03.n_hrv : iPO})  # Help dict, indices of main hrvobj_hrv list
                        all_hrv.append(grainarymod03.hrv(timenow)) #vytvor nove sklizne do pola sklizni
                        hrvobj_hrv = grainarymod03.harvest()       #harvest obj
                        hrvobj_crw = grainarymod03.harvestCrawl()
                        hrvobj_comm = grainarymod03.commentaries()
                        hrvobj_paths = grainarymod03.paths()
                        hrvobj_rev = grainarymod03.revision()
                        uid_hrv= str(uuid.uuid5(uuid.NAMESPACE_DNS, iPO)) #Dohodit do modu asi
                        hrvobj_hrv.app_rec(iPO, warcrec, size, uid_hrv) # pridavanie k harvest containeru este vyladit, ale kombo mena a DNS

                        #List filenames of Warcs a helping dict
                        l_wrc = []
                        l_wrc.insert(1,filename)
                        grainarymod03.all_hrv_dict.append(grainarymod03.hrv_dict_r(iPO, grainarymod03.n_hrv, l_wrc, uid_hrv))

                        #Final establshment of object
                        all_hrv[grainarymod03.n_hrv-1].harvest = hrvobj_hrv
                        all_hrv[grainarymod03.n_hrv - 1].harvest = hrvobj_hrv
                        all_hrv[grainarymod03.n_hrv - 1].harvestCrawl = hrvobj_crw
                        all_hrv[grainarymod03.n_hrv - 1].commentaries = hrvobj_comm
                        all_hrv[grainarymod03.n_hrv - 1].paths = hrvobj_paths
                        all_hrv[grainarymod03.n_hrv - 1].revision = hrvobj_rev
                        pp.pprint(all_hrv[grainarymod03.n_hrv-1].__dict__)
                    else:
                        grainarymod03.n_wrc+=1
                        grainarymod03.d_hrv[iPO] +=1
                        pp.pprint(grainarymod03.all_hrv_dict)

                        #Setting from harvest and to harvest rec
                        print("IPPPPPPPPPPPPPPPPPPPO ", grainarymod03.d_hrv_help)
                        #hrvobj_hrv.upd_size(size) where name is iPO, incrmentovat velkost, presunut definiciu
                    ###for key, value in grainarymod03.d_hrv_help:
                       # if iPO in
                    objcon  = grainarymod03.container.app_rec(objcon,warcrec, size)
                    objtyp  = grainarymod03.type.app_rec(objtyp, warcrec)
                    objpaths = grainarymod03.paths.app_rec(objpaths, dirname)
                    objrev = grainarymod03.revision.app_rec(objrev,True,timenow_raw,hsh)
                    obj.container = objcon
                    obj.type = objtyp
                    obj.paths = objpaths
                    obj.revision = objrev
                    pp.pprint(obj.__dict__)

                    ##Injection
                    # collection_container.insert_one(obj.__dict__)
                else:
                    print("Bad reading, code : ", error)

print("Harvests count : ", len(grainarymod03.d_hrv_help))
print("Harvest and number of their containers: ")
for key, value in grainarymod03.d_hrv.items():
    print(key, " number of warcs: ", value)
print("Absolute number of warc objects consulted: ", grainarymod03.n_wrc_abs)
print("Number of warc objects created: ", grainarymod03.n_wrc)
#print json.dump(obj, indent=1)
# TODO dodat do DB sklizne
#TODO pridat zoznamy vsetkych warcov, vs konzultovanych, diff aka errors a hlasky
print("FINISHED")
