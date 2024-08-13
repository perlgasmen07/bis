from django.shortcuts import render
from buildings.models import Building
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import BuildingForms
# Create your views here.
def get_building(request, building_id):
    try:
        building = Building.objects.get(id=building_id)
        building_data = {
            'id': building.id,
            'shortname': building.shortname,
        }
        return JsonResponse(building_data, safe=False)
    except Building.DoesNotExist:
        return JsonResponse({'error': 'Building not found'}, status=404)

def add_building(request):
    addBuildingsForm = BuildingForms

    if request.method == "POST":
        form = BuildingForms(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'building/addBuilding.html', {'addBuildingsForm':form, 'errors':form.errors})
    return render(request, 'building/addBuilding.html', {'addBuildingsForm':addBuildingsForm})