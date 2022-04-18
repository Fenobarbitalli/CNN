import cv2 as cv
import numpy as np
import serial

#Redes entrenadas 
model_name1= 'clasifica_Pato.npy'
model_name2= 'clasifica_Flor.npy'

#Abre el archivo y define pesos y bases leidos de las redes entrenadas 
with open(model_name1,'rb') as arch:
    pesos_leidos = np.load(arch)[:,0]
    base_leida = np.load(arch)[0]
    pesos_leidos
    pesos_leidos.shape
    num_param=pesos_leidos.shape[0]
    base_leida
    n=int(np.sqrt(num_param/3))

with open(model_name2,'rb') as arch:
    pesos_leidos2 = np.load(arch)[:,0]
    base_leida2 = np.load(arch)[0]
    pesos_leidos2
    pesos_leidos2.shape
    num_param=pesos_leidos2.shape[0]
    base_leida2
    n2=int(np.sqrt(num_param/3))

# Lee las propiedades del video 
NOMBRE_VIDEO = 'Flor2.mp4'
cap = cv.VideoCapture(NOMBRE_VIDEO)
ancho_video = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))   
alto_video = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))  
num_colores = 3
fps = cap.get(cv.CAP_PROP_FPS)
num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
print('alto y ancho de cada frame', alto_video, ancho_video)
print('fps, número de frames, duración', fps, num_frames, num_frames/fps)

#Conexión con el socket 
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50000))

# Conexión serial
ser = serial.Serial(
    port='/dev/ttyS4',
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

ser.write(b'\r\na \r\n')     
img = np.zeros((512,512,3), np.uint8)
position = (30, 30)
text = "Some text including newline \n characters."
font_scale = 0.75
color = (255, 0, 0)
thickness = 3
font = cv.FONT_HERSHEY_SIMPLEX
line_type = cv.LINE_AA

text_size, _ = cv.getTextSize(text, font, font_scale, thickness)
line_height = text_size[1] + 5
x, y0 = position
rep=1

#Abre el video 
leyendo=True
while cap.isOpened():
    if leyendo==True:
        ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    #Obteniene frames para compara con la red entrenada 
    image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    image = cv.resize(frame, (n,n))

    imagen_plana = (image/255).reshape(num_param)
    
    #Obtiene el valor positivo o negativo del producto punto
    numero = np.dot(imagen_plana,pesos_leidos)+base_leida
    numero2= np.dot(imagen_plana,pesos_leidos2)+base_leida2
    
    #Envia al servidor y a la raspberry pi pico 
    print(numero, numero2)
    if numero>0:
      s.sendall(("pato").encode())
      #ser.write(("p").encode('ascii'))
    elif numero2>0:
      s.sendall(("flor").encode())
      #ser.write(("f").encode('ascii'))
    elif numero<0 and numero2<0:
      s.sendall(("otro").encode()) 
      #ser.write(("o").encode('ascii')) 


    cv.imshow('frame', frame)
    k = cv.waitKey(20)

    if k == ord('q'):
        break
    elif k== ord('p'):
        leyendo = not leyendo

cap.release()
cv.destroyAllWindows()
#################
s.close()
#################