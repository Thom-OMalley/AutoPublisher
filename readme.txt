AutoPublisher by Thomas O'Malley at the Illinois State Geological Survey
Intended for use by Hubs and self serving members of the US Geothermal Project

Step 1: Welcome.  Choose Setup or Run.  Choose Setup the first time you run the program.  Setup will allow you to fill in WFS/WMS properties and more.  Run will jump straight to selecting maps to publish.

Step 2: Fill in the properties with your personal (provided you are the primary contact for the US Geothermal Project) and survey information.
	Your Online Resource URL should look similar to "http://geothermal.isgs.illinois.edu/arcgis/services/aasggeothermal/"

Step 3: Path to master directory.  Select the folder the contains the mxd files you wish to publish.  AutoPublisher will search the subfolders for mxd files.  The pop up box for this step is relatively small, and should appear in the center.  It can take a few moments to appear if it has to search for network folders.  If you do not see it after a few moments, try minimizing windows to make sure they aren't covering it.

Step 4: Path to GDB master directory (may be the same as previous directory).  AutoPublisher will search this directory and it's subfolders (and its subfolders' subfolders and so on forever) for GDB files in the case of a broken data source link.  When file folders are moved the data source links can be broken.  This can happen when files are moved to new drive letter, or a new network data server.  Autopublisher will attempt to fix these errors by searching for the 'FolderName/DatabaseName.gdb' from the broken data source in the directory you choose in this step.

Step 5: Naming the mxd folder.  AutoPublisher was designed to accept multiple file structures.  If all the mxd files you wish to publish are kept in folders of the same name, ie. "service_mxd," then you can name the folder and the program will only search for mxd files under that folder name.  If your mxd files are not organized under a identical folder names, ie. one folder is named "IL_maps" and another is "IA_mxds," then you should choose "No Thanks" and the program will search all folders in your given master directory.

Step 6: ArcGIS Server Connection File (*.ags).  To create a server connection file, right-click a folder in the Catalog window and
          click New > ArcGIS Server Connection.  The default save location of this file is Drive:\\Users\Your_Username\AppData\Roaming\ESRI\Desktop10.1\ArcCatalog\.  AutoPublisher should automatically expand this folder making it easy for you to select the file, but you are free to navigate if necessary.

Step 7: Ready to begin.  This is your chance to cancel the operation.  Your settings will be saved, and you can safely exit at this point without losing any settings.  The next time you run the program you can choose "Run" instead of "Setup" if you want to use the same settings.  You can also choose continue to start the operation.  Each map takes 1-4 minutes to process depending on the size of the map and processing power of the computer/server.

Step 8: "Run" jumps straight to this step.  Choose to publish one mxd file, or all the files in the master directory.  Be careful using "All" as it will overwrite previous publications.  This is great if you want to make a large sweeping change, such as changing a contact phone number, but may overwrite changes you've made by hand since the first publication.  Selecting "One" will open up a file selection box (It should open at your master directory, so you won't have to dig through as many file folders to find it).  Navigate to your desired file and select it.  If some of the maps failed to publish the last time you ran AutoPublisher, a third option will be presented in this window: "Retry Last."

Step 9: Autopublisher will now run the operation.  The program is hands-off at this point, and you can safely leave your desk or work on something else.  Avoid using the files being published to ensure Autopublisher has permission to use them.  At the end of the operation, an error report will pop up on screen, informing you of any maps that were not published and stating the errors that prevented publishing.  If a map cannot be published, Autopublisher will move on to the next one.  One map error cannot derail the process.  Maps with errors are added to a list.  After making the appropriate changes, you can select "Retry Last" from Step 8 to make a second attempt at publishing them, without having to republish all the maps in the directory.

Autopublisher Workflow:

Searches for MXD files
For each file:
Edits MXD author and credits
Corrects workpaths of data sources
Check for broken data sources and print
Create service_sd folder to save draft and sd within.
Determine service name from mxd filename
Create SDDraft
Edit WMS properties based on entries from GUI
Change MinInstances to 0
Change MaxImageWidth to 4000
Change title to the name of the Service
Check “inheritLayerNames” in WMS (set to true)
Check to see if map has WFS properties based on whether or not layer is raster layer, or layer data source is an image (TIF or IMG)
If map is WMS only, replace description with WMS service description
If WFS:
	Edit properties based on WFS entries from GUI
	Replace description
	Replace Service type and version (WFS 1.1.0)
Save SDDraft
Analyze draft for errors and print them
If error free, try to upload service
Report upload, Unicode and other exceptions/errors
Print errors to a text file
Save problem maps to a new mxd list for retry
Report time taken, print errors to GUI window.  END

