"""Vision X engine with object-oriented camera lifecycle and module handlers.""" 
 
 
 
from __future__ import annotations 
 
 
 
import math 
 
 
 
 
import threading 
 
 
 
import time 
 
 
 
from pathlib import Path 
 
 
 
 
 
 
 
import cv2 
 
 
 
import numpy as np 
 
 
 
import streamlit as st 
 
from streamlit_webrtc import VideoProcessorBase
 
 
 
 
 
BASE_DIR = Path(__file__).resolve().parent 
 
 
 
SCREENSHOT_DIR = BASE_DIR / "screenshots" 
 
 
 
SCREENSHOT_DIR.mkdir(exist_ok=True) 
 
 
 
 
 
 
 
MODULE_INFO = [ 
 
 
 
    ("✋", "Hand Gesture Recognition", "Track hand landmarks and classify basic gestures."), 
 
 
 
    ("🖱️", "Virtual Mouse", "Move and click the cursor using hand landmarks."), 
 
 
 
    ("🤟", "Sign Language Recognition", "Experimental landmark-based signs (limited alphabet)."), 
 
 
 
    ("🏋️", "Fitness / Form Checker", "Pose landmarks and basic squat/repetition feedback."), 
 
 
 
    ("🚗", "Driver Drowsiness Detection", "Eye-closure alert plus spoken prolonged-sleep warning."), 
 
 
 
    ("📦", "Object Detection", "YOLO object detection when the optional model package is installed."), 
 
 
 
    ("📸", "Screenshot Capture", "Save a frame from the live camera by pressing S."), 
 
 
 
] 
 
 
 
MODULES = { 
 
 
 
    "Hand Gesture Recognition": "hands", 
 
 
 
    "Virtual Mouse": "hands", 
 
 
 
    "Sign Language Recognition": "hands", 
 
 
 
    "Fitness / Form Checker": "pose", 
 
 
 
    "Driver Drowsiness Detection": "driver", 
 
 
 
    "Object Detection": "yolo", 
 
 
 
    "Screenshot Capture": "screenshot", 
 
 
 
} 
 
 
 
 
 
 
 
def _xy(lm, w, h): 
 
 
 
    return int(lm.x * w), int(lm.y * h) 
 
 
 
 
 
 
 
def classify_gesture(hand): 
 
 
 
    lm = hand.landmark 
 
 
 
    index = lm[8].y < lm[6].y 
 
 
 
    middle = lm[12].y < lm[10].y 
 
 
 
    ring = lm[16].y < lm[14].y 
 
 
 
    pinky = lm[20].y < lm[18].y 
 
 
 
    thumb = abs(lm[4].x - lm[3].x) > 0.045 
 
 
 
    up = [thumb, index, middle, ring, pinky] 
 
 
 
    if all(up): return "Open Palm" 
 
 
 
    if not any(up[1:]) and not thumb: return "Fist" 
 
 
 
    if index and not middle and not ring and not pinky: return "Pointing" 
 
 
 
    if index and middle and not ring and not pinky: return "Two Fingers" 
 
 
 
    return "Unknown" 
 
 
 
 
 
 
 
def _hud(frame, title, lines, color=(80, 220, 255)): 
 
 
 
    h, w = frame.shape[:2] 
 
 
 
    bottom = min(h-10, 48 + 25*len(lines)) 
 
 
 
    cv2.rectangle(frame, (12, 12), (min(w-12, 410), bottom), (7, 15, 32), -1) 
 
 
 
    cv2.rectangle(frame, (12, 12), (min(w-12, 410), bottom), color, 1) 
 
 
 
    cv2.putText(frame, title[:35], (24, 37), cv2.FONT_HERSHEY_SIMPLEX, .62, color, 2, cv2.LINE_AA) 
 
 
 
    for i, line in enumerate(lines): 
 
 
 
        yy = 62 + i*23 
 
 
 
        if yy < bottom: 
 
 
 
            cv2.putText(frame, str(line)[:48], (24, yy), cv2.FONT_HERSHEY_SIMPLEX, .5, (235,242,255), 1, cv2.LINE_AA) 
 
 
 
 
 
 
 
