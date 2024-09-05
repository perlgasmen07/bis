from django.shortcuts import render, get_object_or_404, redirect
from buildings.models import Building
from attributes.models import Attribute, BuildingAttribute, Property
from attributes.forms import BuildingAttributeForms, PropertyForms
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import BuildingForms
from django.db.models import Max
from io import BytesIO
import pandas as pd
import json, csv
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
import openpyxl
# Create your views here.

def get_buildings(request, college_id):
    buildings = Building.objects.filter(college_id=college_id)
    building_list = list(buildings.values('id', 'shortname'))
    return JsonResponse({'buildings': building_list})

def get_building(request, building_id):
    try:
        building = Building.objects.get(id=building_id)
        building_attributes = BuildingAttribute.objects.filter(building=building).select_related('attribute')
        
        attributes_data = []
        for ba in building_attributes:
            attribute_data = {
                'attribute__id': ba.attribute.id,
                'attribute__shortname': ba.attribute.shortname,
                'attribute__type': ba.attribute.type,
                'value': ba.value,
            }
            if ba.attribute.type == 'dynamic':
                property_data = Property.objects.filter(building=building, attribute=ba.attribute).values('data').first()
                if property_data:
                    attribute_data['property_data'] = property_data.get('data')
            attributes_data.append(attribute_data)

        building_data = {
            'id': building.id,
            'shortname': building.shortname,
            'attributes': attributes_data,
        }
        return JsonResponse(building_data, safe=False)
    except Building.DoesNotExist:
        return JsonResponse({'error': 'Building not found'}, status=404)
    
def building_detail(request, building_id):
    response = get_building(request, building_id) 
    building_data = response.content.decode('utf-8') 
    building = json.loads(building_data) 

    return render(request, 'building/buildingDetail.html', {
        'building': building
    })

def add_building(request):
    addBuildingsForm = BuildingForms

    if request.method == "POST":
        form = BuildingForms(request.POST)
        if form.is_valid():
            building = form.save(commit=False)
            building.id = (Building.objects.aggregate(max_id=Max('id'))['max_id'] or 0) + 1
            building.inserted_by = request.user
            building.is_deleted = False
            building.save()
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'building/addBuilding.html', {'addBuildingsForm':form, 'errors':form.errors})
    return render(request, 'building/addBuilding.html', {'addBuildingsForm':addBuildingsForm})

