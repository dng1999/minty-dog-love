import mdl
from display import *
from matrix import *
from draw import *
from copy import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1
    for command in commands:
        #print command
        cmd = command[0]
        args = command[1:]
        if cmd == 'push':
            stack.append(deepcopy(stack[-1]))

        elif cmd == 'pop':
            stack.pop()

        elif cmd == 'scale':
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[-1],t)
            stack[-1] = t

        elif cmd == 'move':
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[-1],t)
            stack[-1] = t

        elif cmd == 'rotate':
            theta = float(args[1]) * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(stack[-1],t)
            stack[-1] = t
            
        elif cmd == 'box':
            add_box(tmp,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(stack[-1], tmp)
            draw_polygons(tmp, screen, color)
            tmp = []

        elif cmd == 'sphere':
            add_sphere(tmp,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult(stack[-1], tmp)
            draw_polygons(tmp, screen, color)
            tmp = []

        elif cmd == 'torus':
            add_torus(tmp,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step)
            matrix_mult(stack[-1], tmp)
            draw_polygons(tmp, screen, color)
            tmp = []

        elif cmd == 'circle':
            add_circle(tmp,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult(stack[-1], tmp)
            draw_lines(tmp, screen, color)
            tmp = []

        elif cmd == 'hermite' or cmd == 'bezier':
            add_curve(tmp,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      step, cmd)                      
            matrix_mult(stack[-1], tmp)
            draw_lines(tmp, screen, color)
            tmp = []
            
        elif cmd == 'cmd':            
            add_edge( tmp,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult(stack[-1], tmp)
            draw_lines(tmp, screen, color)
            tmp = []
            
        elif cmd == 'display' or cmd == 'save':
            if cmd == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
