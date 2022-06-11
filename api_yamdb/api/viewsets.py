from rest_framework import mixins, viewsets


class CreateRetrieveListViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
):
    pass
