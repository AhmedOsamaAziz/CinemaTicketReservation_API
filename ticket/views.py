from logging import exception
from os import stat
from unicodedata import name
from django import views
from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets

from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from .models import Movie, Guest, Reservation

# 1- Without REST and No Model >> Function Based View (FBV)


def no_rest_no_model(request):
    guests = [
        {
            'id': 1,
            'name': 'Osama',
            'mobile': '01111109925'
        },
        {
            'id': 2,
            'name': 'Ahmed',
            'mobile': '01111109923'
        }
    ]
    return JsonResponse(guests, safe=False)  # For Non hashable items


# 2- No_REST_With_Model ( Without Django REST Framework)
def no_rest_with_model(request):
    allGuest = Guest.objects.all()
    dataResponse = {
        'guests': list(allGuest.values('name', 'mobile'))
    }
    return JsonResponse(dataResponse, safe=False)


# 3- Function Based View
# 3.1- GET(List)   POST(Create)
@api_view(['GET', 'POST'])
def FBV_LIST(request):
    # GET
    if request.method == 'GET':  # Get Records From DataBase
        # DB Query
        guests = Guest.objects.all()
        # Serialize Data
        # many means more than one
        serializer = GuestSerializer(guests, many=True)
        # Response
        return Response(serializer.data)
    elif request.method == 'POST':  # Create New Record Into DataBase
        # Deserialize
        serializer = GuestSerializer(data=request.data)
        # Validate
        if serializer.is_valid():
            # Save
            serializer.save()
            # Response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 3.2- GET(PK) PUT DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def FBV_PK(request, pk):
    # DB Query
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET
    if request.method == 'GET':
        # Serialize
        serializer = GuestSerializer(guest)
        # Return
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT
    elif request.method == 'PUT':
        # Deserialize
        serializer = GuestSerializer(guest, data=request.data)
        # Validate
        if serializer.is_valid():
            serializer.save()
            # Response
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 4- Class Based View (CBV)
# 4.1- GET(List) POST(Create)
class CBV_List(APIView):
    # BuiltIn Function (GET Request)
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # BuiltIn Function (POST Request)
    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 4.2 GET(PK) PUT DELETE
class CBV_PK(APIView):
    # Built In Function (To Query DataBase)
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExists:
            raise Http404

    # BuiltIn Function (GET PK Request)
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # BuiltIn Function (PUT Request)
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # BuiltIn Function (DELETE Request)
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5 Mixins
# 5.1 Mixins GET(List) POST(Create)
class Mixins_List(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    # Must be named 'queryset'
    queryset = Guest.objects.all()
    # Must be named 'serializer_class'
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# Mixins GET(PK) PUT(Update) DELETE
class Mixins_PK(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    # Must be named 'queryset'
    queryset = Guest.objects.all()
    # Must be named 'serializer_class'
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)


# 6 Generics
# 6.1 GET(List) POST(Create)
class Generics_List(generics.ListCreateAPIView):
    # Must be named 'queryset'
    queryset = Guest.objects.all()
    # Must be named 'serializer_class'
    serializer_class = GuestSerializer


# 6.2 GET(PK) PUT(Update) DELETE
class Generics_PK(generics.RetrieveUpdateDestroyAPIView):
    # Must be named 'queryset'
    queryset = Guest.objects.all()
    # Must be named 'serializer_class'
    serializer_class = GuestSerializer


# 7 ViewSets
class ViewSets_Guest(viewsets.ModelViewSet):
    # Must be named 'queryset'
    queryset = Guest.objects.all()
    # Must be named 'serializer_class'
    serializer_class = GuestSerializer


class ViewSets_Movie(viewsets.ModelViewSet):
    # Must be named 'queryset'
    queryset = Movie.objects.all()
    # Must be named 'serializer_class'
    serializer_class = MovieSerializer
    # Allow Filter
    filter_backend = [filters.SearchFilter]
    # Determine Search Fields
    search_fields = ['hall', 'movie']


class ViewSets_Reservation(viewsets.ModelViewSet):
    # Must be named 'queryset'
    queryset = Reservation.objects.all()
    # Must be named 'serializer_class'
    serializer_class = ReservationSerializer


# Business Functions
@api_view(['GET'])
def find_movie(request):
    try:
        movies = Movie.objects.filter(
            hall=request.data['hall'],
            movie=request.data['movie'],
        )
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        hall=request.data['hall'],
        movie=request.data['movie'],
    )

    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation =Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    serializer = ReservationSerializer(reservation)

    return Response(serializer.data, status=status.HTTP_201_CREATED)