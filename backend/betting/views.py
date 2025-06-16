from django.utils import timezone
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg import openapi

from .models import Group, Bet
from django.views.decorators.http import require_http_methods
from catalog.models import Race, Driver, Driverstanding, Season
import json
from datetime import date
from django.http import JsonResponse
from rest_framework.decorators import api_view


@swagger_auto_schema(
    method='post',
    operation_summary="Create a new betting group",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='username of the owner'),
            'group_name': openapi.Schema(type=openapi.TYPE_STRING, description='name of the group'),
        },
        required=['name', 'group_name'],
    ),
    responses={
        200: openapi.Response('Group created successfully'),
        400: openapi.Response('Group already exists'),
        404: openapi.Response('Owner not found'),
        500: openapi.Response('Server error'),
    }
)
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


@swagger_auto_schema(
    method='post',
    operation_summary="Join an existing betting group",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'group_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the group'),
        },
        required=['group_name'],
    ),
    responses={
        200: openapi.Response('joined group successfully'),
        404: openapi.Response('group not found'),
    }
)
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


@swagger_auto_schema(
    method='post',
    operation_summary="leave a betting group",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'group_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name der Gruppe'),
        },
        required=['group_name'],
    ),
    responses={
        200: openapi.Response('left group successfully'),
        404: openapi.Response('group not found'),
    }
)
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


@swagger_auto_schema(
    method='post',
    operation_summary="join an existing betting group",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'group_name': openapi.Schema(type=openapi.TYPE_STRING, description='name of the group'),
        },
        required=['group_name'],
    ),
    responses={
        200: openapi.Response('joined group successfully'),
        404: openapi.Response('group not found'),
    }
)
@api_view(['POST'])
def get_all_groups(request):
    user = request.user
    groups = Group.objects.all()
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


@swagger_auto_schema(
    method='post',
    operation_summary="delete a betting group",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'group_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID der Gruppe'),
        },
        required=['group_id'],
    ),
    responses={
        200: openapi.Response('group deleted successfully'),
        403: openapi.Response('not authorized to delete this group'),
        404: openapi.Response('group not found'),
    }
)
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

@swagger_auto_schema(
    method='get',
    operation_summary="List all upcoming races available for betting",
    responses={
        200: openapi.Response(
            description="List of upcoming races",
            examples={
                "application/json": [
                    {
                        "id": "2024-07-01",
                        "season": "2024",
                        "circuit": "Silverstone",
                        "date": "2024-07-01"
                    }
                ]
            }
        )
    }
)
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def show_all_races_to_bet(request):
    today = date.today()
    races = Race.objects.filter(date__gte=today).order_by('date')
    race_data = [{"id": r.date, "season": r.season.season, "circuit": r.circuit.name, "date": r.date} for r in races]
    return JsonResponse(race_data, safe=False)

@swagger_auto_schema(
    method='post',
    operation_summary="Create a new bet for a race",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "race": openapi.Schema(type=openapi.TYPE_STRING, description="Race date (ID)"),
            "group": openapi.Schema(type=openapi.TYPE_INTEGER, description="Group ID"),
            "bet_top_3": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="Top 3 drivers bet"),
            "bet_last_5": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="Last 5 drivers bet"),
            "bet_last_10": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="Last 10 drivers bet"),
            "bet_fastest_lap": openapi.Schema(type=openapi.TYPE_STRING, description="Driver ID for fastest lap"),
            "safety_car": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Safety car bet"),
        },
        required=["race", "group"],
    ),
    responses={
        200: openapi.Response("Bet created successfully"),
        400: openapi.Response("You have already placed a bet for this race."),
        404: openapi.Response("Race not found."),
        500: openapi.Response("Server error"),
    }
)
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
        )
        return JsonResponse({"message": "Bet created successfully", "bet_id": bet.id})

    except Race.DoesNotExist:
        return JsonResponse({"error": "Race not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@swagger_auto_schema(
    method='get',
    operation_summary="Get the bet for a specific race",
    manual_parameters=[
        openapi.Parameter(
            'race_id',
            openapi.IN_PATH,
            description="Race date (ID)",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description="Bet details",
            examples={
                "application/json": {
                    "race": "2024-07-01",
                    "bet_top_3": ["hamilton", "verstappen", "norris"],
                    "bet_last_5": ["zhou", "tsunoda", "albon", "sargeant", "magnussen"],
                    "bet_last_10": [],
                    "bet_fastest_lap": "leclerc",
                }
            }
        ),
        404: openapi.Response(description="No bet found for this race."),
    }
)
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
        })

    except Bet.DoesNotExist:
        return JsonResponse({"error": "No bet found for this race."}, status=404)

@swagger_auto_schema(
    method='delete',
    operation_summary="Delete a bet for a specific race",
    manual_parameters=[
        openapi.Parameter(
            'race_id',
            openapi.IN_PATH,
            description="Race date (ID)",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={
        200: openapi.Response("Bet deleted successfully."),
        404: openapi.Response("Bet not found."),
    }
)
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

@swagger_auto_schema(
    method='put',
    operation_summary="Update a bet for a specific race",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "bet_top_3": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="Top 3 drivers bet"),
            "bet_last_5": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="Last 5 drivers bet"),
            "bet_last_10": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="Last 10 drivers bet"),
            "bet_fastest_lap": openapi.Schema(type=openapi.TYPE_STRING, description="Driver ID for fastest lap"),
        },
        required=[],
    ),
    responses={
        200: openapi.Response("Bet updated successfully."),
        404: openapi.Response("No bet found for this race."),
    }
)
@permission_classes([IsAuthenticated])
@api_view(["PUT"])
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
        bet.save()

        return JsonResponse({"message": "Bet updated successfully."})
    except Bet.DoesNotExist:
        return JsonResponse({"error": "No bet found for this race."}, status=404)

@swagger_auto_schema(
    method='get',
    operation_summary="Get the previous 5 drivers before a given driver in the standings",
    manual_parameters=[
        openapi.Parameter(
            'season',
            openapi.IN_PATH,
            description="Season year",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'driver_id',
            openapi.IN_PATH,
            description="Driver ID",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description="List of previous 5 drivers",
            examples={
                "application/json": [
                    {
                        "driver": "verstappen",
                        "forename": "Max",
                        "surname": "Verstappen",
                        "constructor": "Red Bull",
                        "position": "2",
                        "points": "150"
                    }
                ]
            }
        ),
        404: openapi.Response(description="Driver or season not found or invalid position.")
    }
)
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

@swagger_auto_schema(
    method='get',
    operation_summary="Get the next 5 drivers after a given driver in the standings",
    manual_parameters=[
        openapi.Parameter(
            'season',
            openapi.IN_PATH,
            description="Season year",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'driver_id',
            openapi.IN_PATH,
            description="Driver ID",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description="List of next 5 drivers",
            examples={
                "application/json": [
                    {
                        "driver": "hamilton",
                        "forename": "Lewis",
                        "surname": "Hamilton",
                        "constructor": "Mercedes",
                        "position": "4",
                        "points": "120"
                    }
                ]
            }
        ),
        404: openapi.Response(description="Driver or season not found or invalid position.")
    }
)
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
