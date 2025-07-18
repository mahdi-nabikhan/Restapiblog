from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# Custom pagination class that extends DRF's PageNumberPagination
class DefaultPagination(PageNumberPagination):
    # Number of items per page
    page_size = 2

    # Override the method to customize the paginated response format
    def get_paginated_response(self, data):
        return Response({
            # Navigation links for the next and previous pages
            'links': {
                'next': self.get_next_link(),         # URL to the next page (if available)
                'previous': self.get_previous_link()  # URL to the previous page (if available)
            },
            # Total number of objects in the queryset
            'total_objects': self.page.paginator.count,
            # List of items on the current page
            'results': data,
        })
