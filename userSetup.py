#    userSetup.py
#        by: YOUR_NAME 
#        v 1.0

import os, shutil, subprocess, sys
import maya.cmds as cmds
import maya.mel as mel
import maya.utils as utils

###  Change Script Folder  ###

scriptsFolder = "Z:/4_Fall2019 Spring 2020/Tools/Lee_M_Final" 

if scriptsFolder in sys.path:
    print "Could not find"
else:
    print "Directory found!"
    sys.path.append(scriptsFolder)
        
###  Create Menu UI  ###
def us_createScriptsMenu(scriptsFolder):
    
    if cmds.menu('scriptsMenu', exists=1):
        cmds.deleteUI('scriptsMenu')
    
    if scriptsFolder in sys.path:
        print ''
    else:
        sys.path.append(scriptsFolder)
    
    scriptsMenu = cmds.menu('scriptsMenu', p='MayaWindow', to=1, aob=1, l='Scripts')
    cmds.menuItem(p=scriptsMenu, l="Update Menu")
    cmds.menuItem(p=scriptsMenu, l="Change Directory")
    cmds.menuItem(p=scriptsMenu, d=1)
        
    absoluteFiles = []
    relativeFiles = []
    folders = []
    allFiles = []
    currentFile = ''
    
    for root, dirs, files in os.walk(scriptsFolder):
        for x in files:
            correct = root.replace('\\', '/')
            currentFile = (correct + '/' + x)
            allFiles.append(currentFile)
            if currentFile.endswith('.mel'):
                relativeFiles.append(currentFile.replace((scriptsFolder + '/'), ""))
            if currentFile.endswith('.py'):
                relativeFiles.append(currentFile.replace((scriptsFolder + '/'), ""))

        for d in dirs:
            print d
            otherPath = scriptsFolder +'/'+ d
            sys.path.append(otherPath)
                        
    relativeFiles.sort()
    
    for relativeFile in relativeFiles:
        split = relativeFile.split('/')
        fileName = split[-1].split('.')
        print(split)
        i=0
        while i<(len(split)):
            ### Create Folders ###
            if i==0 and len(split) != 1:
                if cmds.menu(split[i] ,ex=1) == 0:
                    cmds.menuItem(split[i], p=scriptsMenu, bld=1, sm=1, to=1, l=split[i])
            if i > 0 and i < (len(split)-1):
                if cmds.menu(split[i] ,ex=1) == 0:
                    cmds.menuItem(split[i], p=split[i-1], bld=1, sm=1, to=1, l=split[i])
            
            ### Create .mel Files  ###
            if fileName[-1] == 'mel':
                if i==len(split)-1 and len(split) > 1:
                    scriptName = split[-1].split('.')
                    temp1 = 'source ' + '"' + scriptsFolder + '/' + relativeFile + '"; ' + scriptName[0]
                    command = '''mel.eval(''' + "'" + temp1 + '''')'''
                    cmds.menuItem(split[i], p=split[i-1], c=command, l=split[i])
                if i==len(split)-1 and len(split) == 1:
                    scriptName = split[-1].split('.')
                    temp1 = 'source ' + '"' + scriptsFolder + '/' + relativeFile + '"; ' + scriptName[0]
                    command = '''mel.eval(''' + "'" + temp1 + '''')'''
                    cmds.menuItem(split[i], p=scriptsMenu, c=command, l=split[i])
                
            ### Create .py Files  ###
            if fileName[-1] == 'py':
                if i==len(split)-1 and len(split) > 1:
                    command = 'import ' + fileName[0] + '\n' + fileName[0] + '.' + fileName[0]+ '()'
                    print command
                    #command = 'import ' + fileName[0]  
                    cmds.menuItem(split[i], p=split[i-1], c=command, l=split[i])
                if i==len(split)-1 and len(split) == 1:
                    command = 'import ' + fileName[0] + '\n' + fileName[0] + '.' + fileName[0]+ '()'
                    cmds.menuItem(split[i], p=scriptsMenu, c=command, l=split[i])
            i+=1
            


utils.executeDeferred('us_createScriptsMenu(scriptsFolder)')

mel.eval('print "Written by xxxx@xxx.com"')
