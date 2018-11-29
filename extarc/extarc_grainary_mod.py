### GRAINARY MODULE

from collections import defaultdict
from datetime import timedelta
import re

## Variables

# Definition of specific variables
operator = "Zdenko Vozár"
g_standard = "Grainery 0.35"

# Definition of general variables
DEFAULT = "NA"
T = "b" == "b"
F = "a" == "b"
root = "/home/lindon/Documents/NKCR/Webarchiv/WARCis"

# Counters and dictionaries of objects
n_wrc = 0
n_wrc_abs = 0 #absolute number of objects
n_cdx = 0
n_hrv = 0
d_wrc = {}
d_hrv = defaultdict(int)
d_hrv_help = dict()
all_hrv = []
all_hrv_dict = []

# Short helping formats

# To all_hrv
class hrv_dict_r(dict):
    def __init__(self, iPO, n_wrc, l_wrc, uri): #TODO priprav na duplicitne cesty
        self['name'] = iPO
        self['n_wrc'] = n_wrc
        self['l_wrc'] = l_wrc
        self['uri'] = uri


## Other functions

# Format time
def timnow(time):
    ret = str(time.strftime("%Y-%m-%dT%H:%M:%SZ"))  #pytz.timezone('Europe/Prague')
    return ret


## Grainary 0.3

# Deprecated
depr_cont = ['http-header-user-agent','description', 'http-header-from']
depr_hrv = ['dateOfOrigin', 'status', 'date', 'harvestId']

# ToSet
toset_hrv = ['harvestName','size', 'harvestDuration', 'harvestId', 'date']

# Case mapping to Grainary for warc export

def switch_wrc(warcdict):
    dictwarcswitch = {
        "WARC-Type": "warcType",
        "WARC-Date": "dateOfOrigin",
        "WARC-Filename": "filename",
        "WARC-Record-ID": "warcID",
        "Content-Type": "mimetypeXML",
        "Content-Length": "contentLength",
        "software": "software",
        "ip": "ip",
        "hostname": "hostname",
        "format": "format",
        "conformsTo": "conformsTo",
        "operator": "operator",
        "publisher": "publisher",
        "audience": "audience",
        "isPartOf": "isPartOf",
        "description": "description",                         # throwing out nine types bacha na ceske znaky #deprecated (should be included)
        "robots": "robots",
        "http-header-user-agent": "http-header-user-agent",       # depr. settings crawlu
        "http-header-from": "http-header-from",            # depr. settings crawlu
    }
    #vallue = dic.get(liner[0], "Unmapped element of Grainery 0.28") #Definition with lambda
    return dict((dictwarcswitch[key], value) for (key, value) in warcdict.items())


## Defining leading objects types

# Type Harvest

class hrv(object):
    def __init__(self, datetime):
        self.recType = "harvest"
        self.author = operator
        self.date = datetime
        self.standard = g_standard
        self.harvest = dict()
        #self.harvestDMDSec = dict()
        self.harvestCrawl = dict()
        self.commentaries = dict()
        self.paths = dict()
        self.revision = dict()


# Type Container

class wrc(object):
    def __init__(self, datetime):
        self.recType = "container"
        self.author = operator
        self.date = datetime
        self.standard = g_standard
        self.container = dict()
        self.type = dict()
        self.paths = dict()
        self.revision = dict()

## Defining unique objects sublasses and their methods

# WARC container

class container(dict):
    def __init__(self):
        self['filename'] = DEFAULT
        self['warcID'] = DEFAULT
        self['isPartOf'] = DEFAULT
        self['hostname'] = DEFAULT
        self['ip'] = DEFAULT
        self['contentLength'] = DEFAULT
        self['operator'] = DEFAULT
        self['robots'] = DEFAULT
        self['software'] = DEFAULT
        self['dateOfOrigin'] = DEFAULT
        #self['timestamp'] = DEFAULT
        #self['method'] = DEFAULT   toDefine
        #self['size'] = DEFAULT
    def app_rec(self, rec, size):
        for key, value in self.items():
            if key not in depr_cont:
                self[key] = rec[key]
        self.update({'size': size})
        a = re.sub("<|>","",self['warcID'])
        self.update({'warcID':a})
        return self

# Harvest matrix

