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

// Motion UI Reveal Observer
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('motion-reveal-active');
        }
    });
}, observerOptions);

// Observe sections without destroying keyframe transform rules
document.querySelectorAll('section, .skill-category, .stat-item').forEach(el => {
    el.classList.add('motion-reveal');
    observer.observe(el);
});

/* ==========================================================================
   Motion UI Custom Cursor & Interactive 3D Tilt System
   ========================================================================== */

const customCursor = document.getElementById('customCursor');
const cursorFollower = document.getElementById('cursorFollower');

if (customCursor && cursorFollower && window.innerWidth > 768) {
    let mouseX = 0, mouseY = 0;
    let followerX = 0, followerY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        customCursor.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0) translate(-50%, -50%)`;
    });

    function animateFollower() {
        followerX += (mouseX - followerX) * 0.12;
        followerY += (mouseY - followerY) * 0.12;
        cursorFollower.style.transform = `translate3d(${followerX}px, ${followerY}px, 0) translate(-50%, -50%)`;
        requestAnimationFrame(animateFollower);
    }
    animateFollower();

    // Hover scale expansion on interactive elements
    const interactiveElements = document.querySelectorAll('a, button, .project-card, .skill-pill, .stat-item, .cert-item');
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            customCursor.classList.add('active');
            cursorFollower.classList.add('active');
        });
        el.addEventListener('mouseleave', () => {
            customCursor.classList.remove('active');
            cursorFollower.classList.remove('active');
        });
    });
}

// 3D Motion Card Tilt Effect on Mouse Move
document.querySelectorAll('.skill-category, .stat-item').forEach(card => {
    card.classList.add('tilt-card');
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -8;
        const rotateY = ((x - centerX) / centerX) * 8;
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
    });
});


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

/* ==========================================================================
   GSAP & ScrollTrigger Motion System (Framer Motion / GSAP Grade)
   ========================================================================== */

if (typeof gsap !== 'undefined') {
    if (typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
    }

    // 1. Hero Staggered Entrance Reveal
    const heroTl = gsap.timeline();
    heroTl.from('.hero-title .greeting', { opacity: 0, y: 30, duration: 0.8, ease: 'power3.out' })
          .from('.name-highlight', { opacity: 0, scale: 0.9, y: 20, duration: 0.9, ease: 'back.out(1.7)' }, '-=0.5')
          .from('.hero-subtitle', { opacity: 0, y: 20, duration: 0.7, ease: 'power3.out' }, '-=0.4')
          .from('.hero-description', { opacity: 0, y: 20, duration: 0.7, ease: 'power3.out' }, '-=0.4')
          .from('.hero-buttons .btn', { opacity: 0, y: 25, stagger: 0.15, duration: 0.8, ease: 'power3.out' }, '-=0.4')
          .from('.social-link', { opacity: 0, scale: 0.5, stagger: 0.1, duration: 0.6, ease: 'back.out(1.7)' }, '-=0.4')
          .from('.hero-visual', { opacity: 0, x: 40, duration: 1, ease: 'power3.out' }, '-=0.8');

    // 2. Multi-Layer Parallax Depth Scrolling
    if (typeof ScrollTrigger !== 'undefined') {
        gsap.to('.orb-1', {
            scrollTrigger: { trigger: 'body', start: 'top top', end: 'bottom bottom', scrub: 1.5 },
            y: 250,
            scale: 1.2
        });
        gsap.to('.orb-2', {
            scrollTrigger: { trigger: 'body', start: 'top top', end: 'bottom bottom', scrub: 2 },
            y: -300,
            scale: 0.8
        });
        gsap.to('.hero-visual', {
            scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1 },
            y: 120,
            opacity: 0.4
        });

        // 3. Scroll-Triggered Section Headers Reveal
        gsap.utils.toArray('.section-header').forEach(header => {
            gsap.from(header.children, {
                scrollTrigger: { trigger: header, start: 'top 85%', toggleActions: 'play none none reverse' },
                opacity: 0,
                y: 40,
                stagger: 0.15,
                duration: 0.8,
                ease: 'power3.out'
            });
        });

        // 4. Staggered Skill Pills Cascade Reveal
        gsap.utils.toArray('.skill-category').forEach(cat => {
            gsap.from(cat.querySelectorAll('.skill-pill'), {
                scrollTrigger: { trigger: cat, start: 'top 80%', toggleActions: 'play none none reverse' },
                opacity: 0,
                scale: 0.8,
                y: 15,
                stagger: 0.05,
                duration: 0.5,
                ease: 'back.out(1.5)'
            });
        });
    }

    // 5. Magnetic Micro-Interactions on Hover
    document.querySelectorAll('.btn-primary, .btn-secondary, .social-link').forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            gsap.to(btn, { x: x * 0.35, y: y * 0.35, duration: 0.3, ease: 'power2.out' });
        });
        btn.addEventListener('mouseleave', () => {
            gsap.to(btn, { x: 0, y: 0, duration: 0.5, ease: 'elastic.out(1, 0.4)' });
        });
    });
}

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
function initChatbot() {
    const chatbotTrigger = document.getElementById('chatbotTrigger');
    const chatbotWindow = document.getElementById('chatbotWindow');
    const chatbotClose = document.getElementById('chatbotClose');
    const chatbotMessages = document.getElementById('chatbotMessages');
    const chatbotInput = document.getElementById('chatbotInput');
    const chatbotSend = document.getElementById('chatbotSend');
    const chatbotTyping = document.getElementById('chatbotTyping');

    if (!chatbotTrigger || !chatbotWindow) return;

    let chatHistory = [];
    // Dynamic API URL: use current origin if on http server, fallback to http://127.0.0.1:8000
    const API_URL = (window.location.protocol.startsWith('http'))
        ? window.location.origin 
        : 'http://127.0.0.1:8000';

    // Format simple markdown (bold and lists) and newlines
    function formatMessageText(text) {
        // Strip self-referential intro phrases if present
        let cleanedText = text
            .replace(/^(As|I'm|I am) Rajeev'?s Virtual Assistant[.,:]?\s*/i, '')
            .replace(/^As an AI assistant[.,:]?\s*/i, '');

        // Escape HTML to prevent XSS
        let formatted = cleanedText
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
    chatbotTrigger.addEventListener('click', () => {
        chatbotWindow.classList.toggle('chatbot-hidden');
        
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
        chatbotWindow.classList.add('chatbot-hidden');
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
            addMessage('bot', `⚠️ Sorry, I ran into an error connecting to backend: ${error.message}. Please verify the server is running on http://127.0.0.1:8000.`);
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
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChatbot);
} else {
    initChatbot();
}

