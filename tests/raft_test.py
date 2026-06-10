from pathlib import Path

import cv2
import torch
import numpy as np
import torchvision.transforms.functional as F
from torchvision.models.optical_flow import raft_small
from torchvision.utils import flow_to_image

HERE = Path(__file__).resolve().parent
VIDEO_PATH = str(HERE / "river_test_video.mp4")
OUTPUT_PATH = str(HERE / "raft_output.mp4")
DEVICE = "cpu"

def load_frame(frame_bgr):
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    tensor = F.to_tensor(frame_rgb)
    tensor = tensor.unsqueeze(0)
    return tensor

def main():
    model = raft_small(weights="DEFAULT")
    model = model.to(DEVICE)
    model.eval()
    print("RAFT-Small cargado.")

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"No se pudo abrir el video: {VIDEO_PATH}")
        return
    fps = cap.get(cv2.CAP_PROP_FPS)
    w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out    = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (w * 2, h))

    ret, prev_bgr = cap.read()
    if not ret:
        print("No se pudo leer el video.")
        return

    frame_idx = 0

    while True:
        ret, curr_bgr = cap.read()
        if not ret:
            break

        img1 = load_frame(prev_bgr).to(DEVICE)
        img2 = load_frame(curr_bgr).to(DEVICE)

        with torch.no_grad():
            flow_list = model(img1, img2)

        flow = flow_list[-1]

        # convertir flow a imagen RGB para visualizacion
        flow_img = flow_to_image(flow[0])
        flow_np  = flow_img.permute(1, 2, 0).cpu().numpy()
        flow_bgr = cv2.cvtColor(flow_np, cv2.COLOR_RGB2BGR)

        # lado izquierdo: frame original | lado derecho: optical flow
        combined = np.hstack([curr_bgr, flow_bgr])
        out.write(combined)

        prev_bgr  = curr_bgr
        frame_idx += 1

        if frame_idx % 30 == 0:
            print(f"  frames procesados: {frame_idx}")

    cap.release()
    out.release()
    print(f"Listo. Output: {OUTPUT_PATH}")
    print(f"Total frames procesados: {frame_idx}")

if __name__ == "__main__":
    main()
