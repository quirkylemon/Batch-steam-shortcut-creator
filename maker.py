import sys, os
#-------------------------------------------------------------------------------

# ToDo

# fix not being able to add games with path/name with "&" symbol
# add detection for non-standard installations of steam
# add the option to add all the games to favorite (is there a tag for that?)
# allow multiple path to scan 
# be able to remove game/tools after you delete them

#let me know if there is something else you want me to add

#-------------------------------------------------------------------------------
#functions

#this splits the path into a name, a full path, and the directory the game is in (credit to someone in the python discord for this bit)
def split_path(path):
  path = path
  start, name = path.rsplit("\\", 1)
  #that makes sure that everything is spaced properly as well as adds double quotes to the names/paths
  return '"'+name.split(".")[0]+'"'+" "+'"'+path+'"'+" "+'"'+start+'"'

shortcut = ('py -2 shortcuts.py') #this will be used later for running the second python script with the arguments after it
#-------------------------------------------------------------------------------
#checks for itch.io directory to scan and askes for one if it is not detected
itchDIRfile = open('info\\itchDIR.txt', 'r+')
itchDIRcheck = itchDIRfile.readline()
if (itchDIRcheck == ""):
    itchDIR = input("copy and paste itch games directory ")
    itchDIRfile.write(itchDIR)
    itchDIRfile.close
else:
    itchDIR = itchDIRcheck
    #print (itchDIR) #for debugging
#-------------------------------------------------------------------------------
#checks for steam ID or askes for it if it is not detected
steamIDfile = open('info\\steamID.txt', 'r+')
steamIDcheck = steamIDfile.readline()
if (steamIDcheck == ""):
    steamIDpath = "C:\\Program Files (x86)\\Steam\\userdata"
    #opens steam user folder for users so they can copy and paste the numbers that represent their ID
    steamIDpath = os.path.realpath(steamIDpath)
    os.startfile(steamIDpath)
    steamID = str(input("copy and paste the numbers from the folder"))
    steamIDfile.write(steamID)
    steamIDfile.close()
else:
    steamID = steamIDcheck
    #print (steamID) #for debugging

#if you installed steam somewhere other than the default location then uncomment the following lines and put the path the your "shortcuts.vdf file"
#emergencyVDF = ('"'+"your path here"+'"'+" ")
#pathVDF = emergencyVDF
#-------------------------------------------------------------------------------
#comment out line 47 if you need to use emergencyVDF
pathVDF = ('"'+"C:\\Program Files (x86)\\Steam\\userdata\\"+steamID+"\\config\\shortcuts.vdf"+'"'+" ")
#-------------------------------------------------------------------------------
# A bunch of variables that will be needed later
name = "" #this gets defined later
path = ''# same
start = ""# same
hidden = " 0 " #change the "0" to a "1" for hidden if you want to hide all the games that this tool adds 
allow_desktop_config = "1 "
allow_steam_overlay = "1 "
last_playtime = "0 " 
categories = '"non-steam-game"' #I have the categories set as non steam game but if you want to set it as something else feel free

#extensions = (pathVDF+cleanresult+" "+hidden+allow_desktop_config+allow_steam_overlay+inVRLibrary+last_playtime+categories) #this is a template in case I have to move stuff around
#-------------------------------------------------------------------------------
#scans set directory for .exe files
for root, dirs, files in os.walk(itchDIR):
    for file in files:
        if file.endswith(".exe"):
             result = (os.path.join(root, file))             
#-----------------------------------------------------------------------------------------------
# the next subsection if a VR check to add the game to your VR library if it's sub/root folders have a certain .dll file (no its not flawless, but it gets the job done for now)
             #this is the openVR_api check
             inVRLibrary = "0 "
             DLLcheck, junk = result.rsplit("\\", 1)
             for base, sub, FL in os.walk(DLLcheck):
                 for file in FL:
                     if file.endswith(".dll"):
                         DLLcheck1 = file
                         if (DLLcheck1 == "openvr_api.dll"):
                            inVRLibrary = ("1 ")
             #this is the OVRplugin check
             DLLcheck, junk = result.rsplit("\\", 1)
             for base, sub, FL in os.walk(DLLcheck):
                 for file in FL:
                     if file.endswith(".dll"):
                         DLLcheck1 = file
                         if (DLLcheck1 == "OVRPlugin.dll"):
                             inVRLibrary = ("1 ")
             #-----------------------------------------------------------------
             if ("&" in (result)):
                 andcheck = 1
             else:
                    #the below lines are for ensuring you don't have a 1,000,000,000 setup/uninstaller tools
                    #if you find something you know people will never use please add it to the blacklist for me
                 blacklist = ("unins000.exe", "UnityCrashHandler64.exe", "UnityCrashHandler32.exe", "UnrealCEFSubProcess.exe", "UE4PrereqSetup_x64.exe", "dxwebsetup.exe","uninstall.exe","vc_redist","oalinst.exe","UE4Game-Win64-Shipping.exe")
                 if result.endswith(blacklist):
                    pass
                 else:
                    splitresult = split_path(result)
                    #some notes: the "result" after "splitresult" is to set the game icon
                    extensions = (" "+pathVDF+splitresult+" "+'"'+result+'"'+" "+'""'+" "+'""'+" "+hidden+allow_desktop_config+allow_steam_overlay+inVRLibrary+last_playtime+categories)
                    #print (shortcut+extensions) #this line is for checking the output without it making shortcuts coding (the line below must be commented out or it will still make shortcuts)
                    os.system('cmd /c'+'"'+shortcut+extensions+'"')
             

#--------------------------------------------------------------------------------
#just a couple of words for the user
print ("")
print ("thanks for using my tool")
print ("")
print ("let me know if something broke @ https://github.com/herosilas12/autoItchtoSteamlibrary")
print ("")
if (andcheck == 1):
    print ('BTW one of the apps/games you wanted to add to steam contained the "&" symbol, which for some reason breaks the script so you will have to add that app/game manually. sorry for the inconvienience')
print ("")
print ("")
print ("")
close = input ("press enter to close")