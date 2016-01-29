"""
Created By: Kim Sundeen, 10/13/2015
Script Tool: Post & Reconcile Webedit version
Purpose: This tool automates posting and reconciling of webedit
version every day when run through Window's Scheduler to ensure the wededit
version's edits are sent to "Current" version.
"""

import arcpy, os
from datetime import datetime

# defines the output logfile for recording geoprocessing messages
# converts the datetime.now() into strings to be accessed & added the end of logfile; updated by KSundeen 10-19-2015
i = datetime.now()
todaysDatetime = i.strftime("%Y%m%d_%H%M%S")
dir = "S:/GIS_Public/Tools/Code/Python/Tasks_Scheduled/WebeditorReconcileLogs/"
logfile =  dir + "WebEditorReconcile_Log" + todaysDatetime + ".txt" 

print logfile

# Tool to reconcile & post webedit version to current version & write geoprocessing messages to logfile
arcpy.ReconcileVersions_management(r"Database Connections\cihl-gisdat-01_sde_webedit_webeditor.sde",
                                   "ALL_VERSIONS",
                                   "SDE.sde_Current",
                                   "WEBEDITOR.sde_webedit",
                                   "LOCK_ACQUIRED",
                                   "ABORT_CONFLICTS",
                                   "BY_OBJECT",
                                   "FAVOR_TARGET_VERSION",
                                   "POST",
                                   "KEEP_VERSION",
                                   logfile # blank () returns all messages, 0=messages; 1=warnings; 2=error
                                   ) 

print 'Reconcile for webedit version complete'

# delete extra xml file create during reconcile log process
for file in os.listdir(dir):
    print 'Listing file:', file

    f = open(logfile, "a")
    try:
        if file.endswith('.xml'):
            print os.path.exists(dir+file)  # exists() requires a filepath\filename
            print '\nFile ending with .xml:', file

            # before removing file, want to check I'm accessing it correctly!
##            print 'Now deleting file', file
            #f = open(logfile, 'a')
            fullFilename = dir + file
            os.remove(fullFilename)
            if os.path.exists(fullFilename) == False:
                
                # opens logfile without the .xml in it to open for appending
                with open(fullFilename[0:-4], 'a') as f:
                    f.write('Deleted the extra *.xml file')
    except OSError:
        pass
