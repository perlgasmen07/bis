from django.shortcuts import render
from buildings.models import Building
from attributes.models import Attribute, BuildingAttribute
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import BuildingForms
# Create your views here.
def get_building(request, building_id):
    try:
        building = Building.objects.get(id=building_id)
        building_attributes = BuildingAttribute.objects.filter(building=building_id).select_related('attribute')
        attributes = building_attributes.values('id', 'attribute__shortname')
        building_data = {
            'id': building.id,
            'shortname': building.shortname,
            'attributes': list(attributes),  # Add related attributes to the response
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

def edit_building(request, building_id):
    try:
        building = Building.objects.get(id=building_id)
        room_data = {
            'id': building.id,
            'shortname': building.shortname,
            'college_id': building.college_id,
            'is_deleted':building.is_deleted,
        }
        return JsonResponse(room_data, safe=False)
    except Building.DoesNotExist:
        return JsonResponse({'error': 'Building not found'}, status=404)

def delete_building(request, building_id):
     return HttpResponse(building_id)