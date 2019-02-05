### GRAINARY MODULE

from collections import defaultdict
from datetime import timedelta
import re

## Variables

version = 3.3                                       # Version of module itself


# Definition of specific variables
operator = "Zdenko Vozár"                           # Operator of script
g_standard = "Grainery 0.36"                        # Version of standard used here
root = "/home/lindon/GIT/wa-dev/grainery/extarc"    # Root for your os walk your warcs, possible to change

# Definition of general variables
DEFAULT = "NA"
DEFAULT_b = False
T = "b" == "b"
F = "a" == "b"

# Counters and dictionaries of objects
n_wrc = 0
n_wrc_abs = 0 #absolute number of objects
n_cdx = 0
n_cdx_abs = 0 #abslotue number of cdx
n_hrv = 0
d_wrc = {}
d_hrv = defaultdict(int)
d_hrv_help = dict()
all_hrv = []
all_hrv_dict = []

# Short helping formats

# To all_hrv
class hrv_dict_r(dict):
    def __init__(self, iPO, n_wrc, l_wrc, uri, size, w_uri): #TODO priprav na duplicitne cesty
        self['name'] = iPO
        self['n_wrc'] = n_wrc
        self['l_wrc'] = l_wrc
        self['uri'] = uri
        self['w_uri'] = w_uri
        self['size'] = size


## Other functions

# Format time
def timnow(time):
    ret = str(time.strftime("%Y-%m-%dT%H:%M:%SZ"))  #pytz.timezone('Europe/Prague')
    return ret


## Grainary 0.3

# Format shell commands

def shell_comm(filename, what):
    if what == "head_cdx":
        arg = "head -n 2 " + filename
    else:
        if what == "md5sum":
            arg = "md5sum " + filename
        else:
            if what == "wc -l":
                arg = "wc -l " + filename
    return arg

# Deprecated
depr_cont = ['http-header-user-agent','description', 'http-header-from']
depr_hrv = ['dateOfOrigin', 'status', 'date', 'harvestId']

# ToSet
toset_hrv = ['harvestName', 'harvestType','harvestSubtype', 'size', 'harvestDuration', 'harvestID', 'date', 'warcsNumber']

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

def switch_cdx(cdxdict):
    dictwarcswitch = {
        #after_spec in https://iipc.github.io/warc-specifications/specifications/cdx-format/cdx-2015/
        "N": "massaged_url",
        "b": "date",
        "a": "original_url",
        "m": "mime_type_original_document",
        "s": "response_code",
        "k": "new_style_checksum",
        "r": "redirect",
        "M": "meta_tags_AIF",
        "S": "compressed_record_size",
        "V": "compressed_arc_file_offset",
        "g": "file_name",
        "format_len": "columns",            # depr. settings crawlu
    }
    return dict((dictwarcswitch[key], value) for (key, value) in cdxdict.items())

## Defining leading objects types

# Type Harvest

class Hrv(object):
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
    def upd_rec_hrv(self, size, wrc_n, uri, w_uri, uri_l):
        self.harvest['size'] = size
        self.harvest['warcsNumber'] = wrc_n
        self.paths['warcID'] = w_uri
        self.paths['warcFilenames'] = uri_l
        self.paths['harvestID'] = uri
        return self


# Type Container

class Wrc(object):
    def __init__(self, datetime):
        self.recType = "container"
        self.author = operator
        self.date = datetime
        self.standard = g_standard
        self.container = dict()
        self.type = dict()
        self.paths = dict()
        self.revision = dict()

# Type Container

class Cdx(object):
    def __init__(self, datetime):
        self.recType = "cdx"
        self.author = operator
        self.date = datetime
        self.standard = g_standard
        self.cdx = dict()
        self.paths = dict()
        self.revision = dict()
    def upd_rec_cdx(self, uri_l):
        #self.cdx['exists'] = True
        #self.cdx['columns'] = wrc_n
        #self.cdx['lines'] = w_uri
        self.paths['warcFilenames'] = uri_l
        return self

## Defining unique objects sublasses and their methods

