from drf_yasg.inspectors import BaseInspector


class CustomPagination(BaseInspector):
    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'results': schema,
            },
        }
