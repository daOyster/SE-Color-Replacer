import sys
import os
from lxml import etree as ET

"""
-----------------------------------------------------------------
@author: Brandon Osterhout ( aka "daOyster" )

This program gvies you every color found in a space engineers
blueprint file, and lets you update a selected color to a new 
color and then save a new blueprint file containing the changes.
-----------------------------------------------------------------

reference:
:
cubeGrids = None
for c in shipBP:
	if c.tag == "CubeGrids":
		cubeGrids = c
cubeGrid = cubeGrids[0]
# Get the list of CubeBlocks

for child in cubeGrid :
	print("|--"+child.tag+"\n")
"""
# checks in the list of colors for the current blocks color.
# Returns the index if the color is already in the color
# list, or returns -1 if not found.
def checkInColors(colors, block):
	index = 0
	for c in colors:
		# print(c[0].attrib,":::" ,block.attrib)
		if c[0].attrib == block.attrib:
			return index
		index += 1
	return -1


def getCubeColorID(cubeColors, block):
	index = 0
	bid = -1
	for col in cubeColors:
		if col[0].attrib == block.attrib:
			bid = index
			return bid
		index += 1
	return -1

def doColorChange( bpPath):
	# Normalize the file path so that it works on windows without causing escape character issues
	bpFilePath = os.path.normpath( bpPath + '/bp.sbc' )
	print( '.sbc Filepath:\n',bpFilePath )
	tree = ET.parse( bpFilePath)
	root = tree.getroot()

	# Make a backup of the current tree with 'back_' prefixed
	# tree.write( bpPath + "bp.sbc_backup" )

	# print(root.tag)

	shipBPs = root[0]
	shipBP = shipBPs[0]

	# list containing all of the colors in the currently loaded blueprint file
	cubeColors = []

	for block in root.iter("ColorMaskHSV"):
		if not cubeColors:
			newColor = [block]
			cubeColors.append(newColor)
		elif checkInColors( cubeColors, block ) >= 0:
			index = checkInColors( cubeColors, block )
			cubeColors[ index ].append(block)
		else:
			newColor = [block]
			cubeColors.append(newColor)

	# Print out the list of colors found in the build
	print("Colors:\n")
	index = 0
	for b in cubeColors:
		print(index,'{:<18}'.format(' | hue (x): ' + b[0].attrib['x']),end='')
		print('{:<24}'.format('| saturation (y): ' + b[0].attrib['y']),end='')
		print('{:<18}'.format('| value (z): ' + b[0].attrib['z']),end='\n')
		
		index += 1

	# Print a blank line and request input for the new color choice
	print()
	num = input("Type the index of the color to replace or 'e' to exit: ")
	if num.lower() == 'exit' or num.lower() == 'e':
		print()
		return 2

	x = input("New Hue(x): ")
	y = input("New Saturation(Y): ")
	z = input("New Value (Z): ")
	print('\nNew Color:')
	print(index,'{:<18}'.format(' | hue (x): ' + cubeColors[int(num)][0].attrib['x']),end='')
	print('{:<24}'.format('| saturation (y): ' + cubeColors[int(num)][0].attrib['y']),end='')
	print('{:<18}'.format('| value (z): ' + cubeColors[int(num)][0].attrib['z']),end='\n')

	# set the hsv_mask attribute in all of the blocks found with the previous color
	for block in cubeColors[int(num)]:
		block.set('x',x)
		block.set('y',y)
		block.set('z',z)

	# write the new blueprint file containing the updaterd hsv mask
	tree.write(os.path.normpath( bpPath + '/bpn.sbc'))
	# rename .bspPB file so that Space Engineers will generate a new one on next ship load	
	try:

		os.remove(os.path.normpath(bpPath +'/old_bp.sbc'))
		os.remove(os.path.normpath(bpPath +'/old_bp.sbcPB'))
	except:
		print("No backups exist, making new ones.")

	try:
		os.rename(os.path.normpath( bpPath+'/bp.sbcPB'), os.path.normpath(bpPath+'/old_bp.sbcPB'))
	except:
		print('No bp.sbcBP file found, skipping it\'s renaming.')
	try:
		os.rename(os.path.normpath( bpPath+'/bp.sbc'), os.path.normpath(bpPath +'/old_bp.sbc'))
	except:
		print('No bp.sbc file found, skipping it\'s renaming.')

	# Change the name of the new, modified blueprint back to bp.sbc
	os.rename(os.path.normpath( bpPath+'/bpn.sbc'), os.path.normpath( bpPath +'/bp.sbc'))
	print()
	return 0
# ----------------- Main Program ------------------------ 

bpName = input("\nPlease type in the name of the Blueprint you wish to modify: ")
print()
appDataPath = os.getenv('APPDATA')
bpPath = appDataPath + '/'+'SpaceEngineers/Blueprints/local/' + bpName
bpPath = os.path.normpath( bpPath )
exit = False
print('Blueprint Folder Location:\n', bpPath + '\\\n')

if not os.path.isdir( bpPath ):
	print( "Error: Blueprint Doesn't Exist\n" )
	exit = True
else:
	while( exit == False ):
		print("0: Edit (E)")
		print("1: quit/exit (q)\n")
		userInput = input( "--> ")
		if userInput.lower() == 'e' or userInput.lower() == 'edit' or userInput.lower() == '0':
			print()
			returnValue = doColorChange ( bpPath )
			if returnValue == 2:
			    break
		elif userInput.lower() == "q" or userInput.lower() =="exit" or userInput.lower() == "quit" or userInput.lower() == '0':
			print()
			exit = True
			break



