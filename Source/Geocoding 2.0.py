#-------------------------------------------------------
#--Implement polygon encoding logic, master coordinater floting pointers, central field details pointer
#-------------------------------------------------------
# Get lat/long coordinates of an address from Google Maps

import os,urllib,math,json,time
#---------------Define--------------
LatLang=[]
MainLatLangBkp=[]
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

##Bangalore - Park - Flat
LatLang.append('13.026295,77.593699')
LatLang.append('13.025762,77.593597')
LatLang.append('13.025584,77.594421')
LatLang.append('13.026138,77.594571')
#-----------
LatLang.append('13.026000,77.593633')
LatLang.append('13.026216,77.594116')
LatLang.append('13.025883,77.594500')
LatLang.append('13.025666,77.593983')


## Nandi Hills - Hilly region
##LatLang.append('13.3547,77.68665')
##LatLang.append('13.3554166666667,77.6869')
##LatLang.append('13.3558,77.6856333333333')
##LatLang.append('13.3549833333333,77.68525')
##LatLang.append('13.35455,77.6862333333333')
###-------------
##LatLang.append('13.3547666666667,77.68575')
##LatLang.append('13.3554,77.6854333333333')
##LatLang.append('13.3556666666667,77.6862')




#print LatLang
#------------------------------------
#------------Input-2&3---------------
#DetailsLevel = int(raw_input('Details Level[Min - 0, max - 5]: '))
#MtrLvl = int(raw_input('Mininum Distance(in mts): '))
requestCounter=0
DetailsLevel = 1 #------was supposed to be used for increasing or decreasing details but the concept is not implemented yet
MtrLvl = 10 #-----------no that says how many meter/ft apart you wish to take a sample for the altitude measurement.
RequestLimit=60 #-------As we use googles free request service the no of altitude request a single ip can make and the no of sub request a request can have is restricted,this is the subrequest number.
AltReductionRange=2 #---altitude scale; if set to 1 then the lowest point will be shown as 1 ft/mtr tall from the ground and other points will get adjusted accordingly.
FieldName='Field1'
FilePath = 'C:\Users\slaik\Desktop\\' + FieldName + '.kml'
KMLDesignStart = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\
\n<Document> \n    <name>FieldMap.kml</name>\n    <Style id="thinWhiteLine">\n      <LineStyle>\n        <color>ffffffff</color>\n        <width>2</width>\n      </LineStyle>\n    </Style>\n    <Style id="polyLow"> \n       <LineStyle> \n            <color>ff00ff00</color> \n        </LineStyle> \n        <PolyStyle>\
\n            <color>ff00ff00</color> \n        </PolyStyle> \n    </Style> \n    <Style id="polyMid"> \n        <LineStyle> \n            <color>ff00ffff</color> \n        </LineStyle>\
\n        <PolyStyle> \n            <color>ff00ffff</color> \n        </PolyStyle> \n    </Style> \n    <Style id="polyHigh"> \n        <LineStyle> \n            <color>ff0000ff</color>\
\n        </LineStyle> \n        <PolyStyle> \n            <color>ff0000ff</color> \n        </PolyStyle> \n    </Style>'
PlaceMarkDesignStart1 = '\n<Placemark> \n    <name>Point No: '
PlaceMarkDesignStart2 = '</name>\n    <description>Altitude: '
PlaceMarkDesignStart3 = 'ft [w.r.t the lowest point]</description> \n    <styleUrl>'
PlaceMarkDesignMid = '</styleUrl> \n        <Polygon> \n            <altitudeMode>absolute</altitudeMode> \n            <outerBoundaryIs> \n                <LinearRing> \n                    <coordinates> \n'
PlaceMarkDesignEnd = '\n                    </coordinates> \n                </LinearRing> \n            </outerBoundaryIs> \n        </Polygon> \n</Placemark>'
#--------------------------
MainCoordNoPlaceMarkDesignStart='<Placemark>\n    <name>'
MainCoordNoPlaceMarkDesignMid1='</name>\n    <visibility>1</visibility>\n    <description>'
MainCoordNoPlaceMarkDesignMid1_1='</description>\n    <LookAt>\n      <longitude>'
MainCoordNoPlaceMarkDesignMid2='</longitude>\n      <latitude>'
MainCoordNoPlaceMarkDesignMid3='</latitude>\n      <altitude>'
MainCoordNoPlaceMarkDesignMid4='</altitude>\n      <heading>0</heading>\n      <tilt>90</tilt>\n      <range>100</range>\n      <altitudeMode>relativeToGround</altitudeMode>\n    </LookAt>\
\n    <Style>\n      <IconStyle>\n        <Icon>\n          <href>http://maps.google.com/mapfiles/kml/pal4/icon28.png</href></Icon>\n      </IconStyle>\n    </Style>\n    <Point>\n      <altitudeMode>relativeToGround</altitudeMode>\n      <coordinates>'
MainCoordNoPlaceMarkDesignEnd='</coordinates>\n    </Point>\n  </Placemark>'
#----------------------------
DistancePlacemarkStart='\n<Placemark>\n      <name>'
DistancePlacemarkMid1='</name>\n      <visibility>1</visibility>\n      <description>'
DistancePlacemarkMid2='</description>\n      <styleUrl>#thinWhiteLine</styleUrl>\n      <LineString>\n        <tessellate>1</tessellate>\n        <altitudeMode>relativeToGround</altitudeMode>\n        <coordinates>'
DistancePlacemarkEnd='\n        </coordinates>\n      </LineString>\n    </Placemark>'
KMLDesignEnd = '\n</Document> \n</kml>'
#print DetailsLevel+' '+MtrLvl
#------------------------------------

