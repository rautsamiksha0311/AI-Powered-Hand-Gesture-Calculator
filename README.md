# ✋ AI-Powered Hand Gesture Calculator

A computer vision calculator built with Python, OpenCV, and MediaPipe that lets you save numbers and perform arithmetic operations using hand gestures.

---

## 🌟 About the Project

**AI-Powered Hand Gesture Calculator** is a webcam-based application that combines hand tracking and gesture recognition to create a touch-free calculator.

The project uses MediaPipe's pretrained machine-learning model to detect hand landmarks and Python logic to recognize specific gestures. Users can save numbers, calculate results, and reset the calculator using hand gestures.

This project explores artificial intelligence, computer vision, machine learning integration, and real-time gesture-based interaction.

## 🚀 Features

- ✋ **Real-Time Hand Detection** — Detect hands through your webcam.
- 🔢 **Finger Counting** — Estimate the number of raised fingers.
- 🤘 **Gesture-Based Number Saving** — Save numbers using the Rock sign.
- 🤙 **Gesture-Based Calculation** — Calculate results using the Shaka sign.
- 👌 **Gesture-Based Reset** — Reset the calculator using the OK sign.
- ➕ **Arithmetic Operations** — Addition, subtraction, multiplication, and division.
- ⏱️ **Hold-to-Activate Controls** — Hold gestures briefly to reduce accidental actions.
- 📷 **Live Camera Preview** — View hand landmarks and calculator values in real time.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| OpenCV | Webcam access and video processing |
| MediaPipe | Hand detection and landmark tracking |
| Computer Vision | Analyze hand positions and finger movements |

## 🎮 Gesture Controls

| Gesture | Action |
|---|---|
| 🤘 Rock sign | Save a number |
| 🤙 Shaka sign | Calculate the result |
| 👌 OK sign | Reset the calculator |

### Keyboard Controls

| Key | Operation |
|---|---|
| A | Addition (+) |
| B | Subtraction (-) |
| M | Multiplication (*) |
| D | Division (/) |
| Q | Quit the application |

## 📸 Application Preview

*Add a screenshot of your running calculator here.*

After uploading a screenshot to your repository, you can display it using:

```markdown
![AI Hand Gesture Calculator](screenshots/gesture-calculator.png)
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Hand-Gesture-Calculator.git
cd AI-Hand-Gesture-Calculator
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python gesture_calculator.py
```

Allow camera access if prompted and make sure your webcam is connected.

## 📁 Project Structure

```text
AI-Hand-Gesture-Calculator/
├── gesture_calculator.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## 🧠 How It Works

1. OpenCV captures live video from the webcam.
2. MediaPipe's pretrained model detects the hand and estimates its landmarks.
3. Python logic analyzes the landmarks to recognize finger positions and selected gestures.
4. The application saves numbers and performs the requested arithmetic operation.
5. The result is displayed on the camera window.

## 🔐 Privacy and Security

- Webcam processing is performed locally by the application.
- The project does not require an external AI API.
- No API keys are required.
- Keep your virtual environment and unnecessary local files out of the repository.

## 🎯 Future Improvements

- 🧠 Train a custom machine-learning model for gesture classification.
- ➗ Select arithmetic operations using hand gestures.
- 🔊 Add voice feedback for calculation results.
- 🎨 Build a more interactive calculator interface.
- 📊 Improve gesture accuracy and hand-position robustness.
- 📱 Explore touch-free controls for other applications.

## 📜 License

This project is available under the MIT License. See the `LICENSE` file for details.

## 📞 Contact

GitHub: [Samiksha Raut](https://github.com/rautsamiksha0311)

