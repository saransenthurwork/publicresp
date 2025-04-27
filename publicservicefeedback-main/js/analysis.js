function analyzeFeedback() {
    const feedback = document.getElementById('feedbackText').value;
    if (!feedback) {
        alert('Please enter feedback text');
        return;
    }
    displayResults([feedback]);
}

function analyzeFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        const text = e.target.result;
        const feedbacks = text.split('\n')
            .slice(1) // Skip header
            .filter(line => line.trim())
            .map(line => line.replace(/^"|"$/g, '')); // Remove quotes
        
        displayResults(feedbacks);
    };
    reader.readAsText(file);
}

function displayResults(feedbacks) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<h2>Analysis Results</h2>';

    const summaryHtml = feedbacks.map(feedback => `
        <div class="feedback-item">
            <p>${feedback}</p>
            <div class="sentiment">
                ${analyzeSentiment(feedback)}
            </div>
        </div>
    `).join('');

    resultsDiv.innerHTML += summaryHtml;
}

function analyzeSentiment(feedback) {
    // Simple sentiment analysis based on keywords
    const positiveWords = ['good', 'satisfied', 'helpful', 'appreciate'];
    const negativeWords = ['poor', 'bad', 'terrible', 'worst'];
    
    const lowerFeedback = feedback.toLowerCase();
    let sentiment = 'neutral';

    if (positiveWords.some(word => lowerFeedback.includes(word))) {
        sentiment = 'positive';
    } else if (negativeWords.some(word => lowerFeedback.includes(word))) {
        sentiment = 'negative';
    }

    return `Sentiment: <span class="${sentiment}">${sentiment}</span>`;
}