# CDX record

class Cdx_r(dict):
    def __init__(self):
        self['fileName'] = DEFAULT
        self['warcName'] = DEFAULT
        self['exists'] = DEFAULT_b
        self['path'] = DEFAULT
        self['md5'] = DEFAULT #TODO tobe deprecated, see Paths
        self['size'] = DEFAULT
        self['columns'] = DEFAULT
        self['lines'] = DEFAULT
        # self['version'] = DEFAULT # Depr
    def upd_rec_cdx_m(self, filN, warcN, size, md5, cols, lines):
        self['fileName'] = filN
        self['warcName'] = warcN
        self['exists'] = True
        self['size'] = size
        self['columns'] = cols
        self['lines'] = lines
        self['md5'] = md5
        #TODO count?
        return self

# WARC container

class Container(dict):
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
        uri_clean = re.sub("<|>","",self['warcID'])
        self.update({'warcID':uri_clean})
        return self
    def give_uri(self, uri_raw):    #Just new method ## TODO apply methods from core to all objects
        uri_clean = re.sub("<|>", "", uri_raw)
        return uri_clean

# Harvest matrix

class Harvest(dict):
    def __init__(self):   #TODO elements non validated, only through revision of all warc records, step CONSOLIDATION, verify folder, verify childrens, verify logs
        #self['harvestName'] = DEFAULT   #def down
        self['status'] = "NonValidated"
        self['date'] = DEFAULT
        self['harvestID'] = DEFAULT
        self['description'] = DEFAULT
        self['operator'] = DEFAULT
        self['operator'] = DEFAULT
        self['publisher'] = DEFAULT
        self['audience'] = DEFAULT
        self['robots'] = DEFAULT
        self['http-header-user-agent'] = DEFAULT
        self['http-header-from'] = DEFAULT
        self['harvestType'] = DEFAULT
        self['harvestSubtype'] = {}
        #self['harvestDuration'] = DEFAULT
        self['size'] = DEFAULT
        self['warcsNumber'] = DEFAULT
    def app_rec(self, hrv_name, rec, size, uuid):
        notregard = toset_hrv + depr_hrv
        for key, value in self.items():
            if key not in notregard:
                self[key] = rec[key]
        self.update({'harvestName': hrv_name})
        self.update({'size': size})
        self.update({'harvestDuration': DEFAULT})
        self.update({'harvestID' : uuid})
        self.update({'date':rec['dateOfOrigin']})
        try:
            a = re.compile("[0-9]{4}").split(hrv_name)
            b = re.compile("[0-9]{2}").split(a[1])
            type_coll = a[0].strip()
            self.update({'harvestType' : type_coll})
            subtype_coll = []
            sbt_coll = b[1].split("_")
            for sbt in sbt_coll:
                subtype_coll.append(sbt.strip("-"))
            self.update({'harvestSubtype': subtype_coll})

        except:
            self.update({'harvestType': traceback.print_exc(file=sys.stdout)})
            self.update({'harvestSubtype': traceback.print_exc(file=sys.stdout)})
            pass
    #(1[A-Z])\w+
        return self
    def upd_size(self, size):
        self['size']+=size
        return self

# More info about logs crawl folder

class HarvestCrawl(dict):
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

class Type(dict):
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

class Paths(dict):
    def __init__(self):
        self['storage'] = DEFAULT
        self['mount'] = DEFAULT
        self['pathToHarvest'] = DEFAULT
        self['LTP'] = DEFAULT
        self['harvestID'] = DEFAULT
        self['cdxID'] = DEFAULT
    def app_rec(self, path, uri):
        strp = str(path) #TODO split when system mount, add mount
        self['pathToHarvest'] = strp ##TODO tree
        self['harvestID'] = uri
        return self
    # for warcID, warcFilen see completation in Hrv class

# Revision subclass

class Revision(dict):
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

class Commentaries(dict):
    def __init__(self):
        self['exists'] = F
        self['text'] = DEFAULT
    def app_rec(self, rec):
        for key, value in self.items():
            self[key] = rec[key]
        return self

