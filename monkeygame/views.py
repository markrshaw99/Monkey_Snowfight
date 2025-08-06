from django.shortcuts import render

def game_view(request):
    return render(request, 'monkeygame/play.html')
