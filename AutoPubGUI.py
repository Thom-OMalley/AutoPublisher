#Import GUI essential modules
import easygui as eg
setupOptIn = eg.buttonbox("Welcome to the GIS AutoPublisher \n Created by Thomas O'Malley \n GIS Data Processor at the Illinois State Geological Survey \n Click Setup to Get Started", title="AutoPublisher",image="ISGSLOGO.gif", choices=["Setup","Run"])

import os, sys
import cPickle as pickle

#Create save folder for pickled files
saveLoc = os.path.expanduser('~\\Documents\\GIS_Script_Data\\AutoPublisher10_1')

if not os.path.exists(saveLoc):
            os.makedirs(saveLoc)
            
###-GRAPHIC USER INTERFACE-###
msg         = "Enter your personal and survey information. For Online Resource URL, the service name and everything after will be generated.  Example entry: http://geothermal.isgs.illinois.edu/arcgis/services/aasggeothermal/"
title       = "WMS/WFS Properties"
fieldNames  = ('Name',
          'Position',
          'Organization (Provider)',
          'Website',
          'Street Address',
          'City',
          'State',
          'Postal (Zip) Code',
          'Country',
          'Phone',
          'Email',
          'Hours of Service',
          'Role',
          'Online Resource URL')
            
fieldValues = ()

try:
    pklFile = file(saveLoc+"\\ContactInfo.txt", 'r')
    restoreVal = pickle.load(pklFile)
    if setupOptIn == 'Setup':
        fieldValues = eg.multenterbox(msg,title, fieldNames, restoreVal)
    else: fieldValues = restoreVal
    pklFile.close()
except:
    print "No Values to Load"
    fieldValues = eg.multenterbox(msg + ".  No Values to Load" ,title, fieldNames)

# make sure that none of the fields were left blank
while 1:  # do forever, until we find acceptable values and break out
    if fieldValues == None: 
        break
    errmsg = ""
    
    # look for errors in the returned values
    for i in range(len(fieldNames)):
        if fieldValues[i].strip() == "":
            errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        
    if errmsg == "": 
        break # no problems found
    else:
        # show the box again, with the errmsg as the message    
        fieldValues = eg.multenterbox(errmsg, title, fieldNames, fieldValues)
    
#Save entries
pklFile = file(saveLoc+"\\ContactInfo.txt", 'w')
pickle.dump(fieldValues, pklFile)
pklFile.close()

#Makes lists into dictionary

fieldDict = dict(zip(fieldNames,fieldValues))
#Save Dict
pklFileDict = file(saveLoc+"\\pklFileDict.txt", 'w')
pickle.dump(fieldDict, pklFileDict)
pklFileDict.close()

#Use special folder name?
try:
    pklFile = file(saveLoc+"\\pklFileFLDROptIn.txt", 'r')
    restoreValFLDROptIn = pickle.load(pklFile)
    if setupOptIn == 'Setup':
        choices = ["Name Folder", "No Thanks"]
        FLDROptIn = eg.buttonbox("AutoPub can limit it's MXD search to folders of a certain name to avoid publishing old mxd files or files not ready for service.  Use this option if your master folder contains MXD files you do not want published.  This will only work if your files are organized under the same folder name, such as Illinois/your_mxd_folder/your_mxds.mxd and Iowa/your_mxd_folder/your_mxds.mxd. 'your_mxd_folder' must match.", choices=choices)
    else: FLDROptIn = restoreValFLDROptIn
except:
    choices = ["Name Folder", "No Thanks"]
    FLDROptIn = eg.buttonbox("AutoPub can limit it's MXD search to folders of a certain name to avoid publishing old mxd files or files not ready for service.  Use this option if your master folder contains MXD files you do not want published.  This will only work if your files are organized under the same folder name, such as Illinois/your_mxd_folder/your_mxds.mxd and Iowa/your_mxd_folder/your_mxds.mxd. 'your_mxd_folder' must match.", choices=choices)

pklFile.close()
pklFile = file(saveLoc+"\\pklFileFLDROptIn.txt", 'w')
pickle.dump(FLDROptIn, pklFile)
pklFile.close()

