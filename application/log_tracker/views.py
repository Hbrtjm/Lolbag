from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Log
from .serializers import LogSerializer
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear, TruncDay, TruncHour


def homepage(request):
    return render(request, "pages/homepage.html")


@api_view(["GET", "POST"])
def log_list(request):
    if request.method == "GET":
        logs = Log.objects.all()
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def log_detail(request, id):
    if not str(id).isnumeric():
        return Response("Given value is not a number",status=status.HTTP_400_BAD_REQUEST)
    log = get_object_or_404(Log, id=id)
    if request.method == "GET":
        serializer = LogSerializer(log)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = LogSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def chart_page(request):
    chart_type = ["bar"]
    datetime_selection = request.GET.get("datetime_selection", "")
    aggregate_by = request.GET.get("aggregation", "")
    logs = Log.objects.all()
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    level = request.GET.get("level", "")
    query = request.GET.get("query", "")
    if datetime_selection == "last_24h" or datetime_selection == "":
        shift = timedelta(days=1)
    elif datetime_selection == "last_week":
        shift = timedelta(days=7)
    elif datetime_selection == "last_month":
        shift = timedelta(days=30)
    elif datetime_selection == "last_6_mth":
        shift = timedelta(days=180)
    elif datetime_selection == "last_year":
        shift = timedelta(days=365)
    else:
        shift = timedelta(days=0)
    # Filter by date range
    if not start_date:
        start_date = (datetime.now() - shift).strftime("%Y-%m-%dT%H:%M:%S")
    logs = logs.filter(log_date_time__gte=start_date)
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    logs = logs.filter(log_date_time__lte=end_date)
    if shift != timedelta(days=0):
        start_date = ""
        end_date = ""
    # Filter by level
    if level:
        logs = logs.filter(level=level)

    # Filter by query string
    if query:
        logs = logs.filter(message__icontains=query)

    # Aggregate data
    if aggregate_by == "day":
        chart_type = ["line"]
        log_counts = (
            logs.annotate(day=TruncDay("log_date_time"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )
        data = [log["count"] for log in log_counts]
        labels = [log["day"].strftime("%Y-%B-%d") for log in log_counts]
    elif aggregate_by == "month":
        log_counts = (
            logs.annotate(month=TruncMonth("log_date_time"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )
        data = [log["count"] for log in log_counts]
        labels = [log["month"].strftime("%Y-%B") for log in log_counts]
    elif aggregate_by == "year":
        log_counts = (
            logs.annotate(year=TruncYear("log_date_time"))
            .values("year")
            .annotate(count=Count("id"))
            .order_by("year")
        )
        data = [log["count"] for log in log_counts]
        labels = [log["year"].strftime("%Y") for log in log_counts]
    elif aggregate_by == "week":
        # From today to the Monday of the current week, then we continue going backwards
        log_counts = logs.annotate()
    elif aggregate_by == "hour":
        chart_type = ["line"]
        log_counts = (
            logs.annotate(hour=TruncHour("log_date_time"))
            .values("hour")
            .annotate(count=Count("id"))
            .order_by("hour")
        )
        data = [log["count"] for log in log_counts]
        labels = [log["hour"].strftime("%B-%d %H:%M") for log in log_counts]
    else:
        log_counts = (
            logs.values("level").annotate(count=Count("level")).order_by("level")
        )
        data = [log["count"] for log in log_counts]
        labels = [log["level"] for log in log_counts]

    context = {
        "datetime_selection": datetime_selection,
        "chart_type": chart_type,
        "labels": labels,
        "data": data,
        "start_date": start_date,
        "end_date": end_date,
        "level": level,
        "query": query,
        "aggregation": aggregate_by,
    }
    return render(request, "pages/chart_page.html", context=context)


def contact_sent(request):
    table = ["name", "email", "subject", "message"]
    for element in table:
        print(request.POST.get(element))
    # Send the contant info
    return render(request, "pages/contact.html")
