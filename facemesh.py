import mediapipe as mp
import cv2

def faceMeshProcess(frameArray):
    face_mesh = mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)
    videoLenght = len(frameArray)
    faceLandmarks = [None]*(videoLenght+1)
    for i,frame in enumerate(frameArray):
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame).multi_face_landmarks
            faceLandmarks[i] = results[0] if results else None
    return faceLandmarks