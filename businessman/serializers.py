from rest_framework import serializers

from .models import User, Chat


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'company', 'location', 'user_role',
                  'google_location_url', 'latitude', 'longitude']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        read_only_fields = ['status']

    def create(self, validated_data):
        validated_data['status'] = 'pending'
        return super().create(validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'user_role', 'location', 'google_location_url',
                  'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data


class LocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['latitude', 'longitude']
