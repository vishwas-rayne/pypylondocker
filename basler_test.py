from pypylon import pylon
from pypylon import genicam
import sys

def grab(camera):
    # Number of images to be grabbed.
    countOfImagesToGrab = 100

    # The exit code of the sample application.
    exitCode = 0

    try:
        # Create an instant camera object with the camera device found first.
        # camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()

        # Print the model name of the camera.
        print("Using device ", camera.GetDeviceInfo().GetModelName())

        # demonstrate some feature access
        new_width = camera.Width.GetValue() - camera.Width.GetInc()
        if new_width >= camera.Width.GetMin():
            camera.Width.SetValue(new_width)

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer = 5

        # Start the grabbing of c_countOfImagesToGrab images.
        # The camera device is parameterized with a default configuration which
        # sets up free-running continuous acquisition.
        camera.StartGrabbingMax(countOfImagesToGrab)

        # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        # when c_countOfImagesToGrab images have been retrieved.
        while camera.IsGrabbing():
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            # Image grabbed successfully?
            if grabResult.GrabSucceeded():
                # Access the image data.
                print("SizeX: ", grabResult.Width)
                print("SizeY: ", grabResult.Height)
                img = grabResult.Array
                print("Gray value of first pixel: ", img[0, 0])
            else:
                print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
            grabResult.Release()
        camera.Close()

    except genicam.GenericException as e:
        # Error handling.
        print("An exception occurred.")
        # print(e.GetDescription())
        exitCode = 1

    sys.exit(exitCode)

def main():
    factory = pylon.TlFactory.GetInstance()
    ptl = factory.CreateTl('BaslerGigE')

    empty_camera_info = ptl.CreateDeviceInfo()
    ip = '10.223.109.131'
    empty_camera_info.SetPropertyValue('IpAddress', ip)

    camera_device = factory.CreateDevice(empty_camera_info)
    cam_obj = pylon.InstantCamera(camera_device)
    grab(cam_obj)

def backup():
    ip_address = '10.223.109.131'
    info = pylon.DeviceInfo()
    info.SetPropertyValue('IpAddress', ip_address)

    print(info.GetPropertyNames())
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))
    grab(camera)

backup()