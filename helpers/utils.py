import os
import settings
import imghdr
import socket
from requests_futures.sessions import FuturesSession
# Function to check validity of an image
def is_valid_image(image_name):

    # check if the uploaded image is already an image
    return '.' in image_name and \
           image_name.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS


# check if SSO, ERP, and CLOUD are running
#Deprecated
def check_services():
    session = FuturesSession()
    # These requests will run at the same time
    try:
        cloud = session.get(settings.CLOUD_URL)
        erp = session.get(settings.ERP_URL)
        sso = session.get(settings.SSO_BASE_URL)

        cloud_result = cloud.result()
        erp_result = erp.result()
        sso_result = sso.result()

        return True
    except:
        return False

# check if SSO, ERP, and CLOUD are running
def is_services_online():
    """ This function checks to see if a host nam of SSO, ERP, or CLOUD e has a DNS entry by checking
        for socket info. If the website gets something in return,
        we know it's available to DNS.
    """
    try:
        socket.gethostbyname(settings.CLOUD_DOMAIN)
        socket.gethostbyname(settings.ERP_DOMAIN)
        socket.gethostbyname(settings.SSO_DOMAIN)
    except socket.gaierror:
        return False
    else:
        return True

message = {
    'error': {'message': 'Something went wrong!'},
    'server_down': {'message': 'We are sorry!. Service is temporarily unavailable.'},
    'phone_exist': {'message':'This phone already exists.'},
    'Reset_password_success': {'message': 'Your password has been reset successfully'},
    'required_fields': {'message': 'Some fields are required!'},
    'image_not_valid': {'message':'File must be an image type ans less than 10MB'},
    'unauthorized': {'message':'Unauthorized!'},
    'update_user_success': {'message':'Profile has been updated successfully'},
    'user_instructor_success': 'لقد تم تفعيل حساب المدرس الخاص بك، يمكنك تسجيل الدخول في لوحة التحكم الخاص بك لإنشاء اول حصة لك على منصة فاريانس',
    'user_instructor_successs':{"message" : "user added succefully"} ,


    #Anas Messages
    'login_in_SSO_not_valid': {'message':"there's someting wrong during the login!"},
    'user_instructor_successs': {'message': "user added succefully"},
    'save_language_successs': {'message': "language saved succefully"},

}
