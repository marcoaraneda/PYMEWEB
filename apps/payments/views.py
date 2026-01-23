import uuid

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType


@api_view(["POST"])
@permission_classes([AllowAny])
def init_webpay(request):
    amount = request.data.get("amount")

    if not amount:
        return Response({"error": "amount requerido"}, status=400)

    buy_order = f"orden_{uuid.uuid4().hex[:10]}"
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key
    return_url = "http://127.0.0.1:8000/api/payments/webpay/return/"

    webpay_options = WebpayOptions(
        settings.WEBPAY_COMMERCE_CODE,
        settings.WEBPAY_API_KEY,
        IntegrationType.TEST
    )

    tx = Transaction(webpay_options)

    response = tx.create(
        buy_order=buy_order,
        session_id=session_id,
        amount=int(amount),
        return_url=return_url
    )

    return Response({
        "token": response["token"],
        "url": response["url"]
    })


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def webpay_return(request):
    """Recibe el retorno de Webpay y devuelve el token recibido.
    Ajusta la lógica de confirmación según el flujo real de captura/commit."""
    token = request.query_params.get("token_ws") or request.data.get("token_ws")
    if not token:
        return Response({"detail": "token_ws no recibido"}, status=400)

    return Response({
        "status": "ok",
        "token": token,
    })