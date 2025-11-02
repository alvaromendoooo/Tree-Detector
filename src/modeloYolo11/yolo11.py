from ultralytics import YOLO
#model  = YOLO("../yolo11s.pt")
#data_path = "TreeDetector-2\data.yaml"
#model.train(data=data_path,
#            epochs=40,
#            imgsz=640,)

custom_model = YOLO("../runs/detect/train/weights/best.pt")
res = custom_model("../Detector-Árboles-1/test/images")
res[2].show()
