document.addEventListener("DOMContentLoaded", () => {
    const apiUrl = "http://127.0.0.1:8000/api/cart/";

    async function fetchCart() {
        try {
            const response = await fetch(apiUrl, {
                method: "GET",
                credentials: "include",
            });
            if (!response.ok) {
                throw new Error("خطا در دریافت سبد خرید");
            }
            const cartData = await response.json();
            renderCart(cartData);
        } catch (error) {
            console.error(error.message);
        }
    }

    function renderCart(cartData) {
        const cartList = document.querySelector(".cart-canvas-parent");
        const totalElement = document.querySelector(".cart-canvas-foot-sum h5");
        const itemCountElement = document.querySelector("#offcanvasCartLabel small");
    
        cartList.innerHTML = "";
    
        if (!cartData.items || cartData.items.length === 0) {
            cartList.innerHTML = `
                <li class="nav-item">
                    <p class="text-center text-muted">سبد خرید خالی است</p>
                </li>
            `;
            totalElement.textContent = "0 تومان";
            itemCountElement.textContent = "(0 مورد)";
            return;
        }
    
        let totalPrice = 0;
        const uniqueItemsCount = cartData.items.length;
        cartData.items.forEach((item) => {
            const originalPrice = item.original_price || 0;
            const productPrice = item.product_price || 0; 
            const productQuantity = item.quantity || 1;
    
            totalPrice += productPrice * productQuantity;
    
            const cartItemHTML = `
                <li class="nav-item">
                    <div class="cart-canvas">
                        <div class="row align-items-center">
                            <div class="col-4 ps-0">
                                <img src="${item.product_image || 'assets/image/default-product.jpg'}" alt="تصویر محصول">
                            </div>
                            <div class="col-8">
                                <h3 class="text-overflow-3 font-16">${item.product_name || "نام محصول"}</h3>
                                <div class="product-box-suggest-price my-2 d-flex align-items-center justify-content-between">
                                    ${
                                        originalPrice > productPrice
                                            ? `<del class="text-muted">${originalPrice.toLocaleString()} تومان</del>`
                                            : ""
                                    }
                                    <ins class="font-25">${productPrice.toLocaleString()} تومان</ins>
                                </div>
                                <div class="cart-canvas-foot d-flex align-items-center justify-content-between">
                                    <div class="cart-canvas-count">
                                        <span>تعداد:</span>
                                        <span class="fw-bold">${productQuantity}</span>
                                    </div>
                                    <div class="cart-canvas-delete">
                                        <button class="btn delete-cart-item" data-product-id="${item.product}">
                                            <i class="bi bi-x"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </li>
            `;
            cartList.insertAdjacentHTML("beforeend", cartItemHTML);
        });
    
        totalElement.textContent = `${totalPrice.toLocaleString()} تومان`;
        itemCountElement.textContent = `(${uniqueItemsCount} مورد)`;
        addDeleteEventListeners();
    }
    
    function addDeleteEventListeners() {
        const deleteButtons = document.querySelectorAll(".delete-cart-item");
        deleteButtons.forEach((button) => {
            button.addEventListener("click", async (event) => {
                const productId = button.getAttribute("data-product-id");
                if (!productId) return;
    
                try {
                    const response = await fetch(apiUrl, {
                        method: "DELETE",
                        credentials: "include",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ product: productId })
                    });
    
                    if (!response.ok) {
                        throw new Error("خطا در حذف محصول");
                    }
    
                    const data = await response.json();
                    if (data) {
                        renderCart(data);
                    } else {
                        console.error("داده‌های نامعتبر از سرور دریافت شد");
                    }
                } catch (error) {
                    console.error("خطا:", error);
                }
            });
        });
    }

    fetchCart();
});
