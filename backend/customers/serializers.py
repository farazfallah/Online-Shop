from rest_framework import serializers
from customers.models import Customer, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address_line', 'city', 'state', 'postal_code']
        

class CustomerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    image = serializers.ImageField(required=False, allow_empty_file=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'image', 'is_otp_verified', 'addresses']

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if image:
            # If there's an existing image that's not the default, delete it
            if instance.image and instance.image.name != 'users/default.png':
                instance.image.delete(save=False)
            
            # Set the new image
            instance.image = image
        
        instance.save()
        return instance