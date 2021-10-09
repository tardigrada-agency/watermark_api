def get_new_logo_size(_, img_size, scale):
    return int(img_size[0] * ((0.05 * scale) + 0.05))


default = {
    'color': 'white',
    'type': 'eng',
    'size': 2,
    'mode': 'right_top'
}


def margin(logo_size, img_size, scale):
    return img_size[0] * 0.02


def right(logo_size, img_size, scale):
    return int(img_size[0] - get_new_logo_size(logo_size, img_size, scale) - margin(logo_size, img_size, scale))


def left(logo_size, img_size, scale):
    return 0 + margin(logo_size, img_size, scale)


def top(logo_size, img_size, scale):
    return 0 + margin(logo_size, img_size, scale)


def bottom(logo_size, img_size, scale):
    return int(img_size[1] - int(logo_size[1] *
                                 get_new_logo_size(logo_size, img_size, scale) / logo_size[0])
               - margin(logo_size, img_size, scale))


mode_for_langs = {
    'right_bottom':
        {
            'x': right,
            'y': bottom,
            'scale': get_new_logo_size,
            'opacity': lambda _, __, ___: 0.8,
            'button_text': '⌟'
        },
    'left_bottom':
        {
            'x': left,
            'y': bottom,
            'scale': get_new_logo_size,
            'opacity': lambda _, __, ___: 0.8,
            'button_text': '⌞'
        },
    'left_top':
        {
            'x': left,
            'y': top,
            'scale': get_new_logo_size,
            'opacity': lambda _, __, ___: 0.8,
            'button_text': '⌜'
        },
    'right_top':
        {
            'x': right,
            'y': top,
            'scale': get_new_logo_size,
            'opacity': lambda _, __, ___: 0.8,
            'button_text': '⌝'
        }
}

modes = {
    'rus': {
        'mode': mode_for_langs,
        'button_text': 'Русский'
    },
    'eng': {
        'mode': mode_for_langs,
        'button_text': 'Английский'
    }
}
