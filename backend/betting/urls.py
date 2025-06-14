from django.urls import path
from .views import (
    create_group,
    join_group,
    leave_group,
    get_all_groups,
    remove_group,
    set_bet,
    show_all_races_to_bet,
    show_bet,
    delet_bet,
    update_bet,
)

urlpatterns = [
    path('group/creategroup/', create_group, name='create_group'),
    path('group/joingroup/', join_group, name='join_group'),
    path('group/leavegroup/', leave_group, name='leave_group'),
    path('group/getallgroups/', get_all_groups, name='get_all_groups'),
    path('group/removegroup/', remove_group, name='remove_group'),

    path('bet/setbet/', set_bet, name='set_bet'),
    path('bet/showallracestobet/', show_all_races_to_bet, name='leave_group'),
    path('bet/showbet/', show_bet, name='show_bet'),
    path('bet/deletbet/', delet_bet, name='delet_bet'),
    path('bet/updatebet/', update_bet, name='update_bet'),
]
