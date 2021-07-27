import os
import settings
from helpers import utils
import uuid
import time

class UserHelper:
    def upload_file(image_name):
        try:

            #image directory
            image_dir = settings.UPLOAD_DIR + image_name

            cloud_dir = ''.join( (settings.UPLOAD_DIR_IN_CLOUD, '/', str(uuid.uuid4()), image_name) )

            start = time.perf_counter()
            settings.CLOUD.put_file(cloud_dir, image_dir)
            end = time.perf_counter()
            print(round(end-start,2))
            start = time.perf_counter()
            image_link = settings.CLOUD.share_file_with_link(cloud_dir)
            end = time.perf_counter()
            print(round(end-start,2))
            # Remove image from media directory
            os.remove(image_dir)

            # we can also use
            #os.path.join(settings.BASE_DIR, str(image.filename))
            return image_link.get_link() + '/preview'

        except Exception as e:
            print(e)
            return False

def upload_certificate(image_name,sso_sub):
    
        #image directory
        image_dir = settings.STATIC_DIR +'images/{}'.format(image_name)
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


        cloud_dir = '{}/{}'.format(image_dir_in_cloud, image_name)


        oc.put_file(cloud_dir, image_dir)

        image_link = oc.share_file_with_link(cloud_dir)

        # Remove image from media directory
        os.remove(image_dir)


        return image_link.get_link() + '/preview'