class DrowsinessAlarm:
    """Start beep and spoken warning after eyes stay closed for 2 seconds."""

    def __init__(self, spoken_delay=2.0, repeat_voice_seconds=3.0):
        self.spoken_delay = spoken_delay
        self.repeat_voice_seconds = repeat_voice_seconds
        self.closed_since = None
        self._stop_event = threading.Event()
        self._thread = None
        self._voice_thread = None
        self._last_voice_at = 0.0
        self._lock = threading.Lock()

    def _beep_loop(self):
        # This thread starts only after the 2-second eye-closure threshold.
        try:
            import winsound
            while not self._stop_event.is_set():
                try:
                    winsound.Beep(2400, 250)
                except RuntimeError:
                    winsound.MessageBeep(winsound.MB_ICONHAND)
                if self._stop_event.wait(0.10):
                    break
        except Exception:
            # Terminal bell fallback; browser/cloud audio is not guaranteed.
            while not self._stop_event.is_set():
                print("\a", end="", flush=True)
                if self._stop_event.wait(0.4):
                    break

    def _speak_warning(self):
        try:
            import pyttsx3
            speech = pyttsx3.init()
            speech.setProperty("rate", 155)
            speech.setProperty("volume", 1.0)
            speech.say("Warning! Driver sleeping. Please open your eyes and wake up.")
            speech.runAndWait()
            speech.stop()
        except Exception as exc:
            print(f"Voice warning unavailable: {exc}")

    def update(self, eyes_closed: bool):
        now = time.monotonic()
        if eyes_closed:
            if self.closed_since is None:
                self.closed_since = now
                self._stop_event.clear()
                self._last_voice_at = 0.0
                self._thread = None

            elapsed = now - self.closed_since
            # Start beep and voice only after continuous closure for 2 seconds.
            if elapsed >= self.spoken_delay:
                if self._thread is None or not self._thread.is_alive():
                    self._stop_event.clear()
                    self._thread = threading.Thread(target=self._beep_loop, daemon=True)
                    self._thread.start()

                if now - self._last_voice_at >= self.repeat_voice_seconds:
                    self._last_voice_at = now
                    self._voice_thread = threading.Thread(target=self._speak_warning, daemon=True)
                    self._voice_thread.start()

            return elapsed >= self.spoken_delay, elapsed

        # Eyes reopened or face disappeared: stop alarm and reset the timer.
        self.closed_since = None
        self._stop_event.set()
        self._thread = None
        return False, 0.0

    def close(self):
        self._stop_event.set()


