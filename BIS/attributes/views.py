from django.shortcuts import render
from attributes.models import Attribute, Property, BuildingAttribute
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .forms import AttributeForms, PropertyForms, BuildingAttributeForms
from django.urls import reverse
from django.db.models import Max
import json
# Create your views here.
def get_attribute(request, attribute_id):
    try:
        attribute = Attribute.objects.get(id=attribute_id)
        properties = Property.objects.filter(attribute=attribute)
        property_data = {}
        
        if properties.exists():
            property_instance = properties.first()
            property_data = property_instance.data
        
        attribute_data = {
            'id': attribute.id,
            'shortname': attribute.shortname,
            'type': attribute.type,
            'properties': property_data
        }
        return JsonResponse(attribute_data, safe=False)
    except Attribute.DoesNotExist:
        return JsonResponse({'error': 'Attribute not found'}, status=404)
    
def get_property(request, property_id):
    try:
        property = Property.objects.get(id=property_id)
        property_data = {
            'id': property.id,
            'data': property.data,
        }
        return JsonResponse(property_data, safe=False)
    except Property.DoesNotExist:
        return JsonResponse({'error': 'Property not found'}, status=404)

def add_attribute(request):
    if request.method == "POST":
        form = AttributeForms(request.POST)
        form_b = BuildingAttributeForms(request.POST)
        
        if form.is_valid() and form_b.is_valid():
            attribute = form.save(commit=False)
            buildingattribute = form_b.save(commit=False)
            
            attribute.inserted_by = request.user
            attribute.is_deleted = False
            attribute.save()
            
            buildingattribute.attribute = attribute
            buildingattribute.inserted_by = request.user
            buildingattribute.is_deleted = False
            buildingattribute.save()
            
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'attribute/addAttribute.html', {
                'addAttributesForm': form,
                'addBuildingAttributeForm': form_b,
                'errors': form.errors
            })
    
    else:
        form = AttributeForms()
        form_b = BuildingAttributeForms()
        
    return render(request, 'attribute/addAttribute.html', {
        'addAttributesForm': form,
        'addBuildingAttributeForm': form_b
    })
def add_property(request):
    addPropertiesForm = PropertyForms()
    
    if request.method == "POST":
        form = PropertyForms(request.POST)
        if form.is_valid():
            property_instance = form.save(commit=False)
            
            new_keys = request.POST.getlist('new_keys[]')
            new_values = request.POST.getlist('new_values[]')
            data = {}
            if new_keys:
                for i, key in enumerate(new_keys):
                    value = new_values[i] if i < len(new_values) else None
                    data[key] = value
                property_instance.data = data
            property_instance.inserted_by = request.user
            property_instance.save()
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'property/addProperty.html', {'addPropertiesForm': form, 'errors': form.errors})
        
    attribute_id = request.GET.get('attribute')
    existing_data = {}

    if attribute_id:
        try:
            attribute = Attribute.objects.get(id=attribute_id)
            properties = Property.objects.filter(attribute=attribute).first()
            if properties:
                existing_data = properties.data
        except Attribute.DoesNotExist:
            pass
    
    return render(request, 'property/addProperty.html', {
        'addPropertiesForm': addPropertiesForm,
        'existing_data': json.dumps(existing_data)
    })
from django.shortcuts import get_object_or_404

def edit_attribute(request, attribute_id):
    attribute = get_object_or_404(Attribute, id=attribute_id)
    if request.method == 'POST':
        form = AttributeForms(request.POST, instance=attribute)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sysadmin'))
    else:
        form = AttributeForms(instance=attribute)
    
    return render(request, 'attribute/editAttribute.html', {
        'addAttributesForm': form
    })

def edit_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = PropertyForms(request.POST, instance=property_instance)
        if form.is_valid():
            new_keys = request.POST.getlist('new_keys[]')
            new_values = request.POST.getlist('new_values[]')
            data = {}
            if new_keys:
                for i, key in enumerate(new_keys):
                    value = new_values[i] if i < len(new_values) else None
                    data[key] = value
                property_instance.data = data
            
            form.save()
            return HttpResponseRedirect(reverse('sysadmin'))
    else:
        form = PropertyForms(instance=property_instance)
    
    return render(request, 'property/editProperty.html', {
        'addPropertiesForm': form,
        'existing_data': json.dumps(property_instance.data)
    })

def delete_attribute(request, attribute_id):
    attribute = get_object_or_404(Attribute, id=attribute_id)
    attribute.is_deleted = True
    attribute.deleted_by = request.user
    attribute.save()
    return HttpResponseRedirect(reverse('sysadmin'))

def delete_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    property_instance.is_deleted = True
    property_instance.deleted_by = request.user
    property_instance.save()
    return HttpResponseRedirect(reverse('sysadmin'))

def recover_attribute(request, attribute_id):
    attribute = get_object_or_404(Attribute, id=attribute_id)
    attribute.is_deleted = False
    attribute.deleted_by = None
    attribute.save()
    return HttpResponseRedirect(reverse('sysadmin'))

def recover_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    property_instance.is_deleted = False
    property_instance.deleted_by = None
    property_instance.save()
    return HttpResponseRedirect(reverse('sysadmin'))