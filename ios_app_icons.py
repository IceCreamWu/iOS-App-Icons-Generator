# -*- coding: utf-8 -*-
from PIL import Image
import os
import shutil
import json

iconFileName = 'icon.png'
iconSizeAndScale_iPhone = [(20, 2), (20, 3), (29, 1), (29, 2), (29, 3), (40, 2), (40, 3), (57, 1), (57, 2), (60, 2), (60, 3)]
iconSizeAndScale_iPad = [(20, 1), (20, 2), (29, 1), (29, 2), (40, 1), (40, 2), (50, 1), (50, 2), (72, 1), (72, 2), (76, 1), (76, 2), (83.5, 2)]


AssetsDirName = 'Assets.xcassets'
AppIconDirName = 'AppIcon.appiconset'
FinalDirName = os.path.join(AssetsDirName, AppIconDirName)

def outputXcodeContents():
    info = {}
    info['author'] = 'xcode'
    info['version'] = '1'

    images = []
    for size, scale in iconSizeAndScale_iPhone:
        item = {}
        item['idiom'] = 'iphone'
        item['size'] = ('%dx%d' if isinstance(size, int) else '%.1fx%.1f') % (size, size)
        item['scale'] = '%dx' % scale
        item['filename'] = 'icon_%d.png' % (size * scale)
        images.append(item)
    for size, scale in iconSizeAndScale_iPad:
        item = {}
        item['idiom'] = 'ipad'
        item['size'] = ('%dx%d' if isinstance(size, int) else '%.1fx%.1f') % (size, size)
        item['scale'] = '%dx' % scale
        item['filename'] = 'icon_%d.png' % (size * scale)
        images.append(item)

    contents = {}
    contents['images'] = images
    contents['info'] = info

    fileName = os.path.join(FinalDirName, 'Contents.json')
    json.dump(contents, open(fileName, 'wb'), indent=True)

def outputImages():
    allSizes = [size*scale for size, scale in iconSizeAndScale_iPhone + iconSizeAndScale_iPad]
    iconSizes = list(set(allSizes))
    iconSizes.sort()
    for iconSize in iconSizes:
        iconImage = Image.open(iconFileName)
        iconImage.thumbnail((iconSize, iconSize))

        fileName = os.path.join(FinalDirName, 'icon_%d.png' % iconSize)
        iconImage.save(fileName)
        iconImage.close()

if __name__ == '__main__':
    if not os.path.exists(iconFileName):
        print "No File exist: %s!" % iconFileName

    if os.path.exists(AssetsDirName) and os.path.isdir(AssetsDirName):
        shutil.rmtree(AssetsDirName)
    os.mkdir(AssetsDirName)
    os.mkdir(FinalDirName)

    outputImages()
    outputXcodeContents()


