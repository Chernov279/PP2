from django.shortcuts import render


def index(request):
    context = {
        "title": "Профиль Пользователя",
        # "user_info" : request.json
    }
    return render(request=request, context=context, template_name="users/index.html")


