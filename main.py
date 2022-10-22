import pyglet
import random,math,time


window=pyglet.window.Window(width=800,height=600,resizable=True)
batch=pyglet.graphics.Batch()

num_points=100 # 100
speed=[i for i in range(-5,6) if i!=0]


points=[[pyglet.shapes.Circle(400+random.randint(-100,100),300+random.randint(-100,100),5,batch=batch),random.choice(speed),random.choice(speed)] for i in range(num_points)]
lines=[pyglet.shapes.Line(points[i][0].x,points[i][0].y,0,0,batch=batch) for i in range(num_points)]

_dt=lambda x,y,x1,y1: round(math.sqrt( (x-x1)**2 + (y-y1)**2 ))

last_tick=time.time()
def update(dt):
    global last_tick
    for p in points:
        if p[0].x<1: p[1]=random.choice([i for i in speed if i>0])
        if p[0].x>window.width-1: p[1]=random.choice([i for i in speed if i<0])
        if p[0].y<1: p[2]=random.choice([i for i in speed if i>0])
        if p[0].y>window.height-1: p[2]=random.choice([i for i in speed if i<0])

    for p in points:
        p[0].x+=p[1]
        p[0].y+=p[2]


    # Get the closest point
    for p,point in enumerate(points):
        closest_point=0
        for j,k in enumerate(points):
            if point[0].x==k[0].x and point[0].y==k[0].y: continue
            if j==len(points)-1: break
            _d=_dt(point[0].x,point[0].y,k[0].x,k[0].y)
            if _d < _dt(points[closest_point][0].x, points[closest_point][0].y, point[0].x,point[0].y):
                closest_point = j
        lines[p].x2=points[closest_point][0].x
        lines[p].y2=points[closest_point][0].y

    # update the lines
    for i,line in enumerate(lines):
        line.x=points[i][0].x
        line.y=points[i][0].y

    # calculate time between ticks and fps
    current_tick = time.time()
    print(
        f'time between ticks: {round(current_tick - last_tick, 2)} seconds with {round(1 / round(current_tick - last_tick, 3))} fps',
        end="\r")
    last_tick = current_tick


@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.clock.schedule_interval(update,1/30) #use this to adjust speed (fine tune)
pyglet.app.run()
