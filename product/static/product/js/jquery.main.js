// page init
jQuery(function(){
  initSlider();
  initCustomHover();
  initMasonry();
  initFixedScrollBlock();
  new WOW({
    duration: 0.5,
    offset: 50
  }).init();

	jQuery(window).trigger('resize');
});

function initMasonry() {
  var featuredBlog = jQuery('.featured-blog');

  if (featuredBlog.length) {
    featuredBlog.masonry({
      itemSelector: '.blog-item',
      columnWidth: 1,
      percentPosition: true
    });
  }
}

function initSlider() {
  jQuery('.intro-carousel').slick({
    adaptiveHeight: true,
    slide: '.slide-item',
    autoplay: true,
    autoplaySpeed: 6000,
    appendArrows: '.intro-carousel .carousel-arrows'
  });
}

// add classes on hover/touch
function initCustomHover() {
  jQuery('.featured-article .article-img').touchHover();
}

// initialize fixed blocks on scroll
function initFixedScrollBlock() {
	jQuery('#wrapper').fixedScrollBlock({
		slideBlock: '#header',
		positionType: 'fixed'
	});
}

/*
 * FixedScrollBlock
 */
;(function($, window) {
	'use strict';
	var isMobileDevice = ('ontouchstart' in window) ||
						(window.DocumentTouch && document instanceof DocumentTouch) ||
						/Windows Phone/.test(navigator.userAgent);

	function FixedScrollBlock(options) {
		this.options = $.extend({
			fixedActiveClass: 'fixed-position',
			slideBlock: '[data-scroll-block]',
			positionType: 'auto',
			fixedOnlyIfFits: true,
			container: null,
			animDelay: 100,
			animSpeed: 200,
			extraBottom: 0,
			extraTop: 0
		}, options);
		this.initStructure();
		this.attachEvents();
	}
	FixedScrollBlock.prototype = {
		initStructure: function() {
			// find elements
			this.win = $(window);
			this.container = $(this.options.container);
			this.slideBlock = this.container.find(this.options.slideBlock);

			// detect method
			if(this.options.positionType === 'auto') {
				this.options.positionType = isMobileDevice ? 'absolute' : 'fixed';
			}
		},
		attachEvents: function() {
			var self = this;

			// bind events
			this.onResize = function() {
				self.resizeHandler();
			};
			this.onScroll = function() {
				self.scrollHandler();
			};

			// handle events
			this.win.on({
				resize: this.onResize,
				scroll: this.onScroll
			});

			// initial handler call
			this.resizeHandler();
		},
		recalculateOffsets: function() {
			var defaultOffset = this.slideBlock.offset(),
				defaultPosition = this.slideBlock.position(),
				holderOffset = this.container.offset(),
				windowSize = this.win.height();

			this.data = {
				windowHeight: this.win.height(),
				windowWidth: this.win.width(),

				blockPositionLeft: defaultPosition.left,
				blockPositionTop: defaultPosition.top,

				blockOffsetLeft: defaultOffset.left,
				blockOffsetTop: defaultOffset.top,
				blockHeight: this.slideBlock.innerHeight(),

				holderOffsetLeft: holderOffset.left,
				holderOffsetTop: holderOffset.top,
				holderHeight: this.container.innerHeight()
			};
		},
		isVisible: function() {
			return this.slideBlock.prop('offsetHeight');
		},
		fitsInViewport: function() {
			if(this.options.fixedOnlyIfFits && this.data) {
				return this.data.blockHeight + this.options.extraTop <= this.data.windowHeight;
			} else {
				return true;
			}
		},
		resizeHandler: function() {
			if(this.isVisible()) {
				FixedScrollBlock.stickyMethods[this.options.positionType].onResize.apply(this, arguments);
				this.scrollHandler();
			}
		},
		scrollHandler: function() {
			if(this.isVisible()) {
				if(!this.data) {
					this.resizeHandler();
					return;
				}
				this.currentScrollTop = this.win.scrollTop();
				this.currentScrollLeft = this.win.scrollLeft();
				FixedScrollBlock.stickyMethods[this.options.positionType].onScroll.apply(this, arguments);
			}
		},
		refresh: function() {
			// refresh dimensions and state if needed
			if(this.data) {
				this.data.holderHeight = this.container.innerHeight();
				this.data.blockHeight = this.slideBlock.innerHeight();
				this.scrollHandler();
			}
		},
		destroy: function() {
			// remove event handlers and styles
			this.slideBlock.removeAttr('style').removeClass(this.options.fixedActiveClass);
			this.win.off({
				resize: this.onResize,
				scroll: this.onScroll
			});
		}
	};

	// sticky methods
	FixedScrollBlock.stickyMethods = {
		fixed: {
			onResize: function() {
				this.slideBlock.removeAttr('style');
				this.recalculateOffsets();
			},
			onScroll: function() {
				if(this.fitsInViewport() && this.currentScrollTop + this.options.extraTop > this.data.blockOffsetTop) {
					if(this.currentScrollTop + this.options.extraTop + this.data.blockHeight > this.data.holderOffsetTop + this.data.holderHeight - this.options.extraBottom) {
						this.slideBlock.css({
							position: 'absolute',
							top: this.data.blockPositionTop + this.data.holderHeight - this.data.blockHeight - this.options.extraBottom - (this.data.blockOffsetTop - this.data.holderOffsetTop),
							left: this.data.blockPositionLeft
						});
					} else {
						this.slideBlock.css({
							position: 'fixed',
							top: this.options.extraTop,
							left: this.data.blockOffsetLeft - this.currentScrollLeft
						});
					}
					this.slideBlock.addClass(this.options.fixedActiveClass);
				} else {
					this.slideBlock.removeClass(this.options.fixedActiveClass).removeAttr('style');
				}
			}
		},
		absolute: {
			onResize: function() {
				this.slideBlock.removeAttr('style');
				this.recalculateOffsets();

				this.slideBlock.css({
					position: 'absolute',
					top: this.data.blockPositionTop,
					left: this.data.blockPositionLeft
				});

				this.slideBlock.addClass(this.options.fixedActiveClass);
			},
			onScroll: function() {
				var self = this;
				clearTimeout(this.animTimer);
				this.animTimer = setTimeout(function() {
					var currentScrollTop = self.currentScrollTop + self.options.extraTop,
						initialPosition = self.data.blockPositionTop - (self.data.blockOffsetTop - self.data.holderOffsetTop),
						maxTopPosition =  self.data.holderHeight - self.data.blockHeight - self.options.extraBottom,
						currentTopPosition = initialPosition + Math.min(currentScrollTop - self.data.holderOffsetTop, maxTopPosition),
						calcTopPosition = self.fitsInViewport() && currentScrollTop > self.data.blockOffsetTop ? currentTopPosition : self.data.blockPositionTop;

					self.slideBlock.stop().animate({
						top: calcTopPosition
					}, self.options.animSpeed);
				}, this.options.animDelay);
			}
		}
	};

	// jQuery plugin interface
	$.fn.fixedScrollBlock = function(options) {
		return this.each(function() {
			var params = $.extend({}, options, {container: this}),
				instance = new FixedScrollBlock(params);
			$.data(this, 'FixedScrollBlock', instance);
		});
	};

	// module exports
	window.FixedScrollBlock = FixedScrollBlock;
}(jQuery, this));

