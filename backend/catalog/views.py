from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from catalog.models import Season, Circuit, Driver, Constructor, Race, DriverTeam, QualifyingResult, Result, \
    Driverstanding, Constructorstanding, DataUpdate
import json
from datetime import date, datetime
from django.http import JsonResponse
from django.db.models import IntegerField, Sum, Min, FloatField, Case, When, Value
from django.db.models.functions import Cast
from drf_yasg.utils   import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from django.http      import JsonResponse
from math import floor, ceil


@swagger_auto_schema(
    method='post',
    operation_summary="Initialdaten abrufen",
    operation_description="Gibt Mappings der Fahrernamen und Teamnamen zu ihren IDs zurück, damit das Frontend die Eingaben zuordnen kann.",
    responses={
        200: openapi.Response(
            description="Mapping-Objekte für Fahrer und Teams",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "drivers": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Mapping von Vollnamen zu driver_id",
                        additional_properties=openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="driver_id"
                        )
                    ),
                    "teams": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Mapping von Teamnamen zu team_id",
                        additional_properties=openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="team_id"
                        )
                    ),
                }
            )
        ),
        400: openapi.Response(description="Fehlerhafte Anfrage"),
    }
)
@api_view(['POST'])
def get_init(request):
    """
    Liefert die Mapping-Tabellen für Frontend-Initialisierung:
    - drivers: { "Vorname Nachname": "driver_id", … }
    - teams:   { "Team Name":       "team_id",   … }
    """
    # Fahrer-Mapping
    driver_qs = Driver.objects.all().order_by('surname', 'forename')
    drivers = {
        f"{d.forename} {d.surname}": d.driver
        for d in driver_qs
    }

    # Team-Mapping
    team_qs = Constructor.objects.all().order_by('name')
    teams = {
        c.name: c.constructor
        for c in team_qs
    }

    return JsonResponse({
        "drivers": drivers,
        "teams": teams,
    })



@swagger_auto_schema(
    method='post',
    operation_summary="Aktuelle Fahrer abrufen",
    operation_description="Gibt eine Liste der Fahrer der aktuellen Saison zurück.",
    responses={200: openapi.Response('Liste der Fahrer')}
)
@api_view(['POST'])
def get_current_drivers(request):
    """
    Returns a list of current drivers with their details.
    """
    # 1. Aktuelle Saison bestimmen
    latest_season = (
        Season.objects
        .annotate(as_int=Cast('season', IntegerField()))
        .order_by('-as_int')
        .first()
    )
    if not latest_season:
        return JsonResponse({'error': "Database has no season"}, status=404)

    # 2. Alle Fahrer-Teams der aktuellen Saison laden
    driver_teams = DriverTeam.objects.filter(
        season=latest_season
    ).select_related('driver', 'constructor')

    # 3. Fahrerwertung der aktuellen Saison einlesen
    standings_qs = Driverstanding.objects.filter(
        season=latest_season
    ).values('driver_id', 'points', 'positionText')
    # Mapping driver_id -> {'points': ..., 'position': ...}
    standings_map = {
        s['driver_id']: {
            'points': s['points'],
            'position': s['positionText'],
        }
        for s in standings_qs
    }

    # 4. Ergebnis-Liste zusammenbauen
    drivers_data = []
    for dt in driver_teams:
        driver = dt.driver
        standing = standings_map.get(driver.driver, {})
        drivers_data.append({
            'number': dt.driver_season_number,
            'forename': driver.forename,
            'surname': driver.surname,
            'nationality': driver.nationality,
            'team': dt.constructor.name,
            'points': standing.get('points', '0'),
            'position': standing.get('position', ''),
            'driver_id': driver.driver,
        })

    return JsonResponse({'drivers': drivers_data})

