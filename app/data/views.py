from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .function import (get_global_data_per_month,
                       total_revenue,
                       number_of_clients,
                       products_sold,
                       make_query_product
                       )


class DataPerMonthView(APIView):
    """
    View to return stats about the sales over the year
    """

    # authentication_classes = (JWTAuthentication,)
    # permission_classes = [IsAuthenticatedAndReadOnlyPermission]

    def get(self, request):
        answer = get_global_data_per_month()

        return Response(
            answer, status=HTTP_200_OK
        )


class GetDataPerProduct(APIView):
    """
    get sales data by products
    """

    # authentication_classes = (JWTAuthentication,)
    # permission_classes = [IsAuthenticatedAndReadOnlyPermission]

    def get(self, request):
        answer = make_query_product()

        return Response(
            answer,
            status=HTTP_200_OK
        )


class GetdescriptiveData(APIView):
    """
    get the total number of clients
    """

    # authentication_classes = (JWTAuthentication,)
    # permission_classes = [IsAuthenticatedAndReadOnlyPermission]
    def get(self, request):
        revenue = total_revenue()
        clients = number_of_clients()
        products = products_sold()
        answer = [
            revenue[0],
            clients[0],
            products[0],
        ]
        return Response(
            answer,
            status=HTTP_200_OK
        )
