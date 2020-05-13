# The render process for the cli does NOT use the rend project for a couple
# of reasons
# 1. Config needs to be very early in the startup, therefore it cannot use
#    asyncio, all rend funcs use asyncio
# 2. Config will nto allow for template wrapping as the render is just a
#    single command line render


def process(hub, renderer, value):
    """
    Take a renderer adn a value, process it, and return the processed value
    """
    return getattr(hub, f"config.render.{renderer}.render")(value)
