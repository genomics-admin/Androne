#-------------------------------------------------------
#--Implement polygon encoding logic, master coordinater floting pointers, central field details pointer
#--everywhere in this code just like google maps it's latitude first, but while writing KML it's lanitude first
#-------------------------------------------------------
# Get lat/long coordinates of an address from Google Maps

import os,urllib,math,json,time,sys
#---------------Define--------------
LatLang=[]
MainLatLangBkp=[]
MainLatLangAlt=[]
LatList=[]
LngList=[]
AltList=[]
Nearby_hash={}
LatLangDist_hash = {}
LatLangAlt_hash = {}
#-----------------------------------
#------------Input-1-----------------
#addr = raw_input('(Lat,Long)[Enter done to finish entering data]: ')
#
#while addr <> 'done':
#    LatLang.append(addr)
#    addr = raw_input('(Lat,Long)[Enter done to finish entering data]: ')   


###Bangalore - Park - Flat - sequential
##LatLang.append('13.026295,77.593699')
##LatLang.append('13.026000,77.593633')
##LatLang.append('13.025762,77.593597')
##LatLang.append('13.025666,77.593983')
##LatLang.append('13.025584,77.594421')
##LatLang.append('13.025883,77.594500')
##LatLang.append('13.026138,77.594571')
##LatLang.append('13.026216,77.594116')
###-----------

####Bangalore - Park - Flat - nonsequencial # sheet design will faulter with nonsequential coordinates

LatLang.append('13.026295,77.593699')
LatLang.append('13.025762,77.593597')
LatLang.append('13.025584,77.594421')
LatLang.append('13.026138,77.594571')
###-----------
##LatLang.append('13.026000,77.593633')
##LatLang.append('13.026216,77.594116')
##LatLang.append('13.025883,77.594500')
##LatLang.append('13.025666,77.593983')


###Nandi Hills - Hilly region - Sequential
##LatLang.append('13.3547,77.68665')
##LatLang.append('13.3554166666667,77.6869')
##LatLang.append('13.3556666666667,77.6862')
##LatLang.append('13.3558,77.6856333333333')
##LatLang.append('13.3554,77.6854333333333')
##LatLang.append('13.3549833333333,77.68525')
##LatLang.append('13.3547666666667,77.68575')
##LatLang.append('13.35455,77.6862333333333')
###-------------




#print LatLang
#------------------------------------
#------------Input-2&3---------------
#DetailsLevel = int(raw_input('Details Level[Min - 0, max - 5]: '))
#MtrLvl = int(raw_input('Mininum Distance(in mts): '))
requestCounter=0
DetailsLevel = 1 #------was supposed to be used for increasing or decreasing details but the concept is not implemented yet
MtrLvl = 1 #-----------no that says how many meter/ft apart you wish to take a sample for the altitude measurement.
RequestLimit=60 #-------As we use googles free request service the no of altitude request a single ip can make and the no of sub request a request can have is restricted,this is the subrequest number.
AltReductionRange=2 #---altitude scale; if set to 1 then the lowest point will be shown as 1 ft/mtr tall from the ground and other points will get adjusted accordingly.
FieldName='Field1'
FilePath = 'C:\Users\slaik\Desktop\\' + FieldName + '.kml'
SideWall=1 #-----------Control for the sidewall structure in the KML, is set to 1 side walls will be created in the KML
KMLDesignStart = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\
\n<Document> \n    <name>FieldMap.kml</name>\
\n    <Style id="transBluePoly">\n      <LineStyle>\n        <color>ffff0000</color>\n        <width>0.1</width>\n      </LineStyle>\n      <PolyStyle>\n        <color>ffff0000</color>\n      </PolyStyle>\n    </Style>\
\n    <Style id="transRedPoly">\n      <LineStyle>\n        <color>7d0000ff</color>\n        <width>1.5</width>\n      </LineStyle>\n      <PolyStyle>\n        <color>7d0000ff</color>\n      </PolyStyle>\n    </Style>\
\n    <Style id="transGreenPoly">\n      <LineStyle>\n        <color>ff00ff00</color>        <width>0.1</width>\n      </LineStyle>\n      <PolyStyle>\n        <color>ff00ff00</color>\n      </PolyStyle>\n    </Style>\
\n    <Style id="transYellowPoly">\n      <LineStyle>\n        <width>1.5</width>\n      </LineStyle>\n      <PolyStyle>\n        <color>7d00ffff</color>\n      </PolyStyle>\n    </Style>\
\n    <Style id="thinWhiteLine">\n      <LineStyle>\n        <color>ffffffff</color>\n        <width>2</width>\n      </LineStyle>\n    </Style>\
\n    <Style id="polyLow"> \n       <LineStyle> \n            <color>ff00ff00</color> \n        </LineStyle> \n        <PolyStyle>\n            <color>ff00ff00</color> \n        </PolyStyle> \n    </Style>\
\n    <Style id="polyMid"> \n        <LineStyle> \n            <color>ff00ffff</color> \n        </LineStyle>\n        <PolyStyle> \n            <color>ff00ffff</color> \n        </PolyStyle> \n    </Style>\
\n    <Style id="polyHigh"> \n        <LineStyle> \n            <color>ff0000ff</color>\n        </LineStyle> \n        <PolyStyle> \n            <color>ff0000ff</color> \n        </PolyStyle> \n    </Style>'
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
#----------------------------
SheetBasePlacemarkStart='\n<Placemark>\n    <styleUrl>'
SheetBasePlacemarkMid='</styleUrl>\n        <Polygon>\n            <altitudeMode>relativeToGround</altitudeMode>\n            <outerBoundaryIs>\
\n                <LinearRing>\n                    <coordinates>'
SheetBasePlacemarkEnd = '\n                    </coordinates> \n                </LinearRing> \n            </outerBoundaryIs> \n        </Polygon> \n</Placemark>'
#-----------------------------
KMLDesignEnd = '\n</Document> \n</kml>'
#------------------------------------

