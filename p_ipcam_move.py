
from time import sleep

from onvif import ONVIFCamera

XMAX = 100
XMIN = -100
YMAX = 100
YMIN = -100


def perform_move(ptz,request,timeout):
     # Start continuous move
        ptz.ContinuousMove(request)
     # Wait a certain time
        sleep(timeout)
     # Stop continuous move
        ptz.Stop({'ProfileToken': request.ProfileToken})

def move_up(perform_move):
        super(move_up,self)._init_(ptz,request,timeout=1)
        print ("move up...")
        request.Velocity.PanTilt._x = 0
        request.Velocity.PanTilt._y = YMAX
#perform_move(ptz, request, timeout)

def move_down(perform_move):
        super(move_down,self)._init_(ptz, request, timeout=1)
        print ('move down...')
        request.Velocity.PanTilt._x = 0
        request.Velocity.PanTilt._y = YMIN
#perform_move(ptz, request, timeout)
def move_right(perform_move): 
        super(move_right,self)._init_(ptz, request, timeout=1)
        print ('move right...')
        request.Velocity.PanTilt._x = XMAX
        request.Velocity.PanTilt._y = 0
#perform_move(ptz, request, timeout)

def move_left(perform_move):
        super(move_left,self)._init_(ptz, request, timeout=1)
        print ('move left...')
        request.Velocity.PanTilt._x = XMIN
        request.Velocity.PanTilt._y = 0
# perform_move(ptz, request, timeout)

def continuous_move():
    
    print "1"
    mycam = ONVIFCamera('192.168.43.161', 29444, 'admin', '88888888','/usr/local/lib/python2.7/dist-packages/onvif_zeep-0.2.12-py2.7.egg/wsdl')
    print "2"
    # Create media service object
    media = mycam.create_media_service()
    # Create ptz service object
    ptz = mycam.create_ptz_service()

    # Get target profile
    media_profile = media.GetProfiles()[0];
    print "a"
    # Get PTZ configuration options for getting continuous move range
    request = ptz.create_type('GetConfigurationOptions')
    request.ConfigurationToken = media_profile.PTZConfiguration._token
    ptz_configuration_options = ptz.GetConfigurationOptions(request)
    print "b"
    request = ptz.create_type('ContinuousMove')
    request.ProfileToken = media_profile._token
    print "c"
    ptz.Stop({'ProfileToken': media_profile._token})

    # Get range of pan and tilt
    # NOTE: X and Y are velocity vector
    global XMAX, XMIN, YMAX, YMIN
    XMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
    XMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
    YMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
    YMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min
    print "D"
    # move right
    move_right(ptz, request)

    # move left
    move_left(ptz, request)

    # Move up
    move_up(ptz, request)

    # move down
    move_down(ptz, request)
    print"e"

if __name__ == '__main__':
    continuous_move()
