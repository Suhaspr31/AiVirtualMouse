# AI Virtual Mouse

This project implements an AI-powered virtual mouse system using computer vision and hand tracking. Control your computer mouse using hand gestures captured via webcam.

## Features

### Virtual Mouse

- **Mouse Movement**: Move the cursor by pointing with your index finger
- **Clicking**: Perform left-click by bringing index and middle fingers together
- **Scrolling**: Scroll up with three fingers up, scroll down with four fingers up
- Real-time hand tracking with smooth cursor movement

## Requirements

- Python 3.7+
- Webcam
- Operating System: Windows/Linux/Mac

## Dependencies

Install the required packages using pip:

```bash
pip install opencv-python numpy mediapipe pyautogui
```

## Installation

1. Clone or download this repository
2. Install the dependencies as mentioned above
3. Ensure your webcam is connected and accessible

## Usage

### Virtual Mouse

Run the main mouse control script:

```bash
python AiVirtualMouseProject.py
```

- Point with your index finger to move the mouse
- Bring index and middle fingers together to click
- Use three fingers for scroll up, four fingers for scroll down
- Press Ctrl+C in terminal to stop

## How It Works

The system uses MediaPipe's hand tracking to detect hand landmarks in real-time from webcam feed. The custom HandTrackingModule processes these landmarks to determine finger positions and gestures.

For mouse control:

- Index finger position maps to screen coordinates
- Finger combinations trigger different actions (move, click, scroll)

## Project Structure

- `AiVirtualMouseProject.py`: Main mouse control script
- `HandTrackingModule.py`: Custom hand detection and tracking module
- `test.py`: Test script for hand tracking
- `tempCodeRunnerFile.py`: Temporary code runner file

## Troubleshooting

- Ensure good lighting for better hand detection
- Keep hands within camera frame
- Adjust detection confidence in the code if needed
- Make sure webcam permissions are granted

## License

This project is open-source. Feel free to modify and distribute.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
