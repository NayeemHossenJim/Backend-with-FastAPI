// Main Todo App JavaScript

// API Configuration
const API_BASE_URL = window.location.origin;
let currentUser = null;
let tasks = [];
let currentFilter = 'all';

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

async function initializeApp() {
    // Show loading screen
    showLoadingScreen();
    
    // Check authentication
    const isAuthenticated = await checkAuthentication();
    
    // Initialize UI
    initializeUI();
    
    // Load initial data if authenticated
    if (isAuthenticated) {
        await loadTasks();
        await loadUserProfile();
        showAuthenticatedUI();
    } else {
        showGuestUI();
    }
    
    // Hide loading screen and show app
    hideLoadingScreen();
    
    // Initialize event listeners
    initializeEventListeners();
    
    // Initialize theme
    initializeTheme();
    
    // Show dashboard by default
    showSection('dashboard');
}

// Authentication functions
async function checkAuthentication() {
    const token = localStorage.getItem('access_token');
    if (!token) return false;
    
    try {
        // Verify token by making a test request
        const response = await fetchWithAuth('/tasks/');
        return response.ok;
    } catch (error) {
        console.error('Authentication check failed:', error);
        localStorage.removeItem('access_token');
        localStorage.removeItem('token_type');
        return false;
    }
}

async function loadUserProfile() {
    try {
        // Since we don't have a dedicated profile endpoint, we'll use task data to infer user info
        const profileInfo = document.querySelector('.profile-info');
        if (currentUser) {
            profileInfo.querySelector('.profile-name').textContent = currentUser.username || 'User';
            profileInfo.querySelector('.profile-role').textContent = currentUser.role || 'Free Plan';
        }
    } catch (error) {
        console.error('Failed to load user profile:', error);
    }
}

// Task management functions
async function loadTasks() {
    try {
        const response = await fetchWithAuth('/tasks/');
        if (response.ok) {
            tasks = await response.json();
            updateTaskCounts();
            renderTasks();
            updateDashboard();
        } else {
            throw new Error('Failed to load tasks');
        }
    } catch (error) {
        console.error('Error loading tasks:', error);
        showToast('error', 'Failed to load tasks', error.message);
    }
}

async function createTask(taskData) {
    try {
        const response = await fetchWithAuth('/tasks/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });
        
        if (response.ok) {
            const result = await response.json();
            showToast('success', 'Task created successfully!');
            await loadTasks(); // Refresh tasks
            closeModal('taskModal');
            return result;
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create task');
        }
    } catch (error) {
        console.error('Error creating task:', error);
        showToast('error', 'Failed to create task', error.message);
        throw error;
    }
}

async function updateTask(taskId, taskData) {
    try {
        const response = await fetchWithAuth(`/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });
        
        if (response.ok) {
            const result = await response.json();
            showToast('success', 'Task updated successfully!');
            await loadTasks(); // Refresh tasks
            closeModal('taskModal');
            return result;
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to update task');
        }
    } catch (error) {
        console.error('Error updating task:', error);
        showToast('error', 'Failed to update task', error.message);
        throw error;
    }
}

async function deleteTask(taskId) {
    try {
        const response = await fetchWithAuth(`/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showToast('success', 'Task deleted successfully!');
            await loadTasks(); // Refresh tasks
            return true;
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to delete task');
        }
    } catch (error) {
        console.error('Error deleting task:', error);
        showToast('error', 'Failed to delete task', error.message);
        throw error;
    }
}

async function toggleTaskStatus(taskId, currentStatus) {
    try {
        const task = tasks.find(t => t.id === taskId);
        if (!task) throw new Error('Task not found');
        
        const updatedTask = {
            ...task,
            status: !currentStatus
        };
        
        delete updatedTask.id;
        delete updatedTask.owner_id;
        
        await updateTask(taskId, updatedTask);
    } catch (error) {
        console.error('Error toggling task status:', error);
        showToast('error', 'Failed to update task status', error.message);
    }
}

// UI functions
function initializeUI() {
    // Initialize sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebar = document.getElementById('sidebar');
    
    [sidebarToggle, mobileMenuBtn].forEach(btn => {
        if (btn) {
            btn.addEventListener('click', () => {
                sidebar.classList.toggle('open');
            });
        }
    });
    
    // Initialize navigation
    const navLinks = document.querySelectorAll('.nav-link[data-section]');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.getAttribute('data-section');
            showSection(section);
            
            // Update active state
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            link.closest('.nav-item').classList.add('active');
            
            // Update page title
            const pageTitle = link.querySelector('span').textContent;
            document.getElementById('pageTitle').textContent = pageTitle;
            
            // Close mobile menu
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('open');
            }
        });
    });
}

