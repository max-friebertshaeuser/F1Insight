from django.urls import path
from .views import (
    create_group,
    join_group,
    leave_group,
    get_all_groups,
    remove_group,
)

urlpatterns = [
    path('creategroup/', create_group, name='create_group'),
    path('joingroup/', join_group, name='join_group'),
    path('leavegroup/', leave_group, name='leave_group'),
    path('getallgroups/', get_all_groups, name='get_all_groups'),
    path('removegroup/', remove_group, name='remove_group'),
]
