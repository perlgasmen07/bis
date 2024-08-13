from django.shortcuts import render
from colleges.models import College
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import CollegeForms

# Create your views here.

def get_college(request, college_id):
    try:
        college = College.objects.get(id=college_id)
        college_data = {
            'id': college.id,
            'shortname': college.shortname,
        }
        return JsonResponse(college_data, safe=False)
    except College.DoesNotExist:
        return JsonResponse({'error': 'College not found'}, status=404)


def add_college(request):
    addCollegesForm = CollegeForms

    if request.method == "POST":
        form = CollegeForms(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'college/addCollege.html', {'addCollegesForm':form, 'errors':form.errors})
    return render(request, 'college/addCollege.html', {'addCollegesForm':addCollegesForm})