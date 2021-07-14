import owncloud
import os
import settings
from helpers import utils
class UserHelper():

    def upload_file(image, sso_sub):

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

            try:
                base_dir = 'upload/users'
                oc.mkdir(base_dir)
            except Exception as e:
                pass

            try:
                users_dir = '{}/{}'.format(base_dir,sso_sub)
                oc.mkdir(users_dir)
            except Exception as e:
                pass

            try:
                image_dir_in_cloud = '{}/images'.format(users_dir)
                oc.mkdir(image_dir_in_cloud)
            except Exception as e:
                pass


            cloud_dir = '{}/{}'.format(image_dir_in_cloud, 'profile_img{}'.format(os.path.splitext(image.filename)[1]))


            oc.put_file(cloud_dir, image_dir)

            image_link = oc.share_file_with_link(cloud_dir)

            # Remove image from media directory
            os.remove(image_dir)

            # we can also use
            #os.path.join(settings.BASE_DIR, str(image.filename))

            return image_link.get_link() + '/preview'
        except Exception as e:
            return False
