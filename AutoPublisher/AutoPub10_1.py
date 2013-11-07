#import modules
import os, pickle, sys

#Save folder for pickled files
saveLoc = os.path.expanduser('~\\Documents\\GIS_Script_Data\\AutoPublisher10_1')

#Load Pickled Data
pklFile = file(saveLoc+"\\pklFileDict.txt", 'r')
fieldDict = pickle.load(pklFile)

pklFile = file(saveLoc+"\\pklFileDIR.txt", 'r')
path = pickle.load(pklFile)

pathGlob = path

try:
    pklFile = file(saveLoc+"\\MXD_File.txt", 'r')
    MXD_File = pickle.load(pklFile)
except: print "No MXD file to load"

pklFile = file(saveLoc+"\\OneOrAll.txt", 'r')
OneOrAll = pickle.load(pklFile)



pklFile = file(saveLoc+"\\pklFileFLDROptIn.txt", 'r')
FLDROptIn = pickle.load(pklFile)

if FLDROptIn == 'Name Folder':
    pklFile = file(saveLoc+"\\pklFileFLDR_MXD.txt", 'r')
    FLDR_MXD = pickle.load(pklFile)
else: pass

pklFileGDB = file(saveLoc+"\\pklFileGDBDIR.txt", 'r')
GDBpathORG = pickle.load(pklFileGDB)

try:
    pklFileErr = file (saveLoc+"\\pklFileErrMaps.txt", 'r')
    retryMaps = pickle.load(pklFileErr)
    pklFileErr.close()
except: retryMaps = [] #no maps to load

print "WORKING"
#IMPORT all other modules
import glob, arcpy, time, math
import xml.dom.minidom as DOM

#States Dictionary
USstates = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

StateSurveys = {
        'AK': 'Alaska Division of Geological and Geophysical Surveys',
        'AL': 'Alabama Geolgical Survey',
        'AR': 'Arkansas Geological Commission',
        'AS': 'American Samoa',
        'AZ': 'Arizona Geological Survey',
        'CA': 'California',
        'CO': 'Colorado Geological Survey',
        'CT': 'Connecticut Geological and Natural History Survey',
        'DC': 'District of Columbia',
        'DE': 'Delaware Geological Survey',
        'FL': 'Florida Geological Survey',
        'GA': 'Georgia Department of Natural Resources',
        'GU': 'Guam',
        'HI': 'Hawaii Department of Land and Natural Resources',
        'IA': 'Iowa Geological Survey Bureau',
        'ID': 'Idaho Geological Survey',
        'IL': 'Illinois State Geological Survey',
        'IN': 'Indiana Geological Survey',
        'KS': 'Kansas Geological Survey',
        'KY': 'Kentucky Geological Survey',
        'LA': 'Louisiana Geological Survey',
        'MA': 'Massachusetts Executive Office of Environmental Affairs',
        'MD': 'Maryland Geological Survey ',
        'ME': 'Maine Geological Survey',
        'MI': 'Michigan Department of Environmental Quality, Geological Survey Division',
        'MN': 'Minnesota Geological Survey',
        'MO': 'Missouri Division of Geology and Land Survey',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi Department of Environmental Quality',
        'MT': 'Montana Bureau of Mines and Geology',
        'NA': 'National',
        'NC': 'North Carolina Geological Survey ',
        'ND': 'North Dakota Geological Survey',
        'NE': 'University of Nebraska-Lincoln of Agriculture & Natural Resources Conservation and Survey Division',
        'NH': 'New Hampshire Department of Environmental Services',
        'NJ': 'New Jersey Geological Survey',
        'NM': 'New Mexico Bureau of Mines and Mineral Resources',
        'NV': 'Nevada Bureau of Mines and Geology',
        'NY': 'New York State Geological Survey',
        'OH': 'Ohio Department of Natural Resources, Division of Geological Survey',
        'OK': 'Oklahoma Geological Survey',
        'OR': 'Oregon Department of Geology and Mineral Industries',
        'PA': 'Pennsylvania Department of Conservation and Natural Resources, Bureau of Topographic and Geologic Survey',
        'PR': 'Puerto Rico Department of Natural and Environmental Resources, Bureau of Geology',
        'RI': 'Rhode Island Geological Survey',
        'SC': 'South Carolina Geological Survey',
        'SD': 'South Dakota Geological Survey',
        'TN': 'Tennesee Department of Environment and Conservation, Geology Division',
        'TX': 'Texas Bureau of Economic Geology',
        'UT': 'Utah Geological Survey',
        'VA': 'Virginia Division of Mineral Resources',
        'VI': 'Virgin Islands',
        'VT': 'Vermont Agency of Natural Resources',
        'WA': 'Washington Division of Geology and Earth Resources',
        'WI': 'Wisconsin Geological and Natural History Survey',
        'WV': 'West Virginia Geological and Economic Survey',
        'WY': 'Geological Survey of Wyoming'
}

