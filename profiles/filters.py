from profiles.models import TodoList
from django_filters import BaseInFilter
from django_filters import rest_framework as filters
from datetime import datetime

class TodoListFilter(filters.FilterSet):
    date = BaseInFilter(
        field_name="date", method="date_wise_filter"
    )
    is_urgent = BaseInFilter(
        field_name="is_urgent", method="is_urgent_wise_filter"
    )
    is_done = BaseInFilter(
        field_name="is_done", method="is_done_wise_filter"
    )
    
    class Meta:
        model = TodoList
        fields = ["date", "is_urgent", "is_done"]

    @staticmethod
    def date_wise_filter(queryset, _, value):
        dates = []
        for each in value:
            formated_date = datetime.strptime(each, "%d/%m/%Y")
            formated_date.strftime('YYYY-MM-DD')
            dates.append(formated_date)
        return queryset.filter(date__in=dates)
    
    @staticmethod
    def is_urgent_wise_filter(queryset, _, value):
        filter = []
        for each in value:
            if each.lower() == "true":
                filter.append(True)
            elif each.lower() == "false":
                filter.append(False)
        return queryset.filter(is_urgent__in=filter)
    
    @staticmethod
    def is_done_wise_filter(queryset, _, value):
        filter = []
        for each in value:
            if each.lower() == "true":
                filter.append(True)
            elif each.lower() == "false":
                filter.append(False)
        return queryset.filter(is_done__in=filter)