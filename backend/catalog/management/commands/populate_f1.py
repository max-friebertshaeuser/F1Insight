import time
from copyreg import constructor

import requests
from requests.exceptions import HTTPError
from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Season, Circuit, Driver, Constructor, Race, DriverTeam, QualifyingResult, Result, Driverstanding, Constructorstanding, DataUpdate
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.db.models import IntegerField
from django.db.models.functions import Cast

BASE_URL = 'https://api.jolpi.ca/ergast/f1'

def fetch_json(self, endpoint):
    """Hilfsfunktion: JSON von Ergast abrufen und paginieren."""

    offset = 0
    limit = 100
    all_items = []

    while True:
        url = f"{BASE_URL}{endpoint}.json?limit={limit}&offset={offset}"

        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except HTTPError as e:
            if resp.status_code == 429:
                retry_after = int(resp.headers.get('Retry-After', 60))
                time.sleep(retry_after)
                self.stdout.write(f'Zu viele Requests erstmal warten')
                continue
            raise
        data = resp.json()
        # Pfad je nach Endpunkt, z.B. data['MRData']['StandingsTable']['StandingsLists']
        items = extract_items(data, endpoint)
        if not items:
            break
        all_items.extend(items)
        offset += limit
        time.sleep(2)
    return all_items

def extract_items(data, endpoint):
    """Extrahiert den richtigen JSON-Pfad je nach Endpunkt."""
    mr = data['MRData']

    match endpoint:
        case "/seasons":
            return mr['SeasonTable']['Seasons']

        case "/circuits":
            return mr['CircuitTable']['Circuits']

        case ep if ep.endswith("drivers"):
            return mr['DriverTable']['Drivers']

        case ep if ep.endswith("constructors"):
            return mr['ConstructorTable']['Constructors']

        case ep if ep.endswith("races"):
            return mr['RaceTable']['Races']

        case ep if ep.endswith("qualifying"):
            return mr['RaceTable']['Races']

        case ep if ep.endswith("results"):
            return mr['RaceTable']['Races']

        # Fängt alle Endpunkte ab, die auf "driverStandings" enden
        case ep if ep.endswith("driverStandings"):
            standings_lists = mr['StandingsTable']['StandingsLists']
            if not standings_lists:
                return []

            first_list = standings_lists[0]
            return first_list.get('DriverStandings', [])

        case ep if ep.endswith("constructorstandings"):
            standings_lists = mr['StandingsTable']['StandingsLists']
            if not standings_lists:
                return []
            return standings_lists[0].get('ConstructorStandings', [])


    return []

