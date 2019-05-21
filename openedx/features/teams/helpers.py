from random import choice

USER_ICON_COLORS = [
    '#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5',
    '#2196f3', '#009688', '#1b5e20', '#33691e', '#827717',
    '#e65100', '#ff5722', '#795548', '#607d8b'
]

TEAM_BANNER_COLORS = [
    '#AB4642', '#DC9656', '#F7CA88', '#A1B56C', '#86C1B9',
    '#7CAFC2', '#BA8BAF', '#A16946'
]


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


def generate_random_user_icon_color():
    return choice(USER_ICON_COLORS)


def generate_random_team_banner_color():
    return choice(TEAM_BANNER_COLORS)
