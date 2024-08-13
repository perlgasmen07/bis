from django.shortcuts import render
from attributes.models import Attribute, Property
from django.http import JsonResponse, HttpResponseRedirect
from .forms import AttributeForms, PropertyForms
from django.urls import reverse
# Create your views here.
def get_attribute(request, attribute_id):
    try:
        attribute = Attribute.objects.get(id=attribute_id)
        attribute_data = {
            'id': attribute.id,
            'shortname': attribute.shortname,
            'type': attribute.type,
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
            form.save()
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'attribute/addAttribute.html', {'addAttributesForm':form, 'errors':form.errors})
    return render(request, 'attribute/addAttribute.html', {'addAttributesForm':addAttributesForm})

def add_property(request):
    addPropertiesForm = PropertyForms

    if request.method == "POST":
        form = PropertyForms(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'property/addProperty.html', {'addPropertiesForm':form, 'errors':form.errors})
    return render(request, 'property/addProperty.html', {'addPropertiesForm':addPropertiesForm})

