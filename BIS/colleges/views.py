from django.shortcuts import render, redirect, get_object_or_404
from colleges.models import College
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Max
from .forms import CollegeForms
from .models import User

# Create your views here.

def get_college(request, college_id):
    try:
        college = College.objects.get(id=college_id)
        college_data = {
            'id': college.id,
            'shortname': college.shortname,
            'description': college.description,
            'is_deleted': college.is_deleted,
        }
        return JsonResponse(college_data, safe=False)
    except College.DoesNotExist:
        return JsonResponse({'error': 'College not found'}, status=404)


def add_college(request):
    addCollegesForm = CollegeForms

    if request.method == "POST":
        form = CollegeForms(request.POST)
        if form.is_valid():
            college = form.save(commit=False)
            college.id = (College.objects.aggregate(max_id=Max('id'))['max_id'] or 0) +1
            college.inserted_by = request.user
            college.is_deleted = False
            college.save()
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'college/addCollege.html', {'addCollegesForm':form, 'errors':form.errors})
    return render(request, 'college/addCollege.html', {'addCollegesForm':addCollegesForm})

def edit_college(request, college_id=None):
    if college_id:
        college = College.objects.get(id=college_id)
    else:
        college = None

    if request.method == "POST":
        if college:
            form = CollegeForms(request.POST, instance=college)
        else:
            shortname = request.POST.get('shortname')
            college = College.objects.filter(shortname=shortname).first()

            if college:
                form = CollegeForms(request.POST, instance=college)
            else:
                form = CollegeForms(request.POST)

        if form.is_valid():
            form.save()
            return redirect('sysadmin')

    else:
        if college:
            form = CollegeForms(instance=college)
        else:
            form = CollegeForms()

    return render(request, 'college/editCollege.html', {'addCollegesForm': form, 'college': college})

def delete_college(request, college_id):
    college = get_object_or_404(College, id=college_id)
    college.is_deleted = True
    college.save()
    return redirect('sysadmin')

def recover_college(request, college_id):
    college = get_object_or_404(College, id=college_id)
    college.is_deleted = False
    college.save()
    return redirect('sysadmin')