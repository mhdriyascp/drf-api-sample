from rest_framework import serializers
from .models import Color, Person
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('user with this username already exists')
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('email  already exists')

        return data

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']


class PersonSerializer(serializers.ModelSerializer):
    # color = ColorSerializer()
    # color_info = serializers.SerializerMethodField() # For grabbing data from associated table

    class Meta:
        model = Person
        fields = '__all__'
        # depth = 1  # For getting foreign key Model
        # exclude = ['user']

    # def get_color_info(self, obj):
    #     color_obj = Color.objects.get(id=obj.color.id)
    #     return {'color_name': color_obj.color_name, 'HEX_CODE': '#RDFDFF'}
        #return "India";

    # def validate(self, data):
    #     if data['age'] < 18:
    #         raise serializers.ValidationError('Age Should be greater than 18')
    #
    #     if len(data['name']) < 5:
    #         raise serializers.ValidationError('Name Should be greater than 5')
    #
    #     special_charecters = "!@#%^_+&*()/"
    #     if any(c in special_charecters for c in data['name']):
    #         raise serializers.ValidationError("name cannot contain special characters")
    #
    #     return data