@swagger_auto_schema(
    method='post',
    operation_summary="Aktuelle Teams abrufen",
    operation_description="Gibt eine Liste der Teams der aktuellen Saison zurück.",
    responses={200: openapi.Response('Liste der Teams')}
)
@api_view(['POST'])
def get_current_teams(request):
    """
    Returns a list of current-season teams with:
      - team_id
      - name
      - nationality
      - points
      - position
      - drivers: list of drivers in that team this season
    """
    # 1. Aktuelle Saison bestimmen
    latest_season = (
        Season.objects
        .annotate(as_int=Cast('season', IntegerField()))
        .order_by('-as_int')
        .first()
    )
    if not latest_season:
        return JsonResponse({'error': "Database has no season"}, status=404)

    # 2. Alle Constructorstandings der aktuellen Saison laden
    standings_qs = Constructorstanding.objects.filter(
        season=latest_season
    ).select_related('constructor')

    teams_data = []
    for standing in standings_qs:
        team = standing.constructor

        # 3. Fahrer dieses Teams in der aktuellen Saison
        driver_teams = DriverTeam.objects.filter(
            season=latest_season,
            constructor=team
        ).select_related('driver')

        drivers = []
        for dt in driver_teams:
            d = dt.driver
            drivers.append({
                'driver_id': f"{d.driver}",
                'forename':  d.forename,
                'surname':   d.surname,
                'number':    dt.driver_season_number,
            })

        teams_data.append({
            'team_id':     team.constructor,
            'name':        team.name,
            'nationality': team.nationality,
            'points':      standing.points,
            'position':    standing.positionText,
            'drivers':     drivers,
        })

    return JsonResponse({'teams': teams_data})

@swagger_auto_schema(
    method='post',
    operation_summary="Detaillierte Fahrerdaten",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'driver_id': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Eindeutige Fahrer-ID, z.B. "max_verstappen"'
            ),
        },
        required=['driver_id'],  # nur driver_id zwingend
    ),
    responses={200: openapi.Response('Liste der Fahrer')}
)
@api_view(['POST'])
def detailed_driver_view(request):
    driver_id = request.data.get('driver_id')
    if not driver_id:
        return JsonResponse(
            {'error': 'Bitte driver_id im Request-Body mitgeben.'},
            status=400
        )

    try:
        driver = Driver.objects.get(pk=driver_id)
    except Driver.DoesNotExist:
        return JsonResponse(
            {'error': f'Kein Fahrer mit der ID "{driver_id}" gefunden.'},
            status=404
        )

    # 1. Aktuelle Saison holen
    latest = Season.objects.annotate(
        as_int=Cast('season', IntegerField())
    ).order_by('-as_int').first()
    current_season = latest.season

    # 2. Karriere-Statistiken
    career_qs = Result.objects.filter(driver=driver)
    career_wins = career_qs.filter(position='1').count()
    career_podiums = career_qs.filter(position__in=['1', '2', '3']).count()
    career_points = career_qs.aggregate(
        total=Sum(Cast('points', FloatField()))
    )['total'] or 0
    career_poles = QualifyingResult.objects.filter(
        driver=driver, position='1'
    ).count()
    races_entered = career_qs.count()
    championships = Driverstanding.objects.filter(
        driver=driver, positionText='1'
    ).count()
    # Best Grid
    numeric_grids = career_qs.filter(grid__regex=r'^[1-9]\d*$')
    best_grid = numeric_grids.annotate(
        grid_int=Cast('grid', IntegerField())
    ).aggregate(
        best=Min('grid_int')
    )['best']

    # 3. Aktuelle Saison-Statistiken
    #   Team & Nummer
    dt = DriverTeam.objects.filter(
        driver=driver, season=current_season
    ).select_related('constructor').first()
    team_name = dt.constructor.name if dt else None
    current_number = dt.driver_season_number if dt else None

    #   Fahrerwertung
    ds = Driverstanding.objects.filter(
        driver=driver, season=current_season
    ).first()
    current_points = float(ds.points) if ds and ds.points else 0
    current_wins = int(ds.wins) if ds and ds.wins else 0

    #   Saison-Pole-Positions & Podien
    current_poles = QualifyingResult.objects.filter(
        driver=driver,
        date__season=current_season,
        position='1'
    ).count()
    current_podiums = Result.objects.filter(
        driver=driver,
        date__season=current_season,
        position__in=['1', '2', '3']
    ).count()

    # 4. Seasons, in denen der Fahrer aktiv war
    seasons_active = list(
        DriverTeam.objects
        .filter(driver=driver)
        .values_list('season__season', flat=True)
        .distinct()
        .order_by('-season__season')
    )

    # 5. Antwort-Daten
    data = {
        'forename': driver.forename,
        'surname': driver.surname,
        'date_of_birth': driver.dob.isoformat(),
        'place_of_birth': driver.nationality,
        'career_wins': career_wins,
        'career_points': career_points,
        'career_podiums': career_podiums,
        'career_poles': career_poles,
        'grand_prix_entered': races_entered,
        'world_championships': championships,
        'best_grid_position': best_grid,
        'current_team': team_name,
        'current_number': current_number,
        'current_season_points': current_points,
        'current_season_wins': current_wins,
        'current_season_podiums': current_podiums,
        'current_season_poles': current_poles,
        'seasons_active': seasons_active,
    }

    return JsonResponse({'driver': data})


