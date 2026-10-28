"""
collision: figures out whether a falling object is within the basket.
"""


def is_caught(basket_rect, obj):
    # Horizontal: the object's centre must be over the basket.
    within_x = basket_rect.left <= obj.x <= basket_rect.right
    # Vertical: the object's bottom edge must have reached the basket's top
    # edge, and the object must not already have fallen past the basket.
    at_basket_height = (obj.y + obj.radius >= basket_rect.top
                        and obj.y - obj.radius <= basket_rect.bottom)
    return within_x and at_basket_height
