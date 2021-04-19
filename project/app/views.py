from django.views import generic
from . import mixins
from .models import Cost
import datetime
from django.shortcuts import redirect
from .forms import BS4CostForm


class MonthCalendar(mixins.MonthCalendarMixin, generic.TemplateView):
    """月間カレンダーを表示するビュー"""
    template_name = 'app/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    """費用付きの月間カレンダーを表示するビュー"""
    template_name = 'app/month_with_schedule.html'
    model = Cost
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class MyCalendar(mixins.MonthWithScheduleMixin, generic.CreateView):
    """月間カレンダー、スケジュール登録画面"""
    template_name = 'app/mycalendar.html'
    model = Cost
    date_field = 'date'
    form_class = BS4CostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_calendar_context = self.get_month_calendar()
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(
                year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        cost = form.save(commit=False)
        cost.date = date
        cost.save()
        return redirect('app:mycalendar', year=date.year, month=date.month, day=date.day)
