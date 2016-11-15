def to_camel_case(snake_str):
    return "".join(x.title() for x in snake_str.split('_'))
