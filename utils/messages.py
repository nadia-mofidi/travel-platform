from django.contrib import messages


def success_message(request, message):
    messages.success(request, message)


def error_message(request, message):
    messages.error(request, message)