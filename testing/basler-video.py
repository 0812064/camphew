"""
most basic script for connecting a basler camera and reading images
based on the instruction by Aquiles
https://www.pythonforthelab.com/blog/getting-started-with-basler-cameras/

"""
import numpy as np
from pypylon import pylon
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

tl_factory = pylon.TlFactory.GetInstance()
devices = tl_factory.EnumerateDevices()
for device in devices:
    print(device.GetFriendlyName())

#defining camera and gui parameters

exptime = 10 #exposure time in ms
imgcount = 0
fig, ax = plt.subplots()
t00 = time.time()

#initializing camera
camera = pylon.InstantCamera()
camera.Attach(tl_factory.CreateFirstDevice())
camera.Open()
camera.OffsetX.SetValue(0)
camera.OffsetY.SetValue(0)
camera.Width.SetValue(camera.WidthMax.GetValue())
camera.Height.SetValue(camera.HeightMax.GetValue())
#setting camera parameters
camera.ExposureTime.SetValue(exptime*1000)
camera.Height.SetValue(128)

pixel_format = camera.PixelFormat.GetValue()
print('format:', pixel_format)
if pixel_format == 'Mono8':
    cam_dtype = np.uint8
elif pixel_format == 'Mono12' or pixel_format == 'Mono12p':
    cam_dtype = np.uint16

camera.StartGrabbing(1)
grab = camera.RetrieveResult(1000, pylon.TimeoutHandling_Return)
if grab.GrabSucceeded():
    image = grab.GetArray()
    print(f'Size of image: {image.shape}')
    im = ax.imshow(image, cmap=plt.cm.hot, origin='upper')
else:
    image=[]
    print('unable to grab an image')

ypix, xpix = camera.Height.Value, camera.Width.Value

def update(i, image, tproc):
    global imgcount
    if camera.IsGrabbing():
        camera.StopGrabbing()
    nf = 10
    imgarray = np.zeros((xpix, ypix, nf), dtype= cam_dtype)
    camera.StartGrabbingMax(nf)
    t0 = time.time()   #note that system time is given in seconds
    rf = 0
    while camera.IsGrabbing():
        grab = camera.RetrieveResult(500, pylon.TimeoutHandling_ThrowException)
        if grab.GrabSucceeded():
            tempimg = grab.GetArray().T
            imgarray[:, :, rf] = tempimg
            rf += 1
            #basler-video.pyprint(rf, 'success')
        tlap = (time.time() - t0) * 1000
        #if rf >= nf or tlap > tproc:
        #    camera.StopGrabbing()

    grab.Release()
    print(f'Acquired {rf} of {nf} possible frames in {tlap} ms')
    imgcount += rf
    image = tempimg
    im.set_data(image)
    fig.canvas.draw()
    fig.canvas.flush_events()



tproc = 1000     #time duration in ms of image processing
ani = animation.FuncAnimation(fig, update, fargs=(image, tproc), interval=tproc+500)
plt.show()


#closing the camera processes
print(f'Acquired {imgcount} frames in {time.time()-t00:.0f} seconds')

camera.Close()



