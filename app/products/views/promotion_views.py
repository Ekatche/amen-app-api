"""
Views for promotion app
"""

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from ..models import Promotion
from ..functions import updateEndDate


class ProductPromotionView(APIView):
    """
    View for manage promotion APIs
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        promotion = request.POST["id"]
        try:
            updateEndDate(promotion)

            return Response(
                {"status": "success", "message": "Promotion date has been updated"},
                status=status.HTTP_200_OK,
            )

        except Promotion.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "message": "Pomotion id does not corresponf to any valid voucher",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
