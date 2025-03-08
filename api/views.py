from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from core.models import Event
from .serializers import EventSerializer

@api_view(['GET'])
def test(request):
    return Response({'message': 'API Created Successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def event_list(request):
    events = Event.objects.all()

    serializer = EventSerializer(events, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response({'message': 'Event created successfully'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)