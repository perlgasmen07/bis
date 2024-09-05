from django.shortcuts import render, redirect, get_object_or_404
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
            floor.inserted_by = request.user
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
    floor = get_object_or_404(Floor, id=floor_id)
    if request.method == "POST":
        form = FloorForms(request.POST, instance=floor)
        if form.is_valid():
            form.save()
            return redirect('sysadmin')
    else:
        form = FloorForms(instance=floor)
    return render(request, 'floor/editFloor.html', {'form': form})

def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = RoomForms(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('sysadmin')
    else:
        form = RoomForms(instance=room)
    return render(request, 'room/editRoom.html', {'form': form})

def delete_floor(request, floor_id):
    floor = get_object_or_404(Floor, id=floor_id)
    floor.is_deleted = True
    floor.save()

    rooms = Room.objects.filter(floor=floor)
    rooms.update(is_deleted=True)

    return redirect('sysadmin')

def recover_floor(request, floor_id):
    floor = get_object_or_404(Floor, id=floor_id)
    floor.is_deleted = False
    floor.save()

    #Recover rooms related
    rooms = Room.objects.filter(floor=floor)
    rooms.update(is_deleted=False)

    return redirect('sysadmin')

def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.is_deleted = True
    room.save()
    return redirect('sysadmin')

def recover_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if room.floor and room.floor.is_deleted:
        return JsonResponse({'error': 'Cannot recover room because the associated floor is deleted'}, status=400)

    room.is_deleted = False
    room.save()

    return redirect('sysadmin')