def update_building_view(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    building_attributes = BuildingAttribute.objects.filter(building=building).select_related('attribute')
    properties = Property.objects.filter(building=building)

    if request.method == 'POST':

        for ba in building_attributes:
            form = BuildingAttributeForms(request.POST, instance=ba, prefix=f'attr_{ba.id}')
            form.fields.pop('building', None)
            if form.is_valid():
                form.save()

        for prop in properties:
            form = PropertyForms(request.POST, instance=prop, prefix=f'prop_{prop.id}')
            form.fields.pop('building', None) 
            form.fields.pop('attribute', None) 
            if form.is_valid():
                json_data = prop.data or {}
                new_keys = request.POST.getlist(f'new_keys_{prop.id}[]')
                new_values = request.POST.getlist(f'new_values_{prop.id}[]')
                for key, value in zip(new_keys, new_values):
                    json_data[key] = value
                prop.data = json_data
                prop.save()

        return redirect('building_detail', building_id=building.id)

    else:

        attribute_forms = []
        for ba in building_attributes:
            form = BuildingAttributeForms(instance=ba, prefix=f'attr_{ba.id}')
            form.fields.pop('building', None)
            attribute_forms.append(form)

        property_forms = []
        for prop in properties:
            form = PropertyForms(instance=prop, prefix=f'prop_{prop.id}')
            form.fields.pop('building', None) 
            form.fields.pop('attribute', None) 
            if 'attribute' in form.fields:
                form.fields['attribute'].widget.attrs['disabled'] = True 
            property_forms.append(form)

    context = {
        'building': building,
        'attribute_forms': attribute_forms,
        'property_forms': property_forms,
    }
    return render(request, 'building/updateBuilding.html', context)

def edit_building(request, building_id=None):
    if building_id:
        building = get_object_or_404(Building, id=building_id)
    else:
        building = None

    if request.method == "POST":
        if building:
            form = BuildingForms(request.POST, instance=building)
        else:
            shortname = request.POST.get('shortname')
            building = Building.objects.filter(shortname=shortname).first()

            if building:
                form = BuildingForms(request.POST, instance=building)
            else:
                form = BuildingForms(request.POST)

        if form.is_valid():
            form.save()
            return redirect('sysadmin')

    else:
        if building:
            form = BuildingForms(instance=building)
        else:
            form = BuildingForms()  

    return render(request, 'building/editBuilding.html', {'addBuildingsForm': form, 'building': building})

def delete_building(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    building.is_deleted = True
    building.save()
    return redirect('sysadmin')

def recover_building(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    building.is_deleted = False
    building.save()
    return redirect('sysadmin')

def generate_building_report(request):
    buildings = Building.objects.all()
    report_data = []

    for building in buildings:
        building_attributes = BuildingAttribute.objects.filter(building=building).select_related('attribute')
        
        attributes_data = []
        for ba in building_attributes:
            attribute_data = {
                'attribute__id': ba.attribute.id,
                'attribute__shortname': ba.attribute.shortname,
                'attribute__type': ba.attribute.type,
                'value': ba.value,
            }
            if ba.attribute.type == 'dynamic':
                property_data = Property.objects.filter(building=building, attribute=ba.attribute).values('data').first()
                if property_data:
                    attribute_data['property_data'] = property_data.get('data')
            attributes_data.append(attribute_data)

        building_data = {
            'id': building.id,
            'shortname': building.shortname,
            'attributes': attributes_data,
        }

        report_data.append(building_data)

    context = {
        'report_data': report_data,
    }

    return render(request, 'building/buildingReport.html', context)

def export_building_report_excel(request):
    buildings = Building.objects.all()
    data = []
    
    for building in buildings:
        building_attributes = BuildingAttribute.objects.filter(building=building).select_related('attribute')
        
        for ba in building_attributes:
            if ba.attribute.type == 'dynamic':
                property_data = Property.objects.filter(building=building, attribute=ba.attribute).values('data').first()
                if property_data:
                    for key, value in property_data['data'].items():
                        data.append({
                            'Building Name': building.shortname,
                            'Attribute Name': ba.attribute.shortname,
                            'Attribute Value': ba.value,
                            'Property Title': ba.attribute.shortname,
                            'Property Key': key,
                            'Property Value': value
                        })
                else:
                    data.append({
                        'Building Name': building.shortname,
                        'Attribute Name': ba.attribute.shortname,
                        'Attribute Value': ba.value,
                        'Property Title': ba.attribute.shortname,
                        'Property Key': '',
                        'Property Value': ''
                    })
            else:
                data.append({
                    'Building Name': building.shortname,
                    'Attribute Name': ba.attribute.shortname,
                    'Attribute Value': ba.value,
                    'Property Title': '',
                    'Property Key': '',
                    'Property Value': ''
                })
    
    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="building_report.xlsx"'

    df.to_excel(response, index=False)

    return response


def export_building_report_csv(request):
    buildings = Building.objects.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="building_report.csv"'

    writer = csv.writer(response)
    
    writer.writerow(['Building Name', 'Attribute Name', 'Attribute Value', 'Property Title', 'Property Key', 'Property Value'])

    for building in buildings:
        building_attributes = BuildingAttribute.objects.filter(building=building).select_related('attribute')

        for ba in building_attributes:
            if ba.attribute.type == 'dynamic':
                property_data = Property.objects.filter(building=building, attribute=ba.attribute).values('data').first()
                if property_data:
                    for key, value in property_data['data'].items():
                        writer.writerow([building.shortname, ba.attribute.shortname, ba.value, ba.attribute.shortname, key, value])
                else:
                    writer.writerow([building.shortname, ba.attribute.shortname, ba.value, ba.attribute.shortname, '', ''])
            else:
                writer.writerow([building.shortname, ba.attribute.shortname, ba.value, '', '', ''])

    return response
