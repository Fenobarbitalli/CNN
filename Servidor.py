import socket
import threading
from tkinter import*

#Conexión socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50000))
s.listen(1)
conn, addr = s.accept()

recibido = 0
patos,flores,otros=0,0,0
continuar=True

def espera_caracter():
    global continuar,patos,flores,otros
    while continuar:
        data = conn.recv(1024).decode()
        if not data:
            continuar = False
            break
        if data=="pato":
                patos +=1
        elif data=="flor":
                flores +=1  
        elif data=="otro":
                otros +=1    
        print((data),patos,flores,otros)
print()

espera_caracter()
hilo_secundario = threading.Thread(target=espera_caracter)
hilo_secundario.start()

#Crea la tabla
class Table:
     
    def __init__(self,root):
         
        for i in range(total_rows):
            for j in range(total_columns):
                 
                self.e = Entry(root, width=20, fg='black',
                               font=('Times New Roman',12,'bold'))
                 
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])

#Toma los datos para la tabla
lst = [('Patos',patos),('Flores',flores),('Otros',otros)]
  
total_rows = len(lst)
total_columns = len(lst[0])

#Crea la raiz en window 
root = Tk()
t = Table(root)
root.mainloop()

conn.close()