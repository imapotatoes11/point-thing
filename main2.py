import pyglet
import random,math,time


window=pyglet.window.Window(width=800,height=600,resizable=True)
batch=pyglet.graphics.Batch()

num_points=100 # 100
speed=[i for i in range(-5,6) if i!=0]


points=[[pyglet.shapes.Circle(400+random.randint(-100,100),300+random.randint(-100,100),5,batch=batch),random.choice(speed),random.choice(speed)] for i in range(num_points)]
lines=[pyglet.shapes.Line(points[i][0].x,points[i][0].y,0,0,batch=batch) for i in range(num_points)]
lines2=[pyglet.shapes.Line(points[i][0].x,points[i][0].y,0,0,batch=batch) for i in range(num_points)]

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
        # [distance,index]
        lst=[]
        for i,jj in enumerate(points):
            lst.append([_dt(jj[0].x,jj[0].y,point[0].x,point[0].y), i])
        # get min and second min point from lst
        min_point=None
        for index,i in enumerate(lst):
            if min_point==None: min_point=i; #print(min_point)
            if i[0]<min_point[0]: min_point=i; lst.pop(index)
        second_min_point=lst[-1]
        for index,i in enumerate(lst):
            if second_min_point==None: second_min_point=i
            if i[0]<second_min_point[0]: second_min_point=i; lst.pop(index)
        #print(min_point,second_min_point)



        lines[p].x2=points[min_point[1]][0].x
        lines[p].y2=points[min_point[1]][0].y

        lines2[p].x2=points[second_min_point[1]][0].x
        lines2[p].y2=points[second_min_point[1]][0].y

    # update the lines
    for i,line in enumerate(lines):
        line.x=points[i][0].x
        line.y=points[i][0].y

    for i,line in enumerate(lines2):
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
