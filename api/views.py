from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import User,Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Count
from django.db import models

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    data = request.data
    data['created_by'] = request.user.id
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    tasks = Task.objects.all()

    status = request.GET.get('status')
    assigned_to = request.GET.get('assigned_to')
    deadline = request.GET.get('deadline')

    if status:
        tasks = tasks.filter(status=status)

    if assigned_to:
        tasks = tasks.filter(assigned_to=assigned_to)

    if deadline:
        tasks = tasks.filter(deadline__date=deadline)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, id):
    task = get_object_or_404(Task, id=id)
    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return Response({"message": "Task deleted"})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def move_task(request):
    task_id = request.data.get("task_id")
    new_status = request.data.get("new_status")
    new_position = request.data.get("new_position")

    task = get_object_or_404(Task, id=task_id)

    old_status = task.status

    # Step 1: Remove from old column
    Task.objects.filter(
        status=old_status,
        position__gt=task.position
    ).update(position=models.F('position') - 1)

    # Step 2: Shift new column
    Task.objects.filter(
        status=new_status,
        position__gte=new_position
    ).update(position=models.F('position') + 1)

    # Step 3: Update task
    task.status = new_status
    task.position = new_position
    task.save()

    return Response({"message": "Task moved"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    total = Task.objects.count()

    not_started = Task.objects.filter(status='not_started').count()
    in_progress = Task.objects.filter(status='in_progress').count()
    completed = Task.objects.filter(status='completed').count()

    overdue = Task.objects.filter(deadline__lt=now()).exclude(status='completed').count()

    tasks_per_user = Task.objects.values('assigned_to').annotate(count=Count('id'))

    completion_percentage = (completed / total * 100) if total > 0 else 0

    return Response({
        "total_tasks": total,
        "not_started": not_started,
        "in_progress": in_progress,
        "completed": completed,
        "overdue": overdue,
        "completion_percentage": completion_percentage,
        "tasks_per_user": list(tasks_per_user)
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = User.objects.all().values('id', 'username', 'email')
    return Response(users)