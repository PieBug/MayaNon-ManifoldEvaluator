"""
 ________________
|       By       |
| Yozoh / PieBug |
|                | 
|   10/29/2019   |
 ----------------
 
 ~** NAME OF THE TOOL: Non-manifold Evaluator **~
--------------------------------------------------
//DESCRIPTION:// 
----------------
     This script loops through set project or given set 
     folder, and opens either a .fbx or .obj file into
     a new maya scene. It then returns a text file within 
     the same folder, which contains information about 
     non-manifold verticies or edges. 
//HOW TO USE://
---------------
     Open the tool and you'll be prompted with a window to 
     select your settings. Select a directory path to 
     desired folder. If none is selected, the tool with 
     go with the custom set project. Select your choice
     or FBX or OBJ and hit apply. A text file titled 
     "Non-Manifold_Information_Sheet.txt" will now be located 
     in the folder location. This text file contains information 
     of the poly and it's non-manifold verts and edges. 
"""
#Importing maya commands
import maya.cmds as mc
#-------------------------------------------------
"""
                  _________
                 |VARIABLES|
                  ---------
     
     //DESCRIPTION://
     ----------------
     1. fileExtension: Empty var to store file type user wants to examine. 
     2. currentWorkSpace: Obtains current set project workspace.
     3. pathTOAssets: Stores currentWorkSpace.
     4. pathFolder: Global variable used to store the path file of user's desired folder. 
"""
global fileExtension
global currentWorkSpace
currentWorkSpace = mc.workspace(fn=True)
global pathTOAssets
pathTOAssets = currentWorkSpace
global pathFolder
#-------------------------------------------------
"""
                   _________
                  |FUNCTIONS|
                   ---------
     
     //OUTPUTS://
     ------------
     1. changeToOBJ -> Outputs the value "fileExtension" will contain.
     2. changeToFBX -> Outputs the value "fileExtension" will contain.
     3. openWindowWS -> Outputs user's folder path into variable "pathFolder".
     
     //INPUTS://
     -----------
     1. importMesh <- Gets input from an list storing the file locations of the meshes.
     2. findFileExtension <- Gets input of directory path and Extension file type from user. 
     3. writeInfo <- Obtains a string containing information about the non-manifold of the meshes.

     //DESCRIPTION://
     ----------------
     1. changeToOBJ: Sets fileExtension to OBJ file.
     2. changeToFBX: Sets fileExtension to FBX file.
     3. openWindowWS: Opens file dialogue and prompts user to set the folder directory. 
                      Sets new folder path in pathTOAssets, then stores the user's choice in pathFolder.
     4. openScene: Opens a new maya scene and names it "New_Scene.ma".
     5. importMesh: Loops through the given list and imports the meshes into the scene.
     6. findFileExtension: Calls openScene to generate a new maya scene. And traverses through the 
                           path given by the user, and finds the files specified by the user. Once
                           files are found, the files are appended into the list created within the function.
     7. writeFile: Opens up the text file "Non-Manifold_Information_Sheet.txt" within the path folder and writes 
                   in the non-manifold information, given from evaluateAssets function. Then selects non-manifold 
                   edges and verticies.
     8. evaluateAssets: Checks if path and Extension file type given by user exists. Then calls findFileExtension to
                        append files into the listL variable. Then it selects polys within the scene and prints out
                        edges and verts with non-manifold faces. This information is stored within the local variable 
                        "info", creates a new text file called "Non-Manifold_Information_Sheet.txt", and sends info into 
                        writeFile function along with the information of verticies and edges.
"""
def changeToOBJ():
    global fileExtension
    fileExtension = ".obj"
    return fileExtension
def changeToFBX():
    global fileExtension
    fileExtension = ".fbx"
    return fileExtension
def openWindowWS():
    global pathFolder
    pathTOAssets = mc.fileDialog2(fm = 3, rf = True, okc = "Select", dir = currentWorkSpace)
    mc.textFieldGrp(textS, edit = True, text = pathTOAssets[0]) 
    pathFolder = pathTOAssets[0] 
def openScene():
    mc.file(new = True, force = True)
    mc.file(rename = os.path.join(os.getenv("HOME"), "New_Scene.ma"))
def importMesh(listL):
    for i in listL:
        mc.file(i, i=True, pr=True)
def findFileExtension(path, ext):
    global listL
    listL = []
    openScene()
    for root, dirs, files in os.walk(path):
        for i in files:
           ext_path = os.path.splitext(i)
           if ext_path[1] == ext:
               fileP = str((path) + "/" + (i))
               listL.append(fileP)
    importMesh(listL)
def writeFile(info, edges, verticies):
    input = open(pathFolder + "\Non-Manifold_Information_Sheet.txt", 'w')
    input.write(info)
    if edges != "None" and verticies != "None":
        mc.select(edges, verticies) 
def evaluateAssets():
    if os.path.isdir(pathFolder) and (fileExtension == ".obj" or fileExtension == ".fbx"):
        findFileExtension(pathFolder, fileExtension)
        mc.select(all = True)
        verticies = mc.polyInfo( nmv = True)
        edges = mc.polyInfo(nme = True)
        info = str("Non-Manifold Verticies: " + str(verticies) + "\n" + "Non-Manifold Edges: " + str(edges))
        input = open(pathFolder + "\Non-Manifold_Information_Sheet.txt", 'w')
        writeFile(info, edges, verticies)
    else:
        print "Try again."
#-------------------------------------------------
"""
                   _________
                  |WINDOW UI|
                   ---------
     
     //DESCRIPTION://
     ----------------
       Setting up window and UI menu. Adding columnLayout to create a child container 
       under parent window, adding a separator to add distance between the button "Set File" 
       (calls openWindowWS function) and textFieldGrp "Folder". Adding in text to display user's 
       set project path, and two radio buttons (calls changeToFBX and changeToOBJ) to get user's 
       input on Extension file choice. Lastly, is a button called "Apply", which grabs user's input 
       and calls the evaluateAssets function.
"""
currWS = ("Your current Set Project: %s") % currentWorkSpace
window = mc.window(title = "Non-manifold Evaluator", wh = (500,300))
mc.columnLayout(adjustableColumn = True)
mc.separator( h = 15, style = 'none')
mc.button(label = "Set File", command = "openWindowWS()")
mc.separator( h = 10, style = 'none')
textS = mc.textFieldGrp(label = "Folder: ", text = '', columnWidth = (1,128)) 
mc.text(currWS, fn = "boldLabelFont")
mc.radioButtonGrp(labelArray2 = ["FBX", "OBJ"], numberOfRadioButtons = 2, on1 = "changeToFBX()", on2 = "changeToOBJ()")  
mc.button(label = "Apply", command = "evaluateAssets()")
mc.showWindow()
#-------------------------------------------------
# EOF (END OF FILE)


