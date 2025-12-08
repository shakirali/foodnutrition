// Nutrition Advisor Web App - Main JavaScript

class NutritionAdvisorApp {
    constructor() {
        this.apiBase = '/api';
        this.sessionId = this.generateSessionId();
        this.chatMessages = [];
        this.voiceEnabled = false;
        this.currentAudio = null;
        this.recognition = null;
        this.isRecording = false;
        this.speechSupported = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadTheme();
        this.loadVoiceSetting();
        this.initSpeechRecognition();
        this.showWelcomeMessage();
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    setupEventListeners() {
        const sendButton = document.getElementById('send-button');
        const chatInput = document.getElementById('chat-input');
        const themeToggle = document.getElementById('theme-toggle');
        const voiceToggle = document.getElementById('voice-toggle');
        const micButton = document.getElementById('mic-button');

        // Send message on button click
        sendButton.addEventListener('click', () => this.sendMessage());

        // Send message on Enter (Shift+Enter for new line)
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        chatInput.addEventListener('input', () => {
            chatInput.style.height = 'auto';
            chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
        });

        // Theme toggle
        themeToggle.addEventListener('click', () => this.toggleTheme());

        // Voice toggle
        voiceToggle.addEventListener('click', () => this.toggleVoice());

        // Microphone button
        micButton.addEventListener('click', () => this.toggleSpeechRecognition());

        // Quick action buttons
        document.querySelectorAll('.action-button').forEach(button => {
            button.addEventListener('click', (e) => {
                const action = e.currentTarget.dataset.action;
                this.handleQuickAction(action);
            });
        });
    }

    showWelcomeMessage() {
        const welcomeMessage = {
            type: 'agent',
            text: "👋 Hello! I'm your Nutrition Advisor. I'm here to help you achieve your nutrition goals.\n\nWhat's your name?",
            timestamp: new Date()
        };
        this.addMessage(welcomeMessage);
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();

        if (!message) return;

        // Add user message to chat
        this.addMessage({
            type: 'user',
            text: message,
            timestamp: new Date()
        });

        // Clear input
        input.value = '';
        input.style.height = 'auto';

        // Show typing indicator
        this.showTypingIndicator();

        // Disable send button
        const sendButton = document.getElementById('send-button');
        sendButton.disabled = true;

        try {
            // Send to API
            const response = await fetch(`${this.apiBase}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Remove typing indicator
            this.hideTypingIndicator();

            // Add agent response
            this.addMessage({
                type: 'agent',
                text: data.response,
                timestamp: new Date()
            });

            // Play audio if voice is enabled
            if (this.voiceEnabled) {
                await this.playAudioResponse(data.response);
            }

        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage({
                type: 'agent',
                text: 'Sorry, I encountered an error. Please try again.',
                timestamp: new Date()
            });
        } finally {
            sendButton.disabled = false;
        }
    }

    addMessage(message) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageElement = document.createElement('div');
        messageElement.className = `chat-message ${message.type}`;

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        // Parse markdown if it's an agent message, otherwise use plain text
        if (message.type === 'agent' && typeof marked !== 'undefined') {
            // Use marked.js to parse markdown to HTML
            bubble.innerHTML = marked.parse(message.text);
        } else {
            // Use plain text for user messages (or if marked.js not available)
            bubble.textContent = message.text;
        }

        const timestamp = document.createElement('div');
        timestamp.className = 'message-timestamp';
        timestamp.textContent = this.formatTime(message.timestamp);

        messageElement.appendChild(bubble);
        messageElement.appendChild(timestamp);
        messagesContainer.appendChild(messageElement);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Store message
        this.chatMessages.push(message);
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        const typingElement = document.createElement('div');
        typingElement.className = 'chat-message agent';
        typingElement.id = 'typing-indicator';
        
        const typingBubble = document.createElement('div');
        typingBubble.className = 'typing-indicator';
        typingBubble.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        typingElement.appendChild(typingBubble);
        messagesContainer.appendChild(typingElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    handleQuickAction(action) {
        const actions = {
            'analyze-meals': "Can you help me analyze my meals today? I'd like to know if my breakfast, lunch, and dinner have good nutrition.",
            'check-requirements': 'How much nutrition do I need per day?',
            'find-foods': 'Can you help me find foods rich in nutrients?',
            'compare-foods': 'I want to compare different foods nutritionally.'
        };

        const message = actions[action];
        if (message) {
            document.getElementById('chat-input').value = message;
            this.sendMessage();
        }
    }

    formatTime(date) {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        this.updateThemeIcon(newTheme);
    }

    toggleVoice() {
        this.voiceEnabled = !this.voiceEnabled;
        // Stop audio if disabling voice
        if (!this.voiceEnabled && this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio = null;
        }
        this.updateVoiceIcon();
        this.saveVoiceSetting();
    }

    updateVoiceIcon() {
        const voiceToggle = document.getElementById('voice-toggle');
        const voiceIcon = document.getElementById('voice-icon');
        
        if (this.voiceEnabled) {
            voiceIcon.textContent = '🔊';
            voiceToggle.classList.add('active');
            voiceToggle.setAttribute('title', 'Voice responses enabled');
        } else {
            voiceIcon.textContent = '🔇';
            voiceToggle.classList.remove('active');
            voiceToggle.setAttribute('title', 'Voice responses disabled');
        }
    }

    loadVoiceSetting() {
        const saved = localStorage.getItem('voiceEnabled');
        if (saved !== null) {
            this.voiceEnabled = saved === 'true';
        }
        this.updateVoiceIcon();
    }

    saveVoiceSetting() {
        localStorage.setItem('voiceEnabled', this.voiceEnabled.toString());
    }

    async playAudioResponse(text) {
        try {
            if (this.currentAudio) {
                this.currentAudio.pause();
                this.currentAudio = null;
            }

        // Strip markdown before sending to TTS
        const plainText = this.stripMarkdown(text);

        // Call TTS endpoint
        const response = await fetch(`${this.apiBase}/tts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: plainText }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        this.currentAudio = audio;

        audio.addEventListener('ended', () => {
            URL.revokeObjectURL(audioUrl);
            this.currentAudio = null;
        });

        audio.addEventListener('error', (e) => {
            console.error('Audio playback error:', e);
            URL.revokeObjectURL(audioUrl);
            this.currentAudio = null;
        });

        await audio.play();

        } catch (error) {
            console.error('Error playing audio:', error);
        }
    }

    stripMarkdown(markdownText) {
        if (typeof marked === 'undefined') {
            // Fallback: simple regex stripping
            return this.simpleMarkdownStrip(markdownText);
        }
        
        try {
            // Parse markdown to HTML
            const html = marked.parse(markdownText);
            
            // Create temporary DOM element to extract text
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;
            
            // Get plain text content (strips all HTML tags)
            let plainText = tempDiv.textContent || tempDiv.innerText || '';
            
            // Clean up extra whitespace and normalize
            plainText = plainText
                .replace(/\n{3,}/g, '\n\n')      // Max 2 consecutive newlines
                .replace(/[ \t]+/g, ' ')          // Multiple spaces to single space
                .replace(/\s+$/gm, '')            // Trailing whitespace on each line
                .trim();
            
            return plainText;
        } catch (error) {
            console.warn('Error stripping markdown, using fallback:', error);
            return this.simpleMarkdownStrip(markdownText);
        }
    }

    simpleMarkdownStrip(text) {
        // Fallback regex-based stripping
        return text
            .replace(/```[\s\S]*?```/g, '')           // Code blocks
            .replace(/`([^`]+)`/g, '$1')               // Inline code
            .replace(/^#{1,6}\s+(.+)$/gm, '$1')        // Headers
            .replace(/\*\*([^*]+)\*\*/g, '$1')         // Bold
            .replace(/\*([^*]+)\*/g, '$1')             // Italic
            .replace(/__([^_]+)__/g, '$1')             // Bold (alt)
            .replace(/_([^_]+)_/g, '$1')               // Italic (alt)
            .replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1')  // Links
            .replace(/^>\s+(.+)$/gm, '$1')             // Blockquotes
            .replace(/^[\*\-\+]\s+(.+)$/gm, '$1')      // Unordered lists
            .replace(/^\d+\.\s+(.+)$/gm, '$1')         // Ordered lists
            .replace(/^---+$/gm, '')                   // Horizontal rules
            .replace(/\n{3,}/g, '\n\n')                 // Multiple newlines
            .replace(/[ \t]+/g, ' ')                   // Multiple spaces
            .trim();
    }

    initSpeechRecognition() {
        // Check for browser support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            console.warn('Speech recognition not supported in this browser');
            this.speechSupported = false;
            // Optionally hide or disable microphone button
            const micButton = document.getElementById('mic-button');
            if (micButton) {
                micButton.style.display = 'none';
            }
            return;
        }
        
        this.speechSupported = true;
        
        // Initialize recognition
        this.recognition = new SpeechRecognition();
        
        // Configure recognition settings
        this.recognition.continuous = false;  // Stop after first result
        this.recognition.interimResults = false;  // Only return final results
        this.recognition.lang = 'en-US';  // Set language (can be made configurable)
        
        // Set up event handlers
        this.recognition.onstart = () => {
            this.isRecording = true;
            this.updateMicButton();
        };
        
        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            this.handleSpeechResult(transcript);
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.handleSpeechError(event.error);
        };
        
        this.recognition.onend = () => {
            this.isRecording = false;
            this.updateMicButton();
        };
    }

    toggleSpeechRecognition() {
        if (!this.speechSupported || !this.recognition) {
            alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.');
            return;
        }
        
        if (this.isRecording) {
            // Stop recording
            this.recognition.stop();
        } else {
            // Start recording
            try {
                this.recognition.start();
            } catch (error) {
                // Handle case where recognition is already running
                if (error.name === 'InvalidStateError') {
                    console.warn('Recognition already started');
                } else {
                    console.error('Error starting recognition:', error);
                }
            }
        }
    }

    handleSpeechResult(transcript) {
        // Clean up transcript (remove extra spaces, capitalize first letter)
        const cleanedTranscript = transcript.trim();
        
        if (!cleanedTranscript) {
            return;  // Ignore empty results
        }
        
        // Set the transcript in the input field
        const chatInput = document.getElementById('chat-input');
        chatInput.value = cleanedTranscript;
        
        // Auto-resize textarea
        chatInput.style.height = 'auto';
        chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
        
        // Optional: Automatically send the message
        // Uncomment the line below if you want auto-send
        // this.sendMessage();
        
        // Or just focus the input so user can review/edit before sending
        chatInput.focus();
    }

    handleSpeechError(error) {
        this.isRecording = false;
        this.updateMicButton();
        
        let errorMessage = 'Speech recognition error. ';
        
        switch (error) {
            case 'no-speech':
                errorMessage += 'No speech detected. Please try again.';
                break;
            case 'audio-capture':
                errorMessage += 'No microphone found. Please check your microphone.';
                break;
            case 'not-allowed':
                errorMessage += 'Microphone permission denied. Please allow microphone access.';
                break;
            case 'network':
                errorMessage += 'Network error. Please check your connection.';
                break;
            case 'aborted':
                // User stopped recording - not really an error
                return;
            default:
                errorMessage += `Unknown error: ${error}`;
        }
        
        // Show error to user (you can customize this)
        console.error(errorMessage);
        // Optionally show a toast notification or alert
        // alert(errorMessage);
    }

    updateMicButton() {
        const micButton = document.getElementById('mic-button');
        const micIcon = document.getElementById('mic-icon');
        
        if (!micButton || !micIcon) return;
        
        if (this.isRecording) {
            micButton.classList.add('recording');
            micButton.setAttribute('title', 'Recording... Click to stop');
            micIcon.textContent = '🔴';  // Red circle when recording
        } else {
            micButton.classList.remove('recording');
            micButton.setAttribute('title', 'Click to speak');
            micIcon.textContent = '🎤';  // Microphone icon when not recording
        }
    }
        
    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        this.updateThemeIcon(savedTheme);
    }

    updateThemeIcon(theme) {
        const themeToggle = document.getElementById('theme-toggle');
        themeToggle.querySelector('span').textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new NutritionAdvisorApp();
});

