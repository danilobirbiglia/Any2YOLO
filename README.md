<img src="assets/any2yolo.ico" alt="Any2YOLO" width="100" />

# **Any2YOLO**

**Easily convert [AnyLabeling](https://github.com/vietanhdev/anylabeling) JSON into [YOLO](https://github.com/ultralytics/ultralytics) txt files!**

This tool simplifies dataset preparation for YOLO models, whether you're processing a single JSON file or managing batch conversions with multiple labels

---

## 🌟 **Key Features**

- **Batch Conversion**: Upload and process multiple JSON
- **Label Selection**: Choose specific labels for YOLO txt format or include all
- **User-Friendly Interface**: Intuitive GUI
- **Detailed Logs**: Monitor every step of the conversion process
- **Error Handling**: Skips invalid files and provides detailed error logs

---

## 🚀 **Getting Started**

### **Prerequisites**

- Python 3.8 or newer

# 📦 Installation

## Clone the Repository
To get started, clone the repository to your local machine:
```bash
# Clone the repository
git clone https://github.com/danilobirbiglia/Any2YOLO.git

# Navigate into the project directory
cd Any2YOLO
```

## Install Dependencies

### For Linux/macOS
**Note**: The tool is not fully optimized for Linux/macOS. Some features may have limited functionality

Install `tkinter` and `Pillow`:
```bash
sudo apt-get install python3-tk -y
pip install Pillow
```

### For Windows
- Ensure Python is installed with the **tcl/tk and IDLE** option enabled during the installation process
- Then, install `Pillow` using:
  ```bash
  pip install Pillow
  ```

## Verify `tkinter` Installation (Optional)
To confirm that `tkinter` is properly installed, run:
```bash
python -m tkinter
```
If a small GUI window appears, `tkinter` is correctly installed

---

### **Launching the App**

1. Install dependencies:
   ```bash
   # Install Python dependencies
   pip install Pillow
   ```

2. Run the application:
   ```bash
   python src/main.py
   ```
3. Follow the on-screen instructions to upload and convert your JSON files

---

## 🖥️ **How It Works**

1. **Run the App**: Start the GUI with `python src/main.py`
2. **Upload Files**: Click the "📂 Upload JSON Files" button to select one or more files
3. **Review Labels**: View and select labels extracted from your JSON files
4. **Convert Files**: Click "Convert" to generate YOLO compatible `.txt` files
5. **Access Results**: Converted files are saved in the same directory as the input JSON files

---

## 📂 **Project Structure**

| **Folder/File**      | **Description**                                       |
|----------------------|-------------------------------------------------------|
| `src/main.py`        | Entry point for the application                      |
| `src/gui.py`         | GUI logic for file management and conversion controls|
| `src/converter.py`   | Core logic for JSON to YOLO conversion               |
| `src/logger.py`      | Manages logging for debugging and troubleshooting    |
| `src/styles.py`      | Defines styles for the GUI application               |
| `assets/any2yolo.ico`| Icon for the GUI                                      |
| `logs/converter.log`              | Directory for log                              |
| `README.md`          | Project documentation (you’re reading it!)           |

---

## 💻 **Example**

### **Input JSON**
```json
{
  "shapes": [
    {
      "label": "dog",
      "points": [[100, 200], [300, 400]],
      "shape_type": "polygon"
    },
    {
      "label": "cat",
      "points": [[50, 50], [150, 150]],
      "shape_type": "polygon"
    }
  ],
  "imageWidth": 500,
  "imageHeight": 500
}
```

### **Generated YOLO TXT**
```txt
0 0.4 0.6 0.4 0.4
1 0.2 0.2 0.2 0.2
```

**Steps Taken**:  
1. Extracted labels: `dog`, `cat`
2. Calculated bounding box dimensions and coordinates
3. Converted to YOLO txt

---

## 📜 **Logs**

Detailed logs are available through the "Logs" menu in the app

**Example Log Output**:
```log
INFO: Initialized with files: ['annotations.json']
INFO: Extracted labels: ['dog', 'cat']
INFO: Successfully converted annotations.json to annotations.txt
WARNING: Skipped invalid shape in annotations.json
```

---

## ❓ **FAQ**

### **What happens if a file is invalid?**  
The app skips invalid files and logs the issue for review

### **Can I use this for bounding boxes instead of polygons?**  
Yes! YOLO txt files support both polygons and bounding boxes

---

## 📜 **License**

This project is licensed under the [MIT License](LICENSE)

---

## 👤 **About the Creator**

- **Created by**: Danilo Birbiglia  
- **LinkedIn**: [Danilo Birbiglia](https://www.linkedin.com/in/danilo-birbiglia/)  
- **Email**: danilobirbiglia@gmail.com  

---
