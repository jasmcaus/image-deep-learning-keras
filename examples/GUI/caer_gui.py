# Simple tkinter GUI app example, designed to showcase some caer features
# Should only be used as a base to create a new GUI
# It can be re-designed, controls re-grouped and code improved

# Requirements: python3, caer, matplotlib

# Run it either via IDLE or from command prompt / terminal with one of these commands:
# - 'python caer_gui.py'
# - 'python -m caer_gui'
# - 'python3 caer_gui.py'
# - 'python3 -m caer_gui'

# Tested as working in Windows 10 with python v3.6.8 and Kubuntu Linux with python v3.6.8
# You can select one of 9 built-in images to display (startup has "Island" selected as default)
# Selecting any of the images, at any point in time, will always start with a fresh original image and reset controls.
# Replace with or add your own image(s) by following the instructions here: https://caer.readthedocs.io/en/latest/api/io.html
# The above will require that you modify the main() and show_original_image() functions
# All function controls are set to manipulate the currently displayed image
# Edges and Emboss effects are mutually exclusive (you can only have one applied at the time)
# The 'Rotation' button is currently set to keep on rotating the image with every tap

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from tkinter import *
import platform
import math
import caer

pythonVersion = platform.python_version()

def show_original_image(*args):
    global currentImage
    global image_size
    global resizedImgBtn
    global rotateImgBtn

    if resizedImgBtn['bg'] == 'lightblue':
        resizedImgBtn['bg'] = 'lightgrey'
    else:
        rotateImgBtn['bg'] = 'lightgrey'

    selectedImage = imageSelection.get()

    if selectedImage == 'Mountain':
        currentImage = caer.data.mountain(rgb=True)
    elif selectedImage == 'Sunrise':
        currentImage = caer.data.sunrise(rgb=True)
    elif selectedImage == 'Island':
        currentImage = caer.data.island(rgb=True)
    elif selectedImage == 'Puppies':
        currentImage = caer.data.puppies(rgb=True)
    elif selectedImage == 'Black Cat':
        currentImage = caer.data.black_cat(rgb=True)
    elif selectedImage == 'Gold Fish':
        currentImage = caer.data.gold_fish(rgb=True)
    elif selectedImage == 'Bear':
        currentImage = caer.data.bear(rgb=True)
    elif selectedImage == 'Camera':
        currentImage = caer.data.camera(rgb=True)
    else:
        currentImage = caer.data.guitar(rgb=True)

    image_size = [str(int(currentImage.width())), str(int(currentImage.height()))]
    selectedSize.set(image_size[0] + 'x' + image_size[1])

    reset_ghsps()

    image_show(currentImage)

def resize_image():
    global resizedImgBtn
    global rotateImgBtn
    global image_resized
    global image_size

    tempSize = selectedSize.get()

    if 'x' in tempSize:
        try:
            findex = tempSize.index('x')
            lindex = tempSize.rindex('x')

            if findex == lindex:
                image_size = tempSize.replace(' ', '').split('x')

                # test if all values can be represented with an integer
                int(image_size[0])
                int(image_size[1])

                if resizedImgBtn['bg'] == 'lightgrey':
                    resizedImgBtn['bg'] = 'lightblue'
                    rotateImgBtn['bg'] = 'lightgrey'

                image_resized = True

                adjust_ghsps()
            else:
                print('Invalid size specified!')
        except Exception as e:
            print(str(e))
    else:
        print('Invalid size specified!')

