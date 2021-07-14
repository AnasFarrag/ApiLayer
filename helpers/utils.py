import os
import settings
import imghdr



# Function to check validity of an image
def is_valid_image(image):

    filename = image.filename
    # check if the uploaded image is already an image
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS



message = {
    'error': {'message': 'Something went wrong!'},
    'Reset_password_success': {'message': 'Your password has been reset successfully'},
    'required_fields': {'message': 'Some fields are required!'},
    'image_not_valid': {'message':'File must be an image type ans less than 10MB'},
    'unauthorized': {'message':'Unauthorized!'},
    'update_user_success': {'message':'Profile has been updated successfully'},
    'user_instructor_success': 'لقد تم تفعيل حساب المدرس الخاص بك، يمكنك تسجيل الدخول في لوحة التحكم الخاص بك لإنشاء اول حصة لك على منصة فاريانس',
    'user_instructor_successs': "user added succefully",

}
