def get_new_logo_size(_, img_size, scale):
    return int(img_size[0] * ((0.025 * scale)+0.01))


default = {
    'color': 'white',
    'type': 'eng',
    'size': 2,
    'mode': 'right_top'
}

modes = {
    'right_bottom':
        {
            'x': lambda logo_size, img_size, scale:
            int(img_size[0] - get_new_logo_size(logo_size, img_size, scale) - get_new_logo_size(None, img_size, scale)),
            'y': lambda logo_size, img_size, scale:
            int(img_size[1] - int(logo_size[1] *
                                  get_new_logo_size(logo_size, img_size, scale) / logo_size[0])),
            'scale': get_new_logo_size,
            'opacity': lambda _, __, ___: 0.8,
            'button_text': '⌟'
        },
    'left_bottom':
        {
            'x': lambda logo_size, img_size, scale: get_new_logo_size(None, img_size, scale),
            'y': lambda logo_size, img_size, scale:
            int(img_size[1] - int(logo_size[1] *
                                  get_new_logo_size(logo_size, img_size, scale) / logo_size[0])),
            'scale': get_new_logo_size,
            'opacity': lambda _, __, ___: 0.8,
            'button_text': '⌞'
        },
    'left_top':
        {
            'x': lambda logo_size, img_size, scale: get_new_logo_size(None, img_size, scale),
            'y': lambda logo_size, img_size, scale: 0,
            'scale': get_new_logo_size,
            'opacity': lambda _, __, ___: 0.8,
            'button_text': '⌜'
        },
    'right_top':
        {
            'x': lambda logo_size, img_size, scale:
            int(img_size[0] - get_new_logo_size(logo_size, img_size, scale) - get_new_logo_size(None, img_size, scale)),
            'y': lambda logo_size, img_size, scale: 0,
            'scale': get_new_logo_size,
            'opacity': lambda _, __, ___: 0.8,
            'button_text': '⌝'
        }
}