#=============================Methods========================
#-------using a recursive function this method finds out all the entrim points that are a given mtr lvl apart from each other-----------------------------
def PopulateIntermediateCoords(mastercoords,PopulatePoints,LatLang,value,MtrLvl):
    if PopulatePoints > 0:
        startcoords,endcoords = mastercoords.split('|')
        lat1,lng1 = startcoords.split(',')
        latN,lngN = endcoords.split(',')
        
        latX=float(lat1)-PopulatePoints*MtrLvl*(float(lat1)-float(latN))/value
        lngX=float(lng1)-PopulatePoints*MtrLvl*(float(lng1)-float(lngN))/value
        LatLang.append(str(latX)+","+str(lngX))
        
        PopulatePoints-=1
        PopulateIntermediateCoords(mastercoords,PopulatePoints,LatLang,value,MtrLvl)
    else:
        return 1
    return
#------------------this methode will populate and insert the mid level coordinates to a given list-------------------
def Populatemasterintermediatecoordinates(LatLang):
    LatLangStr =''
    for index1, items in enumerate(LatLang):
        if index1+1 < len(LatLang):
            lat1,lng1 = items.split(',')
            latN,lngN = LatLang[index1+1].split(',')
            print lat1+','+lng1+'|'+latN+','+lngN+'\n'
            LatLangStr +=str(index1+1)+';'+Populatemidpointcoordinates(lat1+','+lng1+'|'+latN+','+lngN)+'|'
            
        else:
            lat1,lng1 = items.split(',')
            latN,lngN = LatLang[0].split(',')
            print lat1+','+lng1+'|'+latN+','+lngN+'\n'
            LatLangStr +=str(len(LatLang))+';'+Populatemidpointcoordinates(lat1+','+lng1+'|'+latN+','+lngN)     
    coords = LatLangStr.split('|')
    for index1, items in enumerate(coords):
        index,latlangval = items.split(';')
        #-----never thought febonacchi series will come in so handy here.....
        LatLang.insert(index1+int(index),latlangval)
    print LatLang
    
     
#------------this will always return midpoint coordinates for the given 2 coordinates-------------------------
def Populatemidpointcoordinates(LatLangStr):
    startcoords,endcoords = LatLangStr.split('|')
    lat1,lng1 = startcoords.split(',')
    latN,lngN = endcoords.split(',')
    latX=float(lat1)-(float(lat1)-float(latN))/2
    lngX=float(lng1)-(float(lng1)-float(lngN))/2
    #print str(latX) +','+ str(lngX)
    return str(latX) +','+ str(lngX)
               
            
            
#------------------------------------------------------------
def distance_validator(LatLangDist_hash):
    for key, value in LatLangDist_hash.iteritems() :
        if value>MtrLvl:
            if round(value%MtrLvl,1) == 0:
                PopulatePoints=int(value/MtrLvl)-1
            else:
                PopulatePoints=int(value/MtrLvl)
            print 'Populating Intermediate points...                       ...[IN PROGRESS]'
            PopulateIntermediateCoords(key,PopulatePoints,LatLang,value,MtrLvl)
            print 'Populating Intermediate points...                       ...[DONE]'
            
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
    for items in LatLang:
        lat1,lng1 = items.split(',')
        for item in LatLang:
            lat2,lng2 = item.split(',')
            if (items <> item) and (items+'|'+item not in LatLangDist_hash) and (item+'|'+items not in LatLangDist_hash):
                print 'Calculating Distance between points...                  ...[IN PROGRESS]' 
                LatLangDist_hash[items+'|'+item]=distance(float(lat1),float(lng1),float(lat2),float(lng2))
                print 'Calculating Distance between points...                  ...[DONE]'

    print 'Validating all distances...                             ...[IN PROGRESS]'
    distance_validator(LatLangDist_hash)
    print 'Validating all distances...                             ...[DONE]' 
    
    return


