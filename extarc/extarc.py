#!/usr/bin/env python3
import sys
import os as os
import subprocess
#from collections import defaultdict
import re
#import json
#from bson import json_util
import pytz
import time
import datetime
import pprint
import shlex
from pymongo import MongoClient
import uuid
import grainery
#from hashlib import md5  # using system, maybe to change



## Variables

# Extarc specific variables

version = 3.5   # Version of Extarc itself
all_hrv = []    # All harvest dictionary
ipo_dict = dict #  IPO dict Going from One

time_of_run =  grainery.timnow(datetime.datetime.now())
time_of_run_s = time.time()

# Tools settings
#sys.stdout.reconfigure(encoding='utf-8')

pp = pprint.PrettyPrinter(indent=4)

ts = datetime.datetime.now().timestamp()
print(ts)

mongo = MongoClient()

db = mongo.mydb #prod grainery
collection_harvest = db.harvest
collection_container = db.container



## Def. of processes

def jsonDefault(OrderedDict):
    return OrderedDict.__dict__

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
            warcrex2 = grainery.switch_wrc(warcrex)  # Updating semantics via dict switch
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


##  Running main

if __name__ == "__main__":
    print("======== I n i t i a l i z i n g  E X T A R C ", version ,"  ========")
    print("\n  ++ Standard: ", grainery.g_standard, " ++\n  ++ Module version: ", grainery.version, " ++\n")
    for (dirname, dirs, files) in os.walk(grainery.root):
        print("\n ======== W A L K I N G : : : : ", dirname, " : : : :  ======== \n")
        for filename in files:
            # os.listdir(directory):
            record = ""
            if filename.endswith(".warc.gz"):  ##TODO acc. also to unfinished warcs
                thefile = os.path.join(dirname, filename) #prefering absolute paths, cause od diff python pointers
                grainery.n_wrc_abs+=1
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
                    timenow = grainery.timnow(datetime.datetime.now())
                    timenow_raw = datetime.datetime.now() # TODO rozmysliet kde umiestnit
                    obj = grainery.Wrc(timenow)
                    objcon = grainery.Container()
                    objtyp = grainery.Type()
                    objpaths = grainery.Paths()
                    objrev = grainery.Revision()
                    print(warcrec)

                    # Check harvest dict
                    iPO= warcrec["isPartOf"]
                    iPO= str(iPO)
                    if iPO not in grainery.d_hrv:
                        grainery.n_hrv+=1
                        grainery.n_wrc+=1
                        print("\n ======== N E W : : : : ", iPO ," : : : : H A R V E S T ======== \n")
                        ipo_dict.update({grainery.n_hrv : iPO })

                        grainery.d_hrv.update({iPO : 1})
                        grainery.d_hrv_help.update({grainery.n_hrv : iPO})  # Help dict, indices of main hrvobj_hrv list

                        all_hrv.append(grainery.Hrv(timenow)) #vytvor nove sklizne do pola sklizni
                        hrvobj_hrv = grainery.Harvest()       #harvest obj
                        hrvobj_crw = grainery.HarvestCrawl()
                        hrvobj_comm = grainery.Commentaries()
                        hrvobj_paths = grainery.Paths()
                        hrvobj_rev = grainery.Revision()
                        uid_hrv= str(uuid.uuid5(uuid.NAMESPACE_DNS, iPO)) #Dohodit do modu asi
                        hrvobj_hrv.app_rec(iPO, warcrec, size, uid_hrv) # pridavanie k harvest containeru este vyladit, ale kombo mena a DNS

                        #List filenames of Warcs a helping dict
                        l_wrc = []
                        l_wrc.insert(1,filename)
                        grainery.all_hrv_dict.append(grainery.hrv_dict_r(iPO, grainery.n_hrv, l_wrc, uid_hrv, size))

                        #Final establshment of object
                        all_hrv[grainery.n_hrv-1].harvest = hrvobj_hrv
                        all_hrv[grainery.n_hrv - 1].harvest = hrvobj_hrv
                        all_hrv[grainery.n_hrv - 1].harvestCrawl = hrvobj_crw
                        all_hrv[grainery.n_hrv - 1].commentaries = hrvobj_comm
                        all_hrv[grainery.n_hrv - 1].paths = hrvobj_paths
                        all_hrv[grainery.n_hrv - 1].revision = hrvobj_rev
                        pp.pprint(all_hrv[grainery.n_hrv-1].__dict__)
                    else:
                        grainery.n_wrc+=1
                        grainery.d_hrv[iPO] +=1
                        pp.pprint(grainery.all_hrv_dict)

                        print(ipo_dict)
                        for item in  grainery.all_hrv_dict.__iter__():
                            print(item)
                            if item['name'] == iPO:
                                uid_hrv = item['uri']               ## TODO size and l_wrc list to all_hrv list
                                item['l_wrc'].append(filename)
                                old_siz = item['size']
                                item['size']= old_siz + size

                        #Setting from harvest and to harvest rec
                        #print("IPPPPPPPPPPPPPPPPPPPO ", grainery.d_hrv_help)
                        #print("IPPPO rec:", grainery.all_hrv_dict[0])


                    #Init warc rec object
                    objcon  = grainery.Container.app_rec(objcon,warcrec, size)
                    objtyp  = grainery.Type.app_rec(objtyp, warcrec)
                    objpaths = grainery.Paths.app_rec(objpaths, dirname, uid_hrv)
                    objrev = grainery.Revision.app_rec(objrev,True,timenow_raw,hsh)
                    obj.container = objcon
                    obj.type = objtyp
                    obj.paths = objpaths
                    obj.revision = objrev

                    #Serialization and injection of containers to Mongo DB
                    # pp.pprint(obj.__dict__)
                    #print(json.dumps(jsonDefault(obj), indent=4))
                    collection_container.insert_one(obj.__dict__)
                else:
                    print("Bad reading, code : ", error)

## Final procedures

# Completing harvest: size, list of warcs
print("\n \n \n ======== S U M M A R Y : : : : ", time_of_run ," : : : : R U N ======== \n")
print("\n ======== : : : : H A R V E S T S : : : :  ======== \n")
i = 0
for item in all_hrv:
    item.harvest['size'] = grainery.all_hrv_dict[i]['size']
    #item.harvestUTI.filename = grainery.all_hrv_dict[i]['l_wrc'] # TODO filenames somewhere, or uris
    item.harvest['warcsNumber'] = len(grainery.all_hrv_dict[i]['l_wrc'])
    i += 1
    print(item.harvest['harvestName'], ' :: size :: ', item.harvest['size'], ' :: :: ',item.harvest['warcsNumber'] , ' :: uri :: ', item.harvest['harvestId'])

# Serialization and injection of harvests to MongoDB

for harvest in all_hrv:
    collection_harvest.insert_one(harvest.__dict__)

# Printing harvest final summaries
print("All hrv dict : ", grainery.all_hrv_dict)
#print("Not sure:", grainery.d_hrv)  = if iPO not in grainery.d_hrv: # TODO deprecate old helping variables
print("Total harvests count : ", len(all_hrv))

print("\n ======== : : : : W A R C S : : : :  ======== \n")
print("Absolute number of warc objects consulted: ", grainery.n_wrc_abs)
print("Number of warc objects created: ", grainery.n_wrc)
#TODO pridat zoznamy vsetkych warcov, vs konzultovanych, diff aka errors a hlasky
print("\n \n \n ======== : : : : FINISHED in "," : : : %.1f seconds." % (time.time() - time_of_run_s)," : : : : ======== ")
