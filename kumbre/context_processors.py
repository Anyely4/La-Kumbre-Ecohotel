from .models import Reserva

def cart_count(request):
    if request.user.is_authenticated:
        count = Reserva.objects.filter(usuario=request.user, confirmada=False).count()
    else:
        count = 0
    return {'cart_count': count}