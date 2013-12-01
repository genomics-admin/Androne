#-------------------------------------------------------
#-------------------------------------------------------
# Get lat/long coordinates of an address from Google Maps

import os,urllib,math,json
from pprint import pprint
from pylab import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#---------------Define--------------
LatLang=[]
LatList=[]
LngList=[]
AltList=[]
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
MtrLvl = 8
RequestLimit=512
AltReductionRange=1
FilePath = 'C:\Users\slaik\Desktop\mapplot.kml'
KMLDesignStart = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\
\n<Document> \n    <name>FieldMap.kml</name> \n    <Style id="polyLow"> \n       <LineStyle> \n            <color>ff00ff00</color> \n        </LineStyle> \n        <PolyStyle>\
\n            <color>ff00ff00</color> \n        </PolyStyle> \n    </Style> \n    <Style id="polyMid"> \n        <LineStyle> \n            <color>ff00ffff</color> \n        </LineStyle>\
\n        <PolyStyle> \n            <color>ff00ffff</color> \n        </PolyStyle> \n    </Style> \n    <Style id="polyHigh"> \n        <LineStyle> \n            <color>ff0000ff</color>\
\n        </LineStyle> \n        <PolyStyle> \n            <color>ff0000ff</color> \n        </PolyStyle> \n    </Style>'
PlaceMarkDesignStart = '\n<Placemark> \n    <styleUrl>'
PlaceMarkDesignMid = '</styleUrl> \n        <Polygon> \n            <altitudeMode>relativeToGround</altitudeMode> \n            <outerBoundaryIs> \n                <LinearRing> \n                    <coordinates> \n'
PlaceMarkDesignEnd = '\n                    </coordinates> \n                </LinearRing> \n            </outerBoundaryIs> \n        </Polygon> \n</Placemark>'
KMLDesignEnd = '\n</Document> \n</kml>'
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
            center+='|'+str(results['location']['lat'])+'&'+str(results['location']['lng'])+':'+str(results['elevation'])+'|'
            #print results['location']['lat']
            #print results['location']['lng']
    else:
        print "Data fetch failure. JSON didn't return OK."
    
    return center

#------------------------------------------------------------
def AltiGater(LatLang,RequestLimit):
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
    #print AltiStr
    AltiStr=AltiStr.replace("||","|")
    AltiStr=AltiStr[1:len(AltiStr)-1]

    return AltiStr
#------------------------------------------------------------
def plotter(AltiStr,MtrLvl):
    AltiList = AltiStr.split('|')

    for item in AltiList:
        LatList.append(round(float(item[:item.find('&')]),6))
        LngList.append(round(float(item[item.find('&')+1:item.find(':')]),6))
        AltList.append(float(item[item.find(':')+1:]))
        
    #print sorted(LatList,key=float)
    print LatList
    print '\n'
    #print sorted(LngList,key=float)
    print LngList
    print '\n'
    #print sorted(AltList,key=float)
    #print AltList
    #print '\n'

    Lat_min=min(LatList, key=float)
    Lat_max=max(LatList, key=float)
    Lng_min=min(LngList, key=float)
    Lng_max=max(LngList, key=float)
    Alt_min=min(AltList, key=float)
    Alt_max=max(AltList, key=float)

    print Lat_min,Lat_max,Lng_min,Lng_max

#----------Reduce/reset the altitude levels for general hight reduction---------------------------

    for index, item in enumerate(AltList):
        AltList[index]=AltList[index]-(Alt_min-AltReductionRange)

    
    Alt_min=min(AltList, key=float)
    Alt_max=max(AltList, key=float)
    
    print AltList,Alt_min,Alt_max

#-----------Building the kml File---------------------------------------------------------------------
    f = open(FilePath,'w+')
    
    f.write(KMLDesignStart)

    for index, item in enumerate(AltList):
        f.write(PlaceMarkDesignStart)
        if (AltList[index] < (Alt_max*2)/3):
           if (AltList[index] < (Alt_max/3)):
               f.write('#polyLow')
           else:
               f.write('#polyMid')
        else:
            f.write('#polyHigh')
        f.write(PlaceMarkDesignMid)
        f.write(str(LngList[index])+','+str(LatList[index])+','+str(AltList[index])+'\n'+str(LngList[index])+','+str(LatList[index])+',0')
        f.write(PlaceMarkDesignEnd)
        
    f.write(KMLDesignEnd)
    f.close()
    
#--------------------------------------------------------------------    
   
    return
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
AltiStr=AltiGater(LatLang,RequestLimit)
plotter(AltiStr,MtrLvl)
#------------------------------------------------------------