function initializeEventListeners() {
    // Add task buttons
    const addTaskButtons = document.querySelectorAll('#addTaskBtn, #addTaskBtnMain, #addTodayTaskBtn, #addImportantTaskBtn');
    addTaskButtons.forEach(btn => {
        btn.addEventListener('click', () => openTaskModal());
    });
    
    // Task form submission
    const taskForm = document.getElementById('taskForm');
    if (taskForm) {
        taskForm.addEventListener('submit', handleTaskFormSubmit);
    }
    
    // Modal close buttons
    const modalCloseButtons = document.querySelectorAll('.modal-close, #cancelBtn');
    modalCloseButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            closeModal('taskModal');
            closeModal('confirmModal');
        });
    });
    
    // Click outside modal to close
    const modals = document.querySelectorAll('.modal-overlay');
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal(modal.id);
            }
        });
    });
    
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }
    
    // Filter dropdown
    initializeFilterDropdown();
    
    // Auth buttons
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    
    if (loginBtn) {
        loginBtn.addEventListener('click', () => window.location.href = '/login');
    }
    
    if (registerBtn) {
        registerBtn.addEventListener('click', () => window.location.href = '/register');
    }
    
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
    
    // Clear completed button
    const clearCompletedBtn = document.getElementById('clearCompletedBtn');
    if (clearCompletedBtn) {
        clearCompletedBtn.addEventListener('click', handleClearCompleted);
    }
    
    // Theme toggle
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
}

function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show target section
    const targetSection = document.getElementById(sectionName);
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    // Render appropriate tasks based on section
    if (sectionName !== 'dashboard') {
        renderTasksForSection(sectionName);
    }
}

function renderTasksForSection(section) {
    let filteredTasks = [];
    let containerId = '';
    
    switch (section) {
        case 'tasks':
            filteredTasks = filterTasks(currentFilter);
            containerId = 'tasksListContainer';
            break;
        case 'today':
            filteredTasks = getTodayTasks();
            containerId = 'todayTasksList';
            break;
        case 'important':
            filteredTasks = getImportantTasks();
            containerId = 'importantTasksList';
            break;
        case 'completed':
            filteredTasks = getCompletedTasks();
            containerId = 'completedTasksList';
            break;
        default:
            return;
    }
    
    renderTasksList(filteredTasks, containerId);
}

function renderTasks() {
    // Update all task lists
    renderTasksList(filterTasks(currentFilter), 'tasksListContainer');
    renderTasksList(getTodayTasks(), 'todayTasksList');
    renderTasksList(getImportantTasks(), 'importantTasksList');
    renderTasksList(getCompletedTasks(), 'completedTasksList');
    renderRecentTasks();
}

