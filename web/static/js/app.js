// Nutrition Advisor Web App - Main JavaScript

class NutritionAdvisorApp {
    constructor() {
        this.apiBase = '/api';
        this.sessionId = this.generateSessionId();
        this.chatMessages = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadTheme();
        this.showWelcomeMessage();
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    setupEventListeners() {
        const sendButton = document.getElementById('send-button');
        const chatInput = document.getElementById('chat-input');
        const themeToggle = document.getElementById('theme-toggle');

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
        bubble.textContent = message.text;

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

