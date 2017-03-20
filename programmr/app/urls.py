from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
	url(r'^login/', views.login_view, name='login_view'),
	url(r'^signup/', views.signup_view, name='signup_view'),
	url(r'^logout', views.logout_view, name='logout_view'),
	url(r'^profile/',views.profile,name='profile'),
    url(r'^rules$',views.rules,name='rules'),
    url(r'^announcements$',views.announcements,name='announcements'),
    url(r'^question_detail/(?P<id>[0-9]+)$',views.question_detail,name='question_detail'),
	url(r'^submission/$',views.submission,name='submission'),
	url(r'^leaderboard/$',views.leaderboard,name='leaderboard'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)