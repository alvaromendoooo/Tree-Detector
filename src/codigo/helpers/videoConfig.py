import cv2

# Configuración de la camara
def videoConfiguration(cap):
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FPS, 60)

# Reducción de ruido y mejora en la imagen
def procesamientoFrames(frame):
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=10)

    return frame    