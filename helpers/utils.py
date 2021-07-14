import os
import settings
import imghdr


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS



# Function to check validity of an image
def is_valid_image(image):

    # load allowed image size from settings
    max_image_size = settings.DATA_UPLOAD_MAX_MEMORY_SIZE

    # check if the uploaded image is less than the max file limit and the uploaded image is already an image
    if allowed_file(image.filename):

        # get image size
        image_size = 100

        #image_size = os.stat(settings.BASE_DIR + image.filename).st_size   ---> another way

        if image_size < max_image_size:
            print(image_size)
            return True

    return False








message = {
    'error': {'message': 'Something went wrong!'},
    'server_down': {'message': 'We are sorry!. Service is temporarily unavailable.'},
    'Reset_password_success': {'message': 'Your password has been reset successfully'},
    'required_fields': {'message': 'Some fields are required!'},
    'image_not_valid': {'message':'File must be an image type ans less than 10MB'},
    'unauthorized': {'message':'Unauthorized!'},
    'update_user_success': {'message':'Profile has been updated successfully'},
}
