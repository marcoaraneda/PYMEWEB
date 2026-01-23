from django.contrib.auth import get_user_model
from rest_framework import serializers
from cloudinary import uploader

from .models import UserProfile, StoreMembership
from apps.stores.models import Store


class StoreSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "slug"]


class StoreMembershipSerializer(serializers.ModelSerializer):
    store = StoreSlimSerializer()
    roles = serializers.SlugRelatedField(many=True, read_only=True, slug_field="code")

    class Meta:
        model = StoreMembership
        fields = ["store", "roles"]

User = get_user_model()


class MeSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    upload_avatar = serializers.URLField(write_only=True, required=False, allow_null=True, allow_blank=True)
    memberships = StoreMembershipSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "avatar_url",
            "upload_avatar",
            "memberships",
        ]
        read_only_fields = ["id", "username", "is_staff", "avatar_url", "memberships"]

    def get_avatar_url(self, obj):
        profile = getattr(obj, "profile", None)
        if profile and profile.avatar:
            return profile.avatar.url
        return None

    def update(self, instance, validated_data):
        avatar_url = validated_data.pop("upload_avatar", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if avatar_url:
            profile, _ = UserProfile.objects.get_or_create(user=instance)
            try:
                result = uploader.upload(avatar_url, folder="avatars")
                profile.avatar = result.get("public_id")
                profile.save()
            except Exception:
                pass
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual no es correcta")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este usuario ya existe")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.get_or_create(user=user)
        return user
