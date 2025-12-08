# Analyzing Nitrogen-Water Instabilities Using Python
## A Manim Presentation Project

This repository contains a scientific presentation created using [Manim Community](https://www.manim.community/) - the mathematical animation engine made famous by 3Blue1Brown.

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [Usage](#-usage)
- [Rendering Individual Scenes](#-rendering-individual-scenes)
- [Creating the Complete Presentation](#️-creating-the-complete-presentation)
- [Editing Guide](#️-editing-guide)
- [Troubleshooting](#-troubleshooting)
- [Contact](#-contact)

---

## 🔬 Overview

This presentation demonstrates a computational pipeline for analyzing liquid nitrogen-water instability patterns using Python. The project showcases:

- **Computer Vision**: Circle detection using Hough transforms and geometric algorithms
- **Coordinate Transformations**: Converting Cartesian grids to polar coordinates
- **Signal Processing**: Angular binning and intensity profile analysis
- **Data Visualization**

**Presentation Duration**: ~3 minutes  
**Target Audience**: Technical/scientific community  
**Key Technologies**: Python, OpenCV, SciPy, NumPy, Manim

---

## 📦 Prerequisites

Before running this project, ensure you have:

### Required Software
- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **FFmpeg** - For video rendering
  - Windows: [Download from gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
  - Mac: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`
- **LaTeX** (Optional) - For mathematical symbols
  - Windows: [MiKTeX](https://miktex.org/download)
  - Mac: `brew install --cask mactex`
  - Linux: `sudo apt install texlive-full`
  - *Note: Current version uses Text instead of MathTex, so LaTeX is optional*

### Python Packages
All required packages are listed in `requirements.txt`

---

## 🚀 Installation

### 1. Get the Project Files

#### Option A: Clone from GitHub
```bash
git clone https://github.com/ayman-alashkar/SC_presentation.git
cd SC_presentation
```

#### Option B: Download ZIP
1. Click the green **"Code"** button on GitHub
2. Select **"Download ZIP"**
3. Extract the ZIP file to your desired location
4. Open terminal/command prompt in that folder

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
manim --version
```
Should display: `Manim Community v0.18.x` or similar

---

## 📁 Project Structure

```
SC_presentation/
│
├── scenes/                          # Scene source files
│   ├── scene1.py                    # Introduction with titles
│   ├── scene2.py                    # Circle detection method
│   ├── scene3.py                    # Polar transformation
│   └── scene4.py                    # Results and conclusions
│
├── data/                            # Experimental data
│   └── d4_T20_1.JPG                 # LN2-water experimental image
│
├── media/                           # Generated videos (created after rendering)
│   └── videos/
│       ├── scene1/
│       ├── scene2/
│       ├── scene3/
│       └── scene4/
│
├── merge_list.txt                   # FFmpeg concat file for merging
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── COMPLETE_PRESENTATION.mp4        # Final merged video (after rendering)
```

---

## 🎬 Usage

### Quick Start (First Time)

1. **Activate virtual environment** (if not already active)
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

2. **Render a test scene** (low quality, fast)
   ```bash
   manim -pql scenes/scene1.py IntroSceneWithTitles
   ```

3. **Check the output**
   - Navigate to: `media/videos/scene1/480p15/`
   - Open `IntroSceneWithTitles.mp4`
   - If it plays, you're all set! 🎉

---

## 🎥 Rendering Individual Scenes

### Scene 1: Introduction
```bash
manim -pql scenes/scene1.py IntroSceneWithTitles
```
**Duration**: ~30-35 seconds  
**Content**: Title card, experimental setup, sampling strategy, signal unwrapping

### Scene 2: Circle Detection
```bash
manim -pql scenes/scene2.py CircleDetectionScene
```
**Duration**: ~42-45 seconds  
**Content**: Hough circles, 3-point geometric fallback method

### Scene 3: Polar Transformation
```bash
manim -pql scenes/scene3.py PolarTransformScene
```
**Duration**: ~70-75 seconds  
**Content**: Cartesian to polar grid transformation, angular binning

### Scene 4: Results
```bash
manim -pql scenes/scene4.py ResultsScene
```
**Duration**: ~25-30 seconds  
**Content**: Intensity vs angle plot, peak detection, conclusions

---

## 🎞️ Creating the Complete Presentation

### Method 1: Using FFmpeg (Recommended - Fastest)

**Step 1**: Render all scenes in **high quality**
```bash
manim -pqh scenes/scene1.py IntroSceneWithTitles
manim -pqh scenes/scene2.py CircleDetectionScene
manim -pqh scenes/scene3.py PolarTransformScene
manim -pqh scenes/scene4.py ResultsScene
```

**Step 2**: Verify `merge_list.txt` has correct paths
```
file 'media/videos/scene1/1080p60/IntroSceneWithTitles.mp4'
file 'media/videos/scene2/1080p60/CircleDetectionScene.mp4'
file 'media/videos/scene3/1080p60/PolarTransformScene.mp4'
file 'media/videos/scene4/1080p60/ResultsScene.mp4'
```

**Step 3**: Merge all scenes
```bash
ffmpeg -f concat -safe 0 -i merge_list.txt -c copy COMPLETE_PRESENTATION.mp4
```

**Result**: `COMPLETE_PRESENTATION.mp4` in your project root!

### Method 2: Using Python Script

```bash
pip install moviepy
python merge_scenes.py
```

---

## ✏️ Editing Guide

### Common Modifications

#### Change Colors
```python
# Find:
color=BLUE

# Change to:
color=RED, color=GREEN, color=YELLOW, etc.
```

#### Adjust Timing
```python
# Make animation faster:
run_time=2  →  run_time=1

# Add more pause for narration:
self.wait(2)  →  self.wait(4)
```

#### Modify Text
```python
# Find:
Text("Thank You!", ...)

# Change to:
Text("Thanks for Watching!", ...)
```

#### Change Sizes
```python
# Make text bigger:
font_size=36  →  font_size=48

# Make lines thicker:
stroke_width=3  →  stroke_width=6
```

### Quality Settings

- `-pql` : Low quality (480p, 15fps) - Fast for testing
- `-pqm` : Medium quality (720p, 30fps) - Good balance
- `-pqh` : High quality (1080p, 60fps) - Final export

---

## 🔧 Troubleshooting

### Issue: "manim: command not found"
**Solution**: 
- Make sure virtual environment is activated (look for `(venv)` in terminal)
- Try: `python -m manim` instead of just `manim`

### Issue: "FileNotFoundError" when rendering
**Solution**:
- Check file paths are correct
- Use forward slashes `/` not backslashes `\`
- Verify file exists: `dir scenes\scene1.py`

### Issue: FFmpeg merge fails
**Solution**:
- Check `merge_list.txt` format (must have `file` keyword)
- Use forward slashes in paths
- Wrap paths in single quotes: `file 'path/to/video.mp4'`

### Issue: LaTeX errors (if you enable MathTex)
**Solution**:
- Current version uses `Text()` instead of `MathTex()` - no LaTeX needed!
- If you want LaTeX: Install MiKTeX/MacTeX and restart VS Code

### Issue: Video renders but is blank/black
**Solution**:
- Check image path in scene1.py: `data/d4_T20_1.JPG`
- Verify image exists in data folder
- Try absolute path if relative path doesn't work

---

## 📚 Resources

- **Manim Documentation**: https://docs.manim.community/
- **Tutorial Videos**: https://www.youtube.com/c/TheoremofBeethoven
- **Example Gallery**: https://docs.manim.community/en/stable/examples.html
- **Community Discord**: https://www.manim.community/discord/

---

## 🎯 Rendering Workflow

### For Testing/Editing
```bash
# 1. Make changes to a scene file
# 2. Render quickly in low quality
manim -pql scenes/your_scene.py SceneClassName
# 3. Check output in media/videos/...
# 4. Repeat until satisfied
```

### For Final Presentation
```bash
# 1. Render all scenes in high quality
manim -pqh scenes/scene1.py IntroSceneWithTitles
manim -pqh scenes/scene2.py CircleDetectionScene
manim -pqh scenes/scene3.py PolarTransformScene
manim -pqh scenes/scene4.py ResultsScene

# 2. Merge into complete video
ffmpeg -f concat -safe 0 -i merge_list.txt -c copy COMPLETE_PRESENTATION.mp4

# 3. Your final presentation is ready!
```

---


## 👨‍🔬 Credits

**Created by**: Ayman Alashkar
**Institution**: CFF Unit - OIST (Okinawa Institute of Science and Technology)
**Topic**: Nitrogen-Water Instability Pattern Analysis  
**Animation Framework**: Manim Community Edition  
**Date**: December 2025

---

## 📝 License

This project is created for educational and research purposes.

---

## 🤝 Contributing

If you find issues or want to improve this presentation:
1. Create a detailed issue describing the problem
2. Fork the repository
3. Make your changes
4. Submit a pull request

---

## 📧 Contact

For questions about this presentation or the research:
- **Email**: a.alashkar@oist.jp
- **Research Group**: CFF Unit

---

## ✨ Acknowledgments

Special thanks to:
- **Manim Community** for the excellent animation framework
- **3Blue1Brown** for inspiring mathematical visualization
- **CFF Unit** for supporting this research

---

**Enjoy the presentation!** 🎉
