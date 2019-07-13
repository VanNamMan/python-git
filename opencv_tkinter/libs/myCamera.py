from pypylon import pylon,genicam
import cv2

def getBaslerDevices():
    lstDev = []
    devices = pylon.TlFactory.GetInstance().EnumerateDevices()
    for dev in devices:
        camera = createDevice(dev)
        camera.StartGrabbing()
        lstDev.append([camera,camera.IsGrabbing(),dev.GetSerialNumber()])
    return lstDev

def createDevice(dev):
    return pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(dev))




# Pypylon get camera by serial number
# serial_number = '21043274'
# info = None
# for i in pylon.TlFactory.GetInstance().EnumerateDevices():
#     if i.GetSerialNumber() == serial_number:
#         info = i
#         break
# else:
#     print('Camera with {} serial number not found'.format(serial_number))

# # VERY IMPORTANT STEP! To use Basler PyPylon OpenCV viewer you have to call .Open() method on you camera
# if info is not None:
#     camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(info))
#     camera.StartGrabbing()
#     print(camera.IsGrabbing())
#     while (camera.IsGrabbing()):
#         grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
#         if grabResult.GrabSucceeded():
#             img = grabResult.Array
#             cv2.imshow("",img)
#             if cv2.waitKey(22) == ord("q"):
#                 break
#     cv2.destroyAllWindows()
#     camera.StopGrabbing()