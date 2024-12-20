// auth-validator.js
class AuthValidator {
    constructor() {
        this.isAuthenticated = false;
        this.user = null;
    }

    async validateAuth() {
        try {
            const response = await fetch('/api/validate-token/', {
                method: 'POST',
                credentials: 'include', // برای ارسال کوکی‌ها
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (data.is_valid) {
                this.isAuthenticated = true;
                this.user = data.user;
                return {
                    isAuthenticated: true,
                    user: data.user
                };
            } else {
                // اگر توکن معتبر نبود، ریدایرکت به صفحه لاگین
                window.location.href = '/login/?next=' + window.location.pathname;
                return {
                    isAuthenticated: false,
                    user: null
                };
            }
        } catch (error) {
            console.error('خطا در بررسی وضعیت احراز هویت:', error);
            window.location.href = '/login/?next=' + window.location.pathname;
            return {
                isAuthenticated: false,
                user: null
            };
        }
    }

    // گرفتن اطلاعات کاربر
    getUser() {
        return this.user;
    }

    // چک کردن دسترسی ادمین
    isAdmin() {
        return this.user?.is_staff || false;
    }
}

// ساخت یک نمونه عمومی
window.authValidator = new AuthValidator();