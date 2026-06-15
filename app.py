import os
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import torch
import torchvision
from PIL import Image
import torchvision.transforms as T
from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['RESULT_FOLDER'] = os.path.join('static', 'results')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Create directories if they do not exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Load model globally on startup to make inference fast
print("Loading PyTorch Faster R-CNN model on startup...")
weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
model = fasterrcnn_resnet50_fpn(weights=weights)
model.eval()
transform = T.Compose([T.ToTensor()])
categories = weights.meta['categories']
print("Model loaded successfully.")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Output path
        grayscale = request.form.get('grayscale', 'false') == 'true'
        prefix = 'detected_bw_' if grayscale else 'detected_'
        output_filename = prefix + filename
        output_path = os.path.join(app.config['RESULT_FOLDER'], output_filename)
        
        try:
            # Load and process image
            img = Image.open(input_path).convert("RGB")
            img_tensor = transform(img).unsqueeze(0)
            
            # Run inference
            with torch.no_grad():
                predictions = model(img_tensor)
                
            pred_boxes = predictions[0]['boxes'].cpu().numpy()
            pred_scores = predictions[0]['scores'].cpu().numpy()
            pred_labels = predictions[0]['labels'].cpu().numpy()
            
            # Convert image to OpenCV format
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            if grayscale:
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                img_display = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            else:
                img_display = img_cv.copy()
            
            vehicle_count = {}
            threshold = 0.6
            
            # Draw detections
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
            
            # Save final image
            cv2.imwrite(output_path, img_display)
            
            total_detected = sum(vehicle_count.values())
            
            return jsonify({
                'success': True,
                'original_url': url_for('static', filename=f"uploads/{filename}"),
                'annotated_url': url_for('static', filename=f"results/{output_filename}"),
                'stats': vehicle_count,
                'total': total_detected
            })
            
        except Exception as e:
            print(f"Error during detection: {e}")
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Allowed file types are png, jpg, jpeg, webp'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
