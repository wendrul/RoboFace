from argparse import ArgumentParser
import cv2
import numpy as np
import time
import socket
from collections import deque
from platform import system
from roboface import RoboFace
from interface import RoboSerialInterface
from gaze_tracking import GazeTracking
import json
from util import *
import winsound


from head_pose_estimation.pose_estimator import PoseEstimator
from head_pose_estimation.stabilizer import Stabilizer
from head_pose_estimation.visualization import *
from head_pose_estimation.misc import *


def get_face(detector, image, cpu=False):
    if cpu:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        try:
            box = detector(image)[0]
            x1 = box.left()
            y1 = box.top()
            x2 = box.right()
            y2 = box.bottom()
            return [x1, y1, x2, y2]
        except:
            return None
    else:
        image = cv2.resize(image, None, fx=0.5, fy=0.5)
        box = detector.detect_from_image(image)[0]
        if box is None:
            return None
        return (2*box[:4]).astype(int)


def main():
    # Some constants
    if (not(args.rig)):
        with open("interface/rig.json", "r") as outfile:
            rig = json.load(outfile)
    # Setup face detection models
    if args.cpu:  # use dlib to do face detection and facial landmark detection
        import dlib
        dlib_model_path = 'interface/head_pose_estimation/assets/shape_predictor_68_face_landmarks.dat'
        shape_predictor = dlib.shape_predictor(dlib_model_path)
        face_detector = dlib.get_frontal_face_detector()
    else:  # use better models on GPU
        import face_alignment  # the local directory in this repo
        try:
            import onnxruntime
            use_onnx = True
        except:
            use_onnx = False
        fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, use_onnx=use_onnx,
                                          flip_input=False)
        face_detector = fa.face_detector

    face = RoboFace()
    if (args.connect):
        com = RoboSerialInterface(baudrate=115200)
        face = com.ReadBounds(face)
    gaze = GazeTracking()
    os_name = system()
    if os_name in ['Windows']:  # CAP_DSHOW is required on my windows PC to get 30 FPS
        cap = cv2.VideoCapture(args.cam+cv2.CAP_DSHOW)
    else:  # linux PC is as usual
        cap = cv2.VideoCapture(args.cam)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    _, sample_frame = cap.read()

    # Introduce pose estimator to solve pose. Get one frame to setup the
    # estimator according to the image size.
    pose_estimator = PoseEstimator(img_size=sample_frame.shape[:2])

    # Introduce scalar stabilizers for pose.
    pose_stabilizers = [Stabilizer(
                        state_num=2,
                        measure_num=1,
                        cov_process=0.01,
                        cov_measure=0.1) for _ in range(8)]

    ts = []
    frame_count = 0
    no_face_count = 0
    prev_boxes = deque(maxlen=5)
    prev_marks = deque(maxlen=5)

    if (args.rig):
        HorizL = []
        VertiL = []
        RollL = []
        YawL = []
        MouthL = []
        rigState = 0
        engaged = False

    while True:
        keyPressed = cv2.waitKey(1) & 0xFF
        _, frame = cap.read()
        frame = cv2.flip(frame, 2)
        frame_count += 1
        if args.connect and frame_count > 20:  # send information to unity
            com.SendStatus(face)
        if (frame_count % 60 == 0):
            print(face.Serialize())
        t = time.time()

        # Pose estimation by 3 steps:
        # 1. detect face;
        # 2. detect landmarks;
        # 3. estimate pose

        if frame_count % 2 == 1:  # do face detection every odd frame
            facebox = get_face(face_detector, frame, args.cpu)
            if facebox is not None:
                no_face_count = 0
        elif len(prev_boxes) > 1:  # use a linear movement assumption
            if no_face_count > 1:  # don't estimate more than 1 frame
                facebox = None
            else:
                facebox = prev_boxes[-1] + \
                    np.mean(np.diff(np.array(prev_boxes), axis=0), axis=0)[0]
                facebox = facebox.astype(int)
                no_face_count += 1

        if facebox is not None:  # if face is detected
            prev_boxes.append(facebox)
            # Do facial landmark detection and iris detection.
            if args.cpu:  # do detection every frame
                facee = dlib.rectangle(left=facebox[0], top=facebox[1],
                                      right=facebox[2], bottom=facebox[3])
                marks = shape_to_np(shape_predictor(frame, facee))
            else:
                if len(prev_marks) == 0 \
                        or frame_count == 1 \
                        or frame_count % 2 == 0:  # do landmark detection on first frame
                    # or every even frame
                    face_img = frame[facebox[1]: facebox[3],
                                     facebox[0]: facebox[2]]
                    marks = fa.get_landmarks(face_img[:, :, ::-1],
                                             detected_faces=[(0, 0, facebox[2]-facebox[0], facebox[3]-facebox[1])])
                    marks = marks[-1]
                    marks[:, 0] += facebox[0]
                    marks[:, 1] += facebox[1]
                elif len(prev_marks) > 1:  # use a linear movement assumption
                    marks = prev_marks[-1] + \
                        np.mean(np.diff(np.array(prev_marks), axis=0), axis=0)
                prev_marks.append(marks)

            x_l, y_l, ll, lu = detect_iris(frame, marks, "left")
            x_r, y_r, rl, ru = detect_iris(frame, marks, "right")

            # Try pose estimation with 68 points.
            error, R, T = pose_estimator.solve_pose_by_68_points(marks)
            pose = list(R) + list(T)
            # Add iris positions to stabilize.
            pose += [(ll+rl)/2.0, (lu+ru)/2.0]

            if error > 100:  # large error means tracking fails: reinitialize pose estimator
                # at the same time, keep sending the same information (e.g. same roll)
                pose_estimator = PoseEstimator(img_size=sample_frame.shape[:2])

            else:
                # Stabilize the pose.
                steady_pose = []
                pose_np = np.array(pose).flatten()
                for value, ps_stb in zip(pose_np, pose_stabilizers):
                    ps_stb.update([value])
                    steady_pose.append(ps_stb.state[0])

            gaze.refresh(frame)
            h, v = gaze.horizontal_ratio(), gaze.vertical_ratio()

            roll = np.clip(-(180+np.degrees(steady_pose[2])), -50, 50)
            pitch = np.clip(-(np.degrees(steady_pose[1])), -40, 40)
            yaw = np.clip(-(np.degrees(steady_pose[0])), -50, 50)
            min_ear = min(eye_aspect_ratio(
                marks[36:42]), eye_aspect_ratio(marks[42:48]))
            mar = mouth_aspect_ration(marks[60:68])
            mdst = mouth_distance(marks[60:68])/(facebox[2]-facebox[0])
            roll, yaw = roll[0], yaw[0]

            if (not(args.rig)):
                marr = (mar - rig['minM']) / (rig['maxM'] - rig['minM'])
                face.mouth.SetPosFromRange(marr)
                roll, yaw = (roll - rig['minR']) / (rig['maxR'] - rig['minR']
                                                    ), (yaw - rig['minY']) / (rig['maxY'] - rig['minY'])
                face.neck.SetPosFromRange(roll, yaw)
                if (h != None and v != None):
                    h, v = (h - rig['minH']) / (rig['maxH'] - rig['minH']
                                                ), (v - rig['minV']) / (rig['maxV'] - rig['minV'])
                    face.rightEye.SetPosFromRange(h, 1 - v)
                    face.leftEye.SetPosFromRange(h, v)
            else:
                if (rigState == 0):
                    text = "Rigging eyes: after pressing 'E\n' move your eyes around naturally"
                    if (engaged):
                        if (h != None and v != None):
                            HorizL.append(h)
                            VertiL.append(v)
                elif (rigState == 1):
                    text = "Rigging neck: after pressing 'E'\n move your head around naturally"
                    if (engaged):
                        RollL.append(roll)
                        YawL.append(yaw)
                elif (rigState == 2):
                    text = "Rigging mouth: after pressing 'E'\n open and close your mouth repeatedly"
                    if (engaged):
                        MouthL.append(mar)
                elif (rigState == 3):
                    HorizL.sort()
                    VertiL.sort()
                    RollL.sort()
                    YawL.sort()
                    MouthL.sort()
                    rig = {
                        'minH': mean(HorizL[0:3]),
                        'maxH': mean(HorizL[-3:]),
                        'minV': mean(VertiL[0:3]),
                        'maxV': mean(VertiL[-3:]),
                        'minR': mean(RollL[0:3]),
                        'maxR': mean(RollL[-3:]),
                        'minY': mean(YawL[0:3]),
                        'maxY': mean(YawL[-3:]),
                        'minM': mean(MouthL[0:3]),
                        'maxM': mean(MouthL[-3:])
                    }
                    with open('interface/rig.json', 'w') as outfile:
                        json.dump(rig, outfile)
                    break
                if (engaged):
                    text = "Riggin..."
                if (not(engaged) and keyPressed == ord('e')):
                    engaged = True
                    startT = time.time()
                if (engaged and time.time() > startT + 15):
                    winsound.Beep(880, 300)
                    engaged = False
                    rigState += 1
                cv2.putText(frame, text, (90, 130),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (95, 232, 132), 1)

            if args.debug:  # draw landmarks, etc.

                # show iris.
                if x_l > 0 and y_l > 0:
                    draw_iris(frame, x_l, y_l)
                if x_r > 0 and y_r > 0:
                    draw_iris(frame, x_r, y_r)

                # show facebox.
                draw_box(frame, [facebox])
                if error < 100:
                    frame = gaze.annotated_frame()
                    # show face landmarks.
                    draw_marks(frame, marks, color=(0, 150, 150))

                    # draw stable pose annotation on frame.
                    pose_estimator.draw_annotation_box(
                        frame, np.expand_dims(steady_pose[:3], 0), np.expand_dims(
                            steady_pose[3:6], 0),
                        color=(128, 255, 128))

                    # draw head axes on frame.
                    pose_estimator.draw_axes(frame, np.expand_dims(steady_pose[:3], 0),
                                             np.expand_dims(steady_pose[3:6], 0))

        dt = time.time()-t
        ts += [dt]
        FPS = int(1/(np.mean(ts[-10:])+1e-6))

        if args.debug:
            #draw_FPS(frame, FPS)
            cv2.imshow("face", frame)
            if keyPressed == ord('q'):  # press q to exit.
                break

    # Clean up the process.
    cap.release()
    if args.connect:
        com.CloseConnection()
    if args.debug:
        cv2.destroyAllWindows()
    print('%.3f' % np.mean(ts))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--cam", type=int,
                        help="specify the camera number if you have multiple cameras",
                        default=0)
    parser.add_argument("--cpu", action="store_true",
                        help="use cpu to do face detection and facial landmark detection",
                        default=False)
    parser.add_argument("--debug", action="store_true",
                        help="show camera image to debug (need to uncomment to show results)",
                        default=False)
    parser.add_argument("--connect", action="store_true",
                        help="connect to unity character",
                        default=False)
    parser.add_argument("--rig", action="store_true",
                        help="Launch rigging assistant instead",
                        default=False)
    args = parser.parse_args()
    if (args.rig):
        args.debug = True
        args.connect = False

    main()
