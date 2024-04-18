from datetime import datetime, timedelta, date

from django.shortcuts import render

# Create your views here.
from Utils.viewset import ModelViewSetPlus
from output.models import LastDayOutPut, RealOEEDay


class LastDayOutPutViewSet(ModelViewSetPlus):
    model = LastDayOutPut

    def list(self, request, *args, **kwargs):
        self.get_queryset = self.get_time_queryset
        return super().list(request, *args, **kwargs)

    def get_time_queryset(self):
        today = datetime.now().date()
        # today = date(2024, 4, 14)
        weekday = today.weekday()
        if weekday == 0:
            start_date = today - timedelta(days=1)
        else:
            start_date = today - timedelta(days=weekday)

        before_today_this_week = super().get_queryset().filter(
            time__range=[start_date, today]
        )
        return before_today_this_week

    def post(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RealOEEDayViewSet(ModelViewSetPlus):
    model = RealOEEDay

    def get_queryset(self):
        # today = datetime.today()
        today = datetime(year=2024, month=4, day=5)
        start_of_week = today - timedelta(days=today.weekday())
        before_today_this_week = super().get_queryset().filter(
            time__range=[start_of_week, today]
        ).exclude(time__date=today.date())
        return before_today_this_week
