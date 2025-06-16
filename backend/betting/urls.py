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
    delete_bet,
    update_bet,
)

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
    delete_bet,
    update_bet,
    get_last_5_drivers_before,
    get_last_5_drivers
)

urlpatterns = [
    path('groups/create/', create_group, name='create_group'),
    path('groups/join/', join_group, name='join_group'),
    path('groups/leave/', leave_group, name='leave_group'),
    path('groups/getallgroups/', get_all_groups, name='get_all_groups'),
    path('groups/delete/', remove_group, name='remove_group'),

    path('bets/createbet', set_bet, name='set_bet'),
    path('bets/available-races/', show_all_races_to_bet, name='available_races'),
    path('bets/<int:race_id>/', show_bet, name='show_bet'),
    path('bets/<int:race_id>/delete/', delete_bet, name='delete_bet'),
    path('bets/<int:race_id>/update/', update_bet, name='update_bet'),
    path('bets/standings/<season>/<driver_id>/top5-before-choice/', get_last_5_drivers_before,
         name='bet_standings_top5_before_choice'),
    path('bets/standings/<season>/<driver_id>/bottom5-after-choice/', get_last_5_drivers,
         name='bet_standings_bottom5_after_choice'),
]
