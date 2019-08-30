from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^submit_hand_cards$', views.submit_hand_cards),
    url(r'^submit_flopcards$', views.submit_flopcards),
    url(r'^submit_turn_card$', views.submit_turn_card),
    url(r'^submit_river_card$', views.submit_river_card), 
    url(r'^calculate_hand$', views.calculate_hand),   
    url(r'^clear_board$', views.clear_board),
    url(r'^random_hand$', views.random_hand),
    url(r'^random_flop$', views.random_flop),
    url(r'^random_turn$', views.random_turn),
    url(r'^random_river$', views.random_river),
]