# Overwrite pre-existing files
arcpy.env.overwriteOutput = True

#Start Clock
start = time.time()

#Workspace
arcpy.env.workspace = path

splitter = '\\' #ignore
#clear lists
errorList = []

#Define function for adding map names to errorList and retryMaps
def addMap():
    retryMaps.append(str(map))
    return

#Search home directory and sub directories for mxd files
'''if path.endswith(".mxd"):
    mapList = [path]''' # replaced by OneOrAll
if OneOrAll == 'One':
    mapList = [MXD_File]
elif OneOrAll == "Retry Last":
    mapList = retryMaps[:]

else:
    if FLDROptIn == "Name Folder":
        mapList = []
        findMXD = ['pass']#in order to start the while loop
        mxd_search_params = '.mxd'
        while len(findMXD) > 0: #While a downward search still produces results
            findMXD = glob.glob(pathGlob)
            for item in findMXD:
                if item.rsplit(splitter,1)[0].endswith(FLDR_MXD)==True:
                    if item.endswith(mxd_search_params) == True:
                        mapList.append(item)
            pathGlob = pathGlob + '\\*'

    else:
        print "Searching for MXD files in " + str(path)
        mapList = []
        findMXD = ['pass']#in order to start the while loop
        mxd_search_params = '.mxd'
        while len(findMXD) > 0: #While a downward search still produces results
            findMXD = glob.glob(pathGlob)
            for item in findMXD:
                if item.endswith(mxd_search_params) == True:
                    mapList.append(item)
            pathGlob = pathGlob + '\\*'

#Clear retry list for new maps
retryMaps = []

#Start main editing/publishing loop
for map in mapList:
    print map

for map in mapList:
    try:
        mxd = arcpy.mapping.MapDocument(map)
        mapName = map.rsplit(splitter, 1)[1]
        parentFolder = map.rsplit(splitter, 2)[0]  #For SD output, assumes MXD and SD files are in separate folders in the same directory

