from django.shortcuts import render
from floors.models import Floor, Room
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import FloorForms,RoomForms

# Create your views here.
def get_floor(request, floor_id):
    try:
        floor = Floor.objects.get(id=floor_id)
        floor_data = {
            'id': floor.id,
            'Level': floor.level,
        }
        return JsonResponse(floor_data, safe=False)
    except Floor.DoesNotExist:
        return JsonResponse({'error': 'Floor not found'}, status=404)
    
def get_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        room_data = {
            'id': room.id,
            'room_no': room.room_no,
        }
        return JsonResponse(room_data, safe=False)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)

def add_floor(request):
    addFloorsForm = FloorForms

    if request.method == "POST":
        form = FloorForms(request.POST)
        if form.is_valid():
            floor = form.save(commit=False)
            floor.inserted_by = {{request.user.id}}
            floor.is_deleted = False
            floor.save()
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'floor/addFloor.html', {'addFloorsForm':form, 'errors':form.errors})
    return render(request, 'floor/addFloor.html', {'addFloorsForm':addFloorsForm})

def add_room(request):
    addRoomsForm = RoomForms

    if request.method == "POST":
        form = RoomForms(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.is_deleted = False
            room.save()
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'room/addRoom.html', {'addRoomsForm':form, 'errors':form.errors})
    return render(request, 'room/addRoom.html', {'addRoomsForm':addRoomsForm})

def edit_floor(request, floor_id):
    try:
        floor = Floor.objects.get(id=floor_id)
        room_data = {
            'id': floor.id,
            'level': floor.level,
            'building': floor.building_id,
        }
        return JsonResponse(room_data, safe=False)
    except Floor.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)

def edit_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        room_data = {
            'id': room.id,
            'room_no': room.room_no,
            'floor_id': room.floor_id,
        }
        return JsonResponse(room_data, safe=False)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)

def delete_floor(request, floor_id):
    Floor.objects.filter(pk=floor_id).delete()
    return HttpResponseRedirect(reverse('sysadmin'))

def delete_room(request, room_id):
    Room.objects.filter(pk=room_id).delete()
    return HttpResponseRedirect(reverse('sysadmin'))