(function ($) {
    "use strict";
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 400) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });


    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 600, 'linear');
        return false;
    });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Offline Carousel
    $('.class-carousel').owlCarousel({
    center: false,
    smartSpeed: 1000,
    items: 1,
    loop: true,
    stagePadding: 0,
    margin: 0,
    autoplay: true,
    dots: false,
    responsive: {
        600: {
            margin: 20,
            items: 2
            },
        1000: {
            margin: 30,
            stagePadding: 20,
            items: 3
            },
        1200: {
            margin: 30,
            stagePadding: 20,
            items: 4
            }
        }
    });

    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
    center: true,
    smartSpeed: 1000,
    items: 1,
    loop: true,
    autoplay: true,
    dots: false,
    responsive: {
        600: {
            margin: 20,
            items: 2
            },
        1000: {
            margin: 30,
            stagePadding: 20,
            items: 3
            },
        }
    });

    // Custom Filter
    $(document).ready(function() {
        var iso = $('.grid').isotope({
        itemSelector: '.item',
        layoutMode: 'fitRows'
        });
        // Define your filter function
        function customFilter() {
            var trackFilter = $('#track').val();
            var languageFilter = $('#language').val();

            iso.isotope({
              filter: function() {
                var item = $(this);
                var itemTrack = item.attr('data-track');
                var itemLanguage = item.attr('data-language');

                var trackMatch = trackFilter === 'All' || itemTrack === trackFilter;
                var languageMatch = languageFilter === 'All' || itemLanguage === languageFilter;

                return trackMatch && languageMatch;
              }
            });
          }
        // Call the filter function whenever the filter options change
        $('#track').on('change', customFilter);
        $('#language').on('change', customFilter);

        customFilter();
    });

})(jQuery);
