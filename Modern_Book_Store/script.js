// Modern Book Store JavaScript
class BookStore {
    constructor() {
        this.books = [];
        this.filteredBooks = [];
        this.cart = [];
        this.wishlist = [];
        this.currentView = 'grid';
        this.currentPage = 1;
        this.booksPerPage = 12;
        
        this.init();
    }

    init() {
        this.loadBooks();
        this.setupEventListeners();
        this.updateCartCount();
        this.updateWishlistCount();
    }

    // Load books data with dummy data and online images
    loadBooks() {
        this.books = [
            {
                id: 1,
                title: "The Great Gatsby",
                author: "F. Scott Fitzgerald",
                genre: "fiction",
                price: 45.99,
                originalPrice: 59.99,
                rating: 4.5,
                image: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300&h=400&fit=crop",
                description: "A classic American novel set in the Jazz Age, exploring themes of wealth, love, and the American Dream.",
                pages: 180,
                published: "1925",
                badge: "Bestseller"
            },
            {
                id: 2,
                title: "To Kill a Mockingbird",
                author: "Harper Lee",
                genre: "fiction",
                price: 38.50,
                originalPrice: 45.00,
                rating: 4.8,
                image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=400&fit=crop",
                description: "A gripping tale of racial injustice and childhood innocence in the American South.",
                pages: 281,
                published: "1960",
                badge: "Classic"
            },
            {
                id: 3,
                title: "1984",
                author: "George Orwell",
                genre: "sci-fi",
                price: 42.00,
                originalPrice: 50.00,
                rating: 4.7,
                image: "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=300&h=400&fit=crop",
                description: "A dystopian social science fiction novel about totalitarian control and surveillance.",
                pages: 328,
                published: "1949",
                badge: "Must Read"
            },
            {
                id: 4,
                title: "Pride and Prejudice",
                author: "Jane Austen",
                genre: "romance",
                price: 35.75,
                originalPrice: 42.00,
                rating: 4.6,
                image: "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=400&fit=crop",
                description: "A romantic novel about Elizabeth Bennet and Mr. Darcy in Georgian England.",
                pages: 432,
                published: "1813",
                badge: "Romance"
            },
            {
                id: 5,
                title: "The Catcher in the Rye",
                author: "J.D. Salinger",
                genre: "fiction",
                price: 40.25,
                originalPrice: 48.00,
                rating: 4.3,
                image: "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=400&fit=crop",
                description: "A coming-of-age story about teenage rebellion and alienation in 1950s America.",
                pages: 277,
                published: "1951",
                badge: "Coming of Age"
            },
            {
                id: 6,
                title: "The Hobbit",
                author: "J.R.R. Tolkien",
                genre: "fiction",
                price: 48.99,
                originalPrice: 55.00,
                rating: 4.9,
                image: "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=400&fit=crop",
                description: "A fantasy novel about a hobbit's unexpected journey to help dwarves reclaim their homeland.",
                pages: 310,
                published: "1937",
                badge: "Fantasy"
            },
            {
                id: 7,
                title: "Sapiens",
                author: "Yuval Noah Harari",
                genre: "non-fiction",
                price: 52.00,
                originalPrice: 60.00,
                rating: 4.4,
                image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=400&fit=crop",
                description: "A brief history of humankind, exploring how Homo sapiens came to dominate the world.",
                pages: 443,
                published: "2011",
                badge: "History"
            },
            {
                id: 8,
                title: "The Girl with the Dragon Tattoo",
                author: "Stieg Larsson",
                genre: "mystery",
                price: 44.50,
                originalPrice: 52.00,
                rating: 4.2,
                image: "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=400&fit=crop",
                description: "A psychological thriller about a journalist and a hacker investigating a decades-old disappearance.",
                pages: 465,
                published: "2005",
                badge: "Thriller"
            },
            {
                id: 9,
                title: "The Alchemist",
                author: "Paulo Coelho",
                genre: "fiction",
                price: 36.99,
                originalPrice: 42.00,
                rating: 4.1,
                image: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300&h=400&fit=crop",
                description: "A philosophical novel about a young Andalusian shepherd's journey to find treasure.",
                pages: 163,
                published: "1988",
                badge: "Philosophy"
            },
            {
                id: 10,
                title: "Steve Jobs",
                author: "Walter Isaacson",
                genre: "biography",
                price: 55.00,
                originalPrice: 65.00,
                rating: 4.6,
                image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=400&fit=crop",
                description: "The exclusive biography of Steve Jobs, based on more than forty interviews with the Apple co-founder.",
                pages: 656,
                published: "2011",
                badge: "Biography"
            },
            {
                id: 11,
                title: "The Silent Patient",
                author: "Alex Michaelides",
                genre: "mystery",
                price: 41.75,
                originalPrice: 48.00,
                rating: 4.3,
                image: "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=400&fit=crop",
                description: "A psychological thriller about a woman who refuses to speak after allegedly murdering her husband.",
                pages: 323,
                published: "2019",
                badge: "Psychological"
            },
            {
                id: 12,
                title: "Atomic Habits",
                author: "James Clear",
                genre: "non-fiction",
                price: 39.99,
                originalPrice: 45.00,
                rating: 4.7,
                image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=400&fit=crop",
                description: "An easy and proven way to build good habits and break bad ones.",
                pages: 320,
                published: "2018",
                badge: "Self-Help"
            }
        ];

        this.filteredBooks = [...this.books];
        this.renderBooks();
    }

    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const searchBtn = document.querySelector('.search-btn');
        
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.handleSearch(e.target.value);
            });
        }

        if (searchBtn) {
            searchBtn.addEventListener('click', () => {
                this.handleSearch(searchInput.value);
            });
        }

        // Filter functionality
        const sortSelect = document.getElementById('sortSelect');
        const priceRange = document.getElementById('priceRange');
        const genreSelect = document.getElementById('genreSelect');
        const clearFilters = document.getElementById('clearFilters');

        if (sortSelect) {
            sortSelect.addEventListener('change', () => this.applyFilters());
        }

        if (priceRange) {
            priceRange.addEventListener('input', (e) => {
                document.getElementById('priceValue').textContent = `K ${e.target.value}`;
                this.applyFilters();
            });
        }

        if (genreSelect) {
            genreSelect.addEventListener('change', () => this.applyFilters());
        }

        if (clearFilters) {
            clearFilters.addEventListener('click', () => this.clearFilters());
        }

        // View toggle
        const viewBtns = document.querySelectorAll('.view-btn');
        viewBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.toggleView(e.target.dataset.view);
            });
        });

        // Category filters
        const categoryCards = document.querySelectorAll('.category-card');
        categoryCards.forEach(card => {
            card.addEventListener('click', (e) => {
                const category = e.currentTarget.dataset.category;
                this.filterByCategory(category);
            });
        });

        // Cart and wishlist
        const cartBtn = document.getElementById('cartBtn');
        const wishlistBtn = document.getElementById('wishlistBtn');

        if (cartBtn) {
            cartBtn.addEventListener('click', () => this.openCart());
        }

        if (wishlistBtn) {
            wishlistBtn.addEventListener('click', () => this.openWishlist());
        }

        // Modal close buttons
        this.setupModalListeners();

        // Load more button
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', () => this.loadMoreBooks());
        }
    }

    setupModalListeners() {
        // Cart modal
        const cartModal = document.getElementById('cartModal');
        const closeCart = document.getElementById('closeCart');
        const clearCart = document.getElementById('clearCart');
        const checkout = document.getElementById('checkout');

        if (closeCart) {
            closeCart.addEventListener('click', () => this.closeModal('cartModal'));
        }

        if (clearCart) {
            clearCart.addEventListener('click', () => this.clearCart());
        }

        if (checkout) {
            checkout.addEventListener('click', () => this.checkout());
        }

        // Wishlist modal
        const wishlistModal = document.getElementById('wishlistModal');
        const closeWishlist = document.getElementById('closeWishlist');

        if (closeWishlist) {
            closeWishlist.addEventListener('click', () => this.closeModal('wishlistModal'));
        }

        // Book modal
        const bookModal = document.getElementById('bookModal');
        const closeBook = document.getElementById('closeBook');

        if (closeBook) {
            closeBook.addEventListener('click', () => this.closeModal('bookModal'));
        }

        // Close modals when clicking outside
        [cartModal, wishlistModal, bookModal].forEach(modal => {
            if (modal) {
                modal.addEventListener('click', (e) => {
                    if (e.target === modal) {
                        this.closeModal(modal.id);
                    }
                });
            }
        });
    }

    handleSearch(query) {
        if (!query.trim()) {
            this.filteredBooks = [...this.books];
        } else {
            this.filteredBooks = this.books.filter(book => 
                book.title.toLowerCase().includes(query.toLowerCase()) ||
                book.author.toLowerCase().includes(query.toLowerCase()) ||
                book.genre.toLowerCase().includes(query.toLowerCase())
            );
        }
        this.renderBooks();
    }

    applyFilters() {
        let filtered = [...this.books];

        // Genre filter
        const genre = document.getElementById('genreSelect').value;
        if (genre) {
            filtered = filtered.filter(book => book.genre === genre);
        }

        // Price filter
        const maxPrice = parseFloat(document.getElementById('priceRange').value);
        filtered = filtered.filter(book => book.price <= maxPrice);

        // Sort filter
        const sortBy = document.getElementById('sortSelect').value;
        switch (sortBy) {
            case 'newest':
                filtered.sort((a, b) => new Date(b.published) - new Date(a.published));
                break;
            case 'oldest':
                filtered.sort((a, b) => new Date(a.published) - new Date(b.published));
                break;
            case 'price-low':
                filtered.sort((a, b) => a.price - b.price);
                break;
            case 'price-high':
                filtered.sort((a, b) => b.price - a.price);
                break;
            case 'rating':
                filtered.sort((a, b) => b.rating - a.rating);
                break;
            case 'popular':
                filtered.sort((a, b) => b.rating - a.rating);
                break;
        }

        this.filteredBooks = filtered;
        this.renderBooks();
    }

    clearFilters() {
        document.getElementById('sortSelect').value = 'newest';
        document.getElementById('priceRange').value = 1000;
        document.getElementById('priceValue').textContent = 'K 1,000';
        document.getElementById('genreSelect').value = '';
        document.getElementById('searchInput').value = '';
        
        this.filteredBooks = [...this.books];
        this.renderBooks();
    }

    filterByCategory(category) {
        this.filteredBooks = this.books.filter(book => book.genre === category);
        this.renderBooks();
        
        // Update genre select
        document.getElementById('genreSelect').value = category;
    }

    toggleView(view) {
        this.currentView = view;
        
        // Update button states
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-view="${view}"]`).classList.add('active');

        // Update grid class
        const booksGrid = document.getElementById('booksGrid');
        if (view === 'list') {
            booksGrid.classList.add('list-view');
        } else {
            booksGrid.classList.remove('list-view');
        }
    }

    renderBooks() {
        const booksGrid = document.getElementById('booksGrid');
        if (!booksGrid) return;

        const startIndex = 0;
        const endIndex = startIndex + this.booksPerPage;
        const booksToShow = this.filteredBooks.slice(startIndex, endIndex);

        booksGrid.innerHTML = booksToShow.map(book => this.createBookCard(book)).join('');

        // Add event listeners to book cards
        this.addBookCardListeners();
    }

    createBookCard(book) {
        const stars = this.createStars(book.rating);
        const discount = book.originalPrice ? Math.round((1 - book.price / book.originalPrice) * 100) : 0;

        return `
            <div class="book-card" data-book-id="${book.id}">
                <div class="book-image">
                    <img src="${book.image}" alt="${book.title}" loading="lazy">
                    ${book.badge ? `<div class="book-badge">${book.badge}</div>` : ''}
                    ${discount > 0 ? `<div class="book-badge discount">-${discount}%</div>` : ''}
                </div>
                <div class="book-content">
                    <h3 class="book-title">${book.title}</h3>
                    <p class="book-author">by ${book.author}</p>
                    <div class="book-rating">
                        <div class="stars">${stars}</div>
                        <span>${book.rating}</span>
                    </div>
                    <div class="book-price">
                        <span class="price">K ${book.price.toFixed(2)}</span>
                        ${book.originalPrice ? `<span class="original-price">K ${book.originalPrice.toFixed(2)}</span>` : ''}
                    </div>
                    <div class="book-actions">
                        <button class="book-btn secondary" onclick="bookStore.addToWishlist(${book.id})">
                            <i class="fas fa-heart"></i>
                        </button>
                        <button class="book-btn primary" onclick="bookStore.addToCart(${book.id})">
                            <i class="fas fa-cart-plus"></i> Add to Cart
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    createStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

        let stars = '';
        
        // Full stars
        for (let i = 0; i < fullStars; i++) {
            stars += '<i class="fas fa-star star"></i>';
        }
        
        // Half star
        if (hasHalfStar) {
            stars += '<i class="fas fa-star-half-alt star"></i>';
        }
        
        // Empty stars
        for (let i = 0; i < emptyStars; i++) {
            stars += '<i class="far fa-star star"></i>';
        }

        return stars;
    }

    addBookCardListeners() {
        document.querySelectorAll('.book-card').forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.closest('.book-btn')) {
                    const bookId = parseInt(card.dataset.bookId);
                    this.showBookDetails(bookId);
                }
            });
        });
    }

    showBookDetails(bookId) {
        const book = this.books.find(b => b.id === bookId);
        if (!book) return;

        // Populate modal with book details
        document.getElementById('bookTitle').textContent = book.title;
        document.getElementById('bookImage').src = book.image;
        document.getElementById('bookImage').alt = book.title;
        document.getElementById('bookRating').textContent = book.rating;
        document.getElementById('bookStars').innerHTML = this.createStars(book.rating);
        document.getElementById('bookDescription').textContent = book.description;
        document.getElementById('bookAuthor').textContent = book.author;
        document.getElementById('bookGenre').textContent = book.genre.charAt(0).toUpperCase() + book.genre.slice(1);
        document.getElementById('bookPages').textContent = book.pages;
        document.getElementById('bookPublished').textContent = book.published;
        document.getElementById('bookPrice').textContent = `K ${book.price.toFixed(2)}`;
        
        if (book.originalPrice) {
            document.getElementById('bookOriginalPrice').textContent = `K ${book.originalPrice.toFixed(2)}`;
        } else {
            document.getElementById('bookOriginalPrice').textContent = '';
        }

        // Add event listeners to modal buttons
        document.getElementById('addToWishlist').onclick = () => {
            this.addToWishlist(bookId);
            this.closeModal('bookModal');
        };

        document.getElementById('addToCart').onclick = () => {
            this.addToCart(bookId);
            this.closeModal('bookModal');
        };

        this.openModal('bookModal');
    }

    addToCart(bookId) {
        const book = this.books.find(b => b.id === bookId);
        if (!book) return;

        const existingItem = this.cart.find(item => item.id === bookId);
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.cart.push({ ...book, quantity: 1 });
        }

        this.updateCartCount();
        this.showNotification(`${book.title} added to cart!`, 'success');
    }

    addToWishlist(bookId) {
        const book = this.books.find(b => b.id === bookId);
        if (!book) return;

        if (this.wishlist.find(item => item.id === bookId)) {
            this.showNotification('Book already in wishlist!', 'warning');
            return;
        }

        this.wishlist.push(book);
        this.updateWishlistCount();
        this.showNotification(`${book.title} added to wishlist!`, 'success');
    }

    removeFromCart(bookId) {
        this.cart = this.cart.filter(item => item.id !== bookId);
        this.updateCartCount();
        this.renderCart();
    }

    removeFromWishlist(bookId) {
        this.wishlist = this.wishlist.filter(item => item.id !== bookId);
        this.updateWishlistCount();
        this.renderWishlist();
    }

    updateCartCount() {
        const count = this.cart.reduce((total, item) => total + item.quantity, 0);
        const cartCount = document.getElementById('cartCount');
        if (cartCount) {
            cartCount.textContent = count;
        }
    }

    updateWishlistCount() {
        const count = this.wishlist.length;
        const wishlistCount = document.getElementById('wishlistCount');
        if (wishlistCount) {
            wishlistCount.textContent = count;
        }
    }

    openCart() {
        this.renderCart();
        this.openModal('cartModal');
    }

    openWishlist() {
        this.renderWishlist();
        this.openModal('wishlistModal');
    }

    renderCart() {
        const cartItems = document.getElementById('cartItems');
        if (!cartItems) return;

        if (this.cart.length === 0) {
            cartItems.innerHTML = '<p class="text-center">Your cart is empty</p>';
            return;
        }

        cartItems.innerHTML = this.cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-image">
                    <img src="${item.image}" alt="${item.title}">
                </div>
                <div class="cart-item-info">
                    <h4 class="cart-item-title">${item.title}</h4>
                    <p class="cart-item-author">by ${item.author}</p>
                    <p class="cart-item-price">K ${item.price.toFixed(2)}</p>
                </div>
                <div class="cart-item-controls">
                    <button class="quantity-btn" onclick="bookStore.updateQuantity(${item.id}, -1)">-</button>
                    <span>${item.quantity}</span>
                    <button class="quantity-btn" onclick="bookStore.updateQuantity(${item.id}, 1)">+</button>
                    <button class="quantity-btn" onclick="bookStore.removeFromCart(${item.id})" style="margin-left: 10px; color: #ef4444;">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');

        // Update cart total
        const total = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        document.getElementById('cartTotal').textContent = `K ${total.toFixed(2)}`;
    }

    renderWishlist() {
        const wishlistItems = document.getElementById('wishlistItems');
        if (!wishlistItems) return;

        if (this.wishlist.length === 0) {
            wishlistItems.innerHTML = '<p class="text-center">Your wishlist is empty</p>';
            return;
        }

        wishlistItems.innerHTML = this.wishlist.map(book => `
            <div class="cart-item">
                <div class="cart-item-image">
                    <img src="${book.image}" alt="${book.title}">
                </div>
                <div class="cart-item-info">
                    <h4 class="cart-item-title">${book.title}</h4>
                    <p class="cart-item-author">by ${book.author}</p>
                    <p class="cart-item-price">K ${book.price.toFixed(2)}</p>
                </div>
                <div class="cart-item-controls">
                    <button class="book-btn primary" onclick="bookStore.addToCart(${book.id})">
                        <i class="fas fa-cart-plus"></i> Add to Cart
                    </button>
                    <button class="quantity-btn" onclick="bookStore.removeFromWishlist(${book.id})" style="margin-left: 10px; color: #ef4444;">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }

    updateQuantity(bookId, change) {
        const item = this.cart.find(item => item.id === bookId);
        if (!item) return;

        item.quantity += change;
        if (item.quantity <= 0) {
            this.removeFromCart(bookId);
        } else {
            this.updateCartCount();
            this.renderCart();
        }
    }

    clearCart() {
        this.cart = [];
        this.updateCartCount();
        this.renderCart();
        this.showNotification('Cart cleared!', 'info');
    }

    checkout() {
        if (this.cart.length === 0) {
            this.showNotification('Your cart is empty!', 'warning');
            return;
        }

        const total = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        this.showNotification(`Checkout initiated! Total: K ${total.toFixed(2)}`, 'success');
        
        // In a real application, you would redirect to a payment page
        this.closeModal('cartModal');
    }

    loadMoreBooks() {
        // In a real application, this would load more books from an API
        this.showNotification('Loading more books...', 'info');
    }

    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize the book store when the page loads
let bookStore;
document.addEventListener('DOMContentLoaded', () => {
    bookStore = new BookStore();
});

// Newsletter subscription
document.querySelector('.newsletter-form button')?.addEventListener('click', (e) => {
    e.preventDefault();
    const email = document.querySelector('.newsletter-form input').value;
    if (email) {
        bookStore.showNotification('Thank you for subscribing!', 'success');
        document.querySelector('.newsletter-form input').value = '';
    }
});

// Hero buttons
document.querySelector('.hero-actions .btn-primary')?.addEventListener('click', () => {
    document.querySelector('.books-section').scrollIntoView({ behavior: 'smooth' });
});

document.querySelector('.hero-actions .btn-secondary')?.addEventListener('click', () => {
    // Filter to show bestsellers
    bookStore.filteredBooks = bookStore.books.filter(book => book.rating >= 4.5);
    bookStore.renderBooks();
    document.querySelector('.books-section').scrollIntoView({ behavior: 'smooth' });
});
