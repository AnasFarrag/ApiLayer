import os
import settings
import imghdr

# Function to check validity of an image
def is_valid_image(image):

    # list of valid image types
    image_types = ['gif', 'jpeg','jpg', 'bmp', 'png']

    # get image size
    image_size = os.stat(settings.BASE_DIR + image.filename).st_size

    # load allowed image size from settings
    max_image_size = settings.DATA_UPLOAD_MAX_MEMORY_SIZE

    # check of the uploaded image is less than the max file limit and the uploaded image is already an image
    if image_size > max_image_size and (imghdr.what(image.filename) not in image_types):
        return False
    return True



def upload_file_to_cloud(arg):
    pass

message = {
    'error': {'message': 'something went wreong'},

}
