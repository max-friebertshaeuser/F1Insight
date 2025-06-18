import uuid
from uuid import UUID

from django.utils import timezone
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg import openapi

from .models import Group, Bet, BetStat, BetTop3
from catalog.models import Race, Driver, Driverstanding, Season, Result
import json
from datetime import date, datetime
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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    owner_username = request.data.get('name')
    group_name = request.data.get('group_name')
    created_at = timezone.now()
    join_id = uuid.uuid4()
    if not owner_username or not group_name:
        return Response({'status': 'missing required fields'}, status=400)
    try:
        owner = User.objects.get(username=owner_username)
    except User.DoesNotExist:
        return Response({'status': 'owner not found'}, status=404)

    if Group.objects.filter(name=group_name).exists():
        return Response({'status': 'group already exists'}, status=400)

    try:
        group = Group.objects.create(owner=owner, name=group_name, created_at=created_at, join_id=join_id)
        BetStat.objects.create(user=owner, group=group)
        group.save()
        return Response({'status': 'group created', 'group_id': group.id, 'join_link': str(join_id)})
    except Exception as e:
        return Response({'status': 'error', 'detail': str(e)}, status=500)


@swagger_auto_schema(
    method='post',
    operation_summary="Join an existing betting group",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'group_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the group'),
            'join_id': openapi.Schema(type=openapi.TYPE_STRING, description='Join ID of the group'),
        },
        required=['group_name', 'join_id'],
    ),
    responses={
        200: openapi.Response('joined group successfully'),
        400: openapi.Response('missing required fields'),
        404: openapi.Response('group not found or invalid join id'),
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_group(request):
    group_name = request.data.get('group_name')
    #join_id = request.data.get('join_id')
    if not group_name:
        return Response({'status': 'missing required fields'}, status=400)
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return Response({'status': 'group not found or invalid join id'}, status=404)

    user = request.user
    _, created = BetStat.objects.get_or_create(user=user, group=group)

    return Response({'status': 'joined group successfully'})


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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_group(request):
    group_name = request.data.get('group_name')
    user = request.user

    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return Response({'status': 'group not found'}, status=404)
    try:
        BetStat.objects.filter(user=request.user, group=group).delete()
    except BetStat.DoesNotExist:
        return Response({'status': 'user is not in any group'}, status=400)

    return Response({'status': 'left group successfully'})


@swagger_auto_schema(
    method='get',
    operation_summary="Get all betting groups",
    responses={
        200: openapi.Response(
            description="List of all groups",
            examples={
                "application/json": [
                    {
                        "group_id": 1,
                        "group_name": "Champions",
                        "owner": "user1",
                        "created_at": "2024-07-01T12:00:00Z",
                        "members": ["user1", "user2"]
                    }
                ]
            }
        ),
    }
)
@api_view(['GET'])
def get_all_groups(request):
    groups = Group.objects.all()
    group_list = []
    for group in groups:
        group_list.append({
            'group_id': group.id,
            'group_name': group.name,
            'owner': group.owner.username,
            'created_at': group.created_at.isoformat(),
            'members': [
                bs.user.username for bs in BetStat.objects.filter(group=group)
            ]

        })
    return Response({'status': 'success', 'groups': group_list})


@swagger_auto_schema(
    method='post',
    operation_summary="delete a betting group",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_INTEGER, description='name der Gruppe'),
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
    name = request.data.get('name')
    try:
        group = Group.objects.get(name=name)
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
    next_race = (
        Race.objects
        .filter(date__gte=today)
        .order_by('date')
        .select_related('season', 'circuit')
        .first()
    )

    if not next_race:
        return JsonResponse(
            {'error': 'No upcoming races found.'},
            status=404
        )

    data = {
        'id': next_race.date,
        'season': next_race.season.season,
        'circuit': next_race.circuit.name,
        'date': next_race.date,
    }
    return JsonResponse(data)


@swagger_auto_schema(
    method='post',
    operation_summary="Create a new bet for a race",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "Bsp": '{"group": 1,"race": "2025-12-07","bet_top_3": ["norris", "max_verstappen", "lawson"],"bet_last_5": "ocon","bet_last_10": "ocon","bet_fastest_lap": "max_verstappen"}',
            "race": openapi.Schema(type=openapi.TYPE_STRING, description="Race date (ID)"),
            "group": openapi.Schema(type=openapi.TYPE_INTEGER, description="Group ID"),
            "bet_top_3": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING),
                                        description="Top 3 drivers bet"),
            "bet_last_5": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING),
                                         description="Last 5 drivers bet"),
            "bet_last_10": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING),
                                          description="Last 10 drivers bet"),
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
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_bet(request):
    user = request.user
    data = request.data

    # 1) Pflichtdaten prüfen
    race_str = data.get("race")
    group_id = data.get("group")
    if not race_str or not group_id:
        return JsonResponse(
            {"error": "Missing race or group field."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2) Race & Group laden
    try:
        race = Race.objects.get(date=datetime.strptime(race_str, "%Y-%m-%d").date())
    except (ValueError, Race.DoesNotExist):
        return JsonResponse({"error": "Race not found or invalid date."},
                            status=status.HTTP_404_NOT_FOUND)

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return JsonResponse({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    # 3) Keine Doppel-Wetten
    if Bet.objects.filter(user=user, race=race).exists():
        return JsonResponse(
            {"error": "You have already placed a bet for this race."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 4) Hilfsfunktion zum Fahrer-Lookup
    def get_driver(code):
        if not code:
            return None
        return Driver.objects.filter(driver__iexact=code).first()

    # 5) Bet anlegen (ohne Top-3)
    bet = Bet.objects.create(
        user=user,
        group=group,
        race=race,
        bet_last_5=get_driver(data.get("bet_last_5")),
        bet_last_10=get_driver(data.get("bet_last_10")),
        bet_fastest_lap=get_driver(data.get("bet_fastest_lap")),
    )

    # 6) Top-3 über Through-Model anlegen
    top3_codes = data.get("bet_top_3", [])
    not_found = []
    for idx, code in enumerate(top3_codes, start=1):
        driver = get_driver(code)
        if not driver:
            not_found.append(code)
        else:
            BetTop3.objects.create(bet=bet, driver=driver, position=idx)

    if not_found:
        # Rollback Top3 if einige ungültig waren
        BetTop3.objects.filter(bet=bet).delete()
        bet.delete()
        return JsonResponse(
            {"error": f"Drivers not found for bet_top_3: {not_found}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 7) Alles gespeichert – Antwort mit exakter Reihenfolge
    ordered_top3 = [bt3.driver.driver for bt3 in bet.bettop3_set.all()]

    return JsonResponse({
        "message": "Bet created successfully",
        "bet": {
            "id": bet.id,
            "user": user.username,
            "group": group.id,
            "race": race_str,
            "bet_top_3": ordered_top3,
            "bet_last_5": bet.bet_last_5.driver if bet.bet_last_5 else None,
            "bet_last_10": bet.bet_last_10.driver if bet.bet_last_10 else None,
            "bet_fastest_lap": bet.bet_fastest_lap.driver if bet.bet_fastest_lap else None,
            "bet_date": bet.bet_date.isoformat(),
        }
    }, status=status.HTTP_201_CREATED)


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

    # 1) Datum parsen und Race lookup
    try:
        dt = datetime.strptime(race_id, "%Y-%m-%d").date()
        race = Race.objects.get(date=dt)
    except ValueError:
        return JsonResponse(
            {"error": "Invalid date format, expected YYYY-MM-DD."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Race.DoesNotExist:
        return JsonResponse(
            {"error": f"Race {race_id} not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 2) Bet holen
    try:
        bet = Bet.objects.get(user=user, race=race)
    except Bet.DoesNotExist:
        return JsonResponse(
            {"error": "No bet found for this race."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 3) Top-3 aus dem Through-Model auslesen (Meta.ordering = ['position'])
    top3_ids = [bt3.driver.driver for bt3 in BetTop3.objects.filter(bet=bet)]

    # 4) FK-Felder serialisieren
    last5_id = bet.bet_last_5.driver if bet.bet_last_5 else None
    last10_id = bet.bet_last_10.driver if bet.bet_last_10 else None
    fastest_id = bet.bet_fastest_lap.driver if bet.bet_fastest_lap else None

    return JsonResponse({
        "race": race_id,
        "bet_top_3": top3_ids,
        "bet_last_5": last5_id,
        "bet_last_10": last10_id,
        "bet_fastest_lap": fastest_id,
    })


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

    # 1) Datum parsen
    try:
        race_date = datetime.strptime(race_id, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse(
            {"error": "Invalid date format, expected YYYY-MM-DD."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2) Race lookup
    try:
        race = Race.objects.get(date=race_date)
    except Race.DoesNotExist:
        return JsonResponse(
            {"error": f"Race {race_id} not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 3) Bet lookup & delete
    try:
        bet = Bet.objects.get(user=user, race=race)
    except Bet.DoesNotExist:
        return JsonResponse(
            {"error": "Bet not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    bet.delete()
    return JsonResponse(
        {"message": "Bet deleted successfully."},
        status=status.HTTP_200_OK
    )


@swagger_auto_schema(
    method='put',
    operation_summary="Update a bet for a specific race",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "bet_top_3": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING),
                                        description="Top 3 drivers bet"),
            "bet_last_5": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING),
                                         description="Last 5 drivers bet"),
            "bet_last_10": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING),
                                          description="Last 10 drivers bet"),
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
    data = request.data

    # 1) Pflichtfelder prüfen
    race_str = data.get("race")
    group_id = data.get("group")
    if not race_str or not group_id:
        return JsonResponse(
            {"error": "Missing required field: 'race' or 'group'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2) Rennen parsen und laden
    try:
        race_date = datetime.strptime(race_id, "%Y-%m-%d").date()
        race = Race.objects.get(date=race_date)
    except ValueError:
        return JsonResponse(
            {"error": "Invalid date format, expected YYYY-MM-DD."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Race.DoesNotExist:
        return JsonResponse(
            {"error": f"Race {race_id} not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 3) Existierende Wette laden
    try:
        bet = Bet.objects.get(user=user, race=race)
    except Bet.DoesNotExist:
        return JsonResponse(
            {"error": "No existing bet for this race."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 4) Gruppe updaten
    try:
        bet.group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return JsonResponse(
            {"error": f"Group {group_id} not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 5) Fahrer‐Lookup‐Helper
    def get_driver(code):
        if not code:
            return None
        return Driver.objects.filter(driver__iexact=code).first()

    # 6) FK‐Felder updaten
    if "bet_last_5" in data:
        bet.bet_last_5 = get_driver(data["bet_last_5"])
    if "bet_last_10" in data:
        bet.bet_last_10 = get_driver(data["bet_last_10"])
    if "bet_fastest_lap" in data:
        bet.bet_fastest_lap = get_driver(data["bet_fastest_lap"])

    # 7) Erst speichern, dann die Top-3 via through-Model setzen
    bet.save()

    top3_codes = data.get("bet_top_3")
    if top3_codes is not None:
        # Lösche vorhandene Einträge
        BetTop3.objects.filter(bet=bet).delete()

        not_found = []
        for idx, code in enumerate(top3_codes, start=1):
            driver = get_driver(code)
            if not driver:
                not_found.append(code)
            else:
                BetTop3.objects.create(bet=bet, driver=driver, position=idx)

        if not_found:
            # Rollback bei ungültigen Codes
            BetTop3.objects.filter(bet=bet).delete()
            return JsonResponse(
                {"error": f"Drivers not found for bet_top_3: {not_found}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # 8) Response: Top-3 in stored order (via BetTop3.Meta.ordering)
    ordered_top3 = [bt3.driver.driver for bt3 in BetTop3.objects.filter(bet=bet)]

    return JsonResponse({
        "message": "Bet updated successfully",
        "bet": {
            "id": bet.id,
            "user": user.username,
            "group": bet.group.id,
            "race": race_id,
            "bet_top_3": ordered_top3,
            "bet_last_5": bet.bet_last_5.driver if bet.bet_last_5 else None,
            "bet_last_10": bet.bet_last_10.driver if bet.bet_last_10 else None,
            "bet_fastest_lap": bet.bet_fastest_lap.driver if bet.bet_fastest_lap else None,
            "bet_date": bet.bet_date.isoformat(),
        }
    }, status=status.HTTP_200_OK)


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
def get_last_5_drivers_before(request):
    last_race = Race.objects.filter(date__lt=date.today()).order_by('-date').first()
    if not last_race:
        return JsonResponse({"error": "No completed races found."}, status=404)

    drivers = (
        Result.objects
        .filter(date=last_race)
        .exclude(position__in=["", "\\N"])
        .extra(select={'pos_int': "CAST(position AS INTEGER)"})
        .order_by('-pos_int')[5:10]
    )

    data = [
        {
            "driver": res.driver.driver,
            "forename": res.driver.forename,
            "surname": res.driver.surname,
            "constructor": res.constructor.name,
            "position": res.position,
            "points": res.points
        }
        for res in reversed(drivers)  # optional: kleinste Position zuerst
    ]
    return JsonResponse(data, safe=False)


@swagger_auto_schema(
    method='get',
    operation_summary="Get the last 5 drivers of the most recent race",
    responses={
        200: openapi.Response(
            description="List of last 5 drivers in the most recent race",
            examples={
                "application/json": [
                    {
                        "driver": "sargeant",
                        "forename": "Logan",
                        "surname": "Sargeant",
                        "constructor": "Williams",
                        "position": "20",
                        "points": "0"
                    }
                ]
            }
        ),
        404: openapi.Response(description="No completed races found.")
    }
)
@api_view(["GET"])
def get_last_5_drivers(request):
    last_race = Race.objects.filter(date__lt=date.today()).order_by('-date').first()
    if not last_race:
        return JsonResponse({"error": "No completed races found."}, status=404)

    drivers = (
        Result.objects
        .filter(date=last_race)
        .extra(select={'pos_int': "CAST(position AS INTEGER)"})
        .exclude(position__in=["", "\\N"])
        .order_by('-pos_int')[:5]
    )

    data = [
        {
            "driver": res.driver.driver,
            "forename": res.driver.forename,
            "surname": res.driver.surname,
            "constructor": res.constructor.name,
            "position": res.position,
            "points": res.points
        }
        for res in reversed(drivers)
    ]
    return JsonResponse(data, safe=False)

@api_view(['Post'])
@permission_classes([IsAuthenticated])
def get_group_info(request):
    group_id = request.data.get('group_id')
    if not group_id:
        return Response({'status': 'missing group_id'}, status=400)
    try:
        group = Group.objects.get(id=group_id)
        bet_stats  = BetStat.objects.filter(group=group)
        group_info = {
            'group_id': group.id,
            'group_name': group.name,
            'owner': group.owner.username,
            'bet_stats': [
                {
                    'user': bs.user.username,
                    'points': bs.points
                } for bs in bet_stats
            ]
        }
        return Response(group_info)

    except Group.DoesNotExist:
        return Response({'status': 'group not found'}, status=404)



