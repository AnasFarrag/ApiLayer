from apps.telegram import views

BASE_ROUTE = '/telegram'
urls = [
    (views.TelegramSubscription, BASE_ROUTE + '/telegram_subscripe')
]
