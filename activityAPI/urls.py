from django.urls import include, path, re_path
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register(r'master', views.MasterViewSet)
# router.register(r'golf', views.GolfViewSet)


urlpatterns = [
    path(r'dashboard/', views.dashboard),
    path(r'dashboard/<str:industry>/<slug:action>', views.dashboard_filter),
    re_path(r'dashboard/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<action>[-\w]+)/(?P<employee>\w+)', views.dashboard_table),
    path(r'industry/<str:industry>', views.industry),
    path(r'<str:industry>/open/', views.industry_open),
    path(r'<str:industry>/today/', views.industry_today),
    path(r'<str:industry>/this_week/', views.industry_this_week),
    path(r'opportunity/<int:oppNumber>', views.opportunity),
    re_path(r'edit/(?P<pk>[0-9]+)$', views.edit_action),
    path(r'input/', views.input),
 ]