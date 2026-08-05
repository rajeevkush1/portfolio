// Navigation functionality
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');
const navbar = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');

// Toggle mobile menu
hamburger?.addEventListener('click', () => {
    navMenu?.classList.toggle('active');
});

// Close mobile menu when clicking on a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu?.classList.remove('active');
    });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        navbar?.classList.add('scrolled');
    } else {
        navbar?.classList.remove('scrolled');
    }
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all sections and cards
document.querySelectorAll('section, .project-card, .skill-category, .stat-item, .cert-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Skill bars animation
const skillBars = document.querySelectorAll('.skill-progress');
const skillObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const width = entry.target.style.width;
            entry.target.style.width = '0';
            setTimeout(() => {
                entry.target.style.width = width;
            }, 100);
        }
    });
}, { threshold: 0.5 });

skillBars.forEach(bar => skillObserver.observe(bar));

// Active nav link on scroll
const sections = document.querySelectorAll('section[id]');

function highlightNav() {
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');
        const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            navLinks.forEach(link => link.classList.remove('active'));
            navLink?.classList.add('active');
        }
    });
}

window.addEventListener('scroll', highlightNav);

// Typing effect for hero subtitle (optional enhancement)
const subtitle = document.querySelector('.hero-subtitle');
if (subtitle) {
    const text = subtitle.textContent;
    subtitle.textContent = '';
    let i = 0;
    
    function typeWriter() {
        if (i < text.length) {
            subtitle.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, 50);
        }
    }
    
    setTimeout(typeWriter, 500);
}

// Parallax effect for gradient orbs
document.addEventListener('mousemove', (e) => {
    const orbs = document.querySelectorAll('.gradient-orb');
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    orbs.forEach((orb, index) => {
        const speed = (index + 1) * 20;
        orb.style.transform = `translate(${x * speed}px, ${y * speed}px)`;
    });
});

console.log('Portfolio loaded successfully! 🚀');

// ==========================================================================
// Chatbot Widget Functionality
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
    const chatbotTrigger = document.getElementById('chatbotTrigger');
    const chatbotWindow = document.getElementById('chatbotWindow');
    const chatbotClose = document.getElementById('chatbotClose');
    const chatbotMessages = document.getElementById('chatbotMessages');
    const chatbotInput = document.getElementById('chatbotInput');
    const chatbotSend = document.getElementById('chatbotSend');
    const chatbotTyping = document.getElementById('chatbotTyping');

    let chatHistory = [];
    // Default API URL (can be changed to production URL in deployment)
    const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? 'http://127.0.0.1:8000' 
        : 'http://127.0.0.1:8000'; // Default to localhost backend

    // Format simple markdown (bold and lists) and newlines
    function formatMessageText(text) {
        // Escape HTML to prevent XSS
        let formatted = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
        
        // Bold: **text** -> <strong>text</strong>
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Code blocks: `code` -> <code>code</code>
        formatted = formatted.replace(/`(.*?)`/g, '<code>$1</code>');

        // Newlines -> <br>
        formatted = formatted.replace(/\n/g, '<br>');

        return formatted;
    }

    // Add a message to the chat display
    function addMessage(sender, text) {
        if (!chatbotMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chatbot-message', sender);

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.innerHTML = formatMessageText(text);

        const timeSpan = document.createElement('span');
        timeSpan.classList.add('message-time');
        const now = new Date();
        timeSpan.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeSpan);
        chatbotMessages.appendChild(messageDiv);

        // Scroll to the bottom
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Toggle chatbot window
    chatbotTrigger?.addEventListener('click', () => {
        chatbotWindow?.classList.toggle('chatbot-hidden');
        
        // Remove notification dot once opened
        const notificationDot = chatbotTrigger.querySelector('.chatbot-notification-dot');
        if (notificationDot) {
            notificationDot.style.display = 'none';
        }

        // Focus input if opened
        if (chatbotWindow && !chatbotWindow.classList.contains('chatbot-hidden')) {
            chatbotInput?.focus();
        }
    });

    // Close chatbot window
    chatbotClose?.addEventListener('click', () => {
        chatbotWindow?.classList.add('chatbot-hidden');
    });

    // Send message function
    async function handleSendMessage() {
        if (!chatbotInput || !chatbotSend || !chatbotTyping || !chatbotMessages) return;
        
        const message = chatbotInput.value.trim();
        if (!message) return;

        // Display user message
        addMessage('user', message);
        chatbotInput.value = '';
        
        // Disable inputs while loading
        chatbotInput.disabled = true;
        chatbotSend.disabled = true;
        chatbotTyping.classList.remove('chatbot-hidden');
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

        try {
            const response = await fetch(`${API_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    history: chatHistory
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to get response');
            }

            // Hide typing indicator
            chatbotTyping.classList.add('chatbot-hidden');

            // Add bot response to UI
            addMessage('bot', data.response);

            // Update local history
            chatHistory.push({ role: 'user', content: message });
            chatHistory.push({ role: 'assistant', content: data.response });

        } catch (error) {
            console.error('Chatbot API Error:', error);
            chatbotTyping.classList.add('chatbot-hidden');
            addMessage('bot', `⚠️ Sorry, I ran into an error: ${error.message}. Please make sure the backend server is running and the GEMINI_API_KEY is configured.`);
        } finally {
            // Re-enable inputs
            chatbotInput.disabled = false;
            chatbotSend.disabled = false;
            chatbotInput.focus();
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        }
    }

    // Send button click
    chatbotSend?.addEventListener('click', handleSendMessage);

    // Enter key press in input
    chatbotInput?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });
});
