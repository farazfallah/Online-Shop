document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - Starting auth check');
    
    function checkAuthStatus() {
        console.log('Checking auth status...');
        
        fetch('http://127.0.0.1:8000/api/validate-token/', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('API Response:', data);
            
            if (data.is_valid) {
                console.log('User is authenticated:', data.user);
                handleAuthenticatedUser(data.user);
            } else {
                console.log('User is not authenticated. Error:', data.error);
                handleUnauthenticatedUser();
            }
        })
        .catch(error => {
            console.error('Error in auth check:', error);
            handleUnauthenticatedUser();
        });
    }

    function handleAuthenticatedUser(user) {
        console.log('Handling authenticated user');
        const authSections = document.querySelectorAll('.user-auth-section');
        console.log('Found auth sections:', authSections.length);
    
        authSections.forEach(section => {
            section.innerHTML = `
                <div class="top-header-link d-lg-flex">
                    <div class="dropdown text-end">
                        <a href="" data-bs-toggle="dropdown" aria-expanded="false" role="button"
                           class="btn btn-white auth-dropdown header-register border-0">
                            <div class="d-flex align-items-center">
                                <figure class="avatar">
                                    <img src="${user.image_url}" alt="${user.first_name} ${user.last_name}">
                                </figure>
                                <span class="ms-3 d-md-block d-none font-18">${user.first_name} ${user.last_name}
                                    <i class="bi bi-chevron-down arrow-auth font-12 ms-2"></i>
                                </span>
                            </div>
                        </a>
                        <ul class="dropdown-menu flex-column" style="min-width: 250px;">
                            <li class="w-100">
                                <a href="/account" class="dropdown-item fs-6">
                                    <i class="bi bi-house-door me-2"></i>داشبورد
                                </a>
                            </li>
                            <li class="w-100">
                                <a href="/account/orders" class="dropdown-item fs-6 py-2">
                                    <i class="bi bi-cart-check me-2"></i>سفارش های من
                                </a>
                            </li>
                            <li class="w-100">
                                <a href="/account/address" class="dropdown-item fs-6 py-2">
                                    <i class="bi bi-pin-map me-2"></i>آدرس های من
                                </a>
                            </li>
                            <li class="w-100">
                                <a href="/account/logout" class="dropdown-item fs-6 py-2 mct-hover">
                                    <i class="bi bi-arrow-right-square me-2"></i>خروج از حساب کاربری
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>`;
        });
        console.log('Updated all auth sections');
    }
    
    function handleUnauthenticatedUser() {
        console.log('Handling unauthenticated user');
        const authSections = document.querySelectorAll('.user-auth-section');
        console.log('Found auth sections:', authSections.length);
        
        authSections.forEach(section => {
            section.innerHTML = `
                <div class="auth-link">
                    <a href="/account/login/">
                        <i class="bi bi-person"></i>
                        <span class="fw-bold">ورود / عضویت</span>
                    </a>
                </div>`;
        });
        console.log('Updated all auth sections');
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    checkAuthStatus();
});