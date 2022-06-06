from rest_framework import mixins, viewsets


class CreateRetrieveListViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet
):
    pass