#------------------------------------------------------------
def ActualAltiGetor(LatLangStr):
    timer=0
    center =""
    url='http://maps.googleapis.com/maps/api/elevation/json?sensor=false&locations=' + LatLangStr
    
    # Get XML location
    json_str = urllib.urlopen(url).read()
    
    j = json.loads(json_str)
    if j['status']=='OK':
        for results in j['results']:
            center+='|'+str(results['location']['lat'])+'&'+str(results['location']['lng'])+':'+str(results['elevation'])+'|'
    else:
        print "Data fetch failure. JSON didn't return OK.Raising error and aborting."
        #incase data query limit exceeded
        print(j['status'])
        if j['status']=='OVER_QUERY_LIMIT':
            print 'Closing connections with the service...                 ...[ERROR]'
            print 'INFO: Google server rejected connection...              ...[ERROR]'
            print '1.Either wait 24 HRS for the connection to reactivate......[ERROR]'
            print '2.Or run the code from another IP/network/Data card...  ...[ERROR]'
            print '3.Or buy business key from Google...                    ...[ERROR]'
            print 'Script will abort now!!      Sorry...                   ...[EXECUTION TERMINATED]'
            sys.exit()
        
    return center

#------------------------------------------------------------
def AltiGater(LatLang,RequestLimit):
    print 'Connecting to Google Map Elevation service...           ...[IN PROGRESS]'
    AltiStr=""
    loopcount=len(LatLang)/RequestLimit
    if loopcount==0:
        AltiStr=ActualAltiGetor('|'.join(str(x) for x in LatLang[:len(LatLang)]))
    else:
        for index in range(loopcount):
            index+=1
            AltiStr+=ActualAltiGetor('|'.join(str(x) for x in LatLang[(int(index)-1)*RequestLimit:(int(index)*RequestLimit)]))
        if int(index)*RequestLimit<>len(LatLang):
            AltiStr+=ActualAltiGetor('|'.join(str(x) for x in LatLang[int(index)*RequestLimit:len(LatLang)]))
    AltiStr=AltiStr.replace("||","|")
    AltiStr=AltiStr[1:len(AltiStr)-1]

    print 'Closing connections with the service...                 ...[DONE]'
    return AltiStr
#------------------------------------------------------------
def plotter(AltiStr,MtrLvl,MainLatLangBkp):
    print 'KML file building...                                    ...[IN PROGRESS]'
    AltiList = AltiStr.split('|')

    print 'Calculating Max/Min Altitude from the data pool...      ...[IN PROGRESS]'
    for item in AltiList:
        LatList.append(round(float(item[:item.find('&')]),6))
        LngList.append(round(float(item[item.find('&')+1:item.find(':')]),6))
        AltList.append(float(item[item.find(':')+1:]))

    Lat_min=min(LatList, key=float)
    Lat_max=max(LatList, key=float)
    Lng_min=min(LngList, key=float)
    Lng_max=max(LngList, key=float)
    Alt_min=min(AltList, key=float)
    Alt_max=max(AltList, key=float)
    Alt_min_bkp=Alt_min
    Alt_max_bkp=Alt_max

#----------Reduce/reset the altitude levels for general hight reduction---------------------------

    for index, item in enumerate(AltList):
        AltList[index]=AltList[index]-(Alt_min-1)

    
    Alt_min=min(AltList, key=float)
    Alt_max=max(AltList, key=float)
    
    print 'Calculating Max/Min Altitude from the data pool...      ...[DONE]'
#-----------Building the kml File---------------------------------------------------------------------
    f = open(FilePath,'w+')
    
    f.write(KMLDesignStart)

    print 'Plotting data samples...                                ...[IN PROGRESS]'
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
    print 'Plotting data samples...                                ...[DONE]'
    
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
        print 'Plotting master coordinates...                          ...[DONE]'
        
#---------Distance Display----------------------------------
#---the design will flot max altitude +1ft in the space
        print 'Plotting distance lines...                              ...[IN PROGRESS]'
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
        print 'Plotting distance lines...                              ...[DONE]'
        