function renderTasksList(tasks, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <h3>No tasks found</h3>
                <p>Create a new task to get started!</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = tasks.map(task => `
        <div class="task-item ${task.status ? 'completed' : ''}" data-task-id="${task.id}">
            <div class="task-checkbox ${task.status ? 'checked' : ''}" onclick="toggleTaskStatus(${task.id}, ${task.status})">
            </div>
            <div class="task-content">
                <div class="task-title">${escapeHtml(task.task)}</div>
                <div class="task-description">${escapeHtml(task.description)}</div>
            </div>
            <div class="task-priority priority-${getPriorityName(task.priority)}">
                ${getPriorityName(task.priority)}
            </div>
            <div class="task-actions">
                <button class="task-action-btn edit" onclick="editTask(${task.id})" title="Edit task">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="task-action-btn delete" onclick="confirmDeleteTask(${task.id})" title="Delete task">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function renderRecentTasks() {
    const container = document.getElementById('recentTasksList');
    if (!container) return;
    
    const recentTasks = tasks
        .sort((a, b) => b.id - a.id) // Sort by ID (most recent first)
        .slice(0, 5); // Get latest 5 tasks
    
    if (recentTasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-plus-circle"></i>
                <h3>No tasks yet</h3>
                <p>Create your first task to get started!</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = recentTasks.map(task => `
        <div class="recent-task-item" onclick="editTask(${task.id})">
            <div class="recent-task-checkbox ${task.status ? 'checked' : ''}" onclick="event.stopPropagation(); toggleTaskStatus(${task.id}, ${task.status})">
            </div>
            <div class="recent-task-content">
                <div class="recent-task-title">${escapeHtml(task.task)}</div>
                <div class="recent-task-meta">
                    <span class="priority priority-${getPriorityName(task.priority)}">
                        ${getPriorityName(task.priority)} priority
                    </span>
                </div>
            </div>
        </div>
    `).join('');
}

// Task filtering functions
function filterTasks(filter) {
    switch (filter) {
        case 'pending':
            return tasks.filter(task => !task.status);
        case 'completed':
            return tasks.filter(task => task.status);
        case 'high':
            return tasks.filter(task => task.priority === 3);
        case 'medium':
            return tasks.filter(task => task.priority === 2);
        case 'low':
            return tasks.filter(task => task.priority === 1);
        default:
            return tasks;
    }
}

function getTodayTasks() {
    // For now, return all pending tasks
    // In a real app, you'd filter by date
    return tasks.filter(task => !task.status);
}

function getImportantTasks() {
    return tasks.filter(task => task.priority === 3);
}

function getCompletedTasks() {
    return tasks.filter(task => task.status);
}

// Task modal functions
function openTaskModal(taskId = null) {
    const modal = document.getElementById('taskModal');
    const modalTitle = document.getElementById('modalTitle');
    const form = document.getElementById('taskForm');
    
    if (taskId) {
        // Edit mode
        const task = tasks.find(t => t.id === taskId);
        if (!task) return;
        
        modalTitle.textContent = 'Edit Task';
        document.getElementById('taskId').value = taskId;
        document.getElementById('taskTitle').value = task.task;
        document.getElementById('taskDescription').value = task.description;
        document.getElementById('taskPriority').value = task.priority;
        document.getElementById('taskStatus').value = task.status;
    } else {
        // Create mode
        modalTitle.textContent = 'Add New Task';
        form.reset();
        document.getElementById('taskId').value = '';
    }
    
    showModal('taskModal');
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
    }
}

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
    }
}

async function handleTaskFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('#saveBtn');
    const formData = new FormData(form);
    
    const taskData = {
        task: formData.get('task'),
        description: formData.get('description'),
        priority: parseInt(formData.get('priority')),
        status: formData.get('status') === 'true'
    };
    
    // Validate required fields
    if (!taskData.task.trim()) {
        showToast('error', 'Task title is required');
        return;
    }
    
    setButtonLoading(submitBtn, true);
    
    try {
        const taskId = formData.get('taskId');
        
        if (taskId) {
            // Update existing task
            await updateTask(parseInt(taskId), taskData);
        } else {
            // Create new task
            await createTask(taskData);
        }
    } catch (error) {
        console.error('Form submission error:', error);
    } finally {
        setButtonLoading(submitBtn, false);
    }
}

// Task actions
window.editTask = function(taskId) {
    openTaskModal(taskId);
};

window.confirmDeleteTask = function(taskId) {
    const modal = document.getElementById('confirmModal');
    const confirmTitle = document.getElementById('confirmTitle');
    const confirmMessage = document.getElementById('confirmMessage');
    const confirmActionBtn = document.getElementById('confirmAction');
    
    confirmTitle.textContent = 'Delete Task';
    confirmMessage.textContent = 'Are you sure you want to delete this task? This action cannot be undone.';
    
    confirmActionBtn.onclick = async function() {
        setButtonLoading(this, true);
        try {
            await deleteTask(taskId);
            closeModal('confirmModal');
        } catch (error) {
            console.error('Delete error:', error);
        } finally {
            setButtonLoading(this, false);
        }
    };
    
    showModal('confirmModal');
};

window.toggleTaskStatus = async function(taskId, currentStatus) {
    await toggleTaskStatus(taskId, currentStatus);
};

// Search functionality
function handleSearch(e) {
    const query = e.target.value.toLowerCase().trim();
    
    if (!query) {
        renderTasks();
        return;
    }
    
    const filteredTasks = tasks.filter(task => 
        task.task.toLowerCase().includes(query) || 
        task.description.toLowerCase().includes(query)
    );
    
    // Update all visible task lists with filtered results
    const activeSection = document.querySelector('.content-section.active');
    if (activeSection) {
        const sectionId = activeSection.id;
        let containerId = '';
        
        switch (sectionId) {
            case 'tasks':
                containerId = 'tasksListContainer';
                break;
            case 'today':
                containerId = 'todayTasksList';
                break;
            case 'important':
                containerId = 'importantTasksList';
                break;
            case 'completed':
                containerId = 'completedTasksList';
                break;
        }
        
        if (containerId) {
            renderTasksList(filteredTasks, containerId);
        }
    }
}

// Filter dropdown
function initializeFilterDropdown() {
    const filterToggle = document.querySelector('.dropdown-toggle');
    const filterDropdown = document.querySelector('.filter-dropdown');
    const filterLinks = document.querySelectorAll('.dropdown-menu a[data-filter]');
    
    if (filterToggle) {
        filterToggle.addEventListener('click', () => {
            filterDropdown.classList.toggle('active');
        });
    }
    
    filterLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const filter = link.getAttribute('data-filter');
            currentFilter = filter;
            renderTasksForSection('tasks');
            filterDropdown.classList.remove('active');
            
            // Update filter button text
            filterToggle.innerHTML = `<i class="fas fa-filter"></i> ${link.textContent}`;
        });
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!filterDropdown.contains(e.target)) {
            filterDropdown.classList.remove('active');
        }
    });
}

// Clear completed tasks
async function handleClearCompleted() {
    const completedTasks = getCompletedTasks();
    
    if (completedTasks.length === 0) {
        showToast('info', 'No completed tasks to clear');
        return;
    }
    
    const modal = document.getElementById('confirmModal');
    const confirmTitle = document.getElementById('confirmTitle');
    const confirmMessage = document.getElementById('confirmMessage');
    const confirmActionBtn = document.getElementById('confirmAction');
    
    confirmTitle.textContent = 'Clear Completed Tasks';
    confirmMessage.textContent = `Are you sure you want to delete ${completedTasks.length} completed task(s)? This action cannot be undone.`;
    
    confirmActionBtn.onclick = async function() {
        setButtonLoading(this, true);
        
        try {
            const deletePromises = completedTasks.map(task => deleteTask(task.id));
            await Promise.all(deletePromises);
            showToast('success', 'All completed tasks cleared!');
            closeModal('confirmModal');
        } catch (error) {
            console.error('Clear completed error:', error);
            showToast('error', 'Failed to clear some tasks');
        } finally {
            setButtonLoading(this, false);
        }
    };
    
    showModal('confirmModal');
}

// UI state management
function showAuthenticatedUI() {
    const authActions = document.getElementById('authActions');
    const logoutAction = document.getElementById('logoutAction');
    
    if (authActions) authActions.style.display = 'none';
    if (logoutAction) logoutAction.style.display = 'flex';
}

function showGuestUI() {
    const authActions = document.getElementById('authActions');
    const logoutAction = document.getElementById('logoutAction');
    
    if (authActions) authActions.style.display = 'flex';
    if (logoutAction) logoutAction.style.display = 'none';
    
    // Update profile for guest user
    const profileInfo = document.querySelector('.profile-info');
    if (profileInfo) {
        profileInfo.querySelector('.profile-name').textContent = 'Guest User';
        profileInfo.querySelector('.profile-role').textContent = 'Demo Mode';
    }
    
    // Show demo tasks for guest users
    tasks = getDemoTasks();
    updateTaskCounts();
    renderTasks();
    updateDashboard();
}

// Demo data for guest users
function getDemoTasks() {
    return [
        {
            id: 1,
            task: 'Complete project proposal',
            description: 'Finalize the project proposal document and send it to the client for review.',
            priority: 3,
            status: false
        },
        {
            id: 2,
            task: 'Review team feedback',
            description: 'Go through all the feedback received from team members on the recent project.',
            priority: 2,
            status: true
        },
        {
            id: 3,
            task: 'Schedule client meeting',
            description: 'Set up a meeting with the client to discuss project requirements and timeline.',
            priority: 2,
            status: false
        },
        {
            id: 4,
            task: 'Update documentation',
            description: 'Update all project documentation with the latest changes and improvements.',
            priority: 1,
            status: true
        },
        {
            id: 5,
            task: 'Prepare presentation',
            description: 'Create slides for the upcoming quarterly business review presentation.',
            priority: 3,
            status: false
        }
    ];
}

// Dashboard update functions
function updateDashboard() {
    const totalTasks = tasks.length;
    const completedTasks = tasks.filter(task => task.status).length;
    const pendingTasks = totalTasks - completedTasks;
    const importantTasks = tasks.filter(task => task.priority === 3).length;
    
    // Update dashboard stats
    document.getElementById('dashTotalTasks').textContent = totalTasks;
    document.getElementById('dashCompletedTasks').textContent = completedTasks;
    document.getElementById('dashPendingTasks').textContent = pendingTasks;
    document.getElementById('dashImportantTasks').textContent = importantTasks;
}

function updateTaskCounts() {
    const totalTasks = tasks.length;
    const todayTasks = getTodayTasks().length;
    const importantTasks = getImportantTasks().length;
    const completedTasks = getCompletedTasks().length;
    const completedPercentage = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;
    
    // Update sidebar counts
    document.getElementById('allTasksCount').textContent = totalTasks;
    document.getElementById('todayTasksCount').textContent = todayTasks;
    document.getElementById('importantTasksCount').textContent = importantTasks;
    document.getElementById('completedTasksCount').textContent = completedTasks;
    
    // Update sidebar stats
    document.getElementById('totalTasks').textContent = totalTasks;
    document.getElementById('completedPercentage').textContent = `${completedPercentage}%`;
}

// Utility functions
function getPriorityName(priority) {
    const priorities = { 1: 'low', 2: 'medium', 3: 'high' };
    return priorities[priority] || 'medium';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

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

// Loading screen functions
function showLoadingScreen() {
    const loadingScreen = document.getElementById('loadingScreen');
    if (loadingScreen) {
        loadingScreen.classList.remove('hidden');
    }
}

function hideLoadingScreen() {
    const loadingScreen = document.getElementById('loadingScreen');
    const appContainer = document.getElementById('appContainer');
    
    setTimeout(() => {
        if (loadingScreen) {
            loadingScreen.classList.add('hidden');
        }
        if (appContainer) {
            appContainer.classList.add('loaded');
        }
    }, 1000);
}

// Theme management
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    
    showToast('info', `Switched to ${newTheme} theme`);
}

function updateThemeIcon(theme) {
    const themeIcon = document.querySelector('#themeToggle i');
    if (themeIcon) {
        themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// Toast notifications
function showToast(type, title, message = '') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icon = getToastIcon(type);
    toast.innerHTML = `
        <i class="${icon}"></i>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            ${message ? `<div class="toast-message">${message}</div>` : ''}
        </div>
    `;
    
    container.appendChild(toast);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.style.animation = 'slideOutToast 0.3s ease-in forwards';
            setTimeout(() => toast.remove(), 300);
        }
    }, 4000);
    
    // Add click to close
    toast.addEventListener('click', () => {
        toast.style.animation = 'slideOutToast 0.3s ease-in forwards';
        setTimeout(() => toast.remove(), 300);
    });
}

function getToastIcon(type) {
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-times-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };
    return icons[type] || icons.info;
}

// Authentication helpers
async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('access_token');
    const tokenType = localStorage.getItem('token_type') || 'Bearer';
    
    const headers = {
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `${tokenType} ${token}`;
    }
    
    return fetch(`${API_BASE_URL}${url}`, {
        ...options,
        headers
    });
}

function handleLogout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
    showToast('info', 'Logged out successfully');
    
    setTimeout(() => {
        window.location.href = '/login';
    }, 1500);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutToast {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .task-item {
        transition: all 0.2s ease;
    }
    
    .task-item:hover {
        transform: translateX(4px);
    }
    
    .task-checkbox {
        transition: all 0.2s ease;
    }
    
    .task-checkbox:hover {
        transform: scale(1.1);
    }
`;
document.head.appendChild(style);