/*
 * Mobile hover plugin
 */
;(function($){
  // detect device type
  var isTouchDevice = ('ontouchstart' in window) || window.DocumentTouch && document instanceof DocumentTouch,
    isWinPhoneDevice = /Windows Phone/.test(navigator.userAgent);

  // define events
  var eventOn = (isTouchDevice && 'touchstart') || (isWinPhoneDevice && navigator.pointerEnabled && 'pointerdown') || (isWinPhoneDevice && navigator.msPointerEnabled && 'MSPointerDown') || 'mouseenter',
    eventOff = (isTouchDevice && 'touchend') || (isWinPhoneDevice && navigator.pointerEnabled && 'pointerup') || (isWinPhoneDevice && navigator.msPointerEnabled && 'MSPointerUp') || 'mouseleave';

  // event handlers
  var toggleOn, toggleOff, preventHandler;
  if(isTouchDevice || isWinPhoneDevice) {
    // prevent click handler
    preventHandler = function(e) {
      e.preventDefault();
    };

    // touch device handlers
    toggleOn = function(e) {
      var options = e.data, element = $(this);

      var toggleOff = function(e) {
        var target = $(e.target);
        if (!target.is(element) && !target.closest(element).length) {
          element.removeClass(options.hoverClass);
          element.off('click', preventHandler);
          if(options.onLeave) options.onLeave(element);
          $(document).off(eventOn, toggleOff);
        }
      };

      if(!element.hasClass(options.hoverClass)) {
        element.addClass(options.hoverClass);
        element.one('click', preventHandler);
        $(document).on(eventOn, toggleOff);
        if(options.onHover) options.onHover(element);
      }
    };
  } else {
    // desktop browser handlers
    toggleOn = function(e) {
      var options = e.data, element = $(this);
      element.addClass(options.hoverClass);
      $(options.context).on(eventOff, options.selector, options, toggleOff);
      if(options.onHover) options.onHover(element);
    };
    toggleOff = function(e) {
      var options = e.data, element = $(this);
      element.removeClass(options.hoverClass);
      $(options.context).off(eventOff, options.selector, toggleOff);
      if(options.onLeave) options.onLeave(element);
    };
  }

  // jQuery plugin
  $.fn.touchHover = function(opt) {
    window.ele = this;

    var options = $.extend({
      context: this.context,
      selector: this.selector,
      hoverClass: 'hover'
    }, opt);

    $(this.context).on(eventOn, this.selector, options, toggleOn);
    return this;
  };
}(jQuery));