#------------sheet-----------------------------------------
    print 'Plotting Sheet Base...                                  ...[IN PROGRESS]'
    for index, item in enumerate(AltList):
        val=''
        for index1, item1 in enumerate(AltList):
            if index<>index1:
                dist=distance(float(LatList[index]),float(LngList[index]),float(LatList[index1]),float(LngList[index1]))
                if dist<(MtrLvl*1.5):  
                    val=val+','+str(index1)
        Nearby_hash[index]=val[1:]

    #--------Sheetbase-------------------------------------
    #---the design will flot max altitude +20ft in the space
    f.write(SheetBasePlacemarkStart+'#transBluePoly'+SheetBasePlacemarkMid)
    for index, item in enumerate(MainLatLangBkp):
        lat1,lng1 = item.split(',')
        f.write(str(lng1)+','+str(lat1)+','+str(Alt_max+20)+'\n')
        if index==0:
            store=str(lng1)+','+str(lat1)+','+str(Alt_max+20)
    f.write(store+SheetBasePlacemarkEnd)
    print 'Plotting Sheet Base...                                  ...[DONE]'
    
    #---the design will flot max altitude +25ft in the space
    print 'Plotting Sheet design...                                ...[IN PROGRESS]'
    for index, item in Nearby_hash.iteritems():
        f.write(SheetBasePlacemarkStart+'#transGreenPoly'+SheetBasePlacemarkMid)
        f.write(str(LngList[index])+','+str(LatList[index])+','+str(AltList[index]+Alt_max+25)+'\n')
        itemArray=item.split(',')
        for items in itemArray:
            f.write(str(LngList[int(items)])+','+str(LatList[int(items)])+','+str(AltList[int(items)]+Alt_max+25)+'\n')
        f.write(str(LngList[index])+','+str(LatList[index])+','+str(AltList[index]+Alt_max+25)+'\n')
        f.write(SheetBasePlacemarkEnd)
    print 'Plotting Sheet design...                                ...[DONE]'

    #---side walls-------------------------------------------
    if SideWall==1:
        for index, item in enumerate(MainLatLangBkp):
            lat1,lng1 = item.split(',')
            for index1, item1 in enumerate(AltList):
                if str(float(lat1))==str(LatList[index1]) and str(float(lng1))==str(LngList[index1]):
                    MainLatLangAlt.append(str(LatList[index1])+','+str(LngList[index1])+','+str(AltList[index1]))
        #----adding the first value as the last value to complete the grid loop for side wall-------------------
        MainLatLangAlt.append(MainLatLangAlt[0])
        
        for index, item in enumerate(MainLatLangAlt):
            lat1,lng1,alt1 = item.split(',')
            if index+1 < len(MainLatLangAlt):
                lat2,lng2,alt2 = MainLatLangAlt[index+1].split(',')
                f.write(SheetBasePlacemarkStart+'#transBluePoly'+SheetBasePlacemarkMid)
                f.write(str(lng1)+','+str(lat1)+','+str(Alt_max+20)+'\n')
                f.write(str(lng1)+','+str(lat1)+','+str(Alt_max+float(alt1)+25)+'\n')
                f.write(str(lng2)+','+str(lat2)+','+str(Alt_max+float(alt2)+25)+'\n')
                f.write(str(lng2)+','+str(lat2)+','+str(Alt_max+20)+'\n')
                f.write(SheetBasePlacemarkEnd)
        print 'Plotting Sheet walls...                                 ...[DONE]'

#---------Total Info Display------------------------------------------------
#---------for that find the point farthest from all the main points---------
        
    f.write(KMLDesignEnd)
    f.close()
    print 'KML file building...                                    ...[DONE]'
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
            #MainLatLangBkp=LatLang[:]
            while (DetailsLevel > 0):
                print 'All initial parameter check...                          ...[DONE]'
                Populatemasterintermediatecoordinates(LatLang)
                MainLatLangBkp=LatLang[:]
                print 'Initiating Co-ordinate multiplication...                ...[IN PROGRESS]'
                if DetailsLevel == 1:
                    multiplier(LatLang)
                print 'Initiating Co-ordinate multiplication...                ...[DONE]'
                DetailsLevel-=1
    
    print 'Requesting for altitude values...                       ...[IN PROGRESS]'
    AltiStr=AltiGater(LatLang,RequestLimit)
    print 'All altitude values received...                         ...[DONE]' 
    print 'Time for some KML Magic...                              ...[IN PROGRESS]'
    plotter(AltiStr,MtrLvl,MainLatLangBkp)
    print 'Time for some KML Magic...                              ...[DONE]' 
    print 'Launch the KML file in Google Earth...                  ...[EXECUTION END]'
#------------------------------------------------------------
