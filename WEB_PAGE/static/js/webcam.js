document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('canvas');
    const captureBtn = document.getElementById('capture-btn');
    const enhanceContainer = document.getElementById('enhance-container');
    const statusDiv = document.getElementById('status');
    const emotionResult = document.getElementById('emotion-result');
    const emotionText = document.getElementById('emotion-text');
    const confidenceText = document.getElementById('confidence-text');
    const confidenceBar = document.getElementById('confidence-bar');
    
    // Access the webcam
    async function startWebcam() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                },
                audio: false 
            });
            video.srcObject = stream;
            statusDiv.innerHTML = 'Camera is active! Click "Detect Emotion" when ready.';
            statusDiv.className = 'alert alert-success text-center';
            captureBtn.disabled = false;
        } catch (err) {
            statusDiv.innerHTML = `Camera access error: ${err.message}`;
            statusDiv.className = 'alert alert-danger text-center';
            console.error('Error accessing webcam:', err);
        }
    }
    
    // Capture image and detect emotion
    async function captureImage() {
        statusDiv.innerHTML = 'Detecting emotion...';
        statusDiv.className = 'alert alert-info text-center';
        captureBtn.disabled = true;
        
        // Draw video frame to canvas
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Get the image data
        const imageData = canvas.toDataURL('image/jpeg');
        
        try {
            // Send to backend for processing
            const response = await fetch('/detect_emotion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image_data: imageData }),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.status === 'success') {
                // Update UI with emotion results
                emotionText.textContent = result.emotion.charAt(0).toUpperCase() + result.emotion.slice(1);
                
                const confidenceValue = Math.round(result.confidence);
                confidenceText.textContent = confidenceValue;
                confidenceBar.style.width = `${confidenceValue}%`;
                confidenceBar.setAttribute('aria-valuenow', confidenceValue);
                
                // Set color based on emotion
                let barColor = 'bg-primary';
                if (result.emotion === 'happy' || result.emotion === 'surprise') {
                    barColor = 'bg-success';
                } else if (result.emotion === 'angry' || result.emotion === 'disgust') {
                    barColor = 'bg-danger';
                } else if (result.emotion === 'sad' || result.emotion === 'fear') {
                    barColor = 'bg-warning';
                } else {
                    barColor = 'bg-info';
                }
                confidenceBar.className = `progress-bar ${barColor}`;
                
                // Show results and enhance button
                emotionResult.style.display = 'block';
                enhanceContainer.style.display = 'block';
                
                statusDiv.innerHTML = 'Emotion detected! Click "Enhance My Mood" to continue.';
                statusDiv.className = 'alert alert-success text-center';
            } else {
                throw new Error(result.error || 'Unknown error');
            }
        } catch (err) {
            statusDiv.innerHTML = `Error detecting emotion: ${err.message}`;
            statusDiv.className = 'alert alert-danger text-center';
            console.error('Error:', err);
        } finally {
            captureBtn.disabled = false;
        }
    }
    
    // Event listeners
    captureBtn.addEventListener('click', captureImage);
    
    // Start webcam when page loads
    startWebcam();
});