from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Group


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_group(request):
    owner_username = request.data.get('name')
    group_name = request.data.get('group_name')
    created_at = timezone.now()
    members_usernames = request.data.get('members', [])
    members_usernames.append(owner_username)

    try:
        owner = User.objects.get(username=owner_username)
    except User.DoesNotExist:
        return Response({'status': 'owner not found'}, status=404)

    try:
        if Group.objects.filter(name=group_name).exists():
            return Response({'status': 'group already exists'}, status=400)

        group = Group.objects.create(owner=owner, name=group_name, created_at=created_at)
        members = User.objects.filter(username__in=members_usernames)
        group.members.set(members)
        group.save()
        return Response({'status': 'group created', 'group_id': group.id})
    except Exception as e:
        return Response({'status': 'error', 'detail': str(e)}, status=500)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def join_group(request):
    group_name = request.data.get('group_name')
    user = User.objects.get(username=request.user.username)
    try:
        group = Group.objects.get(name=group_name)
        group.members.add(user)
        return Response({'status': 'joined group successfully'})
    except Group.DoesNotExist:
        return Response({'status': 'group not found'}, status=404)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def leave_group(request):
    group_name = request.data.get('group_name')
    user = User.objects.get(username=request.user.username)
    try:
        group = Group.objects.get(name=group_name)
        group.members.remove(user)
        return Response({'status': 'left group successfully'})
    except Group.DoesNotExist:
        return Response({'status': 'group not found'}, status=404)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def get_all_groups(request):
    user = request.user
    groups = Group.objects.filter(members=user)
    group_list = []
    for group in groups:
        group_list.append({
            'group_id': group.id,
            'group_name': group.name,
            'owner': group.owner.username,
            'created_at': group.created_at.isoformat(),
            'members': [member.username for member in group.members.all()]
        })
    return Response({'status': 'success', 'groups': group_list})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def remove_group(request):
    group_id = request.data.get('group_id')
    try:
        group = Group.objects.get(id=group_id)
        if group.owner != request.user:
            return Response({'status': 'not authorized to delete this group'}, status=403)
        group.delete()
        return Response({'status': 'group deleted successfully'})
    except Group.DoesNotExist:
        return Response({'status': 'group not found'}, status=404)
