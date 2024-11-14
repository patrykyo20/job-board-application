from rest_framework import serializers
from .models import User, Job, Location, Salary, Image
from django.core.exceptions import ValidationError
    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
    
class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'name', 'photo']

class UserSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    jobApplication = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    jobOfferPosted = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    
    password = serializers.CharField(write_only=True) 
    
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):

        if len(value) < 8:
            raise ValidationError("Hasło musi mieć co najmniej 8 znaków.")
        return value

    def create(self, validated_data):

        password = validated_data.pop('password')
        location_data = validated_data.pop('location', None)
        user = User.objects.create(**validated_data)
        
        if location_data:
            location = Location.objects.create(**location_data)
            user.location = location
            user.save()

        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)
        location_data = validated_data.pop('location', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        if location_data:
            location = Location.objects.update_or_create(**location_data)
            instance.location = location

        instance.save()
        return instance

class JobSerializer(serializers.ModelSerializer):
    location = LocationSerializer() 
    salary = SalarySerializer()
    image = ImageSerializer()
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Job
        fields = [
            'id',
            'position',
            'company',
            'location',
            'image',
            'salary',
            'description',
            'experience',
            'timeDimension',
            'isPremium',
            'author',
            'createdAt',
        ]

    def create(self, validated_data):
        image_data = validated_data.pop('image', None)
        location_data = validated_data.pop('location')
        salary_data = validated_data.pop('salary')
        
        location, _ = Location.objects.get_or_create(**location_data)
        salary, _ = Salary.objects.get_or_create(**salary_data)
        
        if image_data:
            image = Image.objects.create(**image_data)
        else:
            image = None
        
        job = Job.objects.create(image=image, location=location, salary=salary, **validated_data)
        
        return job
