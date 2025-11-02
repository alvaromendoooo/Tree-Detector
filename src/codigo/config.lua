-- Configuración de vídeo
return{
    video = {
        source = 0,                -- 0 = cámara, o ruta a archivo
        fps_reducido = 8.0,        -- FPS del vídeo de salida
        imgsz = 320,               -- Tamaño de imagen para YOLO
        calidad = "media"          -- Puede ser "alta", "media", "baja"
    },

    -- Configuración de detección
    deteccion = {
        umbral_confianza = 0.5,    -- Nivel mínimo de confianza para contar detección
        alerta_umbral = 3          -- Número de árboles para disparar alerta
    },

    -- Configuración de guardado
    output = {
        carpeta = "videos/",
        formato_video = "mp4v"
    }
}