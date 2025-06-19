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
from catalog.models import Race, Driver, Driverstanding, Season, Result, DriverTeam
import json
from datetime import date, datetime
from django.http import JsonResponse
from rest_framework.decorators import api_view


@swagger_auto_schema(
    method='post',
    operation_summary="Create a new betting group",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'group_name'],
        properties={
            'name':       openapi.Schema(type=openapi.TYPE_STRING, description='Owner username'),
            'group_name': openapi.Schema(type=openapi.TYPE_STRING, description='Group name'),
        },
    ),
    responses={
        200: openapi.Response('Group created successfully'),
        400: openapi.Response('Missing/invalid fields or group exists'),
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
        required=['group_name'],
        properties={
            'group_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the group'),
        },
    ),
    responses={
        200: openapi.Response('Joined group successfully'),
        400: openapi.Response('Missing required fields'),
        404: openapi.Response('Group not found'),
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
    operation_summary="Leave a betting group",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['group_name'],
        properties={
            'group_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the group'),
        },
    ),
    responses={
        200: openapi.Response('Left group successfully'),
        404: openapi.Response('Group not found'),
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
            description="List of groups",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                    'groups': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'group_id':   openapi.Schema(type=openapi.TYPE_INTEGER),
                                'group_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'owner':      openapi.Schema(type=openapi.TYPE_STRING),
                                'created_at': openapi.Schema(type=openapi.TYPE_STRING),
                                'members':    openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                            }
                        )
                    )
                }
            )
        )
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
    operation_summary="Delete a betting group",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Group name'),
        },
    ),
    responses={
        200: openapi.Response('Group deleted successfully'),
        403: openapi.Response('Not authorized to delete this group'),
        404: openapi.Response('Group not found'),
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
    operation_summary="Get the next upcoming race",
    responses={
        200: openapi.Response(
            description="Next race details",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id':      openapi.Schema(type=openapi.TYPE_STRING),
                    'season':  openapi.Schema(type=openapi.TYPE_STRING),
                    'circuit': openapi.Schema(type=openapi.TYPE_STRING),
                    'date':    openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        404: openapi.Response('No upcoming races found'),
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


driver_item = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'driver_id': openapi.Schema(type=openapi.TYPE_STRING, description='Driver code'),
        'name':      openapi.Schema(type=openapi.TYPE_STRING, description='Driver full name'),
    }
)

bet_top3_param = openapi.Parameter(
    'bet_top_3', openapi.IN_BODY,
    description='Array of 3 driver codes in predicted order',
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(type=openapi.TYPE_STRING),
    required=False,
)

@swagger_auto_schema(
    method='post',
    operation_summary="Place a bet",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['group', 'race', 'bet_top_3'],
        properties={
            'group':           openapi.Schema(type=openapi.TYPE_STRING, description='Group name'),
            'race':            openapi.Schema(type=openapi.TYPE_STRING, description='Race date YYYY-MM-DD'),
            'bet_top_3':       openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
            'bet_last_5':      openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
            'bet_last_10':     openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
            'bet_fastest_lap': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        },
    ),
    responses={
        201: openapi.Response('Bet created successfully'),
        400: openapi.Response('Missing or invalid fields'),
        404: openapi.Response('Race or group not found'),
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_bet(request):
    user = request.user
    data = request.data

    # 1) Pflichtdaten prüfen
    race_str = data.get("race")
    group_name = data.get("group")
    if not race_str or not group_name:
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
        group = Group.objects.get(name=group_name)
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


race_id_param = openapi.Parameter(
    'race_id', openapi.IN_PATH,
    description='Race date in YYYY-MM-DD',
    type=openapi.TYPE_STRING,
    required=True
)
@swagger_auto_schema(
    method='get',
    operation_summary="Get a bet for a race",
    manual_parameters=[race_id_param],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['group', 'race'],
        properties={
            'group': openapi.Schema(type=openapi.TYPE_STRING),
            'race':  openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        200: openapi.Response('Bet details'),
        404: openapi.Response('Bet not found'),
    }
)
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def show_bet(request, race_id):
    """
    Expects JSON body:
      {
        "group_name": "<your group name>",
        "race":       "YYYY-MM-DD"
      }
    Returns the user's bet in that group for that race.
    """
    user       = request.user
    group_name = request.data.get('group')
    race_str   = request.data.get('race')

    # 1) Validate inputs
    if not group_name or not race_str:
        return JsonResponse(
            {'error': 'Missing required fields: group_name and race'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2) Lookup Group
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return JsonResponse(
            {'error': f'Group "{group_name}" not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # 3) Parse race date & lookup Race
    try:
        race_date = datetime.strptime(race_str, '%Y-%m-%d').date()
        race      = Race.objects.get(date=race_date)
    except ValueError:
        return JsonResponse(
            {'error': 'Invalid date format for race, expected YYYY-MM-DD.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Race.DoesNotExist:
        return JsonResponse(
            {'error': f'Race {race_str} not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # 4) Fetch the Bet for this user, group and race
    try:
        bet = Bet.objects.get(user=user, group=group, race=race)
    except Bet.DoesNotExist:
        return JsonResponse(
            {'error': 'No bet found for this user–group–race combination.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # 5) Serialize Top-3 from the through-model (ordered by position)
    top3_ids = [
        bt3.driver.driver
        for bt3 in BetTop3.objects.filter(bet=bet).order_by('position')
    ]

    # 6) Serialize the other fields
    last5_id   = bet.bet_last_5.driver      if bet.bet_last_5      else None
    last10_id  = bet.bet_last_10.driver     if bet.bet_last_10     else None
    fastest_id = bet.bet_fastest_lap.driver if bet.bet_fastest_lap else None

    return JsonResponse({
        'group':           group_name,
        'race':            race_str,
        'bet_top_3':       top3_ids,
        'bet_last_5':      last5_id,
        'bet_last_10':     last10_id,
        'bet_fastest_lap': fastest_id,
    })


delete_bet_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['group', 'race'],
    properties={
        'group': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Unique name of the group'
        ),
        'race': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Race date in YYYY-MM-DD'
        ),
    },
)

# Response schemas
delete_bet_response_ok = openapi.Response(description="Bet deleted successfully")
delete_bet_response_400 = openapi.Response(description="Missing required fields")
delete_bet_response_404 = openapi.Response(description="Group, race, or bet not found")

@swagger_auto_schema(
    method='delete',
    operation_summary="Delete a Bet",
    operation_description=(
        "Deletes the authenticated user's bet for the specified group and race.\n\n"
        "Request body must include the unique `group` name and `race` date (YYYY-MM-DD)."
    ),
    request_body=delete_bet_request,
    responses={
        200: delete_bet_response_ok,
        400: delete_bet_response_400,
        404: delete_bet_response_404,
    }
)
@permission_classes([IsAuthenticated])
@api_view(["DELETE"])
def delete_bet(request, race_id):
    """
    Expects JSON body:
      {
        "group_name": "<your group name>",
        "race":       "YYYY-MM-DD"
      }
    Deletes that user's bet for the given group and race.
    """
    user       = request.user
    group_name = request.data.get('group')
    race_str   = request.data.get('race')

    # 1) Validate inputs
    if not group_name or not race_str:
        return JsonResponse(
            {'error': 'Missing required fields: group_name and race'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2) Lookup group
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return JsonResponse(
            {'error': f'Group "{group_name}" not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # 3) Parse race date
    try:
        race_date = datetime.strptime(race_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse(
            {'error': 'Invalid date format for race, expected YYYY-MM-DD.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 4) Lookup race
    try:
        race = Race.objects.get(date=race_date)
    except Race.DoesNotExist:
        return JsonResponse(
            {'error': f'Race {race_str} not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # 5) Lookup and delete the bet
    try:
        bet = Bet.objects.get(user=user, group=group, race=race)
    except Bet.DoesNotExist:
        return JsonResponse(
            {'error': 'Bet not found for this user–group–race combination.'},
            status=status.HTTP_404_NOT_FOUND
        )

    bet.delete()
    return JsonResponse(
        {'message': 'Bet deleted successfully.'},
        status=status.HTTP_200_OK
    )


race_id_param = openapi.Parameter(
    'race_id', openapi.IN_PATH,
    description='Race date in YYYY-MM-DD format',
    type=openapi.TYPE_STRING,
    required=True
)

# Request body schema for update_bet
update_bet_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'group': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Unique group name'
        ),
        'race': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Race date in YYYY-MM-DD (should match path)'
        ),
        'bet_top_3': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description='List of driver codes in new Top-3 order',
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'bet_last_5': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Driver code for best of last 5',
            nullable=True
        ),
        'bet_last_10': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Driver code for best of positions 6–10',
            nullable=True
        ),
        'bet_fastest_lap': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Driver code for fastest lap',
            nullable=True
        ),
    },
    required=['group', 'race']
)

# Response schema
update_bet_response = openapi.Response(
    description="Bet updated successfully",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'bet': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id':              openapi.Schema(type=openapi.TYPE_INTEGER),
                    'user':            openapi.Schema(type=openapi.TYPE_STRING),
                    'group':           openapi.Schema(type=openapi.TYPE_STRING),
                    'race':            openapi.Schema(type=openapi.TYPE_STRING),
                    'bet_top_3':       openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                    'bet_last_5':      openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                    'bet_last_10':     openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                    'bet_fastest_lap': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                    'bet_date':        openapi.Schema(type=openapi.TYPE_STRING, description='ISO datetime'),
                }
            )
        }
    )
)

update_bet_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['group', 'race'],
    properties={
        'group':           openapi.Schema(type=openapi.TYPE_STRING),
        'race':            openapi.Schema(type=openapi.TYPE_STRING),
        'bet_top_3':       openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
        'bet_last_5':      openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        'bet_last_10':     openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        'bet_fastest_lap': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
    }
)
@swagger_auto_schema(
    method='put',
    operation_summary="Update an existing bet",
    manual_parameters=[race_id_param],
    request_body=update_bet_request,
    responses={
        200: openapi.Response('Bet updated successfully'),
        400: openapi.Response('Missing or invalid fields'),
        404: openapi.Response('Bet not found'),
    }
)
@permission_classes([IsAuthenticated])
@api_view(["PUT"])
def update_bet(request, race_id):
    user = request.user
    data = request.data

    # 1) Pflichtfelder prüfen
    race_str = data.get("race")
    group_name = data.get("group")
    if not race_str or not group_name:
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
        bet.group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return JsonResponse(
            {"error": f"Group {group_name} not found."},
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

race_param = openapi.Parameter(
    'race',
    openapi.IN_QUERY,
    description="Date of the race to fetch info for (YYYY-MM-DD)",
    type=openapi.TYPE_STRING,
    required=True
)
@swagger_auto_schema(
    method='get',
    operation_summary="Get Bet Info",
    operation_description=(
        "Returns lists of drivers for betting:\n"
        "- `top3`: the first three finishers of the given race\n"
        "- `last5`: drivers who finished in the last 5 of the previous race\n"
        "- `mid5`: drivers in positions 6–10 of the previous race\n"
        "- `fastest_options`: all drivers participating in the given race"
    ),
    manual_parameters=[race_param],
    responses={
        400: openapi.Response("Missing or invalid `race` parameter"),
        404: openapi.Response("Race or previous race not found")
    }
)
@api_view(["GET"])
def get_bet_info(request):
    """
    Returns driver lists for betting UI:
      - drivers: all current-season drivers (for top3 and fastest-lap selections)
      - last5:   drivers who finished in the last 5 of a specified race
      - mid5:    drivers who finished in positions 6-10 of that race
    """
    race_date = request.GET.get('race')
    if not race_date:
        return JsonResponse({'error': 'Missing required parameter: race (YYYY-MM-DD)'}, status=400)

    # 1) Parse and lookup the target race
    try:
        date_obj = datetime.strptime(race_date, '%Y-%m-%d').date()
        eval_race = Race.objects.get(date=date_obj)
    except ValueError:
        return JsonResponse({'error': 'Invalid date format, expected YYYY-MM-DD.'}, status=400)
    except Race.DoesNotExist:
        return JsonResponse({'error': f'Race {race_date} not found.'}, status=404)

    # 2) Find the previous race by date
    prev_race = (
        Race.objects
        .filter(date__lt=eval_race.date)
        .order_by('-date')
        .first()
    )
    if not prev_race:
        return JsonResponse({'error': 'No previous race available.'}, status=404)

    # 3) Current-season drivers for Top-3 & Fastest-lap
    seasons = Season.objects.values_list('season', flat=True)
    years = [int(s) for s in seasons if s.isdigit()]
    if not years:
        return JsonResponse({'error': 'No seasons defined.'}, status=500)
    max_year = max(years)
    latest_season = Season.objects.get(season=str(max_year))
    driver_teams = DriverTeam.objects.filter(season=latest_season).select_related('driver')
    drivers = [
        {'driver_id': dt.driver.driver, 'name': f'{dt.driver.forename} {dt.driver.surname}'}
        for dt in driver_teams
    ]

    # 4) Compute bottom-5 and 6–10 from the previous race
    prev_results = Result.objects.filter(date=prev_race)
    numeric_prev = []
    for r in prev_results:
        try:
            pos = int(r.position)
        except (ValueError, TypeError):
            continue
        numeric_prev.append((pos, r.driver.driver))
    # sort descending (worst finishers first)
    numeric_prev.sort(key=lambda x: x[0], reverse=True)

    last5_codes = [code for _, code in numeric_prev[:5]]
    mid5_codes = [code for _, code in numeric_prev[5:10]]

    # 5) Map driver codes to full details
    def map_codes(codes):
        result = []
        for code in codes:
            d = Driver.objects.filter(driver=code).first()
            if d:
                result.append({
                    'driver_id': d.driver,
                    'name': f'{d.forename} {d.surname}'
                })
        return result

    data = {
        'race': race_date,
        'drivers': drivers,
        'last5': map_codes(last5_codes),
        'mid5': map_codes(mid5_codes),
    }
    return JsonResponse(data)


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


@swagger_auto_schema(
    method='post',
    operation_summary="Get Group Info",
    operation_description="Returns details for a given group, including member standings.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'group_name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Unique name of the group'
            ),
        },
        required=['group_name'],
    ),
    responses={
        200: openapi.Response(
            description="Group info",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'group_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'group_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'owner': openapi.Schema(type=openapi.TYPE_STRING),
                    'bet_stats': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'user': openapi.Schema(type=openapi.TYPE_STRING),
                                'points': openapi.Schema(type=openapi.TYPE_INTEGER),
                            }
                        )
                    ),
                }
            )
        ),
        400: openapi.Response(description="Missing group_name"),
        404: openapi.Response(description="Group not found"),
    }
)
@api_view(['Post'])
@permission_classes([IsAuthenticated])
def get_group_info(request):
    group_name = request.data.get('group_name')
    if not group_name:
        return Response({'status': 'missing group_id'}, status=400)
    try:
        group = Group.objects.get(name=group_name)
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


