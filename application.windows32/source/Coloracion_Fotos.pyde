import copy as cp


img = loadImage("Godel.jpg")
grises = 9
pob=5
Aptitudes=[0]*pob
aptitud_ant=0
aptitud_ant2=0
cont=0
gen=0
escala=4
pob_vacia=True
def setup():
    global img, grayEsc, original, error, mejores, cromosomas, pob, pob_vacia
    img = loadImage("Godel.jpg")
    img.loadPixels()
    size(800,500)
    loadPixels()
    original=[[255 for row in range(img.height)] for col in range(img.width)]
    grayEsc=[[255 for row in range(img.height)] for col in range(img.width)]
    #print(len(grayEsc))
    error=[[[[0,0,0]for row in range(img.height)] for col in range(img.width)],[[[0,0,0]for row in range(img.height)] for col in range(img.width)]]
    mejores=[[[[0,0,0]for row in range(img.height)] for col in range(img.width)],[[[0,0,0]for row in range(img.height)] for col in range(img.width)]]
    cromosomas=[[[[0,0,0]for row in range(img.height)] for col in range(img.width)]for crom in range(pob)]
    print(cromosomas)


def draw():
    global grayEsc, original, cont, gen, grises, pob, Aptitudes, aptitud_ant, aptitud_ant2, cromosomas, error, mejores, escala, pob_vacia
    background(255)
    if millis()<10000:
        img_or=createImage(img.width,img.height,RGB)
        img_or.loadPixels()
        for x in range(img.width):
            for y in range(img.height):
                loc = x+y*img.width
                original[x][y]=[img.pixels[loc] >> 16 & 0xFF, img.pixels[loc] >> 8 & 0xFF, img.pixels[loc] >> 0 & 0xFF]
                img_or.pixels[loc]=color(original[x][y][0],original[x][y][1],original[x][y][2])
        img_or.updatePixels()
        image(img_or, 0, 0, img.width*escala,img.height*escala)
        fill(0)
        textAlign(CENTER)
        textSize(50)
        text("Imagen",width*3/4, height/2-30)
        text("Original",width*3/4, height/2+30)
        #print(millis());
        
    elif millis()>10000 and millis()<15000:
        img_ge=createImage(img.width,img.height, RGB);
        img_ge.loadPixels()
        for x in range(img.width):
            for y in range(img.height):
                loc = x+y*img.width
                grayEsc[x][y]=255*round(((img.pixels[loc] >> 16 & 0xFF)+(img.pixels[loc] >> 8 & 0xFF)+(img.pixels[loc] >> 0 & 0xFF))*(grises-1)/(3*255))/(grises-1)
                img_ge.pixels[loc]=color(grayEsc[x][y])
        img_ge.updatePixels()
        image(img_ge,0,0,img.width*escala,img.height*escala)
        fill(0)
        textAlign(CENTER)
        textSize(50)
        text("Escala de",width*3/4, height/2-30)
        text("Grises",width*3/4, height/2+30)
        #print("Itera")
        if pob_vacia:
            for k in range(pob):
                #print("cromosoma: ",k)
                for x in range(img.width):
                    for y in range(img.height):
                        rgb_color=[floor(random(0,256)),floor(random(0,256)),floor(random(0,256))]
                        #print(grayEsc[x][y],x,y)
                        desviacion=grayEsc[x][y]-sum(rgb_color)/3
                        rgb_color=[rgb_color[0]+desviacion,rgb_color[1]+desviacion,rgb_color[2]+desviacion]
                        cromosomas[k][x][y]=cp.copy(rgb_color)
            #print(cromosomas[0][50][20],cromosomas[1][50][20],cromosomas[2][50][20],cromosomas[3][50][20],cromosomas[4][50][20])
            pob_vacia=False
    else:
        gen+=1
        ################Aptitud y Seleccion##########################
        for k in range(pob):
            aptitud=len(img.pixels)
            errores=[[[0,0,0] for row in range(img.height)] for col in range(img.width)]
            for x in range(img.width):
                for y in range(img.height):
                    falla=0
                    for i in range(3):
                        errores[x][y][i]=original[x][y][i]-cromosomas[k][x][y][i]
                        falla+=abs(errores[x][y][i])/256
                    # errores[x][y]=abs(hue(color(cromosomas[k][x][y][0],cromosomas[k][x][y][1],cromosomas[k][x][y][2]))-hue(color(original[x][y][0],original[x][y][1],original[x][y][2])))
                    # if errores[x][y]>127:
                    #     errores[x][y]=256-errores[x][y]
                    # errores[x][y]*=8
                    # errores[x][y]+=abs(saturation(color(cromosomas[k][x][y][0],cromosomas[k][x][y][1],cromosomas[k][x][y][2]))-saturation(color(original[x][y][0],original[x][y][1],original[x][y][2])))
                    # errores[x][y]+=abs(brightness(color(cromosomas[k][x][y][0],cromosomas[k][x][y][1],cromosomas[k][x][y][2]))-brightness(color(original[x][y][0],original[x][y][1],original[x][y][2])))
                    #errores[x][y]/=256
                    
                    #penalizacion=error;                             #Penalizacion Lineal
                    penalizacion=pow(falla/3,1/2.0);                #Penalizacion Fuerte
                    #penalizacion=pow(abs(errores[t]),2.0);          #Penalizacion Debil
                    #penalizacion=0.5*(pow(2*error-1,1/3.0)+1);      #Penalizacion Sesgada
                    aptitud-=penalizacion
            if aptitud>aptitud_ant:
                mejores[1]=cp.copy(mejores[0])
                mejores[0]=cp.copy(cromosomas[k])
                aptitud_ant2=cp.copy(aptitud_ant)
                aptitud_ant=cp.copy(aptitud)
                error[1]=cp.copy(error[0])
                error[0]=cp.copy(errores)
            elif aptitud>aptitud_ant2:
                mejores[1]=cp.copy(cromosomas[k])
                aptitud_ant2=cp.copy(aptitud)
                error[1]=cp.copy(errores)
            Aptitudes[k]=cp.copy(aptitud)
        
        
        #######################Mutacion#################################
        cromosomas_mutados=[[[[0,0,0]for row in range(img.height)] for col in range(img.width)]for crom in range(pob)]
        for k in range(pob):
            sel=floor(random(2))
            for x in range(img.width):
                for y in range(img.height):
                    cromosomas_mutados[k][x][y]=cp.copy(mejores[sel][x][y])
                    for i in range(3):
                        mutar=random(1)
                        if mutar<abs(error[sel][x][y][i]/256):
                            rgb_color=floor(random(min(0,error[sel][x][y][i]*3),max(0,error[sel][x][y][i]*3)))
                            #rgb_color=floor(random(0,256))
                            cromosomas_mutados[k][x][y][i]=cromosomas_mutados[k][x][y][i]+rgb_color
                    desviacion=grayEsc[x][y]-sum(cromosomas_mutados[k][x][y])/3
                    color_correjido=[cromosomas_mutados[k][x][y][0]+desviacion,cromosomas_mutados[k][x][y][1]+desviacion,cromosomas_mutados[k][x][y][2]+desviacion]
                    cromosomas_mutados[k][x][y]=cp.copy(color_correjido)
        cromosomas=cromosomas_mutados
        
        
        #####################Graficar##################################
        img_cro=createImage(img.width,img.height, RGB)
        img_cro.loadPixels()
        for x in range(img.width):
            for y in range(img.height):
                loc = x+y*img.width
                img_cro.pixels[loc]=color(mejores[0][x][y][0], mejores[0][x][y][1],mejores[0][x][y][2])
        img_cro.updatePixels()
        image(img_cro,0,0,img.width*escala,img.height*escala)
        fill(0)
        textAlign(CENTER)
        textSize(40)
        text("Mejores Replicas",width*3/4, height/2-60)
        textAlign(RIGHT)
        textSize(20)
        text("Generacion: ",width*3/4, height/2)
        textAlign(LEFT)
        text(gen,width*3/4, height/2)
        textAlign(RIGHT)
        text("Mejor Aptitud: ",width*3/4, height/2+30)
        textAlign(LEFT)
        text(max(Aptitudes),width*3/4, height/2+30)
        textAlign(RIGHT)
        text("Aptitud Perfecta: ",width*3/4, height/2+60)
        textAlign(LEFT)
        text(len(img.pixels),width*3/4, height/2+60)
        
        #print("Gen")
    cont+=1
