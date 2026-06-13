/**
 * KYC Chatbot Frontend
 * Manages conversation state and communicates with backend API
 */

// ========================================
// STATE MANAGEMENT
// ========================================

// Conversation history (stored in browser memory)
let conversationHistory = [];

// Backend API URL (change this when deploying)
// const API_URL = 'http://localhost:5001';
const API_URL = 'https://trustworthy-essence-production-324d.up.railway.app';

// DOM elements
const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const statusSpan = document.getElementById('status');
const tokenInfo = document.getElementById('tokenInfo');

// ========================================
// INITIALIZE
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('Chat application loaded');
    
    // Fetch backend configuration
    fetchConfig();
    
    // Add event listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    // Welcome message
    addMessageToChat('assistant', 'Hi! 👋 I\'m your KYC assistant. Ask me anything about onboarding, documents, or verification.');
});

// ========================================
// FETCH BACKEND CONFIG
// ========================================

async function fetchConfig() {
    try {
        const response = await fetch(`${API_URL}/api/config`);
        const config = await response.json();
        console.log('Backend config:', config);
        // You can use config.max_tokens, config.model here if needed
    } catch (error) {
        console.error('Failed to fetch config:', error);
        updateStatus('⚠️ Could not connect to backend');
    }
}

// ========================================
// SEND MESSAGE
// ========================================

async function sendMessage() {
    // Get user input
    const userMessage = userInput.value.trim();
    
    // Validation
    if (!userMessage) {
        alert('Please enter a question');
        return;
    }
    
    // Add user message to chat
    addMessageToChat('user', userMessage);
    
    // Add to conversation history
    conversationHistory.push({
        role: 'user',
        content: userMessage
    });
    
    // Clear input field
    userInput.value = '';
    
    // Disable send button while processing
    sendBtn.disabled = true;
    updateStatus('Thinking...');
    
    try {
        // Call backend API
        const response = await fetch(`${API_URL}/api/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                conversation: conversationHistory
            })
        });
        
        // Check if response is OK
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'API request failed');
        }
        
        // Parse response
        const data = await response.json();
        const assistantMessage = data.answer;
        const tokensUsed = data.tokens_used;
        
        // Add assistant message to chat
        addMessageToChat('assistant', assistantMessage);
        
        // Add to conversation history
        conversationHistory.push({
            role: 'assistant',
            content: assistantMessage
        });
        
        // Update status with token info
        updateStatus('Ready');
        updateTokenInfo(tokensUsed);
        
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('assistant', `❌ Error: ${error.message}`);
        updateStatus('Error - check console');
    } finally {
        // Re-enable send button
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// ========================================
// ADD MESSAGE TO CHAT
// ========================================

function addMessageToChat(role, message) {
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    // Add text (with line breaks preserved)
    // Format the message: convert line breaks and preserve spacing
    const formattedMessage = message
        .replace(/\n/g, '<br>')                    // Convert \n to <br>
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Convert **text** to <strong>
        .replace(/\*(.*?)\*/g, '<em>$1</em>');     // Convert *text* to <em>
    
    messageDiv.innerHTML = formattedMessage;
    
    // Add to chat box
    chatBox.appendChild(messageDiv);
    
    // Auto-scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

// ========================================
// UPDATE STATUS
// ========================================

function updateStatus(status) {
    statusSpan.textContent = status;
}

// ========================================
// UPDATE TOKEN INFO
// ========================================

function updateTokenInfo(tokens) {
    // Haiku pricing: $0.00080 per 1K input, $0.004 per 1K output
    // Rough estimate: total tokens cost
    const estimatedCost = (tokens * 0.004 / 1000).toFixed(4);
    tokenInfo.textContent = `Tokens: ${tokens} (~$${estimatedCost})`;
}