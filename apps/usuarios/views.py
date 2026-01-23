from django.contrib.auth import get_user_model
from django.utils.text import slugify
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from apps.stores.models import Store
from .models import Role, StoreMembership
from .serializers import MeSerializer, PasswordChangeSerializer, SignupSerializer

User = get_user_model()


class MeView(generics.RetrieveUpdateAPIView):
	serializer_class = MeSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		return self.request.user


class PasswordChangeView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, *args, **kwargs):
		serializer = PasswordChangeSerializer(data=request.data, context={"request": request})
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({"detail": "Contraseña actualizada"}, status=status.HTTP_200_OK)


class SignupView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = SignupSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()

		# Crea tienda base y asigna rol admin para que el usuario pueda gestionar de inmediato
		try:
			base_name = request.data.get("first_name") or user.username or "Mi tienda"
			slug_base = slugify(base_name) or "mi-tienda"
			slug_candidate = slug_base
			counter = 1
			while Store.objects.filter(slug=slug_candidate).exists():
				slug_candidate = f"{slug_base}-{counter}"
				counter += 1
			store = Store.objects.create(name=f"Tienda de {base_name}", slug=slug_candidate)

			role_admin, _ = Role.objects.get_or_create(code=Role.ADMIN)
			membership, _ = StoreMembership.objects.get_or_create(user=user, store=store)
			membership.roles.add(role_admin)
		except Exception:
			pass

		refresh = RefreshToken.for_user(user)
		data = {
			"user": MeSerializer(user).data,
			"access": str(refresh.access_token),
			"refresh": str(refresh),
		}
		return Response(data, status=status.HTTP_201_CREATED)