class Command(BaseCommand):
    help = 'Befüllt die F1-Tabellen mit Daten aus der Ergast API'

    @transaction.atomic
    def handle(self, *args, **options):

        upd, created = DataUpdate.objects.get_or_create(name='populate_f1')

        if not created and timezone.now() - upd.last_run < timedelta(minutes=30):
            self.stdout.write('Datenbank wurde erst vor weniger als 10 h aktualisiert – übersprungen.')
            return

        self.load_seasons()
        self.load_circuits()

        if created:
            self.stdout.write('Erster Lauf – lade alle Daten …')
            self.load_drivers()
            self.load_constructors()
            self.load_races()
            self.load_qualifying_results()
            self.load_results()
            self.load_driver_standing()
            self.load_constructor_standing()
        else:
            latest = Season.objects.annotate(as_int=Cast('season', IntegerField())).order_by('-as_int').first()
            season = latest.season
            self.stdout.write(f'Lade Season: {season}')
            self.load_drivers(season)
            self.load_constructors(season)
            self.load_races(season)
            self.load_qualifying_results(season)
            self.load_results(season)
            self.load_driver_standing(season)
            self.load_constructor_standing(season)

        upd.save(update_fields=['last_run'])
        self.stdout.write('Fertig!')

    def load_seasons(self):
        seasons = fetch_json(self, '/seasons')
        for s in seasons:
            Season.objects.update_or_create(
                season= s['season'],
                defaults= {}
            )
        self.stdout.write(f'{len(seasons)} Seasons geladen.')

    def load_circuits(self):
        circuits = fetch_json(self, '/circuits')
        for c in circuits:
            Circuit.objects.update_or_create(
                # Objekt in DB finden falls vorhanden
                circuit= c['circuitId'],
                # Alle Werte aktuallisieren oder erstellen
                defaults= {
                    'name': c['circuitName'],
                    'location': c['Location']['locality'],
                    'country': c['Location']['country'],
                }
            )

        self.stdout.write(f'{len(circuits)} Circuits geladen.')


    def load_drivers(self, latest = 0):
        if latest != 0:
            drivers = fetch_json(self, f'/{latest}/drivers')
        else:
            drivers = fetch_json(self, '/drivers')

        for d in drivers:
            dob_str = d.get('dateOfBirth')
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None

            Driver.objects.update_or_create(
                # Objekt in DB finden falls vorhanden
                driver=d['driverId'],
                # Alle Werte aktuallisieren oder erstellen
                defaults={
                    'number': d.get('permanentNumber', ''),
                    'forename': d['givenName'],
                    'surname': d['familyName'],
                    'dob': dob,
                    'nationality': d['nationality'],
                }
            )
        self.stdout.write(f'{len(drivers)} Drivers geladen.')

    def load_constructors(self, latest = 0):
        if latest != 0:
            constructors = fetch_json(self, f'/{latest}/constructors')
        else:
            constructors = fetch_json(self, '/constructors')

        for c in constructors:
            Constructor.objects.update_or_create(
                # Objekt in DB finden falls vorhanden
                constructor=c['constructorId'],
                # Alle Werte aktuallisieren oder erstellen
                defaults={
                    'name': c['name'],
                    'nationality': c['nationality'],
                }
            )
        self.stdout.write(f'{len(constructors)} Constructors geladen.')

    def load_races(self, latest = 0):
        if latest != 0:
            races = fetch_json(self, f'/{latest}/races')
        else:
            races = fetch_json(self, '/races')

        for race in races:
            date_str = race.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

            Race.objects.update_or_create(
                date = date,
                defaults = {
                    'season_id': race['season'],
                    'circuit_id': race['Circuit']['circuitId'],
                    'round': race['round'],
                }
            )

        self.stdout.write(f'{len(races)} Races geladen.')

    def load_qualifying_results(self, latest = 0):
        if latest != 0:
            qualifying_results = fetch_json(self, f'/{latest}/qualifying')
        else:
            qualifying_results = fetch_json(self, '/qualifying')

        for result in qualifying_results:
            date_str = result.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

            for ql in result.get('QualifyingResults', []):
                    QualifyingResult.objects.update_or_create(
                        date_id = date,
                        driver_id = ql['Driver']['driverId'],
                        defaults = {
                            'position': ql['position'],
                            'q1': ql.get('Q1', ''),
                            'q2': ql.get('Q2', ''),
                            'q3': ql.get('Q3', ''),
                        }
                    )

        self.stdout.write(f'{len(qualifying_results)} Qualifying fuer Races geladen.')

    def load_results(self, latest = 0):
        if latest != 0:
            races = fetch_json(self, f'/{latest}/results')
        else:
            races = fetch_json(self, '/results')

        for race in races:
            date_str = race.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

            season = race['season']
            for result in race.get('Results', []):
                time_str = result.get('Time', {}).get('time', '')
                fastest_lap = result.get('FastestLap', {}).get('Time', {}).get('time', '')
                Result.objects.update_or_create(
                    date_id = date,
                    driver_id = result['Driver']['driverId'],
                    defaults={
                        'constructor_id': result['Constructor']['constructorId'],
                        'number': result['number'],
                        'grid': result['grid'],
                        'position': result['position'],
                        'position_text': result['positionText'],
                        'points': result['points'],
                        'laps': result['laps'],
                        'time': time_str,
                        'fastest_lap': fastest_lap,
                        'status': result['status'],
                    }
                )

                DriverTeam.objects.update_or_create(
                    season_id = season,
                    driver_id = result['Driver']['driverId'],
                    defaults={
                        'constructor_id': result['Constructor']['constructorId'],
                        'driver_season_number': result['number'],
                    }
                )

        self.stdout.write(f'{len(races)} Results fuer Races geladen.')

    def load_driver_standing(self, latest = 0):

        if latest != 0:
            seasons = [latest]
        else:
            seasons = Season.objects.values_list('season', flat=True)

        for year in seasons:
            drivers_standing = fetch_json(self, f'/{year}/driverStandings')

            for standing in drivers_standing:

                driver = standing['Driver']['driverId']
                position = standing.get('position', ''),
                positionText = standing['positionText']
                points = standing['points']
                wins = standing['wins']

                for constructor in standing['Constructors']:

                    Driverstanding.objects.update_or_create(
                        season_id = year,
                        driver_id = driver,
                        defaults = {
                            'constructor_id': constructor['constructorId'],
                            'position': position,
                            'positionText': positionText,
                            'points': points,
                            'wins': wins,
                        }
                    )

    def load_constructor_standing(self, latest = 0):

        if latest != 0:
            seasons = [latest]
        else:
            seasons = Season.objects.values_list('season', flat=True)

        for year in seasons:
            constructors_standing = fetch_json(self, f'/{year}/constructorstandings')

            for standing in constructors_standing:

                Constructorstanding.objects.update_or_create(
                    season_id = year,
                    constructor_id = standing['Constructor']['constructorId'],
                    defaults = {
                        'position': standing.get('position', ''),
                        'positionText': standing['positionText'],
                        'points': standing['points'],
                        'wins': standing['wins'],
                    }
                )


    # erstmal weglassen wird nicht benoetigt
    # def load_laptime(self):
    #     laps = fetch_json(self, '/laps')
    #     for lap in laps:
    #         date_str = lap.get('date')
    #         date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
    #
    #         for lap in lap.get('Laps', []):
    #             lap_number = lap['number']
    #
    #             for timing in lap.get('Timings', []):
    #
    #                 LapTime.objects.update_or_create(
    #                     date= date,
    #                     driver=timing['driverId'],
    #                     lap=lap_number,
    #                     defaults={
    #                         'position': timing['position'],
    #                         'time': timing['time'],
    #                         'milliseconds': to_milliseconds(timing['time']),
    #                     }
    #
    #                 )


# def to_milliseconds(time_str: str) -> int:
#     """
#     Konvertiert einen Zeitstring im Format M:SS.mmm (z.B. "1:57.099")
#     in Millisekunden (int).
#     """
#     minutes_part, sec_ms_part = time_str.split(':')        # ["1", "57.099"]
#     seconds_part, ms_part    = sec_ms_part.split('.')      # ["57", "099"]
#
#     minutes = int(minutes_part)
#     seconds = int(seconds_part)
#     ms      = int(ms_part)
#
#     total_ms = minutes * 60_000 + seconds * 1_000 + ms
#     return total_ms