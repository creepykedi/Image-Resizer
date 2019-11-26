#! python3
# imageResizer.py - gets all the images in the directory and halves their size if they are larger than you need
import os, re, send2trash, threading
import PySimpleGUI as sg
from PIL import Image

# defining picture extensions
def Imagetype(JPG, PNG):
    if JPG is True and PNG is True:
        image_pattern = re.compile(r'(.*)(.jpg|.jpeg|.JPG|.png|.PNG)')
        return image_pattern
    elif JPG is True and PNG is False:
        image_pattern = re.compile(r'(.*)(.jpg|.jpeg|.JPG)')
        return image_pattern
    elif PNG is True:
        image_pattern = re.compile(r'(.*)(.png|.PNG)')
        return image_pattern


def imageResize(path, sizeLimit, resizeFactor, keepOriginal, replace, JPG, PNG):
    os.chdir(path)
    # defining image extensions
    image_pattern = Imagetype(JPG, PNG)
    counter = 0
    files = 0
    # walking through directory
    for folderName, subfolder, file in os.walk(path):
        # cpt is total amount of files in directory
        cpt = sum([len(file) for r, d, files in os.walk(path)])
        if cpt != 0:
            # since progress bar length is 100, determine what % to increment for each file
            add = float(100/cpt)
        for image in file:
            # finding images
            located_files = image_pattern.search(image)
            # updating progress bar
            files = files + add
            window.Element('progbar').UpdateBar(files)
            if located_files is not None:
                # getting image path
                pathToImage = os.path.join(folderName, located_files.group())
                try:
                    imageSize = os.path.getsize(pathToImage)
                    # getting size of file
                    if imageSize > int(sizeLimit)*1000:
                        counter += 1
                        try:
                            # opening needed image
                            curImage = Image.open(pathToImage)
                            width, height = curImage.size
                            # resizing by factor
                            quartesSizedIm = curImage.resize((int(width / float(resizeFactor)),
                                                              int(height / float(resizeFactor))))
                            print('{} resized'.format(image))
                            # saving in the same directory with a new name
                            if replace is False:
                                quartesSizedIm.save(pathToImage[:-4] + 'res' + pathToImage[-4:])
                            else:
                                quartesSizedIm.save(pathToImage)
                            # deleting original
                            if keepOriginal is False and replace is False:
                                send2trash.send2trash(pathToImage.replace('/', '\\'))
                                print(pathToImage.replace('/', '\\'))
                            # avoids error of "file doesn't exist"
                        except OSError as e:
                            continue
                        except ValueError:
                            continue
                except FileNotFoundError:
                    continue
            else:
                continue
    print('Done.{} images resized'.format(counter))



# making graphic interface
layout = [[sg.Text('Choose folder to resize images from: ', justification='right')],
            [sg.InputText('Your folder'), sg.FolderBrowse(button_color=('black', 'white'))],
            [sg.Text('Image extensions:'), sg.T(' ' * 13), sg.Text('Resize images larger than, KB:'),
            sg.T(' ' * 15), sg.Text('Resize factor:')],
            [sg.Checkbox('JPG', default=True), sg.Checkbox('PNG', default=True), sg.T(' ' * 12),
           sg.In(size=(15, 1), default_text=1000), sg.T(' ' * 34), sg.Input(default_text=1.5, size=(7, 1))],
          [sg.Radio('Replace original files', 'originals'), sg.T(' ' * 4),
           sg.Radio('Move original files to trash', 'originals', default=True), sg.T(' ' * 8),
           sg.Radio('Keep originals', 'originals')],
            [sg.Output(size=(70, 8))],
            [sg.T(' ' * 1), sg.ProgressBar(100, orientation='h', size=(41, 20), key='progbar'),
           sg.Button(('    Start    '), button_color=('white', 'green'))],
          [sg.Button('  Stop  ', button_color=('black', 'orange')), sg.T(' ' * 94)]]

window = sg.Window('Image Resizer').Layout(layout)
button, values = window.Read()

while True:
    button, values = window.Read()
    if button in (None, '  Stop  '):
        break 
    if button == '    Start    ':
    #    threading.Thread(target=progress()).start()
        Imagetype(values[1], values[2])
        imageResize(values['Browse'], int(values[3]), float(values[4]), values[7], values[5], values[1], values[2])


