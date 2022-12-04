import taichi as ti

"""还没搞定太极"""
ti.init(arch=ti.cpu)
pixels = ti.Vector.field(3, float, (640, 480))
gui = ti.GUI("try", res=(640, 480))
while gui.running:
    gui.set_image(pixels)
    gui.show()