#=============================Methods========================
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
def distance(lat1,lng1,lat2,lng2):
    Radius=6371
    dlat=math.radians(lat2-lat1)
    dlng=math.radians(lng2-lng1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2) * math.sin(dlng/2)
    c = 2 * math.asin(math.sqrt(a))
    valueResult= Radius*c
    return valueResult*1000

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
def ActualAltiGetor(LatLangStr):
    #print LatLangStr
    timer=0
    center =""
    url='http://maps.googleapis.com/maps/api/elevation/json?sensor=false&locations=' + LatLangStr
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
        #incase data query limit exceeded
        print(j['status'])
            
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
def plotter(AltiStr,MtrLvl,MainLatLangBkp):
    AltiList = AltiStr.split('|')

    for item in AltiList:
        LatList.append(round(float(item[:item.find('&')]),6))
        LngList.append(round(float(item[item.find('&')+1:item.find(':')]),6))
        AltList.append(float(item[item.find(':')+1:]))
        
    #print sorted(LatList,key=float)
    #print LatList
    #print '\n'
    #print sorted(LngList,key=float)
    #print LngList
    #print '\n'
    #print sorted(AltList,key=float)
    #print AltList
    #print '\n'

    Lat_min=min(LatList, key=float)
    Lat_max=max(LatList, key=float)
    Lng_min=min(LngList, key=float)
    Lng_max=max(LngList, key=float)
    Alt_min=min(AltList, key=float)
    Alt_max=max(AltList, key=float)
    Alt_min_bkp=Alt_min
    
    #print Lat_min,Lat_max,Lng_min,Lng_max

#----------Reduce/reset the altitude levels for general hight reduction---------------------------

    for index, item in enumerate(AltList):
        AltList[index]=AltList[index]-(Alt_min-1)

    
    Alt_min=min(AltList, key=float)
    Alt_max=max(AltList, key=float)
    
    #print AltList,Alt_min,Alt_max