@swagger_auto_schema(
    method='post',
    operation_summary="Box-Plot für Fahrer",
    operation_description="(noch nicht implementiert)",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'driver_id': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Fahrer-, z.B. max_verstappen'
            ),
        },
        required=['driver_id'],
    ),
    responses={200: openapi.Response('Erfolgreich'),
               400: openapi.Response('Fehlerhafte Anfrage, z.B. fehlendes driver_id'),
               404: openapi.Response('Fahrer nicht gefunden'),
               }

)
@api_view(['POST'])
def get_driver_box_plot(request):
    driver_id = request.data.get('driver_id')
    if not driver_id:
        return JsonResponse({"error": "Required field: driver_id"}, status=400)

    # 1) Neueste Saison im System ermitteln
    latest = (
        Season.objects
        .annotate(as_int=Cast('season', IntegerField()))
        .order_by('-as_int')
        .first()
    )
    if not latest:
        return JsonResponse({"error": "No seasons defined"}, status=500)
    max_year = int(latest.season)

    # 2) Driver lookup
    try:
        driver = Driver.objects.get(pk=driver_id)
    except Driver.DoesNotExist:
        return JsonResponse({"error": f"No driver found with id {driver_id}"}, status=404)

    # 3) Alle Saisons als ints ≤ max_year, absteigend
    years = sorted(
        (int(s) for s in Season.objects.values_list('season', flat=True) if s.isdigit()),
        reverse=True
    )
    years = [y for y in years if y <= max_year][:4]

    boxplots = []
    for y in years:
        season = Season.objects.get(season=str(y))

        # 4) Alle Platzierungen dieses Fahrers in dieser Saison abrufen
        raw_qs = (
            Result.objects
            .filter(date__season=season, driver=driver)
            .values_list('position', flat=True)
        )
        # zuerst als ints, blinde Einträge rauswerfen
        positions_int = []
        for pos in raw_qs:
            try:
                pi = int(pos)
            except (ValueError, TypeError):
                continue
            positions_int.append(pi)

        if not positions_int:
            continue

        # für Percentile-Sortierung
        sorted_pos = sorted(positions_int)

        boxplots.append({
            "x":             y,
            "positions":     positions_int,                # <— die rohe Serie [1,4,2,1,1,3,…]
            "min":           sorted_pos[0],
            "firstQuartile": _percentile(sorted_pos, 25),
            "median":        _percentile(sorted_pos, 50),
            "thirdQuartile": _percentile(sorted_pos, 75),
            "max":           sorted_pos[-1],
        })

    return JsonResponse({"boxPlots": boxplots})

