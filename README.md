<img src="any2yolo.ico" alt="Any2YOLO" width="100" />

# **Any2YOLO**

**Easily convert [AnyLabeling](https://github.com/vietanhdev/anylabeling) JSON into [YOLO](https://github.com/ultralytics/ultralytics) txt files!**

This tool simplifies dataset preparation for YOLO models, whether you're processing a single JSON file or managing batch conversions with multiple labels.

---

## 🌟 **Key Features**

- **Batch Conversion**: Upload and process multiple JSON files at once
- **Label Selection**: Choose specific labels for YOLO txt format or include all
- **User-Friendly Interface**: Intuitive gui for both technical and non-technical users
- **Detailed Logs**: Monitor every step of the conversion process
- **Error Handling**: Skips invalid files and provides detailed error logs

---

## 🚀 **Getting Started**

### **Prerequisites**

- Python 3.8 or newer

### **Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/danilobirbiglia/Any2YOLO.git
   ```
   
2. **Install dependencies**:

   ## **For Linux/macOS**:
   Install tkinter and Pillow:
   ```bash
   sudo apt-get install python3-tk
   pip install Pillow
   ```

   ## **For Windows**:
   - Ensure Python is installed with the **tcl/tk and IDLE** option selected during installation
   - Then install Pillow:
     ```bash
     pip install Pillow
     ```

3. **Verify tkinter installation** (optional):
   Run the following command to ensure tkinter is properly installed:
   ```bash
   python -m tkinter
   ```
   If a small GUI window appears, `tkinter` is installed correctly

---

### **Launching the App**

1. **Run the application**:
   ```bash
   python main.py
   ```
2. Follow the on-screen instructions to upload and convert your JSON files

---

## 🖥️ **How It Works**

1. **Run the App**: Start the GUI with `python main.py`
2. **Upload Files**: Click the "📂 Upload JSON Files" button to select one or more files
3. **Review Labels**: View and select labels extracted from your JSON files
4. **Convert Files**: Click "Convert" to generate YOLO compatible `.txt` files
5. **Access Results**: Converted files are saved in the same directory as the input JSON files

---

## 📂 **Project Structure**

| **File**           | **Description**                                       |
|---------------------|-------------------------------------------------------|
| `main.py`          | Entry point for the application                      |
| `gui.py`           | GUI logic for file management and conversion controls|
| `converter.py`     | Core logic for JSON to YOLO conversion               |
| `logger.py`        | Manages logging for debugging and troubleshooting    |
| `styles.py`        | Defines styles for the GUI application               |
| `any2yolo.ico`     | Icon for the GUI                        |
| `README.md`        | Project documentation (you’re reading it!)           |

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

This project is licensed under the [MIT License](LICENSE).

---

## 👤 **About the Creator**

- **Created by**: Danilo Birbiglia  
- **LinkedIn**: [Danilo Birbiglia](https://www.linkedin.com/in/danilo-birbiglia/)  
- **Email**: danilobirbiglia@gmail.com  

---

Transform your data with inot **YOLO!** 🎉
