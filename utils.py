import mediapipe as mp
import cv2
import observer

def faceMeshProcess(frameArray):
    face_mesh = mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)
    nbLandmarks = max([num for tup in mp.solutions.face_mesh_connections.FACEMESH_TESSELATION for num in tup])
    videoLenght = len(frameArray)
    faceLandmarks = [[[None,None,None]]*nbLandmarks]*(videoLenght)
    for i,frame in enumerate(frameArray):
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame).multi_face_landmarks
            if results:
                faceLandmarks[i] = [[l.x,l.y,l.z] for l in results[0].landmark]
    return faceLandmarks

def dataListToStr(landmarks,intervals):
    data = '\t'.join([str(interval) for interval in intervals])+"\n___\n"
    data += '\n___\n'.join(['\n'.join('\t'.join([str(l) for l in landmark]) for landmark in frame_landmark) for frame_landmark in landmarks])
    return data

def strToDataList(data):
    landmarks = []
    intervals = []
    parts = data.split('\n___\n')
    intervals = [float(interval) for interval in parts[0].split('\t')]
    landmarks = [[[float(l) for l in landmark.split('\t')] for landmark in part.split('\n')] for part in parts[1:]]
    return landmarks, intervals