#Prep for WMS/WFS Properties
        keyTags = mxd.tags #grab mxd tags for WMS/WFS properties keywords
        if keyTags == "": #No Tags?  Create one called "Geothermal"
            keyTags = "Geothermal"

        stateAbr = mapName[0:2]
        stateName = USstates.get(stateAbr) #Match 2 letter abbreviation against USstates dictionary to get full state name
        dataType = mapName[2:-4] #Cuts off state and .mxd to reveal data type
        Abstract = str(dataType) +" in the state of "+ str(stateName) #WMS/WFS Abstract with full state name

        #Schemas temporarily static
        #Determine Schema from dataType
        if dataType == "WellHeaders":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/wellheader/1.5"
        elif dataType == "WellLogs":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/welllog/0.8"
        elif dataType == "BoreholeLithIntervals":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/bhlithinterval/0.9"
        elif dataType == "HeatFlow1_23":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/heatflow/1.23"
        elif dataType == "ThermalConductivity":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/thermalconductivity/2.0"
        elif dataType == "BoreholeTemperatures":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/boreholetemperature/1.5"
        elif dataType == "AqueousChemistry1_10":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/aqueouschemistry/1.10"
        elif dataType == "aqWellChemistry":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/aqueouschemistry/1.9"
        elif dataType == "BedrockGeology":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/simplefeatures/" #Anomaly
        elif dataType == "HeatPumpFacilities":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/HeatPumpFacility/0.6"
        elif dataType == "DrillStemTests":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/drillstemtest/1.8"
        elif dataType == "DirectUseSites":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/directusesite/1.5"
        elif dataType == "RockChemistry":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/rockchemistry/0.4"
        elif dataType == "ThermalSprings":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/thermalspring/1.6"
        elif dataType == "ThermalSprings1_8":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/thermalspring/1.8"
        elif dataType == "SeismicHypocenters":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/hypocenter/1.7"
        elif dataType == "PhysicalSamples":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/physicalsample/0.8"
        elif dataType == "ActiveFaults":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/activefault/1.2"
        elif dataType == "BoreholeLithIntercepts":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/boreholelithintercept/1.1"
        elif dataType == "ContourLines":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/contourline/1.0"
        elif dataType == "GeothermalAreas":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/geothermalarea/0.7"
        elif dataType == "PowerPlantFacilities":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/powerplantfacility/0.2"
        elif dataType == "HydraulicProperties":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/hydraulicproperty/1.0"
        elif dataType == "PowerPlantProduction":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/plantproduction/1.0"
        elif dataType == "RadiogenicHeatProduction":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/radiogenicheatproduction/0.5"
        elif dataType == "VolcanicVents":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/volcanicvent/1.4"
        elif dataType == "WellFluidProduction":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/fluidproduction/1.1"
        elif dataType == "WellTests":
            AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/welltest/1.0"
        else:
            AppSchemaURI = "null"
            errorList.append(mapName + ": No schema match")

        #MXD Credits
        Hub1 = fieldDict.get('Organization (Provider)')
        Hub = ", Provided by the "+Hub1 #used in Map credits
        try:
            mxd.author = StateSurveys.get(mapName[0:2])
            mxd.credits = mxd.author + Hub
        except: print "Credit edit failed"
        print map

        #Check for broken data sources and print them
        brknList = arcpy.mapping.ListBrokenDataSources(mxd)
        for brknItem in brknList:
            print "\t" + brknItem.name
            print "\t" + brknItem.dataSource
            ###- Repair Data Source (Still in testing)
            oldSource = brknItem.dataSource
            oldSource = oldSource.rsplit(splitter, 1)[0]
            #The following commented out portion works perfectly at ISGS or on a server that used the File System Restructure script
            '''end_of_old = oldSource.rsplit(splitter, 2)[1] + splitter + oldSource.rsplit(splitter, 2)[2]
            newSource = parentFolder + splitter + end_of_old
            brknItem.findAndReplaceWorkspacePath(oldSource,newSource)'''
            #OR
            gdb_folder = oldSource.rsplit(splitter, 2)[1] + splitter + oldSource.rsplit(splitter, 2)[2]       
            gdbSearch = ['pass'] #in order to start the while loop
            GDBpath = GDBpathORG

            while len(gdbSearch) > 0: #While a downward search still produces results
                gdbSearch = glob.glob(GDBpath)
                for item in gdbSearch:
                    if item.endswith(gdb_folder) == True:
                        newSource = item
                GDBpath = GDBpath + '\\*'
            try:
                brknItem.findAndReplaceWorkspacePath(oldSource,newSource)
            except: pass

        #Save MXD
        mxd.save()
        print "New Data Source Saved"
        # Provide path to connection file
        '''To create this file, right-click a folder in the Catalog window and
          click New > ArcGIS Server Connection'''
        pklFile = file(saveLoc+"\\pklFileKHAN.txt", 'r')
        con = pickle.load(pklFile)
        #Prepare Service_SD folder.  Create it if it doesn't exist

        if not os.path.exists(parentFolder +"\\service_sd\\"):
            os.makedirs(parentFolder +"\\service_sd\\")

        # Provide other service details
        Service = mapName[:-4]
        sddraft = parentFolder +"\\service_sd\\"+ Service +".sddraft"
        sd = parentFolder +"\\service_sd\\"+ Service +".sd"

        # Create service definition draft
        print "Creating Service Definition Draft"
        try:
            arcpy.mapping.CreateMapSDDraft(mxd, sddraft, Service, 'ARCGIS_SERVER', con, False, 'aasggeothermal')
        except: print "Creation of SDDraft failed"

        # These are the properties we will change in the sddraft xml.  They pertain to the WMS Server.
        soe = 'WMSServer'
        # You may replace attributes in the following list to suit your needs but do not take them out of order.  The matching system will fail if you do.
        keyList = ('inheritLayerNames', 'name','abstract','keyword', 'contactPerson', 'contactPosition', 'contactOrganization',
                   'address', 'addressType', 'city', 'stateOrProvince', 'postCode', 'country',
                   'contactVoiceTelephone', 'contactElectronicMailAddress', 'fees', 'ListSupportedCRS')
        valueList = ('true', 'WMS', str(Abstract), str(keyTags), fieldDict.get('Name'), fieldDict.get('Position'),
                     fieldDict.get('Organization (Provider)'),fieldDict.get('Street Address'), 'Postal', fieldDict.get('City'), fieldDict.get('State'),
                     fieldDict.get('Postal (Zip) Code'), fieldDict.get('Country'), fieldDict.get('Phone'), fieldDict.get('Email'), 'none', 'EPSG:3857')
        
        #zero out x
        x = 0

        #Check for ListSupportedCRS
        try:
            EPSG = doc.getElementsByTagName("ListSupportedCRS")
        except: EPSG = []

        if len(EPSG) > 0:
            LSCRS = 'exists'
        else: LSCRS = 'create'

        # Read the sddraft xml.
        doc = DOM.parse(sddraft)
        # Find all elements named TypeName. This is where the server object extension (SOE) names are defined.
        typeNames = doc.getElementsByTagName('TypeName')
        for typeName in typeNames:
            # Get the TypeName whose properties we want to modify.
            if typeName.firstChild.data == soe:
                extention = typeName.parentNode
                for extElement in extention.childNodes:
                    # Enabled SOE.
                    if extElement.tagName == 'Enabled':
                        extElement.firstChild.data = 'true'
                    # Modify SOE property. We have to drill down to the relevant property.
                    if extElement.tagName == 'Props':
                        for propArray in extElement.childNodes:
                            if LSCRS == 'create' and x == 0:
                                print 'appending ListSupportedCRS'
                                ele = doc.createElement('PropertySetProperty')
                                ele.attributes['xsi:type']="typens:PropertySetProperty"
                                propArray.appendChild(ele)
                            for propSet in propArray.childNodes:
                                if propSet.hasChildNodes() == False:
                                    print 'appending LSCRS Key'
                                    propSet.appendChild(doc.createElement('Key'))
                                    txt = doc.createTextNode('ListSupportedCRS')
                                    propSet.firstChild.appendChild(txt)
                                    ele = doc.createElement('Value')
                                    ele.attributes['xsi:type']="xs:string"
                                    propSet.appendChild(ele)
                                for prop in propSet.childNodes:
                                    if prop.tagName == "Key":
                                        for key in keyList:
                                            if prop.firstChild.data == key:
                                                print key
                                                if prop.nextSibling.hasChildNodes():
                                                    prop.nextSibling.firstChild.data = valueList[0+x]
                                                else:
                                                    txt = doc.createTextNode(valueList[0+x])
                                                    prop.nextSibling.appendChild(txt)
                                                print key + " paired with " + valueList[0+x]
                                                x = x + 1
        print "WMS Properties Updated"
        #Search Replace MinInstances
        DP = doc.getElementsByTagName("Key")
        key = "MinInstances"
        val = "0"
        for direct in DP:
             if direct.firstChild.data == key:
                if direct.nextSibling.hasChildNodes():
                    direct.nextSibling.firstChild.data = val
                else:
                    txt = doc.createTextNode(val)
                    direct.nextSibling.appendChild(txt)
                
        #Search Replace MaxWidth
        DP = doc.getElementsByTagName("Key")
        key = "MaxImageWidth"
        val = "4000"
        for direct in DP:
             if direct.firstChild.data == key:
                if direct.nextSibling.hasChildNodes():
                    direct.nextSibling.firstChild.data = val
                else:
                    txt = doc.createTextNode(val)
                    direct.nextSibling.appendChild(txt)
                    
        #Determine whether or not to activate WFS by checking if the datasource is an image
        WFSCheck = arcpy.mapping.ListLayers(mxd)
        if str(WFSCheck[0].dataSource).endswith("tif") or str(WFSCheck[0].dataSource).endswith("img") or WFSCheck[0].isRasterLayer == "True":
            print "MAP IS IMAGE"
            #Search Replace Description with WMS Description.
            DP = doc.getElementsByTagName("ItemInfo")
            key = "Description"
            val = "This web map service (WMS) was published using ArcGIS Server v. 10.1 and is compliant with OGC (Open Geospatial Consortium) version 1.3.0 specifications. This service provides dynamic, spatially referenced geographic information using data collected for the National Geothermal Data System (<a href=\"http://www.geothermaldata.org/\">http://www.geothermaldata.org/</a>). In addition to the WMS capabilities, this service was designed to be interoperable with KML (Keyhole Markup Language). A KML service allows the client to view an image of the data in three dimensions, using free software available for download on the internet such as ArcGIS Explorer or Google Earth. For more information on OGC specifications, visit <a href=\"http://www.opengeospatial.org/standards\">http://www.opengeospatial.org/standards</a>."
            for direct in DP:
                nList = direct.childNodes
                for node in nList:
                    if node.tagName == key:
                        print "Found Match.  Replacing Description"
                        if node.hasChildNodes():
                            node.firstChild.data = val
                        else:
                            txt = doc.createTextNode(val)
                            node.appendChild(txt)
        else:
            # These are the properties we will change in the sddraft xml.  They pertain to the WFS Server.
            soe = 'WFSServer'
            # You may replace attributes in the following list to suit your needs but do not take them out of order.  The matching system will fail if you do.
            keyList = ('appSchemaURI','appSchemaPrefix', 'title', 'abstract','keyword','serviceType', 'serviceTypeVersion', 'fees', 'providerName', 'providerSite',
                       'individualName', 'positionName', 'phone', 'deliveryPoint', 'city', 'administrativeArea',
                       'postalCode', 'country', 'electronicMailAddress', 'hoursOfService', 'role')
            valueList = (str(AppSchemaURI),'aasg', str(Service), str(Abstract), str(keyTags), 'WFS', r'1.1.0', 'None', fieldDict.get('Organization (Provider)'),
                         fieldDict.get('Website'),fieldDict.get('Name'),
                         fieldDict.get('Position'),fieldDict.get('Phone'),fieldDict.get('Street Address'),
                         fieldDict.get('City'), fieldDict.get('State'), fieldDict.get('Postal (Zip) Code'), fieldDict.get('Country'),
                         fieldDict.get('Email'),fieldDict.get('Hours of Service'), fieldDict.get('Role'))

            #zero x value
            x = 0
            # Get the TypeName whose properties we want to modify.
            if typeName.firstChild.data == soe:
                extention = typeName.parentNode
                for extElement in extention.childNodes:
                    # Enabled SOE.
                    if extElement.tagName == 'Enabled':
                        extElement.firstChild.data = 'true'
                    # Modify SOE property. We have to drill down to the relevant property.
                    if extElement.tagName == 'Props':
                        for propArray in extElement.childNodes:
                            for propSet in propArray.childNodes:
                                for prop in propSet.childNodes:
                                    if prop.tagName == "Key":
                                        for key in keyList:
                                            if prop.firstChild.data == key:
                                                if prop.nextSibling.hasChildNodes():
                                                    prop.nextSibling.firstChild.data = valueList[0+x]
                                                else:
                                                    txt = doc.createTextNode(valueList[0+x])
                                                    prop.nextSibling.appendChild(txt)
                                                print key + " paired with " + valueList[0+x]
                                                x = x + 1
            #Search Replace Description with WFS capable service description.
            DP = doc.getElementsByTagName("ItemInfo")
            key = "Description"
            val = "This web map service (WMS) was published using ArcGIS Server v. 10.1 and is compliant with OGC (Open Geospatial Consortium) version 1.3.0 specifications. This service provides dynamic, spatially referenced geographic information using data collected for the National Geothermal Data System (<a href=\"http://www.geothermaldata.org/\">http://www.geothermaldata.org/</a>). In addition to the WMS capabilities, this service was designed to be interoperable with both WFS (Web Feature Services) as well as KML (Keyhole Markup Language). The WFS capabilities allow the client to query, make additions and/or modifications to an existing dataset. WFS can be utilized through the interoperability extension in ArcCatalog. For more information on using the ArcGIS data interoperability extension visit <a href=\"http://www.esri.com/software/arcgis/extensions/datainteroperability/common-questions.html\">http://www.esri.com/software/arcgis/extensions/datainteroperability/common-questions.html</a>. A KML service allows the client to view an image of the data in three dimensions, using free software available for download on the internet such as ArcGIS Explorer or Google Earth. For more information on OGC specifications, visit <a href=\"http://www.opengeospatial.org/standards\">http://www.opengeospatial.org/standards</a>."
            for direct in DP:
                nList = direct.childNodes
                for node in nList:
                    if node.tagName == key:
                        print "Found Match.  Replacing Description"
                        if node.hasChildNodes():
                            node.firstChild.data = val
                        else:
                            txt = doc.createTextNode(val)
                            node.appendChild(txt)
                                                    
        # Output to a new sddraft.
        outXml = sddraft     
        f = open(outXml, 'w')     
        doc.writexml( f )     
        f.close()

        # Analyze the service definition draft
        analysis = arcpy.mapping.AnalyzeForSD(sddraft)

        # Print errors, warnings, and messages returned from the analysis
        print "The following information was returned during analysis of "+mapName+":"
        for key in ('messages', 'warnings', 'errors'):
          print '----' + key.upper() + '---'
          vars = analysis[key]
          for ((message, code), layerlist) in vars.iteritems():
            print '    ', message, ' (CODE %i)' % code
            messageError = str(message)
            print '       applies to:',
            for layer in layerlist:
                print layer.name,
                layerError = str(layer.name)
            print

        # Stage and upload the service if the sddraft analysis did not contain errors
        if analysis['errors'] == {}:
            # Execute StageService. This creates the service definition.
            arcpy.StageService_server(sddraft, sd)

            # Execute UploadServiceDefinition. This uploads the service definition and publishes the service.
            try:
                arcpy.UploadServiceDefinition_server(sd, con)
                print "Service successfully published"
            except:
                print "-------Upload Error when trying to publish " + mapName
                
        else:
            print "Service could not be published because errors were found during analysis."
            errorList.append(mapName + ": " + messageError + ", Applies to: " + layerError)
            addMap()

        print arcpy.GetMessages()
        
        print mapName + " complete"
        print '\n'
        
        del sd, mxd
    except UnicodeEncodeError:
        print "ascii codec error"
        errorList.append(mapName + ": unicode error")
        addMap()
    except:
        print "other exception"
        errorList.append(mapName + ": unknown error")
        addMap()

#Print Errors to Text File
outfile = file(saveLoc + "\\ScriptErr.txt", 'w')
outfile.write("\n".join(errorList))
outfile.close
del outfile

#Pickle Errors
pklFileErr = file (saveLoc+"\\pklFileErr.txt", 'w')
pickle.dump(errorList, pklFileErr)
pklFileErr.close()

pklFileErr = file (saveLoc+"\\pklFileErrMaps.txt", 'w')
pickle.dump(retryMaps, pklFileErr)
pklFileErr.close()

#End Time and print
try:
    end = time.time()
    elap = end - start
    minutes = elap / 60
    minutesR = math.ceil(minutes)
    minutesS = str(minutesR)
except:
    print "Time Error"

#Pickle Time, as in Pickle the Time, not 'PICKLE TIME!!!'
pklFileTIME = file (saveLoc+"\\pklFileTIME.txt", 'w')
pickle.dump(minutesS, pklFileTIME)
pklFileTIME.close()
                                 
print "Time: " +str(minutesR)+ " minutes"

print "Reticulation of splines complete"

print "Errors:"

for error in errorList:
    print error
print "These following maps have been added to the retryMaps list."
for mp in retryMaps:
    print mp
