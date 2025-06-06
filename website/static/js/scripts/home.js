const home = {
    init: function () {
        new Glide('.glide', {
            type: 'carousel',
            perView: 4,
            breakpoints: {
                1200: {
                    perView: 4
                },
                992: {
                    perView: 3
                },
                768: {
                    perView: 2
                },
                576: {
                    perView: 1
                }
            }
        }).mount();
    }
};