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
        image_size = image.seek(0, os.SEEK_END)
        #image_size = os.stat(settings.BASE_DIR + image.filename).st_size   ---> another way

        if image_size < max_image_size:
            return True

    return False






def upload_file_to_cloud(arg):
    pass

message = {

    
}
