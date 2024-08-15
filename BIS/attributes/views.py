from django.shortcuts import render
from attributes.models import Attribute, Property, BuildingAttribute
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .forms import AttributeForms, PropertyForms
from django.urls import reverse
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
            'properties': property_data  # Add related properties to the response
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
    addAttributesForm = AttributeForms

    if request.method == "POST":
        form = AttributeForms(request.POST)
        if form.is_valid():
            #attribute = Attribute.objects.get('' == form.building, '')
            form.save()
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'attribute/addAttribute.html', {'addAttributesForm':form, 'errors':form.errors})
    return render(request, 'attribute/addAttribute.html', {'addAttributesForm':addAttributesForm})


def add_property(request):
    addPropertiesForm = PropertyForms()
    
    if request.method == "POST":
        form = PropertyForms(request.POST)
        if form.is_valid():
            property_instance = form.save(commit=False)
            
            # Handle dynamic keys and values
            new_keys = request.POST.getlist('new_keys[]')
            new_values = request.POST.getlist('new_values[]')
            data = {}
            if new_keys:
                for i, key in enumerate(new_keys):
                    value = new_values[i] if i < len(new_values) else None  # Set value to None if not provided
                    data[key] = value
                property_instance.data = data
            
            property_instance.save()
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'property/addProperty.html', {'addPropertiesForm': form, 'errors': form.errors})
        
    # Check if an attribute is selected
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
        'existing_data': json.dumps(existing_data)  # Pass existing data as JSON
    })
def edit_attribute(request, attribute_id):
        return HttpResponse(attribute_id)
def edit_property(request, property_id):
        return HttpResponse(property_id)

def delete_attribute(request, attribute_id):
        return HttpResponse(attribute_id)
def delete_property(request, property_id):
        return HttpResponse(property_id)