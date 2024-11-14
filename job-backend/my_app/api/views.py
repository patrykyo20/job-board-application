from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import User, Job
from .serializer import UserSerializer, JobSerializer
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from .filters import JobFilter
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'This is a protected view'}
        return Response(content)

@api_view(['GET'])
def get_user(request):
  users = User.objects.all()
  serializer = UserSerializer(users, many=True)
  return Response(serializer.data)


@api_view(['POST'])
def create_user(request):
  serializer = UserSerializer(data = request.data)
  if (serializer.is_valid()):
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            return Response({
                'message': 'User created successfully',
                'access_token': access_token,
                'refresh_token': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(request, email=email, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh),
        }, status=200)
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def user_details(request, pk):
  try: 
    user = User.objects.get(pk=pk)
  except User.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == 'GET':
    serializer = UserSerializer(user)
    return Response(serializer.data)
  
  elif request.method == 'PUT':
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
  
  elif request.method == 'DELETE':
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
class JobPagination(PageNumberPagination):
  page_size = 5

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
  
@api_view(['GET'])
def get_job(request):
    jobs = Job.objects.all()

    job_filter = JobFilter(request.GET, queryset=jobs)
    filtered_jobs = job_filter.qs
    
    sort_param = request.GET.get('sort', 'createdAt')

    if sort_param == 'createdAt':
        jobs = jobs.order_by('-createdAt')
    elif sort_param == 'position_asc':
        jobs = jobs.order_by('position')
    elif sort_param == 'position_desc':
        jobs = jobs.order_by('-position')
    elif sort_param == 'company_asc':
        jobs = jobs.order_by('company')
    elif sort_param == 'company_desc':
        jobs = jobs.order_by('-company')

    paginator = Paginator(filtered_jobs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    serializer = JobSerializer(page_obj, many=True)

    return Response({
        'count': paginator.count,
        'next': page_obj.has_next(),
        'previous': page_obj.has_previous(),
        'results': serializer.data 
    })
  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job(request):
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def job_details(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobSerializer(job)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != job.author:
            return Response({"error": "You do not have permission to edit this job."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user != job.author:
            return Response({"error": "You do not have permission to delete this job."}, status=status.HTTP_403_FORBIDDEN)
        
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
