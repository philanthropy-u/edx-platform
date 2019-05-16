def serialize(queryset, request, serializer_cls, serializer_ctx):
    """
    Serialize and paginate objects in a queryset.

    Arguments:
        serializer_cls (serializers.Serializer class): Django Rest Framework Serializer subclass.
        serializer_ctx (dict): Context dictionary to pass to the serializer

    Returns: dict

    """
    # Serialize
    serializer_ctx["request"] = request

    serializer = serializer_cls(queryset, context=serializer_ctx, many=True)
    return serializer.data