@swagger_auto_schema(
    method='post',
    operation_summary="Ausgewertete Wetten und Punkte abrufen",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'group': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Eindeutiger Gruppenname'
            ),
        },
        required=['group'],
    ),
    responses={
        200: openapi.Response('Liste der ausgewerteten Wetten und Gesamtstand der Gruppe'),
        400: openapi.Response('Bad Request'),
        404: openapi.Response('Gruppe nicht gefunden'),
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_evaluated_bets(request):
    """
    For a given group, returns:
      - bets: each evaluated bet, the points earned, and the user's predictions
      - standings: cumulative points per user in that group

    Request JSON:
      { "group": "<unique group name>" }
    """
    group_name = request.data.get('group')
    if not group_name:
        return JsonResponse(
            {'error': 'Missing required field: group'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 1) Lookup group
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return JsonResponse(
            {'error': f'Group "{group_name}" not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # 2) Fetch all evaluated bets for the group
    evaluated_bets = (
        Bet.objects
           .filter(group=group, evaluated=True)
           .select_related('user', 'race',
                           'bet_last_5', 'bet_last_10', 'bet_fastest_lap')
           .order_by('race__date', 'user__username')
    )

    bets_data = []
    for bet in evaluated_bets:
        # Top-3 from the through-model (ordered by position)
        top3 = [
            bt3.driver.driver
            for bt3 in BetTop3.objects.filter(bet=bet).order_by('position')
        ]
        bets_data.append({
            'user':            bet.user.username,
            'race':            bet.race.date.isoformat(),
            'points':          bet.points_awarded,
            'bet_top_3':       top3,
            'bet_last_5':      bet.bet_last_5.driver      if bet.bet_last_5      else None,
            'bet_last_10':     bet.bet_last_10.driver     if bet.bet_last_10     else None,
            'bet_fastest_lap': bet.bet_fastest_lap.driver if bet.bet_fastest_lap else None,
        })

    # 3) Fetch cumulative standings
    stats = BetStat.objects.filter(group=group).select_related('user')
    standings_data = [
        {'user': stat.user.username, 'points': stat.points}
        for stat in stats
    ]

    return JsonResponse({
        'bets':      bets_data,
        'standings': standings_data,
    }, safe=False)