class VisionEngine: 
 
 
 
    """Owns webcam, MediaPipe processors, frame handling and cleanup.""" 
 
 
 
    def __init__(self, module, camera_index=0, mirror=True, show_fps=True, image_slot=None, status_slot=None): 
 
 
 
        self.module = module 
 
 
 
        self.camera_index = camera_index 
 
 
 
        self.mirror = mirror 
 
 
 
        self.show_fps = show_fps 
 
 
 
        self.image_slot = image_slot 
 
 
 
        self.status_slot = status_slot 
 
 
 
        self.alarm = DrowsinessAlarm() 
 
 
 
        self._last_click = 0.0 
 
 
 
        self._pinch_was_down = False 
 
 
 
        self._pyautogui = None 
 
 
 
 
 
 
 
    def _hands_frame(self, frame, hands, mp_hands, draw): 
 
 
 
        h, w = frame.shape[:2] 
 
 
 
        result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) 
 
 
 
        lines = [f"Hands: {len(result.multi_hand_landmarks or [])}"] 
 
 
 
        if result.multi_hand_landmarks: 
 
 
 
            for hand in result.multi_hand_landmarks: 
 
 
 
                draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS) 
 
 
 
                lm = hand.landmark 
 
 
 
                x, y = _xy(lm[8], w, h) 
 
 
 
                cv2.circle(frame, (x,y), 8, (0,255,120), -1) 
 
 
 
                gesture = classify_gesture(hand) 
 
 
 
                cv2.putText(frame, gesture, (max(8,x-50), max(25,y-20)), cv2.FONT_HERSHEY_SIMPLEX, .62, (0,255,120), 2) 
 
 
 
                lines.append(f"Gesture: {gesture}") 
 
 
 
                if self.module == "Virtual Mouse" and self._pyautogui: 
 
                    # Cursor follows index fingertip. Frame is mirrored in run(). 
 
                    sw, sh = self._pyautogui.size() 
 
                    sx = int(np.interp(lm[8].x, [0.03, 0.97], [0, sw - 1])) 
 
                    sy = int(np.interp(lm[8].y, [0.03, 0.97], [0, sh - 1])) 
 
                    sx = max(1, min(sw - 2, sx)) 
 
                    sy = max(1, min(sh - 2, sy)) 
 
 
 
                    if not hasattr(self, "_mouse_x"): 
 
                        self._mouse_x, self._mouse_y = sx, sy 
 
                    # Smoothing: responsive but less jittery. 
 
                    smooth = 0.55 
 
                    self._mouse_x = int(self._mouse_x + (sx - self._mouse_x) * smooth) 
 
                    self._mouse_y = int(self._mouse_y + (sy - self._mouse_y) * smooth) 
 
                    try: 
 
                        self._pyautogui.moveTo(self._mouse_x, self._mouse_y, duration=0) 
 
                    except Exception as exc: 
 
                        lines.append(f"Move error: {str(exc)[:45]}") 
 
 
 
                    # Pinch detection based on palm size, with separate press/release thresholds. 
 
                    # Landmarks: thumb tip=4, index tip=8, wrist=0, middle MCP=9. 
 
                    palm_scale = max(math.hypot(lm[9].x - lm[0].x, lm[9].y - lm[0].y), 0.001) 
 
                    pinch_distance = math.hypot(lm[4].x - lm[8].x, lm[4].y - lm[8].y) 
 
                    press_threshold = max(0.025, palm_scale * 0.32) 
 
                    release_threshold = press_threshold * 1.65 
 
                    was_pinched = self._pinch_was_down 
 
 
 
                    if was_pinched: 
 
                        pinch = pinch_distance < release_threshold 
 
                    else: 
 
                        pinch = pinch_distance < press_threshold 
 
 
 
                    # Require two consecutive frames to avoid accidental clicks from jitter. 
 
                    self._pinch_frames = self._pinch_frames + 1 if pinch else 0 
 
                    now = time.monotonic() 
 
                    thumb_x, thumb_y = _xy(lm[4], w, h) 
 
                    index_x, index_y = _xy(lm[8], w, h) 
 
                    cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), 
 
                             (0, 255, 0) if pinch else (0, 190, 255), 2) 
 
                    cv2.putText(frame, "PINCH DETECTED" if pinch else "PINCH: READY", 
 
                                (18, h - 48), cv2.FONT_HERSHEY_SIMPLEX, 0.62, 
 
                                (0, 255, 0) if pinch else (0, 220, 255), 2, cv2.LINE_AA) 
 
                    lines.append(f"Pinch: {pinch_distance:.3f} | press<{press_threshold:.3f}") 
 
 
 
                    if pinch and self._pinch_frames == 2 and now - self._last_click >= 0.45: 
 
                        try: 
 
                            # Explicit down/up is more reliable across Windows apps than a 
 
                            # one-shot click in some environments. 
 
                            self._pyautogui.moveTo(self._mouse_x, self._mouse_y, duration=0) 
 
                            self._pyautogui.mouseDown(button="left") 
 
                            time.sleep(0.04) 
 
                            self._pyautogui.mouseUp(button="left") 
 
                            self._last_click = now 
 
                            lines.append("ACTION: LEFT CLICK EXECUTED") 
 
                            cv2.putText(frame, "LEFT CLICK!", (18, h - 78), 
 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2, cv2.LINE_AA) 
 
                        except Exception as exc: 
 
                            lines.append(f"CLICK ERROR: {str(exc)[:48]}") 
 
 
 
                    self._pinch_was_down = pinch 
 
                    lines.append("Mouse ACTIVE | pinch thumb + index, then release") 
 
 
 
                # Coordinate labels similar to the supplied visual reference. 
 
 
 
                cv2.putText(frame, f"x:{x} y:{y}", (min(w-130,x+10), max(22,y-10)), cv2.FONT_HERSHEY_SIMPLEX, .48, (245,245,255), 1) 
 
 
 
        else: 
 
            self._pinch_was_down = False 
 
            self._pinch_frames = 0 
 
 
 
        _hud(frame, self.module.upper(), lines) 
 
 
 
        return frame 
 
 
 
 
 
 
 
    @staticmethod 
 
 
 
    def _eye_ratio(face, w, h, ids): 
 
 
 
        pts = face.landmark 
 
 
 
        p = [np.array([pts[i].x*w, pts[i].y*h], dtype=float) for i in ids] 
 
 
 
        vertical = np.linalg.norm(p[1]-p[5]) + np.linalg.norm(p[2]-p[4]) 
 
 
 
        horizontal = 2*np.linalg.norm(p[0]-p[3]) 
 
 
 
        return float(vertical / horizontal) if horizontal else 0.0 
 
 
 
 
 
 
 
    def _driver_frame(self, frame, face_mesh, mp_face, draw): 
 
 
 
        h, w = frame.shape[:2] 
 
 
 
        result = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) 
 
 
 
        faces = result.multi_face_landmarks or [] 
 
 
 
        closed = False 
 
 
 
        ratio = None 
 
 
 
        for face in faces: 
 
 
 
            draw.draw_landmarks(frame, face, mp_face.FACEMESH_CONTOURS, 
 
 
 
                landmark_drawing_spec=None, 
 
 
 
                connection_drawing_spec=draw.DrawingSpec(color=(0,255,170), thickness=1, circle_radius=1)) 
 
 
 
            left = [33,160,158,133,153,144] 
 
 
 
            right = [362,385,387,263,373,380] 
 
 
 
            ratio = (self._eye_ratio(face,w,h,left) + self._eye_ratio(face,w,h,right))/2 
 
 
 
            closed = ratio < 0.22 
 
 
 
        alarm_on, duration = self.alarm.update(closed if faces else False) 
 
 
 
        if not faces: 
 
 
 
            lines = ["Face not detected", "Alarm paused until face returns"] 
 
 
 
        elif closed: 
 
 
 
            lines = [f"Eye ratio: {ratio:.2f}", f"EYES CLOSED: {duration:.1f}s", "BEEP + VOICE WARNING ACTIVE"] 
 
 
 
        else: 
 
 
 
            lines = [f"Eye ratio: {ratio:.2f}", "Status: ALERT / EYES OPEN"] 
 
 
 
        if closed: 
 
 
 
            cv2.rectangle(frame, (0,0), (w, h), (0,0,180), 3) 
 
 
 
            cv2.putText(frame, "WAKE UP! EYES CLOSED", (20,h-28), cv2.FONT_HERSHEY_SIMPLEX, .8, (0,0,255), 2) 
 
 
 
        _hud(frame, "DRIVER DROWSINESS", lines, (0,80,255) if closed else (255,180,60)) 
 
 
 
        return frame 
 
 
 
 
 
 
 
    def _pose_frame(self, frame, pose, mp_pose, draw): 
 
 
 
        h,w = frame.shape[:2] 
 
 
 
        result = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) 
 
 
 
        if result.pose_landmarks: 
 
 
 
            draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS) 
 
 
 
            lm = result.pose_landmarks.landmark 
 
 
 
            p = lambda i: np.array([lm[i].x*w,lm[i].y*h]) 
 
 
 
            a,b,c = p(23),p(25),p(27) 
 
 
 
            ba,bc = a-b,c-b 
 
 
 
            den = np.linalg.norm(ba)*np.linalg.norm(bc) 
 
 
 
            angle = math.degrees(math.acos(np.clip(np.dot(ba,bc)/den,-1,1))) if den else 0 
 
 
 
            stage = "DOWN" if angle < 105 else "UP" 
 
 
 
            _hud(frame, "FITNESS / POSE", [f"Knee angle: {angle:.0f} deg",f"Stage: {stage}","Check posture"], (100,255,130)) 
 
 
 
        else: 
 
 
 
            _hud(frame, "FITNESS / POSE", ["Pose not found"], (100,255,130)) 
 
 
 
        return frame 
 
 
 
 
 
 
 
    def _yolo_frame(self, frame): 
 
 
 
        try: 
 
 
 
            from ultralytics import YOLO 
 
 
 
            if not hasattr(self, "_yolo"): 
 
 
 
                self._yolo = YOLO("yolov8n.pt") 
 
 
 
            result = self._yolo(frame, verbose=False)[0] 
 
 
 
            annotated = result.plot() 
 
 
 
            _hud(annotated, "OBJECT DETECTION", [f"Objects: {len(result.boxes) if result.boxes is not None else 0}", "Model: YOLOv8n"]) 
 
 
 
            return annotated 
 
 
 
        except Exception as exc: 
 
 
 
            _hud(frame, "OBJECT DETECTION", ["Install optional ultralytics/model", str(exc)[:38]], (0,100,255)) 
 
 
 
            return frame 
 
 
 
 
 
 
 
    def run(self): 
 
 
 
        try: 
 
 
 
            import mediapipe as mp 
 
 
 
        except Exception as exc: 
 
 
 
            st.error(f"MediaPipe could not load: {exc}. Use Python 3.11 and install requirements.txt.") 
 
 
 
            return 
 
 
 
        if self.module == "Virtual Mouse": 
 
 
 
            try: 
 
 
 
                import pyautogui 
 
 
 
                self._pyautogui = pyautogui 
 
 
 
                pyautogui.FAILSAFE = True 
 
 
 
            except Exception as exc: 
 
 
 
                st.error(f"Virtual Mouse needs pyautogui: {exc}") 
 
 
 
                return 
 
 
 
 
 
 
 
        cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW if hasattr(cv2,"CAP_DSHOW") else 0) 
 
 
 
        if not cap.isOpened(): 
 
 
 
            st.error("Camera could not open. Close Camera/Zoom/Teams or try camera index 1.") 
 
 
 
            return 
 
 
 
        mp_draw = mp.solutions.drawing_utils 
 
 
 
        mp_hands = mp.solutions.hands 
 
 
 
        mp_face = mp.solutions.face_mesh 
 
 
 
        mp_pose = mp.solutions.pose 
 
 
 
        hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=.6, min_tracking_confidence=.55) if self.module in ("Hand Gesture Recognition","Virtual Mouse","Sign Language Recognition") else None 
 
 
 
        face_mesh = mp_face.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=.55, min_tracking_confidence=.5) if self.module == "Driver Drowsiness Detection" else None 
 
 
 
        pose = mp_pose.Pose(min_detection_confidence=.5, min_tracking_confidence=.5) if self.module == "Fitness / Form Checker" else None 
 
 
 
        fps, prev, count = 0.0, time.time(), 0 
 
 
 
        try: 
 
 
 
            while cap.isOpened(): 
 
 
 
                ok, frame = cap.read() 
 
 
 
                if not ok: break 
 
 
 
                if self.mirror: frame = cv2.flip(frame,1) 
 
 
 
                if hands: 
 
 
 
                    frame = self._hands_frame(frame,hands,mp_hands,mp_draw) 
 
 
 
                    if self.module == "Sign Language Recognition": 
 
 
 
                        cv2.putText(frame,"Experimental hand-pose heuristic only",(15,frame.shape[0]-18),cv2.FONT_HERSHEY_SIMPLEX,.45,(255,220,100),1) 
 
 
 
                elif face_mesh: 
 
 
 
                    frame = self._driver_frame(frame,face_mesh,mp_face,mp_draw) 
 
 
 
                elif pose: 
 
 
 
                    frame = self._pose_frame(frame,pose,mp_pose,mp_draw) 
 
 
 
                elif self.module == "Object Detection": 
 
 
 
                    frame = self._yolo_frame(frame) 
 
 
 
                elif self.module == "Screenshot Capture": 
 
 
 
                    _hud(frame,"SCREENSHOT CAPTURE",["Press S to save current frame","Saved images: screenshots/"]) 
 
 
 
                now = time.time() 
 
 
 
                count += 1 
 
 
 
                if now-prev >= 1: 
 
 
 
                    fps = count/(now-prev); count=0; prev=now 
 
 
 
                if self.show_fps: 
 
 
 
                    cv2.putText(frame,f"FPS: {fps:.1f}",(frame.shape[1]-130,30),cv2.FONT_HERSHEY_SIMPLEX,.62,(100,230,255),2) 
 
 
 
                if self.image_slot is not None: 
 
 
 
                    self.image_slot.image(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB),channels="RGB",use_container_width=True) 
 
 
 
               # cv2.imshow("Vision X - Q/ESC stop | S screenshot",frame) 
 
 
 
                if self.status_slot is not None: 
 
 
 
                    self.status_slot.caption(f"Running: {self.module} • FPS: {fps:.1f} • Camera preview is running in Streamlit.") 
                # Streamlit/headless mode: avoid OpenCV HighGUI keyboard polling. 
                time.sleep(.03) 
 
 
 
        except KeyboardInterrupt: 
 
 
 
            pass 
 
 
 
        finally: 
 
 
 
            self.alarm.close() 
 
 
 
            cap.release() 
 
 
 
            #cv2.destroyAllWindows() 
 
 
 
            if hands: hands.close() 
 
 
 
            if face_mesh: face_mesh.close() 
 
 
 
            if pose: pose.close() 
 
 
 
            if self.status_slot is not None: self.status_slot.info("Camera stopped.") 
 
 
 
 
 
 
 
