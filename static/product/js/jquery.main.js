jQuery(document).ready(function(){
  initSlider();
});

function initSlider() {
  jQuery('.intro-carousel').slick({
    adaptiveHeight: true,
    slide: '.slide-item',
    appendArrows: '.intro-carousel .carousel-arrows'
  });
}