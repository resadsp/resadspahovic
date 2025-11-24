/**
* Template Name: iPortfolio - v3.8.1
* Template URL: https://bootstrapmade.com/iportfolio-bootstrap-portfolio-websites-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let elementPos = select(el).offsetTop
    window.scrollTo({
      top: elementPos,
      behavior: 'smooth'
    })
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select('body').classList.toggle('mobile-nav-active')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '.scrollto', function(e) {
    if (select(this.hash)) {
      e.preventDefault()

      let body = select('body')
      if (body.classList.contains('mobile-nav-active')) {
        body.classList.remove('mobile-nav-active')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Hero type effect
   */
  const typed = select('.typed')
  if (typed) {
    let typed_strings = typed.getAttribute('data-typed-items')
    typed_strings = typed_strings.split(',')
    new Typed('.typed', {
      strings: typed_strings,
      loop: true,
      typeSpeed: 100,
      backSpeed: 50,
      backDelay: 2000
    });
  }

  /**
   * Skills animation
   */
  let skilsContent = select('.skills-content');
  if (skilsContent) {
    new Waypoint({
      element: skilsContent,
      offset: '80%',
      handler: function(direction) {
        let progress = select('.progress .progress-bar', true);
        progress.forEach((el) => {
          el.style.width = el.getAttribute('aria-valuenow') + '%'
        });
      }
    })
  }

  /**
   * Porfolio isotope and filter
   */
  window.addEventListener('load', () => {
    let portfolioContainer = select('.portfolio-container');
    if (portfolioContainer) {
      let portfolioIsotope = new Isotope(portfolioContainer, {
        itemSelector: '.portfolio-item'
      });

      let portfolioFilters = select('#portfolio-flters li', true);

      on('click', '#portfolio-flters li', function(e) {
        e.preventDefault();
        portfolioFilters.forEach(function(el) {
          el.classList.remove('filter-active');
        });
        this.classList.add('filter-active');

        portfolioIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        portfolioIsotope.on('arrangeComplete', function() {
          AOS.refresh()
        });
      }, true);
    }

  });

  /**
   * Initiate portfolio lightbox 
   */
  const portfolioLightbox = GLightbox({
    selector: '.portfolio-lightbox'
  });

  /**
   * Portfolio details slider
   */
  new Swiper('.portfolio-details-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });

  /**
   * Testimonials slider
   */
  new Swiper('.testimonials-slider', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
        spaceBetween: 20
      },

      1200: {
        slidesPerView: 3,
        spaceBetween: 20
      }
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    })
  });

  /**
   * Initiate Pure Counter 
   */
  new PureCounter();
  /**
   * CV modal preview & download logic
   */
  (function(){
    const cvPath = 'assets/files/Resad_Spahovic_CV.pdf';
    let cvBlobUrl = null;
    const iframe = select('#cvIframe');
    const previewBtn = select('#cvPreviewBtn');
    const downloadBtn = select('#cvDownloadBtn');
    const modalEl = select('#cvModal');

    const isMobile = () => /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent || '');

    const loadBlob = () => {
      if (cvBlobUrl) return Promise.resolve(cvBlobUrl);
      return fetch(cvPath).then(res => {
        if (!res.ok) throw new Error('Network response was not ok');
        return res.blob();
      }).then(blob => {
        cvBlobUrl = window.URL.createObjectURL(blob);
        return cvBlobUrl;
      });
    };

    // Preview action: load blob and show in iframe
    if (previewBtn) {
      previewBtn.addEventListener('click', function(e){
        e.preventDefault();
        // On mobile devices prefer direct URL so native viewer handles filename and preview
        if (isMobile()) {
          if (iframe) iframe.src = cvPath;
          return;
        }
        loadBlob().then(url => {
          if (iframe) iframe.src = url;
        }).catch(() => {
          if (iframe) iframe.src = cvPath; // fallback to direct link
        });
      });
    }

    // Download action: ensure blob is loaded then trigger download
    if (downloadBtn) {
      downloadBtn.addEventListener('click', function(e){
        e.preventDefault();
        // On mobile some browsers mishandle blob downloads — open direct URL to let server headers control filename
        if (isMobile()) {
          window.open(cvPath, '_blank');
          return;
        }
        loadBlob().then(url => {
          const a = document.createElement('a');
          a.href = url;
          a.download = 'Resad_Spahovic_CV.pdf';
          document.body.appendChild(a);
          a.click();
          a.remove();
        }).catch(() => {
          window.open(cvPath, '_blank');
        });
      });
    }

    // When modal shown, auto-load preview
    if (modalEl) {
      modalEl.addEventListener('shown.bs.modal', function(){
        // If mobile nav is open, close it so modal is visible
        try {
          const body = select('body');
          if (body && body.classList.contains('mobile-nav-active')) {
            body.classList.remove('mobile-nav-active');
            const navbarToggle = select('.mobile-nav-toggle');
            if (navbarToggle) {
              navbarToggle.classList.remove('bi-x');
              navbarToggle.classList.add('bi-list');
            }
          }
        } catch (err) {
          // ignore
        }

        // Load preview
        loadBlob().then(url => { if (iframe) iframe.src = url; }).catch(()=>{ if (iframe) iframe.src = cvPath; });
      });
      modalEl.addEventListener('hidden.bs.modal', function(){
        if (iframe) iframe.src = '';
        if (cvBlobUrl) { URL.revokeObjectURL(cvBlobUrl); cvBlobUrl = null; }
      });
    }
  })();

})()