from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from catalog.models import Season, Circuit, Driver, Constructor, Race, DriverTeam, QualifyingResult, Result, Driverstanding, Constructorstanding, DataUpdate
import json
from datetime import date
from django.http import JsonResponse
from django.db.models import IntegerField, Sum, Min, FloatField
from django.db.models.functions import Cast

@api_view(['POST'])
def get_current_drivers(request):
    """
    Returns a list of current drivers with their details.
    """

@api_view(['POST'])
def detailed_driver_view(request):
    # 1. Aktuelle Saison bestimmen (hier: nach dem Feld 'season' absteigend)
    latest = Season.objects.annotate(as_int=Cast('season', IntegerField())).order_by('-as_int').first()
    current_season = latest.season
    if not current_season:
        return JsonResponse({'error': "Database has no season"}, status=404)

    # 2. Alle DriverTeam-Einträge der aktuellen Saison laden
    teams = DriverTeam.objects.filter(
        season=current_season
    ).select_related('driver')

    # 3. Punkte aus der Fahrerwertung (Driverstanding) der aktuellen Saison einlesen
    standings = Driverstanding.objects.filter(
        season=current_season
    )
    points_map = {
        s.driver_id: s.points
        for s in standings
    }

    # 4. Ergebnis-Liste zusammenbauen
    drivers_data = []
    for team in teams:
        driver = team.driver
        drivers_data.append({
            'number': team.driver_season_number,
            'forename': driver.forename,
            'surname': driver.surname,
            'nationality': driver.nationality,
            'points': points_map.get(driver.driver, '0'),
            'driver_id': driver.driver,
        })

    return JsonResponse({'drivers': drivers_data})


@api_view(['POST'])
def past_driver_results(request):
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
    latest = Season.objects.annotate(as_int=Cast('season', IntegerField())).order_by('-as_int').first()
    current_season = latest.season

    # 2. Alle Fahrer iterieren


    for driver in drivers:
        # Karriere-Statistiken
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
            driver=driver, position='1'
        ).count()
        best_grid = career_qs.annotate(
            grid_int=Cast('grid', IntegerField())
        ).aggregate(best=Min('grid_int'))['best']

        # Aktuelle Saison-Statistiken
        # Team
        dt = DriverTeam.objects.filter(
            driver=driver, season=current_season
        ).select_related('constructor').first()
        team_name = dt.constructor.name if dt else None

        # Fahrerwertung
        ds = Driverstanding.objects.filter(
            driver=driver, season=current_season
        ).first()
        current_points = ds.points if ds else 0
        current_wins = ds.wins if ds else 0

        # Aktuelle Saison: Poles & Podiums über die Rennen/Q-Sessions
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

        # 3. In Liste packen
        drivers_data.append({
            'forename': driver.forename,
            'surname': driver.surname,
            'date_of_birth': driver.dob,
            'place_of_birth': driver.nationality,
            'career_wins': career_wins,
            'career_points': career_points,
            'career_podiums': career_podiums,
            'career_poles': career_poles,
            'current_team': team_name,
            'current_season_points': current_points,
            'current_season_wins': current_wins,
            'current_season_podiums': current_podiums,
            'current_season_poles': current_poles,
            'grand_prix_entered': races_entered,
            'world_championships': championships,
            'best_grid_position': best_grid,
        })

    return JsonResponse({'drivers': drivers_data})

@api_view(['POST'])
def get_driver_box_plot(request):
    return JsonResponse({'message': 'get_driver_box_plot'})

@api_view(['POST'])
def get_driver_standings(request):
    return JsonResponse({'message': 'get_driver_standings'})

@api_view(['POST'])
def detailed_team_view(request):
    return JsonResponse({'message': 'detailed_team_view'})

@api_view(['POST'])
def get_team_standings(request):
    return JsonResponse({'message': 'get_team_standings'})

@api_view(['POST'])
def past_team_results(request):
    return JsonResponse({'message': 'past_team_results'})

@api_view(['POST'])
def get_team_box_plot(request):
    return JsonResponse({'message': 'get_team_box_plot'})

@api_view(['POST'])
def insight_driver_standings(request):
    year = request.data.get('year')
    if not year:
        return Response({"error": "Missing required field: year"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        season = Season.objects.get(season=str(year))
    except Season.DoesNotExist:
        return Response({"error": f"No data for season {year}"}, status=status.HTTP_404_NOT_FOUND)
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
            "position": s.position,
            "points": s.points,
        })

    return Response(data)

@api_view(['POST'])
def insight_team_standings(request):
    year = request.data.get('year')
    if not year:
        return Response({"error": "Missing required field: year"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        season = Season.objects.get(season=str(year))
    except Season.DoesNotExist:
        return Response({"error": f"No data for season {year}"}, status=status.HTTP_404_NOT_FOUND)

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
            "position": s.position,
            "points": s.points,
        })

    return Response(data)