@swagger_auto_schema(
    method='post',
    operation_summary="Renn-Ergebnisse eines Fahrers",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'driver_id': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Fahrer-, z.B. max_verstappen'
            ),
            'season': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Jahreszahl der Saison (optional), z.B.: 2024'
            ),
        },
        required=['driver_id'],
    ),
    responses={
        200: openapi.Response('Liste der Rennen und Positionen'),
        400: openapi.Response('Bad Request'),
        404: openapi.Response('Keine Daten gefunden'),
    }
)
@api_view(['POST'])
def get_driver_standings(request):
    driver_id   = request.data.get('driver_id')
    season_year = request.data.get('season')

    if not driver_id:
        return JsonResponse({'error': 'driver_id fehlt im Request.'}, status=400)

    # Fahrer laden
    try:
        driver = Driver.objects.get(pk=driver_id)
    except Driver.DoesNotExist:
        return JsonResponse({'error': 'Fahrer nicht gefunden.'}, status=404)

    # Wenn keine Saison übergeben wurde: neuste Saison ermitteln, in der der Fahrer Rennen hatte
    if not season_year:
        seasons = (
            Result.objects
            .filter(driver=driver)
            .values_list('date__season__season', flat=True)
            .distinct()
            .order_by('-date__season__season')
        )
        season_year = seasons.first()
        if not season_year:
            return JsonResponse({'error': 'Keine Renn-Daten für diesen Fahrer.'}, status=404)

    # Nur Ergebnisse dieser Saison laden, casten und ungültige (≤0) ausschließen
    qs = (
        Result.objects
        .filter(driver=driver, date__season__season=season_year)
        .annotate(
            grid_int=Cast('grid', IntegerField()),
            pos_int=Cast('position', IntegerField())
        )
        .exclude(grid_int__lte=0)
        .exclude(pos_int__lte=0)
        .order_by('date__round')
    )

    if not qs.exists():
        return JsonResponse({
            'error': f'Keine Renn-Daten für {driver_id} in Saison {season_year}.'
        }, status=404)

    # Rennen-Daten für diese Saison sammeln
    races = [
        {
            'round':  r.date.round,
            'grid':   r.grid_int,
            'result': r.pos_int,
        }
        for r in qs
    ]

    return JsonResponse({
        'races':  races,
    })


@swagger_auto_schema(
    method='post',
    operation_summary="Detaillierte Team-Daten",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'team_id': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Team-ID (Constructor) z.B. red_bull'
            ),
        },
        required=['team_id'],
    ),
    responses={
        200: openapi.Response('Team-Details'),
        400: openapi.Response('Bad Request'),
        404: openapi.Response('Team nicht gefunden'),
    }
)
@api_view(['POST'])
def detailed_team_view(request):
    team_id = request.data.get('team_id')
    if not team_id:
        return JsonResponse({'error': 'Bitte team_id im Request-Body mitgeben.'}, status=400)

    try:
        team = Constructor.objects.get(pk=team_id)
    except Constructor.DoesNotExist:
        return JsonResponse({'error': f'Kein Team mit der ID "{team_id}" gefunden.'}, status=404)

    # 1. Aktuelle Saison ermitteln
    latest_season_obj = (
        Season.objects
        .annotate(as_int=Cast('season', IntegerField()))
        .order_by('-as_int')
        .first()
    )
    if not latest_season_obj:
        return JsonResponse({'error': 'Keine Saison-Daten gefunden.'}, status=404)

    # 2. Fahrer des Teams in dieser Saison
    current_dts = DriverTeam.objects.filter(
        constructor=team,
        season=latest_season_obj
    ).select_related('driver')
    current_driver_ids = [dt.driver_id for dt in current_dts]
    current_drivers = [
        {
            'id':       dt.driver.driver,
            'forename': dt.driver.forename,
            'surname':  dt.driver.surname,
            'number':   dt.driver_season_number,
        }
        for dt in current_dts
    ]

    # 3. Aktuelle Saison: Punkte & Siege aus Constructorstanding
    try:
        cs_current = Constructorstanding.objects.get(
            constructor=team,
            season=latest_season_obj
        )
        current_points = float(cs_current.points)
        current_wins   = int(cs_current.wins)
    except Constructorstanding.DoesNotExist:
        current_points = 0.0
        current_wins   = 0

    # 4. Karriere: aufsummierte Punkte & Siege aus Constructorstanding
    career_cs = Constructorstanding.objects.filter(constructor=team)
    career_agg = career_cs.aggregate(
        total_points=Sum(Cast('points', FloatField())),
        total_wins=  Sum(Cast('wins',   IntegerField()))
    )
    career_points = career_agg['total_points'] or 0.0
    career_wins   = career_agg['total_wins']   or 0

    # 5. Podien & Poles berechnen
    #    Aktuelle Saison
    current_results = Result.objects.filter(
        constructor=team,
        date__season=latest_season_obj
    )
    current_podiums = current_results.filter(position__in=['1','2','3']).count()
    current_poles   = QualifyingResult.objects.filter(
        position='1',
        date__season=latest_season_obj,
        driver_id__in=current_driver_ids
    ).count()

    #    Karriere (über alle Saisons)
    career_results = Result.objects.filter(constructor=team)
    career_podiums = career_results.filter(position__in=['1','2','3']).count()
    career_poles   = QualifyingResult.objects.filter(
        position='1',
        driver_id__in=DriverTeam.objects
            .filter(constructor=team)
            .values_list('driver_id', flat=True)
            .distinct()
    ).count()

    # 6. JSON-Antwort
    return JsonResponse({
        'team': {
            'id':          team.constructor,
            'name':        team.name,
            'nationality': team.nationality,
        },
        'current_season': {
            'season':  latest_season_obj.season,
            'drivers': current_drivers,
            'wins':    current_wins,
            'points':  current_points,
            'podiums': current_podiums,
            'poles':   current_poles,
        },
        'career': {
            'wins':    career_wins,
            'points':  career_points,
            'podiums': career_podiums,
            'poles':   career_poles,
        }
    })

