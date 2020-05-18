from django.conf.urls import url
from . import views

app_name = 'linker'
# URL patterns used in Linker app
urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='main'),
    url(r'^(?P<link_id>\d+)/result/$', views.result, name='result'),
    url(r'^(?P<short_link>.*)/$', views.redirect_view, name='redirect_view')
    # url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    # url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
]
