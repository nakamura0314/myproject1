import calendar
import datetime
from collections import deque
import itertools


class BaseCalendarMixin:
    """カレンダー関連のMixinの、基底クラス"""
    first_weekday = 6
    # これは日曜日からかくことを想定している
    week_names = ['月', '火', '水', '木', '金', '土', '日']

    def setup_calendar(self):
        """内部カレンダーの設定処理

        calendar.Calendarクラスの機能を利用するため、インスタンス化する
        Calendarクラスのmonthdatescalendarメソッドを利用しているが、デフォルトが日曜日からで、
        火曜日から表示したい(first_weekday=1)、といったケースに対応するためのセットアップ処理

        """
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        """first_weekday(最初に表示される曜日)に合わせて、week_namesをシフトする"""
        week_names = deque(self.week_names)
        # リスト内の要素を右に一つずつ移動
        week_names.rotate(-self.first_weekday)
        return week_names


class MonthCalendarMixin(BaseCalendarMixin):
    """月間カレンダーの機能を提供するMixin"""

    def get_previous_month(self, date):
        """前月分を返す"""
        if date.month == 1:
            return date.replace(year=date.year-1, month=12, day=1)
        else:
            return date.replace(month=date.month-1, day=1)

    def get_next_month(self, date):
        """次月を返す"""
        if date.month == 12:
            return date.replace(year=date.year+1, month=1, day=1)
        else:
            return date.replace(month=date.month+1, day=1)

    def get_month_days(self, date):
        """その月の全ての日を返す"""
        return self._calendar.monthdatescalendar(date.year, date.month)

    def get_current_month(self):
        """現在の月を返す"""
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        if month and year:
            month = datetime.date(year=int(year), month=int(month), day=1)
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_calendar(self):
        """月間カレンダー情報の入った辞書を返す"""
        self.setup_calendar()
        current_month = self.get_current_month()
        calendar_data = {
            'now': datetime.date.today(),
            'month_days': self.get_month_days(current_month),
            'month_current': current_month,
            'month_previous': self.get_previous_month(current_month),
            'month_next': self.get_next_month(current_month),
            'week_names': self.get_week_names(),
        }
        return calendar_data


class MonthWithScheduleMixin(MonthCalendarMixin):
    "スケジュール付きの、月間カレンダーを提供するMixin"

    def get_month_schedules(self, start, end, days):
        lookup = {
            # 例えば、'date__range:(1日,31日)'を動的に作る
            '{}__range'.format(self.date_field): (start, end)
        }
        # 例えば、Cost.objects.filter(date__range=(1日,31日))になる
        _queryset = self.model.objects.filter(**lookup)

        # {1日のdatetime:1日の出費全て,2日のdatetime:2日の出費全て...}のような辞書
        _day_schedules = {day: [] for week in days for day in week}
        for schedule in _queryset:
            schedule_date = getattr(schedule, self.date_fielde)
            _day_schedules[schedule_date].append(schedule)

        # day_schedules辞書を、週毎に分割する。[{1日:1日の出費...},{8日:8日の出費...},...]
        # 7個ずつ取り出して分割する
        size = len(_day_schedules)
        return [{key: _day_schedules[key] for key in itertools.islice(_day_schedules, i, i+7)} for i in range(0, size, 7)]

    def get_month_calendar(self):
        calendar_context = super().get_month_calendar()
        month_days = calendar_context['month_days']
        month_first = month_days[0][0]
        month_last = month_days[-1][-1]
        calendar_context['month_day_schedules'] = self.get_month_schedules(
            month_first,
            month_last,
            month_days
        )
        return calendar_context