@swagger_auto_schema(
    method='post',
    operation_summary="Renn-Ergebnisse eines Teams",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'team_id': openapi.Schema(type=openapi.TYPE_STRING, description='Team-ID z.B.: red_bull'),
            'year':    openapi.Schema(type=openapi.TYPE_INTEGER, description='Saison-Jahr (optional) z.B.: 2024'),
        },
        required=['team_id'],
    ),
    responses={
        200: openapi.Response('Liste der Team-Ergebnisse'),
        400: openapi.Response('Bad Request'),
        404: openapi.Response('Keine Daten gefunden'),
    }
)
@api_view(['POST'])
def get_team_standings(request):
    team_id = request.data.get('team_id')
    year = request.data.get('year') or datetime.now().year

    if not team_id:
        return JsonResponse(
            {"error": "Required fields: team_id, year"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        season = Season.objects.get(season=str(year))
    except Season.DoesNotExist:
        return JsonResponse(
            {"error": f"No data for season {year}"},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        team = Constructor.objects.get(pk=team_id)
    except Constructor.DoesNotExist:
        return JsonResponse(
            {"error": f"No team found with id {team_id}"},
            status=status.HTTP_404_NOT_FOUND
        )

    driver_teams = DriverTeam.objects.filter(
        season=season, constructor=team
    ).select_related('driver')
    if not driver_teams.exists():
        return JsonResponse(
            {"error": f"No drivers found for team {team.name} in {year}"},
            status=status.HTTP_404_NOT_FOUND
        )
    drivers = [dt.driver for dt in driver_teams]

    standings = []
    for race in Race.objects.filter(season=season).order_by('date'):
        qs = (
            Result.objects
            .filter(date=race, constructor=team, driver__in=drivers)
            .select_related('driver')
            .annotate(
                pos_int=Case(
                    When(position__regex=r'^\d+$', then=Cast('position', IntegerField())),
                    default=Value(9999),
                    output_field=IntegerField(),
                )
            )
            .order_by('pos_int')
        )
        if not qs.exists():
            continue

        for r in qs:
            standings.append({
                "driver": f"{r.driver.forename} {r.driver.surname}",
                "round": race.round,
                "position": r.pos_int,
            })

    return JsonResponse({
        "races": standings
    })

@swagger_auto_schema(
    method='post',
    operation_summary="Boxplot eines Teams",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'team_id': openapi.Schema(type=openapi.TYPE_STRING, description='Team-ID z.B.: red_bull'),
        },
        required=['team_id'],
    ),
    responses={
        200: openapi.Response('Liste der Team-Ergebnisse'),
        400: openapi.Response('Bad Request'),
        404: openapi.Response('Keine Daten gefunden'),
    }
)
@api_view(['POST'])
def get_team_box_plot(request):
    team_id = request.data.get('team_id')
    if not team_id:
        return JsonResponse({"error": "Required field: team_id"}, status=400)

    # 1) Latest season
    latest = (
        Season.objects
        .annotate(as_int=Cast('season', IntegerField()))
        .order_by('-as_int')
        .first()
    )
    if not latest:
        return JsonResponse({"error": "No seasons defined"}, status=500)
    max_year = int(latest.season)

    # 2) Team lookup
    try:
        team = Constructor.objects.get(pk=team_id)
    except Constructor.DoesNotExist:
        return JsonResponse({"error": f"No team found with id {team_id}"}, status=404)

    # 3) Candidate years ≤ max_year, desc
    candidate = sorted(
        (int(s) for s in Season.objects.values_list('season', flat=True) if s.isdigit() and int(s) <= max_year),
        reverse=True
    )

    # 4) Only years with results, up to 4
    seasons_with_results = []
    for y in candidate:
        if Result.objects.filter(date__season__season=str(y), constructor=team).exists():
            seasons_with_results.append(y)
        if len(seasons_with_results) >= 4:
            break

    # 5) Compute boxplots
    boxplots = []
    for y in seasons_with_results:
        season = Season.objects.get(season=str(y))

        # gather all raw positions for this team in that season
        raw_positions = []
        for race in Race.objects.filter(season=season):
            qs = Result.objects.filter(
                date=race, constructor=team
            ).values_list('position', flat=True)
            for pos in qs:
                try:
                    pi = int(pos)
                except (ValueError, TypeError):
                    continue
                raw_positions.append(pi)

        if not raw_positions:
            continue

        sorted_pos = sorted(raw_positions)
        boxplots.append({
            "x":             y,
            "positions":     raw_positions,                # raw list, e.g. [5,2,8,1,...]
            "min":           sorted_pos[0],
            "firstQuartile": _percentile(sorted_pos, 25),
            "median":        _percentile(sorted_pos, 50),
            "thirdQuartile": _percentile(sorted_pos, 75),
            "max":           sorted_pos[-1],
        })

    return JsonResponse({"boxPlots": boxplots})

@swagger_auto_schema(
    method='post',
    operation_summary="Fahrer-WM-Stand",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'year': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Jahreszahl der Saison z.B.: 2024'
            ),
        },
        required=['year'],
    ),
    responses={
        200: openapi.Response('Fahrer-WM-Stand'),
        400: openapi.Response('Bad Request'),
        404: openapi.Response('Keine Daten für Saison'),
    }
)
@api_view(['POST'])
def insight_driver_standings(request):
    year = request.data.get('year')
    if not year:
        return JsonResponse({"error": "Missing required field: year"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        season = Season.objects.get(season=str(year))
    except Season.DoesNotExist:
        return JsonResponse({"error": f"No data for season {year}"}, status=status.HTTP_404_NOT_FOUND)
    qs = (
        Driverstanding.objects
        .filter(season=season)
        .select_related('driver', 'constructor')
        .order_by('position')
    )

    data = []
    for s in qs:
        data.append({
            "driver": f"{s.driver.forename} {s.driver.surname}",
            "nationality": s.driver.nationality,
            "team": s.constructor.name,
            "position": s.positionText,
            "points": s.points,
        })
    data.sort(key=lambda x: int(x["position"]) if x["position"].isdigit() else 9999)
    return JsonResponse(data, safe=False)


@swagger_auto_schema(
    method='post',
    operation_summary="Team-WM-Stand",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'year': openapi.Schema(type=openapi.TYPE_INTEGER, description='Jahreszahl der Saison z.B.: 2024'),
        },
        required=['year'],
    ),
    responses={
        200: openapi.Response('Team-WM-Stand'),
        400: openapi.Response('Bad Request'),
        404: openapi.Response('Keine Daten für Saison'),
    }
)
@api_view(['POST'])
def insight_team_standings(request):
    year = request.data.get('year')
    if not year:
        return JsonResponse({"error": "Missing required field: year"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        season = Season.objects.get(season=str(year))
    except Season.DoesNotExist:
        return JsonResponse({"error": f"No data for season {year}"}, status=status.HTTP_404_NOT_FOUND)

    qs = (
        Constructorstanding.objects
        .filter(season=season)
        .select_related('constructor')
        .order_by('position')
    )

    data = []
    for s in qs:
        data.append({
            "team": s.constructor.name,
            "position": s.positionText,
            "points": s.points,
        })
    data.sort(key=lambda x: int(x["position"]) if x["position"].isdigit() else 9999)

    return JsonResponse(data, safe=False)


def _percentile(data, percent):
    """
    Lineare Interpolation für den p-ten Perzentil-Wert
    data: bereits sortierte Liste von Zahlen
    percent: Float zwischen 0 und 100
    """
    if not data:
        return None
    k = (len(data) - 1) * (percent / 100.0)
    f = floor(k)
    c = ceil(k)
    if f == c:
        return data[int(k)]
    d0 = data[f] * (c - k)
    d1 = data[c] * (k - f)
    return d0 + d1