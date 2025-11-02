import cv2
print(cv2)
print("Ruta del módulo:", getattr(cv2, "__file__", "integrado en C"))
print("Tiene __version__?", hasattr(cv2, "__version__"))
