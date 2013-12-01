#-------------------------------------------------------
#-------------------------------------------------------
# Get lat/long coordinates of an address from Google Maps

import os,urllib,math,json
from pprint import pprint
#---------------Define--------------
LatLang=[]
LatLangDist_hash = {}
LatLangAlt_hash = {}
#-----------------------------------
#------------Input-1-----------------
#addr = raw_input('(Lat,Long)[Enter done to finish entering data]: ')
#
#while addr <> 'done':
#    LatLang.append(addr)
#    addr = raw_input('(Lat,Long)[Enter done to finish entering data]: ')   

LatLang.append('13.026295,77.593699')
LatLang.append('13.025762,77.593597')
LatLang.append('13.025584,77.594421')
LatLang.append('13.026138,77.594571')

#print LatLang
#------------------------------------
#------------Input-2&3---------------
#DetailsLevel = int(raw_input('Details Level[Min - 0, max - 5]: '))
#MtrLvl = int(raw_input('Mininum Distance(in mts): '))
DetailsLevel = 1
MtrLvl = 10
RequestLimit=512
#print DetailsLevel+' '+MtrLvl
#------------------------------------

#=============================Methods========================
def distance(lat1,lng1,lat2,lng2):
    Radius=6371
    dlat=math.radians(lat2-lat1)
    dlng=math.radians(lng2-lng1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2) * math.sin(dlng/2)
    c = 2 * math.asin(math.sqrt(a))
    valueResult= Radius*c
    return valueResult*1000
#------------------------------------------------------------
def PopulateIntermediateCoords(mastercoords,PopulatePoints,LatLang,value,MtrLvl):
    
    if PopulatePoints > 0:
        startcoords,endcoords = mastercoords.split('|')
        lat1,lng1 = startcoords.split(',')
        latN,lngN = endcoords.split(',')
        
        latX=float(lat1)-PopulatePoints*MtrLvl*(float(lat1)-float(latN))/value
        lngX=float(lng1)-PopulatePoints*MtrLvl*(float(lng1)-float(lngN))/value
        LatLang.append(str(latX)+","+str(lngX))
        
        PopulatePoints-=1
        #print "\n"+lat1,lng1,latN,lngN,PopulatePoints*MtrLvl,LatLang,value
        #print "\nrange: "+mastercoords+"{"+str(PopulatePoints*MtrLvl)+"}\n"+str(latX)+","+str(lngX)
        PopulateIntermediateCoords(mastercoords,PopulatePoints,LatLang,value,MtrLvl)
    else:
        return 1
    return
#------------------------------------------------------------    
def multiplier(LatLang):
    #print LatLang
    for items in LatLang:
        lat1,lng1 = items.split(',')
        for item in LatLang:
            lat2,lng2 = item.split(',')
            if (items <> item) and (items+'|'+item not in LatLangDist_hash) and (item+'|'+items not in LatLangDist_hash):
               LatLangDist_hash[items+'|'+item]=distance(float(lat1),float(lng1),float(lat2),float(lng2))
    #print LatLangDist_hash
    #print "\n\n\n\n\n   "

    distance_validator(LatLangDist_hash)
    #print "\n\n\n\n\n   " + str(distance(13.02519,77.594354,13.025584,77.594418))
    return
    
#------------------------------------------------------------
def distance_validator(LatLangDist_hash):
    for key, value in LatLangDist_hash.iteritems() :
        #print key, value
        if value>MtrLvl:
            if round(value%MtrLvl,1) == 0:
                PopulatePoints=int(value/MtrLvl)-1
            else:
                PopulatePoints=int(value/MtrLvl)
            #print PopulatePoints
            #print "-------------------------------"    
            PopulateIntermediateCoords(key,PopulatePoints,LatLang,value,MtrLvl)
            #print "-------------------------------"
    return

#------------------------------------------------------------
def ActualAltiGetor(LatLangStr):
    #print LatLangStr
    center =""
    url='http://maps.googleapis.com/maps/api/elevation/json?sensor=true&locations=' + LatLangStr
    #print '\nQuery: %s' % (url)

    # Get XML location
    json_str = urllib.urlopen(url).read()
    #print json_str

    j = json.loads(json_str)
    if j['status']=='OK':
        for results in j['results']:
            center+='|'+str(results['elevation'])+'|'
            #print results['location']['lat']
            #print results['location']['lng']
    else:
        print "Data fetch failure. JSON didn't return OK."
    
    return center

#------------------------------------------------------------
def AltiGater(LatLang,RequestLimit,LatLangAlt_hash):
    #print len(LatLang)
    #print LatLang
    AltiStr=""
    loopcount=len(LatLang)/RequestLimit
    #print "\n\n"
    if loopcount==0:
        AltiStr=ActualAltiGetor('|'.join(str(x) for x in LatLang[:len(LatLang)]))
    else:
        for index in range(loopcount):
            index+=1
            #print str(((int(index)-1)*RequestLimit))+"<->"+str(int(index)*RequestLimit)+"<->"+str(loopcount)
            AltiStr+=ActualAltiGetor('|'.join(str(x) for x in LatLang[(int(index)-1)*RequestLimit:(int(index)*RequestLimit)]))
        if int(index)*RequestLimit<>len(LatLang):
            #print str(int(index)*RequestLimit)+"<->"+str(len(LatLang))
            AltiStr+=ActualAltiGetor('|'.join(str(x) for x in LatLang[int(index)*RequestLimit:len(LatLang)]))
    print AltiStr.replace("||","|")
    return AltiStr
#=============================Methods=END====================

#-------------Boilerplate------------------------------------
#-------------Level wise intermediate co-ord poplate---------
if len(LatLang)<2:
    print 'Please enter atleast 2 co-ordinates in the format of latitude,langitude'
if (MtrLvl < 1):
    print 'Mininum Distance too small -> try a number greter than or equal to 1'
else:    
    if (DetailsLevel < 0) or (DetailsLevel > 5):
        print 'Details Level out of given range'
    else:
        while (DetailsLevel > 0):
            multiplier(LatLang)
            #print DetailsLevel
            DetailsLevel-=1
AltiGater(LatLang,RequestLimit,LatLangAlt_hash)
#------------------------------------------------------------

