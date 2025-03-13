from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from core.models import Event, EventImage
from .serializers import EventSerializer
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import FormParser, MultiPartParser

@api_view(['GET'])
def test(request):
    return Response({'message': 'API Created Successfully'}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='GET',
    operation_summary='Get Event Details',
    operation_description='This endpoint will return an Event Details',
    responses={
        status.HTTP_200_OK: EventSerializer,
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description='Invalid Request',
        )
    }
)
@api_view(['GET'])
def event_list(request):
    events = Event.objects.all()

    serializer = EventSerializer(events, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='POST',
    operation_summary='POST Event Details',
    operation_description='This endpoint will create a Event Details',
    manual_parameters=[
        openapi.Parameter(
            'images',
            openapi.IN_FORM,
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_FILE)
        )
    ],
    request_body=EventSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description='Event Created',
            examples={'application/json': {'message': 'Event created successfully'}}
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
            description='Invalid Request',
            examples={'application/json': {"title": ["This field is required."]}}
        )
    }
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        event = serializer.save()

        images = request.FILES.getlist('images')
        for image in images:
            EventImage.objects.create(event=event, image=image)

        return Response({'message': 'Event created successfully'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['DELETE'])
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()

    return Response({'message': 'Event Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    event_serializer = EventSerializer(event, data=request.data)

    if event_serializer.is_valid():
        event_serializer.save()

        return Response({'message': f'Event pk: {pk}, updated successfully', 'event': event_serializer.data}, status=status.HTTP_200_OK)

    return Response(event_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
