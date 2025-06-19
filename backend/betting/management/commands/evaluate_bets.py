from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q, Case, When, Value
from django.db.models.functions import Cast
from django.forms import IntegerField
from django.utils import timezone
from betting.models import Bet, BetTop3, BetStat, Group
from catalog.models import Result, QualifyingResult, Race
import datetime


class Command(BaseCommand):
    help = 'Evaluate all bets for races that have finished and assign points'

    def handle(self, *args, **options):
        today = timezone.now().date()
        # Fetch bets not yet evaluated for races up to today
        bets = Bet.objects.filter(evaluated=False, race__date__lte=today)
        evaluated_count = 0

        for bet in bets:
            earned_points = 0
            stat, _ = BetStat.objects.get_or_create(group=bet.group, user=bet.user)
            eval_race = bet.race
            # Find the race immediately before the evaluated race
            prev_race = Race.objects.filter(date__lt=eval_race.date).order_by('-date').first()
            if not prev_race:
                continue

            # Results of the evaluated race
            eval_results = list(Result.objects.filter(date=eval_race))
            # Build sorted list of (position_int, driver_code) for eval race
            numeric_eval = []
            for r in eval_results:
                try:
                    pos = int(r.position)
                except (ValueError, TypeError):
                    continue
                numeric_eval.append((pos, r.driver.driver))
            numeric_eval.sort(key=lambda x: x[0])

            # Predicted top3
            predicted_top3 = [
                bt3.driver.driver
                for bt3 in BetTop3.objects.filter(bet=bet).order_by('position')
            ]
            # Actual top3
            actual_top3 = [code for (_, code) in numeric_eval[:3]]

            # 1 point per correct driver, plus 2 bonus if full order matches
            for code in predicted_top3:
                if code in actual_top3:
                    earned_points += 1
            if predicted_top3 == actual_top3:
                earned_points += 2

            # Last 5 prediction: worst 5 from prev_race
            prev_results = list(Result.objects.filter(date=prev_race))
            numeric_prev = []
            for r in prev_results:
                try:
                    pos = int(r.position)
                except (ValueError, TypeError):
                    continue
                numeric_prev.append((pos, r.driver.driver))
            # worst = largest positions
            numeric_prev.sort(key=lambda x: x[0], reverse=True)
            last5_codes = [code for (_, code) in numeric_prev[:5]]
            # best among those in eval race
            best_last5 = None
            for pos, code in numeric_eval:
                if code in last5_codes:
                    best_last5 = code
                    break
            if best_last5 and bet.bet_last_5 and best_last5 == bet.bet_last_5.driver:
                earned_points += 2

            # Positions 6-10 (next 5 worst)
            mid5_codes = [code for (_, code) in numeric_prev[5:10]]
            best_mid5 = None
            for pos, code in numeric_eval:
                if code in mid5_codes:
                    best_mid5 = code
                    break
            if best_mid5 and bet.bet_last_10 and best_mid5 == bet.bet_last_10.driver:
                earned_points += 2

            # Fastest lap prediction (lexicographical fallback)
            fastest_list = []
            for r in eval_results:
                if r.fastest_lap:
                    fastest_list.append((r.fastest_lap, r.driver.driver))
            fastest_list.sort(key=lambda x: x[0])
            if fastest_list:
                actual_fast = fastest_list[0][1]
                if bet.bet_fastest_lap and actual_fast == bet.bet_fastest_lap.driver:
                    earned_points += 2

            stat.points += earned_points
            print(actual_top3)
            print(last5_codes)
            print(best_last5)
            print(mid5_codes)
            print(best_mid5)
            # Save stats and mark bet evaluated
            with transaction.atomic():
                stat.save()
                bet.points_awarded = earned_points
                bet.evaluated = True
                bet.save()
            evaluated_count += 1

        self.stdout.write(self.style.SUCCESS(f'{evaluated_count} bets evaluated'))



