import cv2
import os
import glob
import numpy as np
import pytesseract

# Configuration
SCREENSHOTS_DIR = r"C:\Users\david\Pictures\Screenshots"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def diagnose_image(filepath):
    print(f"\nDistagnosing: {os.path.basename(filepath)}")
    img = cv2.imread(filepath)
    if img is None:
        print("Failed to load.")
        return

    h, w = img.shape[:2]
    print(f"Dimensions: {w}x{h}")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=w//3, maxLineGap=50)
    
    horizontal_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y1 - y2) < 10:
                horizontal_lines.append(int(y1))
    
    horizontal_lines.sort()
    print(f"Long Horizontal Lines (Y-coords): {horizontal_lines}")
    
    # Check bottom 20% for axis
    potential_axes = [y for y in horizontal_lines if y > h * 0.8]
    if potential_axes:
        print(f"Likely Time Axis Candidates (Bottom 20%): {potential_axes}")
    else:
        print("No lines found in bottom 20%.")
        
    # OCR to find legend
    # Look in bottom right, top right, bottom left
    print("Sampling text locations...")
    
    # ROI: Bottom Right for potential legend
    roi_br = img[int(h*0.5):h, int(w*0.7):w]
    text_br = pytesseract.image_to_string(roi_br).strip()
    if text_br:
        print(f"Bottom Right Text sample:\n{text_br[:100]}...")
        
    # ROI: Bottom Left
    roi_bl = img[int(h*0.5):h, 0:int(w*0.3)]
    text_bl = pytesseract.image_to_string(roi_bl).strip()
    if text_bl:
        print(f"Bottom Left Text sample:\n{text_bl[:100]}...")

def main():
    image_files = glob.glob(os.path.join(SCREENSHOTS_DIR, '*.png'))
    for filepath in image_files[:3]: # Check first 3
        diagnose_image(filepath)

if __name__ == "__main__":
    main()
