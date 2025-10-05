// Coffee Shop UI JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Navigation functionality
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Mobile menu toggle
    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });

    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Menu category filtering
    const categoryBtns = document.querySelectorAll('.category-btn');
    const menuItems = document.querySelectorAll('.menu-item');

    categoryBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            
            // Update active button
            categoryBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Filter menu items
            menuItems.forEach(item => {
                if (category === 'all' || item.getAttribute('data-category') === category) {
                    item.style.display = 'block';
                    item.style.animation = 'fadeIn 0.5s ease';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    // Shopping cart functionality
    let cart = [];
    const cartModal = document.getElementById('cart-modal');
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    const addToCartBtns = document.querySelectorAll('.add-to-cart');
    const closeModal = document.querySelector('.close');
    const clearCartBtn = document.getElementById('clear-cart');
    const checkoutBtn = document.getElementById('checkout');

    // Add to cart functionality
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const menuItem = this.closest('.menu-item');
            const name = menuItem.querySelector('h3').textContent;
            const price = parseFloat(menuItem.querySelector('.menu-item-price').textContent.replace('$', ''));
            const image = menuItem.querySelector('img').src;
            
            // Check if item already exists in cart
            const existingItem = cart.find(item => item.name === name);
            
            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                cart.push({
                    name: name,
                    price: price,
                    quantity: 1,
                    image: image
                });
            }
            
            updateCartDisplay();
            showMessage('Item added to cart!', 'success');
        });
    });

    // Update cart display
    function updateCartDisplay() {
        cartItems.innerHTML = '';
        
        if (cart.length === 0) {
            cartItems.innerHTML = '<p style="text-align: center; color: #666;">Your cart is empty</p>';
            cartTotal.textContent = '0.00';
            return;
        }
        
        let total = 0;
        
        cart.forEach((item, index) => {
            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            cartItem.innerHTML = `
                <div class="cart-item-info">
                    <h4>${item.name}</h4>
                    <p>$${item.price.toFixed(2)} each</p>
                </div>
                <div class="cart-item-controls">
                    <button class="quantity-btn" onclick="updateQuantity(${index}, -1)">-</button>
                    <span class="quantity">${item.quantity}</span>
                    <button class="quantity-btn" onclick="updateQuantity(${index}, 1)">+</button>
                    <button class="quantity-btn" onclick="removeItem(${index})" style="background: #dc3545; color: white; margin-left: 10px;">×</button>
                </div>
            `;
            cartItems.appendChild(cartItem);
            
            total += item.price * item.quantity;
        });
        
        cartTotal.textContent = total.toFixed(2);
    }

    // Update quantity
    window.updateQuantity = function(index, change) {
        cart[index].quantity += change;
        
        if (cart[index].quantity <= 0) {
            cart.splice(index, 1);
        }
        
        updateCartDisplay();
    };

    // Remove item
    window.removeItem = function(index) {
        cart.splice(index, 1);
        updateCartDisplay();
    };

    // Clear cart
    clearCartBtn.addEventListener('click', function() {
        cart = [];
        updateCartDisplay();
        showMessage('Cart cleared!', 'success');
    });

    // Checkout
    checkoutBtn.addEventListener('click', function() {
        if (cart.length === 0) {
            showMessage('Your cart is empty!', 'error');
            return;
        }
        
        // Simulate checkout process
        this.innerHTML = '<span class="loading"></span> Processing...';
        this.disabled = true;
        
        setTimeout(() => {
            showMessage('Order placed successfully! Thank you for your business!', 'success');
            cart = [];
            updateCartDisplay();
            cartModal.style.display = 'none';
            this.innerHTML = 'Checkout';
            this.disabled = false;
        }, 2000);
    });

    // Modal functionality
    closeModal.addEventListener('click', function() {
        cartModal.style.display = 'none';
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === cartModal) {
            cartModal.style.display = 'none';
        }
    });

    // Show cart modal when clicking "Order Now" buttons
    const orderBtns = document.querySelectorAll('.btn-primary');
    orderBtns.forEach(btn => {
        if (btn.textContent.includes('Order')) {
            btn.addEventListener('click', function() {
                cartModal.style.display = 'block';
            });
        }
    });

    // Scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.feature-card, .menu-item, .about-text, .about-image');
    animatedElements.forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });

    // Form submission
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            submitBtn.innerHTML = '<span class="loading"></span> Sending...';
            submitBtn.disabled = true;
            
            setTimeout(() => {
                showMessage('Message sent successfully! We\'ll get back to you soon.', 'success');
                this.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }

    // Newsletter subscription
    const newsletterForm = document.querySelector('.newsletter');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = this.querySelector('input[type="email"]').value;
            if (email) {
                showMessage('Thank you for subscribing!', 'success');
                this.querySelector('input[type="email"]').value = '';
            }
        });
    }

    // Show message function
    function showMessage(text, type) {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => msg.remove());
        
        const message = document.createElement('div');
        message.className = `message ${type}`;
        message.textContent = text;
        
        // Insert message at the top of the page
        const hero = document.querySelector('.hero');
        hero.insertBefore(message, hero.firstChild);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            message.remove();
        }, 3000);
    }

    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });

    // Hero button functionality
    const heroButtons = document.querySelectorAll('.hero-buttons .btn');
    heroButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.textContent.includes('Order')) {
                cartModal.style.display = 'block';
            } else if (this.textContent.includes('Menu')) {
                document.querySelector('#menu').scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add hover effects to menu items
    menuItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Add loading animation to buttons
    const allButtons = document.querySelectorAll('.btn');
    allButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            if (!this.disabled && !this.classList.contains('loading')) {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 150);
            }
        });
    });

    // Initialize cart display
    updateCartDisplay();

    // Add some interactive features
    addInteractiveFeatures();
});

// Additional interactive features
function addInteractiveFeatures() {
    // Parallax effect for hero section
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero');
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });

    // Add click animation to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // Add typing effect to hero title
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        let i = 0;
        
        function typeWriter() {
            if (i < text.length) {
                heroTitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        }
        
        // Start typing effect after a short delay
        setTimeout(typeWriter, 500);
    }

    // Add coffee bean animation
    createCoffeeBeans();
}

// Create floating coffee beans animation
function createCoffeeBeans() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    for (let i = 0; i < 5; i++) {
        const bean = document.createElement('div');
        bean.innerHTML = '☕';
        bean.style.position = 'absolute';
        bean.style.fontSize = '20px';
        bean.style.color = '#8B4513';
        bean.style.opacity = '0.3';
        bean.style.left = Math.random() * 100 + '%';
        bean.style.top = Math.random() * 100 + '%';
        bean.style.animation = `float ${3 + Math.random() * 4}s ease-in-out infinite`;
        bean.style.pointerEvents = 'none';
        
        hero.appendChild(bean);
    }
}

// Add CSS for floating animation
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);

