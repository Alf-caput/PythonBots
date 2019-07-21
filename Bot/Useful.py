def draw_debug(renderer, target):
    renderer.begin_rendering()
    renderer.draw_rect_3d(target, 10, 10, True, renderer.red())
    renderer.end_rendering()


