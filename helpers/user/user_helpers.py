import owncloud
import os
import settings
from helpers import utils
class UserHelper():

    def upload_file(image):

        #image directory
        image_dir = settings.UPLOAD_DIR + image.filename
        #check if the uploaded file is valid image
        if not utils.is_valid_image(image):
            return False

        try:
            # save image to the BASE directory
            image.save(image_dir)

            # set CLOUD URL
            oc = owncloud.Client(settings.CLOUD_URL)

            # Log In to the CLOUD
            oc.login(settings.CLOUD_USERNAME, settings.CLOUD_PASSWORD)

            # oc.mkdir('upload/123')
            cloud_dir = 'upload/123/{}'.format(image.filename)

            oc.put_file(cloud_dir, image_dir)

            image_link = oc.share_file_with_link(cloud_dir)

            # Remove image from media directory
            os.remove(image_dir)

            # we can also use
            #os.path.join(settings.BASE_DIR, str(image.filename))

            return image_link.get_link() + '/preview'
        except:
            return False
