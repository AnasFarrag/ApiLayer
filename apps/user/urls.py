
from apps.user import views

BASE_ROUTE = '/user'

urls = [
    (views.UpdateUser, BASE_ROUTE + '/update_user'),
    (views.UpdateUserInfo,BASE_ROUTE + '/update_user_info'),
    (views.ResetPassword,BASE_ROUTE + '/reset/password'),
    (views.GenerateCertificate,BASE_ROUTE + '/generate_certificate'),
]
