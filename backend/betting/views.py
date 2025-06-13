from datetime import timezone

from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from betting.models import Group


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_group(request):
    owner_username = request.data.get('name')
    group_Name = request.data.get('group_Name')
    created_at = timezone.now()
    members_usernames = request.data.get('members', [])
    members_usernames.append(owner_username)
    try:
        owner = User.objects.get(username=owner_username)
    except User.DoesNotExist:
        return Response({'status': 'owner not found'}, status=404)
    try:
        if Group.objects.filter(group_Name=group_Name).exists():
            return Response({'status': 'group already exists'}, status=400)
        Group = Group.objects.create(owner=owner, group_Name=group_Name, created_at=created_at)
        members = User.objects.filter(username__in=members_usernames)
        Group.members.set(members)
        Group.save()
        return Response({'status': 'group created', 'group_id': Group.id})
    except Exception as e:
        return Response({'status': 'error', 'detail': str(e)}, status=500)



@permission_classes([IsAuthenticated])
@api_view(['POST'])

def join_group(request):
    group_name = request.data.get('group_name')
    user = User.objects.get(username=request.user.username)
    try:
        Group = Group.objects.get(name=group_name)
        Group.members.add(user),
    except Group.DoesNotExist:
        return Response({'status': 'group not found'}, status=404)

@permission_classes([IsAuthenticated])
@api_view(['POST'])

def leave_group(request):
    group_name = request.data.get('group_name')
    user = User.objects.get(username=request.user.username)
    try:
        Group = Group.objects.get(name=group_name)
        Group.members.remove(user)
        return Response({'status': 'left group successfully'})
    except Group.DoesNotExist:
        return Response({'status': 'group not found'}, status=404)

@permission_classes([IsAuthenticated])
@api_view(['POST'])

def get_all_groups(request):
    user = User.objects.get(username=request.user.username)
    groups = Group.objects.filter(members=user)
    group_list = []
    for Group in groups:
        group_list.append({
            'group_id': Group.id,
            'group_name': Group.group_Name,
            'owner': Group.owner.username,
            'created_at': Group.created_at.isoformat(),
            'members': [member.username for member in Group.members.all()]
        })
    return Response({'status': 'success', 'groups': group_list})

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def remove_group(request):
    group_id = request.data.get('group_id')
    try:
        Group = Group.objects.get(id=group_id)
        if Group.owner != request.user:
            return Response({'status': 'not authorized to delete this group'}, status=403)
        Group.delete()
        return Response({'status': 'group deleted successfully'})
    except Group.DoesNotExist:
        return Response({'status': 'group not found'}, status=404)
