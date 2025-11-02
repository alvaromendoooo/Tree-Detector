import cv2

def statisticsConfiguration(frame, current_detections, arboles_detectados, fps):
    cv2.putText(frame, f"Arboles detectados: {current_detections}",
            (900, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"Total: {arboles_detectados}",
            (900, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"FPS: {fps:.1f}",
            (900, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, "Presiona 'q' para salir, 's' para capturar",
            (900, 640), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1)
