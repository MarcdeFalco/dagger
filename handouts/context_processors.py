from handouts.models import Handout

def handouts_menu(request):
    handouts = Handout.objects.all()
    return {'handouts_menu' : handouts}

