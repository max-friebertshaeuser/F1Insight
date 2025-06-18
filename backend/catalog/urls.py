from django.urls import path
from . import views

urlpatterns = [

    path('init', views.get_init, name='get_init'),

    path('getcurrentdrivers', views.get_current_drivers, name='get_current_drivers'),
    path('getcurrentteams', views.get_current_teams, name='get_current_teams'),

    path('driver/detailedview', views.detailed_driver_view, name='detailed_driver_view'),
    path('driver/getboxplot', views.get_driver_box_plot, name='get_box_plot'),
    path('driver/getstandings', views.get_driver_standings, name='get_standings'),

    path('team/detailedview', views.detailed_team_view, name='detailed_team_view'),
    path('team/getboxplot', views.get_team_box_plot, name='get_team_box_plot'),
    path('team/getstandings', views.get_team_standings, name='get_team_standings'),

    path('insigth/getdriverstandings', views.insight_driver_standings, name='get_team_standings'),
    path('insigth/getteamstanding', views.insight_team_standings, name='get_team_standings'),

]
