# 🚀 Vision X — AI & Computer Vision Lab

**An Interactive Python-Based AI and Computer Vision Application**

Vision X is a computer vision project designed to explore real-time visual processing, hand tracking, gesture recognition, facial landmark analysis, pose estimation, object detection, and human-computer interaction through an interactive Streamlit dashboard.

The application combines Python, OpenCV, MediaPipe, NumPy, and Streamlit to provide a unified workspace for experimenting with multiple computer vision modules.

> **Project goal:** Build a modular computer vision lab that makes AI-powered visual interaction accessible through a user-friendly interface.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Architecture](#-project-architecture)
- [Computer Vision Modules](#-computer-vision-modules)
- [Installation and Setup](#-installation-and-setup)
- [How to Run](#-how-to-run)
- [Controls and Usage](#-controls-and-usage)
- [Project Structure](#-project-structure)
- [Technical Implementation](#-technical-implementation)
- [Challenges and Solutions](#-challenges-and-solutions)
- [Current Limitations](#-current-limitations)
- [Future Enhancements](#-future-enhancements)
- [Interview Explanation](#-interview-explanation)
- [Learning Outcomes](#-learning-outcomes)
- [Disclaimer](#-disclaimer)

---

## 🎯 Project Overview

Vision X provides a common interface for multiple AI and computer vision experiments instead of maintaining separate applications for each feature.

The application captures frames from a local webcam, processes them using the selected computer vision module, and displays the annotated output in the Streamlit interface.

Depending on the selected module, the application can analyze hand landmarks, estimate body pose, inspect facial landmarks, process objects with an optional YOLO model, or save screenshots.

The project follows a modular design in which the Streamlit user interface is separated from the computer vision processing logic.

### Main objectives

- Explore real-time computer vision using Python.
- Detect and process hand, face, and body landmarks.
- Implement gesture-driven mouse interaction.
- Experiment with driver drowsiness alerts.
- Integrate optional object detection.
- Build a modern interface for selecting and monitoring AI modules.
- Practice modular programming, dependency management, debugging, and application deployment.

---

## ✨ Key Features

### 🖥️ Interactive Dashboard
- Streamlit-based application interface.
- Navigation for Overview, Live Vision Lab, Image & Video, Setup Guide, and About.
- Module selection and camera configuration.
- Camera preview and processing status.
- Optional FPS display.

### ✋ Hand Tracking and Gesture Recognition
- Hand landmark processing using MediaPipe.
- Basic gesture classification using landmark positions.
- Recognition of Open Palm, Fist, Pointing, Two Fingers, and Unknown states.
- Visual landmark annotations on camera frames.

### 🖱️ Virtual Mouse
- Index-finger-based cursor positioning.
- Cursor movement using screen-coordinate mapping.
- Smoothing to reduce cursor jitter.
- Experimental air-tap click detection with a short cooldown.
- PyAutoGUI integration for mouse control.

### 🤟 Sign Language Recognition
- Experimental hand-pose classification.
- Reuses hand landmark detection.
- Provides a foundation for future sign classification models.

**Important:** This module is a limited experimental prototype, not a complete sign-language translator.

### 🏋️ Fitness / Form Checker
- Body pose landmark detection.
- Basic knee-angle estimation.
- Simple UP/DOWN movement-stage feedback.
- Visual pose skeleton and status annotations.

### 🚗 Driver Drowsiness Detection
- Facial landmark processing using MediaPipe Face Mesh.
- Eye Aspect Ratio (EAR)-style calculation for eye-closure estimation.
- Continuous eye-closure timing.
- Repeating beep and spoken warning logic.
- Alarm reset when eyes reopen or the face is no longer detected.

The alarm threshold and voice timing depend on the configured implementation. Actual detection performance varies with lighting, camera position, glasses, and processing speed.

### 📦 Object Detection
- Optional YOLOv8 Nano integration through Ultralytics.
- Object detection on camera frames when the required package and model are available.
- Annotated output with detected-object information.

The object detection module requires its optional dependency and model weights.

### 📸 Screenshot Capture
- Saves the current processed frame as a PNG image.
- Uses a dedicated `screenshots/` directory.
- Provides a foundation for reviewing detection results.

### 🖼️ Image and Video Analyzer
- Dedicated Image & Video interface.
- Intended for experimenting with uploaded visual content and analysis workflows.

The exact supported file formats and processing capabilities depend on the implementation in `app.py`.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11.x | Core programming language |
| Streamlit | Interactive dashboard and UI |
| OpenCV | Camera capture, image processing, drawing, and frame conversion |
| MediaPipe | Hand, face, and pose landmark processing |
| NumPy | Numerical calculations and coordinate transformations |
| PyAutoGUI | Virtual mouse movement and clicks |
| pyttsx3 | Text-to-speech warnings |
| winsound | Windows beep alerts |
| Ultralytics YOLO | Optional object detection |
| Git and GitHub | Version control and source-code hosting |

### Why these technologies?

- **Python:** Provides an accessible ecosystem for computer vision and AI.
- **OpenCV:** Handles webcam frames, drawing operations, and image transformations.
- **MediaPipe:** Provides landmark-based tracking for hands, faces, and body poses.
- **NumPy:** Supports coordinate mapping, interpolation, and geometric calculations.
- **Streamlit:** Makes it possible to create an interactive application without building a separate frontend framework.

---

## 🏗️ Project Architecture

The application uses a simple modular processing pipeline.

```text
                 VISION X APPLICATION
                          |
                          v
                Streamlit Dashboard
                          |
                          v
                 Select AI Module
                          |
                          v
                   Open Webcam
                          |
                          v
                 Capture Video Frame
                          |
                          v
                 OpenCV Processing
                          |
                          v
               Selected AI Processor
                          |
           +--------------+--------------+
           |              |              |
           v              v              v
       Hand Tracking   Face Mesh     Pose / YOLO
           |              |              |
           v              v              v
       Gestures /      Eye-Closure    Pose / Object
       Mouse Control   Estimation     Annotations
           |              |              |
           +--------------+--------------+
                          |
                          v
                  Annotated Frame
                          |
                          v
                 Streamlit Preview
```

### Main source files

- `app.py` — user interface, navigation, configuration, and module selection.
- `vision_engine.py` — camera lifecycle, frame processing, landmark logic, and module handlers.
- `requirements.txt` — Python dependencies.
- `screenshots/` — saved screenshots generated during use.

The exact file structure may vary as the project evolves.

---

## 📦 Installation and Setup

### Prerequisites

- Windows 10 or Windows 11.
- Python 3.11.x.
- A working webcam for live camera modules.
- Visual Studio Code or another Python editor.
- Git, if you want to clone the repository.

**Why Python 3.11?**

The project uses a pinned MediaPipe version. Python 3.11 is the intended environment for the provided dependency setup; compatibility can vary with other Python versions.

### Step 1 — Clone the repository

Replace the placeholder with your actual GitHub repository URL.

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Vision_X
```

If you already have the project locally, open the existing `Vision_X` folder instead.

### Step 2 — Create a virtual environment

```powershell
py -3.11 -m venv .venv
```

### Step 3 — Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the environment's Python executable directly without changing your system execution policy:

```powershell
.\.venv\Scripts\python.exe --version
```

### Step 4 — Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### Step 5 — Install dependencies

```powershell
python -m pip install -r requirements.txt
```

If YOLO-based object detection is required and Ultralytics is not already installed:

```powershell
python -m pip install ultralytics
```

### Step 6 — Verify OpenCV

```powershell
python -c "import cv2; print(cv2.__version__); print(hasattr(cv2, 'VideoCapture')); print(cv2.getBuildInformation())"
```

The `VideoCapture` check should return `True`. A Windows desktop environment that uses OpenCV GUI windows also requires a GUI-enabled OpenCV build.

Avoid installing multiple conflicting OpenCV variants in the same environment.

---

## ▶️ How to Run

From the project directory, with the virtual environment activated:

```powershell
python -m streamlit run app.py
```

Streamlit will display a local application URL in the terminal, typically:

`http://localhost:8501`

Open the URL in your browser.

### Starting a computer vision session

1. Open **Live Vision Lab**.
2. Select the required module.
3. Choose the appropriate camera index.
4. Configure mirroring and FPS display if available.
5. Click **Start processing**.
6. Observe the annotated preview and status messages.
7. Stop the session using the supported controls.

**Local webcam note:** The application uses a local OpenCV camera capture workflow. Running it locally gives it access to the local machine's webcam when permissions and drivers allow it. Hosting the app on a cloud server does not automatically grant access to the visitor's webcam.

---

## 🎮 Controls and Usage

| Control | Action |
|---|---|
| Start processing | Starts the selected vision module |
| Camera index | Selects the camera device |
| Mirror camera preview | Flips the camera frame horizontally |
| Show processing FPS | Displays the calculated processing frame rate |
| Q / ESC | Stops processing when the OpenCV preview window receives keyboard input |
| S | Saves the current frame when keyboard input is received by the OpenCV preview window |

Keyboard controls depend on the active preview implementation and GUI support. They may not work when interacting only with the Streamlit page.

---

## 📂 Project Structure

```text
Vision_X/
│
├── app.py
├── vision_engine.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
```

Optional files, such as YOLO model weights, can be added or downloaded separately according to the implementation.

Keep virtual environments, cache directories, temporary downloads, and large generated files out of Git version control.

---

## ⚙️ Technical Implementation

### 1. Webcam capture

OpenCV's `VideoCapture` API initializes the camera and reads frames.

Each successful frame is passed to the selected processing handler.

### 2. Frame preprocessing

The engine optionally mirrors the frame and converts its color space when preparing images for MediaPipe.

For example, MediaPipe processing commonly uses RGB input, whereas OpenCV camera frames are typically read in BGR format.

### 3. Landmark-based analysis

MediaPipe supplies normalized landmark coordinates. Vision X uses these coordinates for gesture classification, cursor mapping, facial analysis, and pose calculations.

### 4. Gesture classification

The hand gesture module uses the relative positions of selected landmarks to classify a small set of predefined gestures.

This is a rule-based approach rather than a trained deep-learning gesture classifier.

### 5. Virtual mouse mapping

The virtual mouse maps the index fingertip coordinates from the camera frame to screen coordinates. A smoothing calculation reduces sudden cursor jumps.

An experimental finger-bend/air-tap rule is used to trigger clicks in the shared engine implementation.

### 6. Drowsiness estimation

The driver module calculates an eye-ratio measurement from selected facial landmarks and compares it with a threshold to estimate eye closure.

A timer tracks sustained closure before the alarm logic starts. The result is an educational heuristic, not a medically validated or safety-certified system.

### 7. Pose estimation

The fitness module processes body landmarks and calculates a knee angle using vector geometry. A simple threshold maps the estimated angle to an UP or DOWN stage.

### 8. Object detection

When the optional YOLO dependency and model weights are available, the engine runs inference on a frame and renders the annotated result.

### 9. Streamlit output

The processed BGR frame is converted to RGB before it is displayed in the Streamlit image component.

---

## 🧩 Challenges and Solutions

### Challenge 1 — Webcam initialization

**Problem:** The camera may fail to open because another application is using it, the camera index is incorrect, or permissions are unavailable.

**Approach:** Check camera availability, confirm the correct index, close competing applications, and verify that the operating system grants camera access.

### Challenge 2 — Python and dependency compatibility

**Problem:** Computer vision libraries may not support every Python version or package combination.

**Approach:** Use the intended Python 3.11 environment, install dependencies in a virtual environment, and verify the loaded package versions.

### Challenge 3 — OpenCV GUI errors

**Problem:** Functions such as `imshow()` and `destroyAllWindows()` can fail when the loaded OpenCV build lacks GUI support.

**Approach:** Verify the OpenCV build configuration and avoid conflicting GUI-enabled and headless OpenCV packages.

### Challenge 4 — Cursor jitter

**Problem:** Small changes in hand landmarks can produce unstable cursor movement.

**Approach:** Apply coordinate smoothing and clamp screen coordinates to valid bounds.

### Challenge 5 — Unreliable gesture detection

**Problem:** Lighting, hand orientation, occlusion, and differences between users can affect landmark-based rules.

**Approach:** Use confidence thresholds, test different hand positions, and consider collecting training data for a future classification model.

### Challenge 6 — Drowsiness detection reliability

**Problem:** Eye landmarks may become unreliable because of glasses, face angle, low light, or partial occlusion.

**Approach:** Treat the output as an experimental indicator, test across varied conditions, and avoid relying on it for real driving safety.

---

## ⚠️ Current Limitations

- Sign-language recognition is experimental and does not translate full sign language.
- Gesture classification supports only a small predefined set of gestures.
- Virtual mouse performance depends on camera quality, landmark stability, and screen-coordinate mapping.
- The fitness module provides basic angle-based feedback rather than a comprehensive exercise assessment.
- Drowsiness detection may generate false positives or miss eye closure.
- Object detection requires optional dependencies and model weights.
- Local webcam access and desktop GUI controls may behave differently in hosted environments.
- The Image & Video Analyzer's exact capabilities depend on the implemented upload-processing workflow.

---

## 🔮 Future Enhancements

- Train a machine-learning model for more robust gesture classification.
- Develop a dataset-driven sign-language recognition model.
- Add more hand gestures and customizable mouse controls.
- Improve virtual mouse calibration and click detection.
- Introduce repetition counting and additional exercise-form metrics.
- Evaluate drowsiness detection on a labeled dataset and report appropriate metrics.
- Add object tracking and configurable detection thresholds.
- Expand image and video upload analysis.
- Add session history and downloadable analysis reports.
- Improve automated testing, error logging, and deployment documentation.
- Develop a browser-compatible camera workflow for hosted deployments.

These are planned enhancements, not claims about currently implemented functionality.

---

## 🎤 Interview Explanation

### Short introduction

“Vision X is a Python-based AI and computer vision project that combines multiple visual-processing experiments into one interactive Streamlit application. I used OpenCV for webcam capture and image processing, MediaPipe for landmark detection, NumPy for numerical calculations, and PyAutoGUI for virtual mouse control. The project includes hand gesture recognition, an experimental virtual mouse, basic pose analysis, driver drowsiness estimation, screenshot capture, and optional YOLO object detection. My main objective was to understand real-time computer vision and build a modular application that is easy to use and extend.”

### How does your project work?

“The user selects a module from the Streamlit dashboard. The engine initializes the webcam, captures frames, and passes them to the selected processing handler. Depending on the module, it processes hand, face, or pose landmarks or performs object detection. The application then annotates the frame and displays it in the interface.”

### What was your role?

“I worked on integrating the computer vision modules, organizing the processing logic, developing the Streamlit interface, implementing landmark-based rules, integrating virtual mouse control, and troubleshooting Python environment and OpenCV issues.”

Adapt this answer to the parts you personally implemented and tested.

### Why did you choose OpenCV?

“OpenCV provides webcam capture, image transformations, drawing utilities, and frame processing. It acts as the foundation for handling visual input in the application.”

### Why did you choose MediaPipe?

“MediaPipe provides hand, face, and pose landmarks that can be used for geometry-based analysis without requiring me to train a separate neural network for every basic tracking task.”

### Is your sign-language system production-ready?

“No. The current implementation uses limited hand-pose heuristics. A production-quality sign-language system would require an appropriate dataset, a trained model, temporal information for dynamic signs, and systematic evaluation.”

### How do you detect drowsiness?

“The module calculates an eye-ratio measurement using facial landmarks and compares it with a threshold. It tracks the duration of detected eye closure and triggers an audio warning according to the configured timing. It is an educational prototype and is not safety-certified.”

### What was a major technical challenge?

“One challenge was managing compatibility between Python and computer vision dependencies. I learned to isolate dependencies in a virtual environment, verify the OpenCV installation, and distinguish environment errors from application-code errors.”

### How would you improve this project?

“I would first add automated tests and evaluate the current rules with representative data. Then I would improve gesture classification using a labeled dataset, add more robust calibration and tracking, and build a better-tested deployment workflow.”

---

## 📚 Learning Outcomes

Through Vision X, the project provides practical experience with:

- Python application development.
- OpenCV-based webcam processing.
- Landmark-based computer vision.
- Coordinate transformations and vector geometry.
- Streamlit application design.
- Mouse automation and audio feedback.
- Python dependency management and debugging.
- Modular architecture and Git-based development.

---

## 🛡️ Disclaimer

Vision X is an educational project intended for learning and experimentation. Its computer vision outputs are not guaranteed to be accurate in all environments.

The driver drowsiness module is not a certified safety system and must not be relied upon as the sole means of preventing accidents. Always follow applicable driving safety requirements.

---

## 👨‍💻 Project Information

**Project:** Vision X — AI & Computer Vision Lab  
**Language:** Python  
**Interface:** Streamlit  
**Core Libraries:** OpenCV, MediaPipe, NumPy  
**Source Control:** Git and GitHub

**Developed as a hands-on project to explore AI, computer vision, and real-time human-computer interaction.**