#If 'Name Folder' Chosen:
if FLDROptIn == "Name Folder":
    #Folder name for MXD files.
    try:
        pklFile = file(saveLoc+"\\pklFileFLDR_MXD.txt", 'r')
        restoreValFLDR = pickle.load(pklFile)
        if setupOptIn == 'Setup':
            FLDR_MXD = eg.enterbox("Enter the name of the folders containing your MXD files, ie: service_mxd", default= restoreValFLDR)
        else: FLDR_MXD = restoreValFLDR
    except:
        FLDR_MXD = eg.enterbox("Enter the name of the folders containing your MXD files, ie: service_mxd")

    pklFile.close()
    pklFile = file(saveLoc+"\\pklFileFLDR_MXD.txt", 'w')
    pickle.dump(FLDR_MXD, pklFile)
    pklFile.close()
else: pass

# Provide path to connection file
#   To create this file, right-click a folder in the Catalog window and
#   click New > ArcGIS Server Connection
try:
    defaultCon = os.path.expanduser("~\\AppData\\Roaming\\ESRI\\Desktop10.1\\ArcCatalog\\")
except: defaultCon = 'failed'
try:
    pklFile = file(saveLoc+"\\pklFileKHAN.txt", 'r')
    restoreValDIR = pickle.load(pklFile)
    if setupOptIn == 'Setup':
        path = eg.fileopenbox("Navigate to and select the ArcGIS Server Connection file (*.ags)", default= restoreValDIR)
    else: path = restoreValDIR
except:
    if defaultCon != 'failed':
        path = eg.fileopenbox("Navigate to and select the ArcGIS Server Connection file (*.ags)", default = defaultCon)
    else:
        path = eg.fileopenbox("Navigate to and select the ArcGIS Server Connection file (*.ags)")

pklFile.close()
pklFile = file(saveLoc+"\\pklFileKHAN.txt", 'w')
pickle.dump(path, pklFile)
pklFile.close()

#Determine master directory
try:
    pklFile = file(saveLoc+"\\pklFileDIR.txt", 'r')
    restoreValDIR = pickle.load(pklFile)
    if setupOptIn == 'Setup':
        path = eg.diropenbox("Path to master directory.  Program will search subfolders for MXD files.", default= restoreValDIR)
    else: path = restoreValDIR
except:
    path = eg.diropenbox("Path to master directory.  Program will search subfolders for MXD files.")

pklFile.close()
pklFile = file(saveLoc+"\\pklFileDIR.txt", 'w')
pickle.dump(path, pklFile)
pklFile.close()

#Ready to run script?
if setupOptIn == 'Setup':
    msg = "Thank you.  AutoPublisher is now ready to run, depending on the performance of your computer, the size of each map, and number of maps being published, this could take up to several hours.  On average each map takes 1-4 minutes to process.  Upon completion a box will appear displaying a list of maps that experienced errors"
    title = "Ready to Begin"
    if eg.ccbox(msg, title):     # show a Continue/Cancel dialog
        pass  # user chose Continue
    else:  # user chose Cancel
        sys.exit(0)
else: pass

#Choose services to run script on
#Choose single file or folder
choices = ["One","All"]
OneOrAll = eg.buttonbox("Do you wish to publish one file, or all the MXD files in the MXD Master Directory?", choices=choices)
pklFile = file(saveLoc+"\\OneOrAll.txt", 'w')
pickle.dump(OneOrAll, pklFile)
pklFile.close()
if OneOrAll == "One":
    try:
        default_MXD_File = restoreValDIR +'\\*'
        MXD_File = eg.fileopenbox("Navigate to and select your MXD file", default = default_MXD_File)
    except:
        MXD_File = eg.fileopenbox("Navigate to and select your MXD file")
else: pass

###-END GUI-###

#Part Two
try:
    #os.system('AutoPub.py')
    print 'pass'
except: print "Can't execute AutoPub"

#Load errors from AutoPub

pklFileErr = file (saveLoc+"\\pklFileErr.txt", 'r')
errorList = pickle.load(pklFileErr)
pklFileErr.close()

pklFileErr = file (saveLoc+"\\pklFileErrMaps.txt", 'r')
retryMaps = pickle.load(pklFileErr)
pklFileErr.close()

#Load Time
pklFileTIME = file (saveLoc+"\\pklFileTIME.txt", 'r')
minutes = pickle.load(pklFileTIME)
pklFileTIME.close()

#Display errors in GUI
eg.textbox(msg="Time Elapsed: " +str(minutes)+ " minutes. The following maps produced errors", title= 'ERRORS', text='\n'.join(errorList))