def show_rotated_image(external = False):
    global rotationApplied
    global lblCurrentAngle
    global currentAngle
    global resizedImgBtn
    global rotateImgBtn

    angle = selectedAngle.get()

    try:
        # test if angle value can be represented with a float
        float(angle)

        if angle == '':
            angle = '0.0'
            currentAngle = 0.0
            rotationApplied = False
        elif angle == '0.0' or ((float(angle) > 0 or float(angle) < 0) and math.fmod(float(angle), 360) == 0):
            currentAngle = 0.0
            rotationApplied = False
        else:
            if not external:
                currentAngle += float(angle)

            mod = math.fmod(currentAngle, 360)

            if currentAngle > 360 or currentAngle < -360:
                currentAngle = mod
                rotationApplied = True
            elif mod == 0:
                currentAngle = 0.0
                rotationApplied = False
            else:
                rotationApplied = True

        lblCurrentAngle['text'] = str(currentAngle)

        tempAnchorPoint = anchorSelection.get()

        if tempAnchorPoint == 'Center':
            anchor = None
        elif tempAnchorPoint == 'TopLeft':
            anchor = (0, 0)
        elif tempAnchorPoint == 'TopMiddle':
            anchor = ((currentImage.width() // 2), 0)
        elif tempAnchorPoint == 'TopRight':
            anchor = (currentImage.width(), 0)
        elif tempAnchorPoint == 'MiddleLeft':
            anchor = (0, (currentImage.height() // 2))
        elif tempAnchorPoint == 'MiddleRight':
            anchor = (currentImage.width(), (currentImage.height() // 2))
        elif tempAnchorPoint == 'BottomLeft':
            anchor = (0, currentImage.height())
        elif tempAnchorPoint == 'BottomMiddle':
            anchor = ((currentImage.width() // 2), currentImage.height())
        elif tempAnchorPoint == 'BottomRight':
            anchor = (currentImage.width(), currentImage.height())

        if rotateImgBtn['bg'] == 'lightgrey':
            rotateImgBtn['bg'] = 'lightblue'
            resizedImgBtn['bg'] = 'lightgrey'

        # only display the rotated version of the image
        if not transformedImage is None:
            rot = caer.to_tensor(caer.transforms.rotate(transformedImage, float(currentAngle), rotPoint=anchor), cspace = 'rgb')
        else:
            rot = caer.to_tensor(caer.transforms.rotate(currentImage, float(currentAngle), rotPoint=anchor), cspace = 'rgb')

        image_show(rot)
    except Exception as e:
        print(str(e))

def image_show(tens):
    subplot.clear()
    subplot.imshow(tens) # optionally add aspect='auto' to switch to automatic aspect mode
    canvas.draw()

def refresh_axis():
    global showAxis

    # Hide / Show the graph's x / y axis
    if not showAxis:
        subplot.xaxis.set_visible(True), subplot.yaxis.set_visible(True)
        showAxis = True
    else:
        subplot.xaxis.set_visible(False), subplot.yaxis.set_visible(False)
        showAxis = False

    fig.canvas.draw()

def flip_image_horizontally():
    global flip_H

    flip_H = not flip_H
    adjust_ghsps()

def flip_image_vertically():
    global flip_V

    flip_V = not flip_V
    adjust_ghsps()

def set_edges():
    global show_emboss

    if show_edges.get() == 1:
        show_emboss.set(0)

    adjust_ghsps()

def set_emboss():
    global show_edges

    if show_emboss.get() == 1:
        show_edges.set(0)
    
    adjust_ghsps()

def adjust_ghsps(*args):
    global transformedImage

    if not currentImage is None:
        # apply all transformations to currently displayed image
        if image_resized:
            transformedImage = caer.to_tensor(caer.resize(currentImage, target_size=(int(image_size[0]),int(image_size[1])), preserve_aspect_ratio=False), cspace = 'rgb')
            transformedImage = caer.to_tensor(caer.transforms.adjust_hue(transformedImage, hue.get()), cspace = 'rgb')
        else:
            transformedImage = caer.to_tensor(caer.transforms.adjust_hue(currentImage, hue.get()), cspace = 'rgb')

        transformedImage = caer.to_tensor(caer.transforms.adjust_saturation(transformedImage, saturation.get()), cspace = 'rgb')
        transformedImage = caer.to_tensor(caer.transforms.adjust_gamma(transformedImage, imgGamma.get()), cspace = 'rgb')

        if sharpen.get() != 8.9:
            kernel = caer.data.np.array([[-1, -1, -1], [-1, sharpen.get(), -1], [-1, -1, -1]])
            transformedImage = caer.to_tensor(caer.core.cv.filter2D(transformedImage, -1, kernel), cspace = 'rgb')

        gb = gaussian_blur.get()

        if gb > 1:
            transformedImage = caer.to_tensor(caer.core.cv.GaussianBlur(transformedImage, (gb + 1, gb + 1), caer.core.cv.BORDER_DEFAULT), cspace = 'rgb')

        if posterize.get() < 6:
            transformedImage = caer.to_tensor(caer.transforms.posterize(transformedImage, posterize.get()), cspace = 'rgb')

        if solarize.get() < 255:
            transformedImage = caer.to_tensor(caer.transforms.solarize(transformedImage, solarize.get()), cspace = 'rgb')

        if show_edges.get() == 1:
            transformedImage = caer.to_tensor(caer.core.cv.Canny(transformedImage, low_threshold.get(), low_threshold.get() * 2), cspace = 'rgb')

        if show_emboss.get() == 1:
            kernel = caer.data.np.array([[0, 1, 0], [0, 0, 0], [0, -1, 0]])
            transformedImage = caer.to_tensor(caer.core.cv.filter2D(transformedImage, -1, kernel) + emboss.get(), cspace = 'rgb')

        if flip_H:
            transformedImage = caer.to_tensor(caer.transforms.hflip(transformedImage), cspace = 'rgb')

        if flip_V:
            transformedImage = caer.to_tensor(caer.transforms.vflip(transformedImage), cspace = 'rgb')

        if rotationApplied:
            show_rotated_image(True)
        else:
            image_show(transformedImage)

def reset_ghsps():
    global rotationApplied
    global lblCurrentAngle
    global currentAngle
    global image_resized
    global transformedImage
    global imgGamma
    global hue
    global saturation
    global gaussian_blur
    global posterize
    global solarize
    global show_edges
    global low_threshold
    global sharpen
    global show_emboss
    global emboss
    global flip_H
    global flip_V

    transformedImage = None

    # reset flags and variables
    image_resized = False
    rotationApplied = False
    selectedAngle.set('0.0')
    currentAngle = 0.0
    lblCurrentAngle['text'] = str(currentAngle)

    # reset flip buttons
    btnFlip_H.deselect()
    flip_H = False
    btnFlip_V.deselect()
    flip_V = False

    # reset all sliders
    imgGamma.set(1.0)
    hue.set(0.0)
    saturation.set(1.0)
    gaussian_blur.set(0)
    posterize.set(6)
    solarize.set(255)
    show_edges.set(0)
    low_threshold.set(50)
    sharpen.set(8.9)
    show_emboss.set(0)
    emboss.set(114)

def main():
    global root
    global canvas
    global fig
    global subplot
    global currentImage
    global transformedImage
    global imageSelection
    global showAxis
    global sliderSolarize
    global resizedImgBtn
    global flip_H
    global flip_V
    global btnFlip_H
    global btnFlip_V
    global rotateImgBtn
    global selectedSize
    global selectedAngle
    global resizedImgSize
    global rotationAngle
    global anchorSelection
    global rotationApplied
    global lblCurrentAngle
    global currentAngle
    global imgGamma
    global hue
    global saturation
    global gaussian_blur
    global posterize
    global solarize
    global show_edges
    global low_threshold
    global sharpen
    global show_emboss
    global emboss

    # create our window
    root = Tk()
    root.config(background='white')
    root.title('CAER GUI - Python v' + pythonVersion)
    root.geometry('1024x768')

    # the following works for a single screen setup
    # if using a multi-screen setup then see the following link:
    # Ref: https://stackoverflow.com/questions/3129322/how-do-i-get-monitor-resolution-in-python/56913005#56913005
    screenDPI = root.winfo_fpixels('1i')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    currentImage = None
    transformedImage = None
    rotationApplied = False
    showAxis = False
    flip_H, flip_V = False, False
    currentAngle = 0.0

    # bind the 'q' keyboard key to quit
    root.bind('q', lambda event:root.destroy())

    #-----------------------------------------------------------------------

    # add a frame to hold top controls
    frame1 = Frame(root, background='black')
    frame1.pack(side=TOP, fill=X)

    # create the built-in image selection variable and choices
    imageSelection = StringVar()
    imageChoices = { 'Mountain', 'Sunrise', 'Island', 'Puppies', 'Black Cat', 'Gold Fish', 'Bear', 'Camera', 'Guitar'}
    imageSelection.set('Island')
    imageSelection.trace('w', show_original_image)

    # create the built-in image selection popup menu
    popup_menu_image = OptionMenu(frame1, imageSelection, *imageChoices)
    popup_menu_image['width'] = 10
    popup_menu_image['bg'] = 'lightgreen'
    popup_menu_image.pack(side=LEFT, padx=2)

    # create a button to re-size the image
    resizedImgBtn = Button(frame1, text='Resize', width=6, bg='lightgrey', relief=RAISED, command=resize_image)
    resizedImgBtn.pack(side=LEFT, padx=2, pady=2)

    # create an entry box for re-size dimensions
    selectedSize = StringVar()
    resizedImgSize = Entry(frame1, justify=CENTER, textvariable=selectedSize, font='Helvetica 10', width=10, bg='white', relief=RAISED)
    resizedImgSize.pack(side=LEFT, padx=2, pady=2)
    selectedSize.set('')

    # create a button to rotate the image
    rotateImgBtn = Button(frame1, text='Rotate', width=6, bg='lightgrey', relief=RAISED, command=show_rotated_image)
    rotateImgBtn.pack(side=LEFT, padx=2, pady=2)

    # create a label for the rotation angle
    lblAngle = Label(frame1, text='Angle', fg='yellow', bg='black', font='Helvetica 8')
    lblAngle.pack(side=LEFT, padx=2, pady=2)

    # create the rotation angle selection variable and an entry box
    selectedAngle = StringVar()
    rotationAngle = Entry(frame1, justify=CENTER, textvariable=selectedAngle, font='Helvetica 10', width=5, bg='white', relief=RAISED)
    rotationAngle.pack(side=LEFT, padx=2, pady=2)
    selectedAngle.set('0.0')

    # create a read-only label for the current angle
    lblCurrentAngle = Label(frame1, text='0.0', state='disabled', fg='lightgrey', bg='white', font='Helvetica 8', width=5)
    lblCurrentAngle.pack(side=LEFT, padx=2, pady=2)

    # create a label for the rotation anchor
    lblAnchor = Label(frame1, text='Anchor', fg='yellow', bg='black', font='Helvetica 8')
    lblAnchor.pack(side=LEFT, padx=2, pady=2)

    # create the rotation anchor selection variable and choices
    anchorSelection = StringVar()
    anchorChoices = { 'BottomLeft', 'BottomMiddle', 'BottomRight', 'Center', 'MiddleLeft', 'MiddleRight', 'TopLeft', 'TopMiddle', 'TopRight'}
    anchorSelection.set('Center')

    # create the anchor selection popup menu
    popup_menu_anchor = OptionMenu(frame1, anchorSelection, *anchorChoices)
    popup_menu_anchor['width'] = 12
    popup_menu_anchor.pack(side=LEFT, padx=2)

    #-----------------------------------------------------------------------

    # add a frame to hold side controls and screen attributes labels
    frame2 = Frame(root, background='black')
    frame2.pack(side=RIGHT, fill=Y)

    # create the image gamma slider control
    imgGamma = DoubleVar()
    sliderGamma = Scale(frame2, label='Gamma', variable=imgGamma, troughcolor='blue', from_=0.0, to=2.0, resolution=0.1, sliderlength=15, showvalue=False, orient=HORIZONTAL, command=adjust_ghsps)
    sliderGamma.pack(side=TOP, anchor=E, padx=2, pady=2)
    imgGamma.set(1.0)

    # create the image hue slider control
    hue = DoubleVar()
    sliderHue = Scale(frame2, label='Hue', variable=hue, troughcolor='blue', from_=-0.5, to=0.5, resolution=0.05, sliderlength=15, showvalue=False, orient=HORIZONTAL, command=adjust_ghsps)
    sliderHue.pack(side=TOP, anchor=E, padx=2, pady=2)
    hue.set(0.0)

    # create the image saturation slider control
    saturation = DoubleVar()
    sliderSaturation = Scale(frame2, label='Saturation', variable=saturation, troughcolor='blue', from_=0.0, to=2.0, resolution=0.1, sliderlength=15, showvalue=False, orient=HORIZONTAL, command=adjust_ghsps)
    sliderSaturation.pack(side=TOP, anchor=E, padx=2, pady=2)
    saturation.set(1.0)

    # create the image sharpen slider control
    sharpen = DoubleVar()
    sliderSharpen = Scale(frame2, label='Sharpen', variable=sharpen, troughcolor='blue', from_=7.9, to=9.9, resolution=0.05, sliderlength=15, showvalue=False, orient=HORIZONTAL, command=adjust_ghsps)
    sliderSharpen.pack(side=TOP, padx=2, pady=5)
    sharpen.set(8.9)

    # create the image Gaussian Blur slider control
    gaussian_blur = IntVar()
    sliderGaussianBlur = Scale(frame2, label='Gaussian Blur', variable=gaussian_blur, troughcolor='blue', from_=0, to=10, resolution=2, sliderlength=15, showvalue=False, orient=HORIZONTAL, command=adjust_ghsps)
    sliderGaussianBlur.pack(side=TOP, padx=2, pady=5)
    gaussian_blur.set(0)

    # create the image posterize slider control
    posterize = IntVar()
    sliderPosterize = Scale(frame2, label='Posterize', variable=posterize, troughcolor='blue', from_=6, to=1, resolution=1, sliderlength=15, showvalue=False, orient=HORIZONTAL, command=adjust_ghsps)
    sliderPosterize.pack(side=TOP, padx=2, pady=5)
    posterize.set(6)

    # create the image solarize slider control
    solarize = IntVar()
    sliderSolarize = Scale(frame2, label='Solarize', variable=solarize, troughcolor='blue', from_=255, to=0, resolution=1, sliderlength=15, showvalue=False, orient=HORIZONTAL, command=adjust_ghsps)
    sliderSolarize.pack(side=TOP, padx=2, pady=5)
    solarize.set(255)

    # add 'Edges' checkbox
    show_edges = IntVar()
    chbShowEdges = Checkbutton(frame2, text='Edges', variable=show_edges, width=7, command=set_edges)
    chbShowEdges.pack(side=TOP, padx=2, pady=5)
    show_edges.set(0)

    # create the image edges low threshold slider control
    low_threshold = IntVar()
    sliderLowThreshold = Scale(frame2, label='Edges Threshold', variable=low_threshold, troughcolor='blue', from_=100, to=0, resolution=1, sliderlength=15, showvalue=False, orient=HORIZONTAL, command=adjust_ghsps)
    sliderLowThreshold.pack(side=TOP, padx=2, pady=5)
    low_threshold.set(50)

    # add 'Emboss' checkbox
    show_emboss = IntVar()
    chbShowEmboss = Checkbutton(frame2, text='Emboss', variable=show_emboss, width=7, command=set_emboss)
    chbShowEmboss.pack(side=TOP, padx=2, pady=5)
    show_emboss.set(0)

    # create the image emboss slider control
    emboss = IntVar()
    sliderEmboss = Scale(frame2, label='Emboss Threshold', variable=emboss, troughcolor='blue', from_=128, to=99, resolution=1, sliderlength=15, showvalue=False, orient=HORIZONTAL, command=adjust_ghsps)
    sliderEmboss.pack(side=TOP, padx=2, pady=5)
    emboss.set(114)

    lblScreen = Label(frame2, text='Screen', fg='grey', bg='black', font='Helvetica 9')
    lblScreen.pack(side=TOP, anchor=CENTER, pady=15)

    lblResolution = Label(frame2, text='res: ' + str(screen_width) + 'x' + str(screen_height), fg='grey', bg='black', font='Helvetica 9')
    lblResolution.pack(side=TOP, anchor=CENTER)

    lblDPI = Label(frame2, text='dpi: ' + str(int(screenDPI)), fg='grey', bg='black', font='Helvetica 9')
    lblDPI.pack(side=TOP, anchor=CENTER)

    # add exit button
    exitBtn = Button(frame2, text='Exit', width=7, fg='red', bg='lightgrey', relief=RAISED, command=root.destroy)
    exitBtn.pack(side=BOTTOM, anchor=CENTER, pady=4)

    #-----------------------------------------------------------------------

    # create matplotlib figure, subplot, canvas and toolbar
    fig = Figure(figsize=(640//screenDPI, 427//screenDPI), dpi=int(screenDPI))
    subplot = fig.add_subplot(111)
    subplot.xaxis.set_visible(False), subplot.yaxis.set_visible(False)
    fig.set_tight_layout(True)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar._Spacer()
    toolbar._Button('Show Axis', None, toggle=True, command=refresh_axis)
    toolbar._Spacer()
    toolbar._Button('Reload Image', None, toggle=False, command=show_original_image)
    toolbar._Spacer()
    btnFlip_H = toolbar._Button('FlipH', None, toggle=True, command=flip_image_horizontally)
    toolbar._Spacer()
    btnFlip_V = toolbar._Button('FlipV', None, toggle=True, command=flip_image_vertically)
    toolbar.update()

    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    #-----------------------------------------------------------------------

    # set the minimum window size to the current size
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

    show_original_image()

    root.mainloop()

if __name__=='__main__':
    main()
    caer.core.cv.destroyAllWindows()
