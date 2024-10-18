from rest_framework.pagination import PageNumberPagination

# Define a custom pagination class


class CustomPagination(PageNumberPagination):
    # Set the default number of items per page
    page_size = 5

    # Allow the client to set the page size using the 'page_size' query parameter
    page_size_query_param = 'page_size'

    # Set the maximum number of items per page to 10
    max_page_size = 5
