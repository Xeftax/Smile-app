import numpy as np
import cv2
from segment_anything import sam_model_registry, SamPredictor
import mediapipe as mp
import time

sam_checkpoint = "sam_vit_b_01ec64.pth"
model_type = "vit_b"
device = "cpu"

face_mesh = mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

video_capture = cv2.VideoCapture("output.avi")
videoLenght = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
videoWriter = cv2.VideoWriter('output_seg2.avi', cv2.VideoWriter_fourcc(*'XVID'), 30.3, (w,h))
sTime = time.time()
pTime = sTime
for i in range(videoLenght):
    ret, frame = video_capture.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #facemesh
        results = face_mesh.process(frame).multi_face_landmarks[0]
        if results:
            x = [landmark.x for landmark in results.landmark]
            y = [landmark.y for landmark in results.landmark]
            w,h = frame.shape[:2]
            x,y = np.transpose([mp.solutions.drawing_utils._normalized_to_pixel_coordinates(i,j,h,w) for i,j in zip(x,y)])
            xc = int((x[291] + x[61])/2)
            yc = int((y[17] + y[0])/2)
            ry = int((y[17] - y[0])*0.5)
            rx = int((x[291] - x[61])*0.5)
            x1,y1,x2,y2 = xc-rx,yc-ry,xc+rx,yc+ry
            input_box = np.array([x1,y1,x2,y2])

            #segmentation
            sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
            sam.to(device=device)
            predictor = SamPredictor(sam)
            predictor.set_image(frame)

            masks, _, _ = predictor.predict(
            point_coords=None,
            point_labels=None,
            box=input_box,
            multimask_output=False,
            )
            h, w = masks.shape[-2:]
            color = np.array([100, 50, 0])
            mask_image = masks.reshape(h, w, 1) * color.reshape(1, 1, -1)
            mask_image = mask_image.astype(np.uint8)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            combined_mask = cv2.add(frame, mask_image)
            videoWriter.write(frame)
    nTime = time.time()
    print("frame: "+str(i+1)+"/"+str(videoLenght)+" duration:"+str(nTime-pTime))
    pTime = nTime
print("total duration: "+str(pTime-sTime))
videoWriter.release()
video_capture.release()
     