#-----------Building the kml File---------------------------------------------------------------------
    f = open(FilePath,'w+')
    
    f.write(KMLDesignStart)

    for index, item in enumerate(AltList):
        f.write(PlaceMarkDesignStart1)
        f.write(str(index+1))
        f.write(PlaceMarkDesignStart2)
        f.write(str(AltList[index]))
        f.write(PlaceMarkDesignStart3)
        if (AltList[index] < (Alt_max*2)/3):
           if (AltList[index] < (Alt_max/3)):
               f.write('#polyLow')
           else:
               f.write('#polyMid')
        else:
            f.write('#polyHigh')
        f.write(PlaceMarkDesignMid)
        f.write(str(LngList[index])+','+str(LatList[index])+',0\n'+str(LngList[index])+','+str(LatList[index])+','+str((AltList[index]+(Alt_min_bkp+AltReductionRange)))+'\n'+str(LngList[index]+0.0000003)+','+str(LatList[index])+','+str((AltList[index]+(Alt_min_bkp+AltReductionRange)))+'\n'+str(LngList[index])+','+str(LatList[index])+',0\n')
        f.write(str(LngList[index])+','+str(LatList[index])+',0\n'+str(LngList[index])+','+str(LatList[index]+0.0000003)+','+str((AltList[index]+(Alt_min_bkp+AltReductionRange)))+'\n'+str(LngList[index])+','+str(LatList[index])+','+str((AltList[index]+(Alt_min_bkp+AltReductionRange)))+'\n'+str(LngList[index])+','+str(LatList[index])+',0')
        f.write(PlaceMarkDesignEnd)
#-------Additional info & place markers-------------------
#-------Main coordinates numbering------------------------
    #print MainLatLangBkp
    for index, item in enumerate(MainLatLangBkp):
        lat1,lng1 = item.split(',')
        f.write(MainCoordNoPlaceMarkDesignStart)
        f.write('#'+str(index+1))
        f.write(MainCoordNoPlaceMarkDesignMid1)
        f.write(str(lng1)+','+str(lat1))
        f.write(MainCoordNoPlaceMarkDesignMid1_1)
        f.write(str(lng1))
        f.write(MainCoordNoPlaceMarkDesignMid2)
        f.write(str(lat1))
        f.write(MainCoordNoPlaceMarkDesignMid3)
        f.write(str(Alt_max))
        f.write(MainCoordNoPlaceMarkDesignMid4)
        f.write(str(lng1)+','+str(lat1)+','+str(Alt_max))
        f.write(MainCoordNoPlaceMarkDesignEnd)
#---------Distance Display----------------------------------
        for index1, item1 in enumerate(MainLatLangBkp):
            if index1 > index:
                lat2,lng2 = item1.split(',')
                dist=str(distance(float(lat1),float(lng1),float(lat2),float(lng2)))
                f.write(DistancePlacemarkStart)
                f.write('#'+str(index+1)+'-#'+str(index1+1))
                f.write(DistancePlacemarkMid1)
                f.write('Distance between #'+str(index+1)+'['+str(lng1)+','+str(lat1)+'] and #'+str(index1+1)+'['+str(lng2)+','+str(lat2)+'] is : '+str(dist)+' ft')
                f.write(DistancePlacemarkMid2)
                f.write(str(lng1)+','+str(lat1)+',0\n'+str(lng1)+','+str(lat1)+','+str(Alt_max+1)+'\n'+str(lng2)+','+str(lat2)+','+str(Alt_max+1)+'\n'+str(lng2)+','+str(lat2)+',0')
                f.write(DistancePlacemarkEnd)
#---------Total Info Display--------------------------------
        
    f.write(KMLDesignEnd)
    f.close()
    print 'Done'
#--------------------------------------------------------------------    
   
    return
#=============================Methods=END====================

#-------------Boilerplate------------------------------------
if __name__ == '__main__':
#-------------Level wise intermediate co-ord poplate---------
    if len(LatLang)<2:
        print 'Please enter atleast 2 co-ordinates in the format of latitude,langitude'
    if (MtrLvl < 1):
        print 'Mininum Distance too small -> try a number greter than or equal to 1'
    else:
        if (DetailsLevel < 0) or (DetailsLevel > 5):
            print 'Details Level out of given range'
        else:
            MainLatLangBkp=LatLang[:]
            while (DetailsLevel > 0):
                multiplier(LatLang)
                #print DetailsLevel
                DetailsLevel-=1
    AltiStr=AltiGater(LatLang,RequestLimit)
    plotter(AltiStr,MtrLvl,MainLatLangBkp)
#------------------------------------------------------------
