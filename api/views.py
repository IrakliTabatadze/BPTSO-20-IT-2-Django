from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, APIView
from rest_framework import status
from core.models import Event, EventImage
from .serializers import EventSerializer
from rest_framework.generics import get_object_or_404, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import FormParser, MultiPartParser
from .filters import EventFilter
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
import hashlib

# @api_view(['GET'])
# def test(request):
#     return Response({'message': 'API Created Successfully'}, status=status.HTTP_200_OK)

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 20


@swagger_auto_schema(
    method='GET',
    operation_summary='Get Event Details',
    operation_description='This endpoint will return an Event Details',
    manual_parameters=[
      openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
      openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
      openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING),
      openapi.Parameter('location', openapi.IN_QUERY, type=openapi.TYPE_STRING),
      openapi.Parameter('create_date_gte', openapi.IN_QUERY, type=openapi.TYPE_STRING),
      openapi.Parameter('create_date_lte', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ],
    responses={
        status.HTTP_200_OK: EventSerializer,
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description='Invalid Request',
        )
    }
)
@api_view(['GET'])
def event_list(request):

    query_params_string = ''

    for k, v in request.query_params.items():
        query_params_string += f'&{k}:{v}'

    # print(query_params_string)

    cache_key = f'events_{hashlib.md5(query_params_string.encode()).hexdigest()}'

    # print(cache_key)

    result = cache.get(cache_key)

    if not result:

        events = Event.objects.all()

        filterset = EventFilter(request.query_params, queryset=events)

        if filterset.is_valid():
            events = filterset.qs

        paginator = CustomPagination()

        paginated_queryset = paginator.paginate_queryset(events, request)

        serializer = EventSerializer(paginated_queryset, many=True)

        result = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data
        }

        cache.set(cache_key, result, 30)

        print('Events selected from database')
    else:
        print('Events selected from Redis')



    return Response(result, status=status.HTTP_200_OK)


# class EventListView(APIView):
#
#     @swagger_auto_schema(
#         operation_summary='Get Event Details',
#         operation_description='This endpoint will return an Event Details',
#         manual_parameters=[
#             openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
#             openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
#             openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING),
#             openapi.Parameter('location', openapi.IN_QUERY, type=openapi.TYPE_STRING),
#             openapi.Parameter('create_date_gte', openapi.IN_QUERY, type=openapi.TYPE_STRING),
#             openapi.Parameter('create_date_lte', openapi.IN_QUERY, type=openapi.TYPE_STRING),
#         ],
#         responses={
#             status.HTTP_200_OK: EventSerializer,
#             status.HTTP_400_BAD_REQUEST: openapi.Response(
#                 description='Invalid Request',
#             )
#         }
#     )
#     # @staticmethod
#     def get(self, request):
#         query_params_string = ''
#
#         for k, v in request.query_params.items():
#             query_params_string += f'&{k}:{v}'
#
#         # print(query_params_string)
#
#         cache_key = f'events_{hashlib.md5(query_params_string.encode()).hexdigest()}'
#
#         # print(cache_key)
#
#         result = cache.get(cache_key)
#
#         if not result:
#
#             events = Event.objects.all()
#
#             filterset = EventFilter(request.query_params, queryset=events)
#
#             if filterset.is_valid():
#                 events = filterset.qs
#
#             paginator = CustomPagination()
#
#             paginated_queryset = paginator.paginate_queryset(events, request)
#
#             serializer = EventSerializer(paginated_queryset, many=True)
#
#             result = {
#                 'count': paginator.page.paginator.count,
#                 'next': paginator.get_next_link(),
#                 'previous': paginator.get_previous_link(),
#                 'results': serializer.data
#             }
#
#             cache.set(cache_key, result, 30)
#
#             print('Events selected from database')
#         else:
#             print('Events selected from Redis')
#
#         return Response(result, status=status.HTTP_200_OK)

class EventListAPIView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        events = super().get_queryset()
        filterset = EventFilter(self.request.query_params, queryset=events)

        if filterset.is_valid():
            events = filterset.qs

        return events


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('location', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('create_date_gte', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('create_date_lte', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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


class EventCreateAPIView(CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        event = serializer.save()

        images = self.request.FILES.getlist('images')
        for image in images:
            EventImage.objects.create(event=event, image=image)

        return Response({'message': 'Event created successfully'}, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'images',
                openapi.IN_FORM,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_FILE)
            )
        ]
    )
    def post(self, request):
        return super().post(request)



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


class EventUpdateAPIView(UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_update(self, serializer):
        pass


class EventDeleteAPIView(DestroyAPIView):
    queryset = Event.objects.all()
    # lookup_field = 'pk'


# JWT - JSON Web Token