class harvest(dict):
    def __init__(self):   #TODO elements non validated, only through revision of all warc records, step CONSOLIDATION, verify folder, verify childrens, verify logs
        #self['harvestName'] = DEFAULT   #def down
        self['status'] = "NonValidated"
        self['date'] = DEFAULT
        self['harvestId'] = DEFAULT
        self['description'] = DEFAULT
        self['operator'] = DEFAULT
        self['operator'] = DEFAULT
        self['publisher'] = DEFAULT
        self['audience'] = DEFAULT
        self['robots'] = DEFAULT
        self['http-header-user-agent'] = DEFAULT
        self['http-header-from'] = DEFAULT
        #self['harvestType'] = DEFAULT #TODO regex, staci type
        #self['harvestDuration'] = DEFAULT
        #self['size'] = DEFAULT  #def down
    def app_rec(self, hrv_name, rec, size, uuid):
        notregard = toset_hrv + depr_hrv
        for key, value in self.items():
            if key not in notregard:
                self[key] = rec[key]
        self.update({'harvestName': hrv_name})
        self.update({'size': size})
        self.update({'harvestDuration': DEFAULT})
        self.update({'harvestId' : uuid})
        self.update({'date':rec['dateOfOrigin']})
        return self
    def upd_size(self, size):
        self['size']+=size
        return self

# More info about logs crawl folder

class harvestCrawl(dict):
    def __init__(self):   #TODO, unzip, parse
        self['logs'] = DEFAULT
        self['path'] = "NonValidated"
        self['filename'] = DEFAULT
        #self['logsHarvestB'] = F
        #self['logsHarvest'] = DEFAULT
        #self['reportsHarvestB'] = F
        #self['reportsHarvest'] = DEFAULT
        #self['actionsDoneHarvestB'] = F
        #self['actionsDoneHarvest'] = DEFAULT
        #self['seedsListB'] = F
        #self['seedsList'] = DEFAULT
    def app_rec(self, rec):
        for key, value in self.items():
            self[key] = rec[key]
        return self


## Defining modulary sublasses and their methods

# Type subclass

class type(dict):
    def __init__(self):
        self['format'] = DEFAULT
        self['conformsTo'] = DEFAULT
        self['warcType'] = DEFAULT
        self['mimetypeXML'] = DEFAULT
    def app_rec(self, rec):
        for key, value in self.items():
            self[key] = rec[key]
        return self

# Paths subclass

class paths(dict):
    def __init__(self):
        self['storage'] = DEFAULT
        self['mount'] = DEFAULT
        self['pathToHarvest'] = DEFAULT
        self['LTP'] = DEFAULT
        self['harvestID'] = DEFAULT
        self['cdxID'] = DEFAULT
    def app_rec(self, path):
        strp = str(path) #TODO split when system mount, add mount
        self['pathToHarvest'] = strp
        return self

# Revision subclass

class revision(dict):
    def __init__(self):
        self['dateOfValidation'] = DEFAULT
        self['statusOfValidation'] = DEFAULT #FIRST, FIRST-FAILED, VALIDATED, TOBEVALIDATED, FAILED
        self['nextLastDateOfValidation'] = DEFAULT
        self['hashOrig'] = DEFAULT
        self['hashLast'] = DEFAULT #TODO add hashLinuxfixity
    def app_rec(self, first, datetime, hashmd5):
        self['dateOfValidation'] = datetime
        if first:
            if hashmd5 is not "NA":
                self['statusOfValidation'] = "FIRST"
                self['dateOfValidation'] = timnow(datetime)
                self['nextLastDateOfValidation'] = timnow(datetime+ timedelta(days=730))
                self['hashOrig'] = hashmd5
            else:
                self['statusOfValidation'] = "FIRST-FAILED"
                self['dateOfValidation'] = timnow(datetime)
                self['nextLastDateOfValidation'] = timnow(datetime+ timedelta(days=30))
                self['hashOrig'] = hashmd5
        else:
            if hashmd5 is not "NA":
                self['statusOfValidation'] = "VALIDATED"
                self['dateOfValidation'] = timnow(datetime)
                self['nextLastDateOfValidation'] = timnow(datetime + timedelta(days=730))
                self['hashLast'] = hashmd5
            else:
                self['statusOfValidation'] = "FAILED"
                self['dateOfValidation'] = timnow(datetime)
                self['nextLastDateOfValidation'] = timnow(datetime + timedelta(days=30))
                self['hashLast'] = hashmd5

        return self

# Commentaries subclass

class commentaries(dict):
    def __init__(self):
        self['exists'] = F
        self['text'] = DEFAULT
    def app_rec(self, rec):
        for key, value in self.items():
            self[key] = rec[key]
        return self

