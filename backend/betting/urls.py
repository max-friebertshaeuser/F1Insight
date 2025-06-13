from django.urls import path, include

from backend.betting.views import create_group, join_group, leave_group, remove_group, get_all_groups


urlpatterns = [
    path('api/betting/groupmanager/creategoup/', create_group, name='create_group'),
    path('api/betting/groupmanager/joingroup/', join_group, name='join_group'),
    path('api/betting/groupmanager/leavgroup/', leave_group, name='leave_group'),
    path('api/betting/groupmanager/getallgroups/', get_all_groups, name='get_all_groups'),
    path('api/betting/groupmanager/removegroup/', remove_group, name='remove_group'),
]
