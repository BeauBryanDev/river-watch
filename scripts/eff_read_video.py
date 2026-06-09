import os
import cv2
import torch
import onnxruntime as ort
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

app = FastAPI()


IS_PROD = os.getenv("ENVIRONMENT") == "production"
if not IS_PROD:
    torch.set_num_threads(2)
    os.environ["OMP_NUM_THREADS"] = "2"
    os.environ["MKL_NUM_THREADS"] = "2"



onnx_options = ort.SessionOptions()
if not IS_PROD:
    onnx_options.intra_op_num_threads = 2
    onnx_options.inter_op_num_threads = 2



def procesar_video_eficiente(path_video: str):
    """Generador que lee el video cuadro por cuadro de forma ligera."""
    cap = cv2.VideoCapture(path_video)
    
    if not cap.isOpened():
        print("Error: No se pudo abrir el video.")
        return

    frame_idx = 0
    
    # TRUCO 2: Saltarse cuadros en desarrollo para no forzar la CPU
    # En tu laptop procesamos 1 de cada 5 cuadros. En AWS procesamos todos (1).
    SKIP_FRAMES = 5 if not IS_PROD else 1

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break  # Fin del video

            # Saltamos el cuadro si no corresponde al índice configurado
            if frame_idx % SKIP_FRAMES != 0:
                frame_idx += 1
                continue

            # TRUCO 3: Redimensionar el cuadro si es muy grande (ej. 4K o 1080p)
            # Procesar a 640x360 es súper rápido y suficiente para ver anomalías
            if not IS_PROD:
                frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)

            # -------------------------------------------------------
            #  AQUÍ EJECUTAS TUS MODELOS DE INTELIGENCIA ARTIFICIAL
            # 1. Pasar 'frame' a tu SegFormer (ONNX) para detectar agua.
            # 2. Pasar 'frame' actual y anterior a RAFT para velocidad (px/s).
            # -------------------------------------------------------

            # TRUCO 4: Convertir el resultado a JPEG para enviarlo a la web
            # Bajamos la calidad a 70% en desarrollo para ahorrar ancho de banda y CPU
            calidad = 70 if not IS_PROD else 90
            ret_encode, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), calidad])
            
            if not ret_encode:
                continue
                
            # Convertimos el búfer en bytes para transmitirlo
            frame_bytes = buffer.tobytes()
            
            # Formato estándar de Multipart para streaming de video en webs
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            frame_idx += 1
            
    finally:
        # TRUCO 5: Liberar siempre la memoria del lector de video
        cap.release()



