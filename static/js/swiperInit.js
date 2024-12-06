

//========= start free mode ==============/
let swiperFreeMode = new Swiper(".free-mode", {
    slidesPerView: "auto",
    spaceBetween: 10,
    freeMode: true,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});
//========= end free mode ==============/

//=========== product gallery ===================//

let proSwiper = new Swiper(".product-gallery-thumb", {
    spaceBetween: 10,
    slidesPerView: 4,
    freeMode: true,
    watchSlidesProgress: true,
    breakpoints: {
        // when window width is >= 320px
        320: {
            slidesPerView: 3,
            spaceBetween: 10
        },
    },
});
let proThumbswiper = new Swiper(".product-gallery", {
    spaceBetween: 10,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    zoom: {
        maxRatio: 3,
        minRation: 1
    },
    thumbs: {
        swiper: proSwiper,
    },
});

//=========== end product gallery ===================//

//========= start product box ==============/

let swiperProSlider = new Swiper(".pro-slider", {
    slidesPerView: 5,
    spaceBetween: 10,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        100: {
            slidesPerView: 1,
        },
        576: {
            slidesPerView: 2,
        },
        768: {
            slidesPerView: 3,
        },
        1024: {
            slidesPerView: 4,
        },
        1400: {
            slidesPerView: 5,
        }
    },
});

//========= end product box ==============//

// /========= start offer ==============/


var swiperOfferItemLink = new Swiper("#offerItemLink", {
    spaceBetween: 10,
    slidesPerView: 4,
    freeMode: true,
    watchSlidesProgress: true,
    allowTouchMove: false,
});
var swiperOfferItem = new Swiper("#offerItem", {
    effect: "fade",
    speed: 1000,
    loop: true,
    autoplay: {
        delay: 5000,
        disableOnInteraction: false,
    },
    spaceBetween: 10,
    thumbs: {
        swiper: swiperOfferItemLink,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
});

// ========= end offer gallery ==============/


// ========= start blog slider ==============/

var blogSLiderSw = new Swiper(".blog-slider-sw", {
    slidesPerView: 3,
    spaceBetween: 10,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        100: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
    }
});

// ========= end blog slider ==============/

//=========== swiper-small-slider ===========//

var smallSlider = new Swiper(".swiper-small-slider", {
    spaceBetween: 10,
    slidesPerView: 1,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    loop: true,
    speed: 2500,
    autoplay: {
        delay: 3500,
        disableOnInteraction: false,
    },
});

//=========== end swiper-small-slider ===========//

//=========== start category slider ===========//

var catSlider = new Swiper(".cat-slider", {
    slidesPerView: 5,
    spaceBetween: 10,
    loop: true,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
    },
    breakpoints: {
        100: {
            slidesPerView: 1,
        },
        575: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 4,
        },
    },
});

//=========== end category slider ===========//

//=========== amazing slider ===========//
var amazing = new Swiper(".amazing", {
    slidesPerView: "auto",
    spaceBetween: 10,
    freeMode: true,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});
//===========end amazing slider ===========//

//========= start product-slider =========///

var proSlider = new Swiper("#product-slider", {
    slidesPerView: 5,
    spaceBetween: 10,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        100: {
            slidesPerView: 1,
            spaceBetween: 20,
        },
        576: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        1024: {
            slidesPerView: 3,
            spaceBetween: 20,
        },
        1200: {
            slidesPerView: 4,
            spaceBetween: 20,
        },
    },
});

///=============end product-slider ============/

//========= start home slider =========///
var swiperMainSlider = new Swiper("#homeSlider", {
    spaceBetween: 30,
    centeredSlides: true,
    loop: true,
    autoplay: {
        delay: 5500,
        disableOnInteraction: false,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});

///=============end home slider ============/


//========= start product box ==============/

var swiper = new Swiper(".product-slider-swiper", {
    slidesPerView: 5,
    spaceBetween: 10,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        100: {
            slidesPerView: 1,
        },
        576: {
            slidesPerView: 2,
        },
        768: {
            slidesPerView: 3,
        },
        1024: {
            slidesPerView: 4,
        },
        1400: {
            slidesPerView: 5,
        }
    },
});

//========= end product box ==============/

//============= sugget moment =============//

let swiperSugget = new Swiper(".suggetMoment", {
    slidesPerView: 1,
    spaceBetween: 30,
    loop: true,
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
    },
    speed: 500,
    on: {
        init: function () {
            $(".swiper-progress-bar").removeClass("animate");
            $(".swiper-progress-bar").removeClass("active");
            $(".swiper-progress-bar").eq(0).addClass("animate");
            $(".swiper-progress-bar").eq(0).addClass("active");
        },
        slideChangeTransitionStart: function () {
            $(".swiper-progress-bar").removeClass("animate");
            $(".swiper-progress-bar").removeClass("active");
            $(".swiper-progress-bar").eq(0).addClass("active");
        },
        slideChangeTransitionEnd: function () {
            $(".swiper-progress-bar").eq(0).addClass("animate");
        }
    }
});

//============= end sugget moment =============//
