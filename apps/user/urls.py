
from apps.user import views

BASE_ROUTE = '/user'

urls = [
    (views.UpdateUser, BASE_ROUTE + '/update_user'),
    (views.UpdateUserInfo,BASE_ROUTE + '/update_user_info'),
    (views.ResetPassword,BASE_ROUTE + '/reset_password'),
    (views.GenerateCertificate,BASE_ROUTE + '/generate_certificate'),
    (views.UserInstructor,BASE_ROUTE + '/instructor_role'),
    (views.SaveLanguage,BASE_ROUTE + '/save_language')
     
]
