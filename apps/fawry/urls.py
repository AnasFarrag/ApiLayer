from apps.fawry import views

BASE_ROUTE = '/fawry'

urls = [
    (views.Fawry, BASE_ROUTE + '/fawryCallback'),
]
