import cv2
import time
from lupa import LuaRuntime
from ultralytics import YOLO
from codigo.helpers.videoConfig import videoConfiguration, procesamientoFrames
from codigo.helpers.statisticsConfig import statisticsConfiguration
from codigo.helpers.alertDetector import alertDetector

# Cargo la configuracion de Lua
lua = LuaRuntime(unpack_returned_tuples = True)
# Lectura de la configuración de Lua
config = lua.eval('dofile("config.lua")')

# Extraccion de variables desde lua
video_source = config["video"]["source"] # Fuente de la captura del vídeo
fps_reducido = config["video"]["fps_reducido"] # Configuración estándar de fps
imgsz = config["video"]["imgsz"] # Tamanio de la imagen
umbral_confianza = config["deteccion"]["umbral_confianza"] # Nivel mínimo de confianza para contar detecciones
alerta_umbral = config["deteccion"]["alerta_umbral"] # Disparador de alerta al detectar 3 árboles
formato_video = config["output"]["formato_video"] # Configuración del códec

# Variables de detección e inicialización
tree_detections = 0
detection_history = []
frame_count = 0
fps_actual = 0
start_time_fps = time.time()
alerta = False # Controla alertas en pantalla

# Variables para configuración de codec de salida para opencv
fourcc = cv2.VideoWriter_fourcc(*formato_video)
model = YOLO("../runs/detect/train/weights/best.pt") # Carga del modelo preparado en el proyecto
save_screenshot = False

# Variables para manejo de FPS
fps = 0

# Cargamos el video de entrada
# En nuestro caso utilizamos la cámara del dispositivo
cap = cv2.VideoCapture(video_source)
videoConfiguration(cap)

# Obtención de los FPS reales de la cámara
fps_camara = cap.get(cv2.CAP_PROP_FPS);
if fps_camara <= 0:
    fps_camara = 20.0 # Valor por defecto si no se pueden obtener los frames por segundo

# Creo un VideoWriter una sola vez para no sobreescribir el frame
ret, frame = cap.read()
frame = procesamientoFrames(frame)
height, width = frame.shape[:2]
fps_reducido = 8.0
salida = cv2.VideoWriter('output.mp4', fourcc, fps_reducido, (width, height))

# Mientras que está en funcionamiento la cámara, procesamos sus frames
while cap.isOpened():
    # Leemos el frame del video
    ret, frame = cap.read()
    if not ret:
        break

    # Mejoramos la calidad del frame
    frame = procesamientoFrames(frame)
    frame_count += 1
    if frame_count % 30 == 0:
        elapsed = time.time() - start_time_fps
        fps_actual = 30 / elapsed
        start_time_fps = time.time()
        frame_count = 0

    # Realizamos la detección de objetos en el frame actual
    results = model(frame, imgsz=imgsz) # Imgsz original = 640

    current_detections = 0 # Almacenará las detecciones de cada frame
    # Conteo de árboles detectados
    for detection in results[0].boxes:
        if detection.conf > umbral_confianza:
            current_detections += 1  
    tree_detections += current_detections
    detection_history.append(tree_detections)
    print("Detection history items: ", detection_history)    

    # Extraemos los resultados
    annotated_frame = results[0].plot()

    # Mostrar estadísticas recogidas
    statisticsConfiguration(annotated_frame, current_detections, tree_detections, fps_actual)
    
    # Visualización de los resultados
    cv2.imshow('Deteccion de Árboles', annotated_frame)

    # Control de alertas
    alerta = alertDetector(current_detections, alerta_umbral)
    if alerta:
        cv2.putText(annotated_frame, "ALERTA: Multiples arboles detectados!",
                    (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    # Guardamos el vídeo
    salida.write(annotated_frame)

    # Capturas de pantalla
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        cv2.imwrite(f"screenshot_{frame_count}.jpg", annotated_frame)
        print("Captura guardada")
    elif key == ord('q'): # Salimos del bucle si se presiona la tecla 'q'
        break
    elif key == ord('r'):
        print("Recargando configuración desde Lua...")
        config = lua.eval('dofile("config.lua")')
        umbral_confianza = config["deteccion"]["umbral_confianza"]
        alerta_umbral = config["deteccion"]["alerta_umbral"]
        fps_reducido = config["video"]["fps_reducido"]
        print("Configuración actualizada.")

cap.release() # Liberación de recursos de captura de vídeo
salida.release() # Liberación de escritura en vídeo
cv2.destroyAllWindows()    
detection_history.clear() # RESET del diccionario que almacena objetos detectados