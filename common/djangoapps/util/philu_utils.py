

def extract_utm_params(input_dict):
    if not input_dict:
        return dict()

    utm_keys = [
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'utm_content',
        'utm_term'
    ]

    return {i: v for i, v in input_dict.items() if i in utm_keys}
