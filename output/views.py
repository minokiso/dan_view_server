from datetime import datetime, timedelta, date

from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action

from Utils.viewset import ModelViewSetPlus
from output.models import LastDayOutPut, RealOEEDay


class LastDayOutPutViewSet(ModelViewSetPlus):
    model = LastDayOutPut

    def list(self, request, *args, **kwargs):
        self.get_queryset = self.get_time_queryset
        return super().list(request, *args, **kwargs)

    def get_time_queryset(self):
        today = datetime.now().date()
        # today = date(2024, 4, 22)
        weekday = today.weekday()
        if weekday == 0:
            start_date = today - timedelta(days=6)
        else:
            start_date = today - timedelta(days=weekday-1)

        before_today_this_week = super().get_queryset().filter(
            time__range=[start_date, today + timedelta(days=1)]
        )
        return before_today_this_week

    @action(methods=["get"], detail=False)
    def list_all(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RealOEEDayViewSet(ModelViewSetPlus):
    model = RealOEEDay

    def list(self, request, *args, **kwargs):
        self.get_queryset = self.get_time_queryset
        return super().list(request, *args, **kwargs)

    def get_time_queryset(self):
        today = datetime.now().date()
        # today = date(2024, 4, 22)
        weekday = today.weekday()
        if weekday == 0:
            start_date = today - timedelta(days=6)
        else:
            start_date = today - timedelta(days=weekday-1)

        before_today_this_week = super().get_queryset().filter(
            time__range=[start_date, today + timedelta(days=1)]
        )
        return before_today_this_week

    @action(methods=["get"], detail=False)
    def list_all(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
