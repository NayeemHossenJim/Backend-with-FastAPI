// Authentication JavaScript

// API Configuration
const API_BASE_URL = window.location.origin;

// Initialize authentication forms
function initializeLoginForm() {
    const form = document.getElementById('loginForm');
    if (!form) return;

    form.addEventListener('submit', handleLogin);
    
    // Initialize form validation
    initializeFormValidation(form);
    
    // Initialize password toggle
    initializePasswordToggle();
    
    // Check for existing token
    checkExistingAuth();
}

function initializeRegisterForm() {
    const form = document.getElementById('registerForm');
    if (!form) return;

    form.addEventListener('submit', handleRegister);
    
    // Initialize form validation
    initializeFormValidation(form);
    
    // Initialize password toggle
    initializePasswordToggle();
    
    // Initialize password strength indicator
    initializePasswordStrength();
    
    // Check for existing token
    checkExistingAuth();
}

// Handle login form submission
async function handleLogin(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const formData = new FormData(form);
    
    // Show loading state
    setButtonLoading(submitBtn, true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store token
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('token_type', data.token_type);
            
            // Show success message
            showAlert('success', 'Login successful! Redirecting...');
            
            // Redirect to app
            setTimeout(() => {
                window.location.href = '/app';
            }, 1500);
        } else {
            throw new Error(data.detail || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert('error', error.message);
    } finally {
        setButtonLoading(submitBtn, false);
    }
}

// Handle register form submission
async function handleRegister(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const formData = new FormData(form);
    
    // Validate passwords match
    const password = formData.get('password');
    const confirmPassword = formData.get('confirmPassword');
    
    if (password !== confirmPassword) {
        showAlert('error', 'Passwords do not match');
        return;
    }
    
    // Show loading state
    setButtonLoading(submitBtn, true);
    
    try {
        const userData = {
            full_name: formData.get('full_name'),
            username: formData.get('username'),
            email: formData.get('email'),
            password: password,
            role: 'user'
        };
        
        const response = await fetch(`${API_BASE_URL}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('success', 'Registration successful! Please login with your credentials.');
            
            // Redirect to login page
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
        } else {
            throw new Error(data.detail || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showAlert('error', error.message);
    } finally {
        setButtonLoading(submitBtn, false);
    }
}

// Initialize form validation
function initializeFormValidation(form) {
    const inputs = form.querySelectorAll('input[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldError);
    });
}

// Validate individual field
function validateField(e) {
    const input = e.target;
    const inputGroup = input.closest('.input-group');
    
    if (!input.value.trim() && input.hasAttribute('required')) {
        showFieldError(inputGroup, 'This field is required');
        return false;
    }
    
    if (input.type === 'email' && input.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(input.value)) {
            showFieldError(inputGroup, 'Please enter a valid email address');
            return false;
        }
    }
    
    if (input.name === 'username' && input.value) {
        const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
        if (!usernameRegex.test(input.value)) {
            showFieldError(inputGroup, 'Username must be 3-20 characters and contain only letters, numbers, and underscores');
            return false;
        }
    }
    
    if (input.name === 'password' && input.value) {
        if (input.value.length < 8) {
            showFieldError(inputGroup, 'Password must be at least 8 characters long');
            return false;
        }
    }
    
    clearFieldError(inputGroup);
    return true;
}

// Show field error
function showFieldError(inputGroup, message) {
    clearFieldError(inputGroup);
    
    const input = inputGroup.querySelector('input');
    if (input) {
        input.style.borderColor = 'var(--danger-color)';
        input.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
    }
    
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    errorElement.style.cssText = `
        color: var(--danger-color);
        font-size: 0.75rem;
        margin-top: 0.25rem;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    `;
    
    // Add error icon
    const errorIcon = document.createElement('i');
    errorIcon.className = 'fas fa-exclamation-circle';
    errorElement.insertBefore(errorIcon, errorElement.firstChild);
    
    inputGroup.parentNode.appendChild(errorElement);
}

// Clear field error
function clearFieldError(inputOrGroup) {
    const inputGroup = inputOrGroup.closest ? inputOrGroup.closest('.input-group') : inputOrGroup;
    const formGroup = inputGroup.parentNode;
    const existingError = formGroup.querySelector('.field-error');
    
    if (existingError) {
        existingError.remove();
    }
    
    const input = inputGroup.querySelector('input');
    if (input) {
        input.style.borderColor = '';
        input.style.boxShadow = '';
    }
}

// Initialize password toggle functionality
function initializePasswordToggle() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input[type="password"], input[type="text"]');
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.className = 'fas fa-eye-slash';
            } else {
                input.type = 'password';
                icon.className = 'fas fa-eye';
            }
        });
    });
}

// Initialize password strength indicator
function initializePasswordStrength() {
    const passwordInput = document.getElementById('password');
    const strengthContainer = document.querySelector('.password-strength');
    const strengthBar = document.querySelector('.strength-bar');
    const strengthFill = document.querySelector('.strength-fill');
    const strengthText = document.querySelector('.strength-text');
    
    if (!passwordInput || !strengthBar) return;
    
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        const strength = calculatePasswordStrength(password);
        
        if (password.length > 0) {
            strengthContainer.classList.add('visible');
        } else {
            strengthContainer.classList.remove('visible');
        }
        
        updatePasswordStrength(strength, strengthFill, strengthText, strengthBar);
    });
    
    // Hide strength indicator initially
    if (strengthContainer && !passwordInput.value) {
        strengthContainer.classList.remove('visible');
    }
}

// Calculate password strength
function calculatePasswordStrength(password) {
    if (!password) return { score: 0, text: 'Password strength' };
    
    let score = 0;
    
    // Length check
    if (password.length >= 8) score += 1;
    if (password.length >= 12) score += 1;
    
    // Character variety checks
    if (/[a-z]/.test(password)) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[^A-Za-z0-9]/.test(password)) score += 1;
    
    if (score <= 2) {
        return { score: 1, text: 'Weak' };
    } else if (score <= 4) {
        return { score: 2, text: 'Medium' };
    } else {
        return { score: 3, text: 'Strong' };
    }
}

// Update password strength display
function updatePasswordStrength(strength, fill, text, bar) {
    const { score, text: strengthText } = strength;
    
    // Remove existing strength classes
    bar.classList.remove('strength-weak', 'strength-medium', 'strength-strong');
    
    // Add new strength class
    if (score === 1) {
        bar.classList.add('strength-weak');
    } else if (score === 2) {
        bar.classList.add('strength-medium');
    } else if (score === 3) {
        bar.classList.add('strength-strong');
    }
    
    text.textContent = strengthText;
}

// Set button loading state
function setButtonLoading(button, loading) {
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');
    
    if (loading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

// Show alert message
function showAlert(type, message) {
    const container = document.getElementById('alertContainer');
    if (!container) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    
    const icon = getAlertIcon(type);
    alert.innerHTML = `
        <i class="${icon}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(alert);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
    
    // Add click to close
    alert.addEventListener('click', () => {
        alert.remove();
    });
}

// Get alert icon based on type
function getAlertIcon(type) {
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-times-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };
    return icons[type] || icons.info;
}

// Check for existing authentication
function checkExistingAuth() {
    const token = localStorage.getItem('access_token');
    if (token) {
        // Redirect to app if already authenticated
        window.location.href = '/app';
    }
}

// Toggle password visibility
window.togglePassword = function() {
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        const toggle = field.parentNode.querySelector('.toggle-password');
        if (toggle) {
            toggle.click();
        }
    });
};