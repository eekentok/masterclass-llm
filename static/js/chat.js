// Chat Interface JavaScript
class ChatInterface {
    constructor() {
        this.chatHistory = [];
        this.isLoading = false;
        this.init();
    }

    init() {
        this.setupElements();
        this.setupEventListeners();
        this.setWelcomeTime();
        this.checkConnection();
        this.autoResizeTextarea();
    }

    setupElements() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.charCount = document.getElementById('charCount');
        this.clearChatBtn = document.getElementById('clearChat');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        this.quickButtons = document.querySelectorAll('.quick-btn');
    }

    setupEventListeners() {
        // Send message on button click
        this.sendButton.addEventListener('click', () => this.sendMessage());

        // Send message on Enter key (Shift+Enter for new line)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.updateCharCount();
            this.autoResizeTextarea();
        });

        // Clear chat
        this.clearChatBtn.addEventListener('click', () => this.clearChat());

        // Quick action buttons
        this.quickButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const question = btn.getAttribute('data-question');
                this.messageInput.value = question;
                this.sendMessage();
            });
        });

        // Enable/disable send button based on input
        this.messageInput.addEventListener('input', () => {
            this.sendButton.disabled = !this.messageInput.value.trim();
        });
    }

    setWelcomeTime() {
        const welcomeTime = document.getElementById('welcomeTime');
        if (welcomeTime) {
            welcomeTime.textContent = this.formatTime(new Date());
        }
    }

    async checkConnection() {
        try {
            const response = await fetch('/api/health');
            if (response.ok) {
                this.updateStatus('connected', 'Bağlandı');
            } else {
                this.updateStatus('error', 'Bağlantı Hatası');
            }
        } catch (error) {
            this.updateStatus('error', 'Bağlantı Hatası');
        }
    }

    updateStatus(type, text) {
        this.statusDot.className = `status-dot ${type}`;
        this.statusText.textContent = text;
    }

    updateCharCount() {
        const count = this.messageInput.value.length;
        this.charCount.textContent = `${count}/1000`;
        
        // Change color when approaching limit
        if (count > 900) {
            this.charCount.style.color = '#ef4444';
        } else if (count > 800) {
            this.charCount.style.color = '#f59e0b';
        } else {
            this.charCount.style.color = '#6b7280';
        }
    }

    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isLoading) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.autoResizeTextarea();
        this.updateCharCount();
        this.sendButton.disabled = true;

        // Show loading
        this.showLoading();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    history: this.chatHistory
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Add bot response to chat
                this.addMessage(data.answer, 'bot');
                
                // Update chat history
                this.chatHistory.push({ role: 'user', content: message });
                this.chatHistory.push({ role: 'assistant', content: data.answer });
                
                // Limit history size
                if (this.chatHistory.length > 20) {
                    this.chatHistory = this.chatHistory.slice(-20);
                }
            } else {
                this.addMessage(`Hata: ${data.error || 'Bilinmeyen bir hata oluştu'}`, 'bot');
            }
        } catch (error) {
            this.addMessage('Bağlantı hatası oluştu. Lütfen tekrar deneyin.', 'bot');
        } finally {
            this.hideLoading();
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        
        const icon = document.createElement('i');
        icon.className = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
        avatar.appendChild(icon);

        const content = document.createElement('div');
        content.className = 'message-content';

        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = text;

        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = this.formatTime(new Date());

        content.appendChild(messageText);
        content.appendChild(messageTime);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    showLoading() {
        this.isLoading = true;
        this.loadingOverlay.classList.add('show');
        this.messageInput.disabled = true;
    }

    hideLoading() {
        this.isLoading = false;
        this.loadingOverlay.classList.remove('show');
        this.messageInput.disabled = false;
        this.messageInput.focus();
    }

    clearChat() {
        if (confirm('Sohbet geçmişini temizlemek istediğinizden emin misiniz?')) {
            // Keep only the welcome message
            const welcomeMessage = this.chatMessages.querySelector('.bot-message');
            this.chatMessages.innerHTML = '';
            if (welcomeMessage) {
                this.chatMessages.appendChild(welcomeMessage);
            }
            
            // Clear chat history
            this.chatHistory = [];
            
            // Add new welcome message if none exists
            if (!welcomeMessage) {
                this.addMessage('Merhaba! Ben İş Bankası AI Asistanınız. Bankacılık ürünleri, hizmetler ve işlemler hakkında sorularınızı yanıtlamaya hazırım. Size nasıl yardımcı olabilirim?', 'bot');
            }
        }
    }

    formatTime(date) {
        return date.toLocaleTimeString('tr-TR', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// Initialize chat interface when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatInterface();
});

// Add some utility functions for better UX
document.addEventListener('DOMContentLoaded', () => {
    // Prevent form submission on Enter
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.target.tagName === 'TEXTAREA') {
            if (!e.shiftKey) {
                e.preventDefault();
            }
        }
    });

    // Add smooth scrolling to chat container
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.style.scrollBehavior = 'smooth';
    }

    // Add focus management
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        // Focus input when clicking on chat area
        document.querySelector('.chat-container').addEventListener('click', (e) => {
            if (e.target.closest('.chat-messages') || e.target.closest('.chat-input-container')) {
                messageInput.focus();
            }
        });
    }
}); 