def run_camera(module, camera_index=0, mirror=True, show_fps=True, image_slot=None, status_slot=None): 
 
 
 
    """Backwards-compatible entry point used by Streamlit UI.""" 
 
 
 
    VisionEngine(module,camera_index,mirror,show_fps,image_slot,status_slot).run()

class BrowserVisionProcessor(VideoProcessorBase):
    """Process browser-supplied WebRTC frames with the existing VisionEngine handlers.

    This avoids opening cv2.VideoCapture on the cloud server. The original
    run_camera() path remains unchanged for local VS Code use.
    """

    def __init__(self, module, mirror=True, show_fps=True):
        import mediapipe as mp

        self.module = module
        self.mirror = mirror
        self.show_fps = show_fps
        self.engine = VisionEngine(module, camera_index=0, mirror=mirror, show_fps=show_fps)
        # Browser-hosted Python runs on the server, not on the visitor's computer.
        # Therefore pyautogui must remain disabled for hosted sessions.
        if module == "Virtual Mouse":
            self.engine._pyautogui = None

        self.mp = mp
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.mp_face = mp.solutions.face_mesh
        self.mp_pose = mp.solutions.pose

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=.6,
            min_tracking_confidence=.55,
        ) if module in ("Hand Gesture Recognition", "Virtual Mouse", "Sign Language Recognition") else None
        self.face_mesh = self.mp_face.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=.55,
            min_tracking_confidence=.5,
        ) if module == "Driver Drowsiness Detection" else None
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=.5,
            min_tracking_confidence=.5,
        ) if module == "Fitness / Form Checker" else None
        self._fps = 0.0
        self._fps_count = 0
        self._fps_start = time.time()

    def recv(self, frame):
        import av

        img = frame.to_ndarray(format="bgr24")
        if self.mirror:
            img = cv2.flip(img, 1)

        if self.hands:
            img = self.engine._hands_frame(img, self.hands, self.mp_hands, self.mp_draw)
            if self.module == "Sign Language Recognition":
                cv2.putText(img, "Experimental hand-pose heuristic only",
                            (15, img.shape[0] - 18), cv2.FONT_HERSHEY_SIMPLEX,
                            .45, (255, 220, 100), 1)
        elif self.face_mesh:
            img = self.engine._driver_frame(img, self.face_mesh, self.mp_face, self.mp_draw)
        elif self.pose:
            img = self.engine._pose_frame(img, self.pose, self.mp_pose, self.mp_draw)
        elif self.module == "Object Detection":
            img = self.engine._yolo_frame(img)
        elif self.module == "Screenshot Capture":
            _hud(img, "SCREENSHOT CAPTURE", ["Live browser frame", "Use the browser preview to view output"])

        self._fps_count += 1
        now = time.time()
        if now - self._fps_start >= 1.0:
            self._fps = self._fps_count / (now - self._fps_start)
            self._fps_count = 0
            self._fps_start = now
        if self.show_fps:
            cv2.putText(img, f"FPS: {self._fps:.1f}", (img.shape[1] - 130, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, .62, (100, 230, 255), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

    def __del__(self):
        try:
            self.engine.alarm.close()
            if self.hands:
                self.hands.close()
            if self.face_mesh:
                self.face_mesh.close()
            if self.pose:
                self.pose.close()
        except Exception:
            pass

