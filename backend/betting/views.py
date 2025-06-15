from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Group,Bet
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from catalog.models import Race, Driver,Driverstanding, Season
import json
from datetime import date
from django.http import JsonResponse



@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_group(request):
    owner_username = request.data.get('name')
    group_name = request.data.get('group_name')
    created_at = timezone.now()
    members_usernames = [owner_username]
    try:
        owner = User.objects.get(username=owner_username)
    except User.DoesNotExist:
        return Response({'status': 'owner not found'}, status=404)

    try:
        if Group.objects.filter(name=group_name).exists():
            return Response({'status': 'group already exists'}, status=400)

        group = Group.objects.create(owner=owner, name=group_name, created_at=created_at)
        members = User.objects.filter(username__in=members_usernames)
        group.members.set(members)
        group.save()
        return Response({'status': 'group created', 'group_id': group.id})
    except Exception as e:
        return Response({'status': 'error', 'detail': str(e)}, status=500)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def join_group(request):
    group_name = request.data.get('group_name')
    user = User.objects.get(username=request.user.username)
    try:
        group = Group.objects.get(name=group_name)
        group.members.add(user)
        return Response({'status': 'joined group successfully'})
    except Group.DoesNotExist:
        return Response({'status': 'group not found'}, status=404)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def leave_group(request):
    group_name = request.data.get('group_name')
    user = User.objects.get(username=request.user.username)
    try:
        group = Group.objects.get(name=group_name)
        group.members.remove(user)
        return Response({'status': 'left group successfully'})
    except Group.DoesNotExist:
        return Response({'status': 'group not found'}, status=404)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def get_all_groups(request):
    user = request.user
    groups = Group.objects.filter(members=user)
    group_list = []
    for group in groups:
        group_list.append({
            'group_id': group.id,
            'group_name': group.name,
            'owner': group.owner.username,
            'created_at': group.created_at.isoformat(),
            'members': [member.username for member in group.members.all()]
        })
    return Response({'status': 'success', 'groups': group_list})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def remove_group(request):
    group_id = request.data.get('group_id')
    try:
        group = Group.objects.get(id=group_id)
        if group.owner != request.user:
            return Response({'status': 'not authorized to delete this group'}, status=403)
        group.delete()
        return Response({'status': 'group deleted successfully'})
    except Group.DoesNotExist:
        return Response({'status': 'group not found'}, status=404)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def show_all_races_to_bet(request):
    today = date.today()
    races = Race.objects.filter(date__gte=today).order_by('date')
    race_data = [{"id": r.date, "season": r.season.season, "circuit": r.circuit.name, "date": r.date} for r in races]
    return JsonResponse(race_data, safe=False)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def set_bet(request):
    user = request.user
    data = json.loads(request.body)

    try:
        race_id = data["race"]
        race = Race.objects.get(date=race_id)

        if Bet.objects.filter(user=user, race=race).exists():
            return JsonResponse({"error": "You have already placed a bet for this race."}, status=400)

        bet = Bet.objects.create(
            user=user,
            group_id=data["group"],
            race=race,
            bet_top_3=data.get("bet_top_3", []),
            bet_last_5=data.get("bet_last_5", []),
            bet_last_10=data.get("bet_last_10", []),
            bet_fastest_lap_id=data.get("bet_fastest_lap"),
            safety_car=data.get("safety_car", False),
        )
        return JsonResponse({"message": "Bet created successfully", "bet_id": bet.id})

    except Race.DoesNotExist:
        return JsonResponse({"error": "Race not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def show_bet(request, race_id):
    user = request.user
    try:
        race = Race.objects.get(date=race_id)
        bet = Bet.objects.get(user=user, race=race)

        return JsonResponse({
            "race": str(bet.race.date),
            "bet_top_3": bet.bet_top_3,
            "bet_last_5": bet.bet_last_5,
            "bet_last_10": bet.bet_last_10,
            "bet_fastest_lap": bet.bet_fastest_lap.driver if bet.bet_fastest_lap else None,
            "safety_car": bet.safety_car,
        })

    except Bet.DoesNotExist:
        return JsonResponse({"error": "No bet found for this race."}, status=404)


@permission_classes([IsAuthenticated])
@api_view(["DELETE"])
def delete_bet(request, race_id):
    user = request.user
    try:
        race = Race.objects.get(date=race_id)
        bet = Bet.objects.get(user=user, race=race)
        bet.delete()
        return JsonResponse({"message": "Bet deleted successfully."})
    except Bet.DoesNotExist:
        return JsonResponse({"error": "Bet not found."}, status=404)


@permission_classes([IsAuthenticated])
@require_http_methods(["PUT"])
def update_bet(request, race_id):
    user = request.user
    data = json.loads(request.body)
    try:
        race = Race.objects.get(date=race_id)
        bet = Bet.objects.get(user=user, race=race)

        bet.bet_top_3 = data.get("bet_top_3", bet.bet_top_3)
        bet.bet_last_5 = data.get("bet_last_5", bet.bet_last_5)
        bet.bet_last_10 = data.get("bet_last_10", bet.bet_last_10)
        bet.bet_fastest_lap_id = data.get("bet_fastest_lap", bet.bet_fastest_lap_id)
        bet.safety_car = data.get("safety_car", bet.safety_car)
        bet.save()

        return JsonResponse({"message": "Bet updated successfully."})
    except Bet.DoesNotExist:
        return JsonResponse({"error": "No bet found for this race."}, status=404)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def get_last_5_drivers_before(request, season, driver_id):
    try:
        target = Driverstanding.objects.get(season__season=season, driver__driver=driver_id)
        target_pos = int(target.position)
    except (Driverstanding.DoesNotExist, ValueError):
        return JsonResponse({"error": "Driver or season not found or invalid position."}, status=404)

    drivers = (
        Driverstanding.objects
        .filter(season__season=season)
        .exclude(driver__driver=driver_id)
        .extra(select={'pos_int': "CAST(position AS INTEGER)"})
        .filter(position__lt=target_pos)
        .order_by('-pos_int')[:5]
    )

    data = [
        {
            "driver": ds.driver.driver,
            "forename": ds.driver.forename,
            "surname": ds.driver.surname,
            "constructor": ds.constructor.name,
            "position": ds.position,
            "points": ds.points
        }
        for ds in drivers
    ]
    return JsonResponse(data, safe=False)



@api_view(["GET"])
def get_last_5_drivers(request, season, driver_id):
    try:
        target = Driverstanding.objects.get(season__season=season, driver__driver=driver_id)
        target_pos = int(target.position)
    except (Driverstanding.DoesNotExist, ValueError):
        return JsonResponse({"error": "Driver or season not found or invalid position."}, status=404)

    drivers = (
        Driverstanding.objects
        .filter(season__season=season)
        .exclude(driver__driver=driver_id)
        .extra(select={'pos_int': "CAST(position AS INTEGER)"})
        .filter(position__gt=target_pos)
        .order_by('pos_int')[:5]
    )

    data = [
        {
            "driver": ds.driver.driver,
            "forename": ds.driver.forename,
            "surname": ds.driver.surname,
            "constructor": ds.constructor.name,
            "position": ds.position,
            "points": ds.points
        }
        for ds in drivers
    ]
    return JsonResponse(data, safe=False)
