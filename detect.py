import os
import argparse
import cv2
import numpy as np
import torch
import torchvision
from PIL import Image
import torchvision.transforms as T
from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights
import matplotlib.pyplot as plt

def run_detection(img_path, threshold=0.6, output_path="detected_traffic.jpg", show_plot=False):
    if not os.path.exists(img_path):
        print(f"Error: Image path '{img_path}' does not exist.")
        return None

    print(f"Loading Faster R-CNN model...")
    # Load model
    weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
    model = fasterrcnn_resnet50_fpn(weights=weights)
    model.eval()

    # Define transform
    transform = T.Compose([T.ToTensor()])

    print(f"Processing image: {img_path}")
    # Load and process image
    img = Image.open(img_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0)

    # Make prediction
    print("Running inference...")
    with torch.no_grad():
        predictions = model(img_tensor)

    # Extract predictions
    pred_boxes = predictions[0]['boxes'].cpu().numpy()
    pred_scores = predictions[0]['scores'].cpu().numpy()
    pred_labels = predictions[0]['labels'].cpu().numpy()

    # Convert image for OpenCV
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img_display = img_cv.copy()

    print("Drawing detections...")
    vehicle_count = {}
    
    # Class categories
    categories = weights.meta['categories']

    for box, score, label in zip(pred_boxes, pred_scores, pred_labels):
        if score >= threshold:
            x1, y1, x2, y2 = map(int, box)

            # Draw bounding box
            cv2.rectangle(img_display, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Prepare label text
            class_name = categories[label]
            text = f"{class_name}: {score:.2f}"

            # Keep track of counts
            vehicle_count[class_name] = vehicle_count.get(class_name, 0) + 1

            # Draw text background
            (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(img_display, (x1, y1 - text_height - 10), (x1 + text_width, y1), (0, 255, 0), -1)

            # Draw text
            cv2.putText(img_display, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    print("\nDetection Statistics:")
    print("-" * 30)
    total_detected = sum(vehicle_count.values())
    print(f"Total objects detected: {total_detected}")
    for vehicle, count in vehicle_count.items():
        print(f"  {vehicle}: {count}")
    print("-" * 30)

    # Save the result
    cv2.imwrite(output_path, img_display)
    print(f"Result successfully saved as: {output_path}")

    if show_plot:
        plt.figure(figsize=(12, 8))
        plt.imshow(cv2.cvtColor(img_display, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title('Traffic Analysis (Faster R-CNN)')
        plt.show()

    return vehicle_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traffic Detection and Classification CLI")
    parser.add_argument("--image", "-i", type=str, help="Path to the traffic image to analyze")
    parser.add_argument("--threshold", "-t", type=float, default=0.6, help="Confidence threshold (default: 0.6)")
    parser.add_argument("--output", "-o", type=str, default="detected_traffic.jpg", help="Output path for annotated image")
    parser.add_argument("--show", "-s", action="store_true", help="Display the output image window")
    args = parser.parse_args()

    # If no image path provided, search for any jpg/png in the directory
    img_path = args.image
    if not img_path:
        valid_extensions = (".jpg", ".jpeg", ".png")
        files_in_dir = [f for f in os.listdir(".") if f.lower().endswith(valid_extensions)]
        if files_in_dir:
            img_path = files_in_dir[0]
            print(f"No image specified. Automatically picked: '{img_path}'")
        else:
            print("No image file specified and none found in the current directory.")
            print("Please run with: python detect.py --image <path_to_image>")
            exit(1)

    run_detection(img_path, threshold=args.threshold, output_path=args.output, show_plot=args.show)
