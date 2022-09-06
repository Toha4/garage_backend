# coding: utf-8


class EagerLoadingMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()
        if hasattr(serializer_class, "setup_eager_loading") and callable(
                getattr(serializer_class, "setup_eager_loading")
        ):
            queryset = serializer_class.setup_eager_loading(queryset)

        return queryset