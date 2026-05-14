/**
 * Scalora – Main JavaScript
 * Handles: scroll effects, hover animations, AOS-like reveals
 */

(function () {
  'use strict';

  /* ── Intersection Observer for reveal animations ── */
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

  document.querySelectorAll(
    '.feature-card, .step-card, .testimonial-card, .service-card, .blog-card, .ebook-card, .job-card, .visual-card, .metric-item'
  ).forEach(el => {
    el.classList.add('reveal-on-scroll');
    revealObserver.observe(el);
  });

  /* ── 3D tilt effect for cards ── */
  function applyTilt(el) {
    el.addEventListener('mousemove', (e) => {
      const rect = el.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = ((y - centerY) / centerY) * -5;
      const rotateY = ((x - centerX) / centerX) * 5;
      el.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
      el.style.transition = 'transform 0.1s ease';
    });
    el.addEventListener('mouseleave', () => {
      el.style.transform = '';
      el.style.transition = 'transform 0.4s ease';
    });
  }

  document.querySelectorAll('.feature-card, .step-card, .why-card').forEach(applyTilt);

  /* ── Smooth anchor scroll ── */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ── Counter animation ── */
  function animateCounter(el) {
    const target = parseFloat(el.dataset.target || el.textContent.replace(/[^0-9.]/g, ''));
    const suffix = el.textContent.replace(/[0-9.]/g, '');
    const duration = 1800;
    const step = target / (duration / 16);
    let current = 0;
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = (Number.isInteger(target) ? Math.floor(current) : current.toFixed(1)) + suffix;
      if (current >= target) clearInterval(timer);
    }, 16);
  }

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.stat-num, .metric-val').forEach(el => {
    counterObserver.observe(el);
  });

  /* ── Glassmorphism shimmer on hover ── */
  document.querySelectorAll('.glass-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      card.style.setProperty('--shimmer-x', `${x}%`);
      card.style.setProperty('--shimmer-y', `${y}%`);
    });
  });

  /* ── Navbar active link ── */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.scalora-nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href !== '/' && currentPath.startsWith(href)) {
      link.classList.add('active-nav');
      link.style.color = 'var(--gold)';
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active-nav');
      link.style.color = 'var(--gold)';
    }
  });

})();

/* ── Reveal animation CSS injected ── */
const style = document.createElement('style');
style.textContent = `
  .reveal-on-scroll {
    opacity: 0;
    transform: translateY(28px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }
  .reveal-on-scroll.revealed {
    opacity: 1;
    transform: translateY(0);
  }
  .feature-card:nth-child(2) { transition-delay: 0.08s; }
  .feature-card:nth-child(3) { transition-delay: 0.16s; }
  .feature-card:nth-child(4) { transition-delay: 0.24s; }
  .feature-card:nth-child(5) { transition-delay: 0.32s; }
  .feature-card:nth-child(6) { transition-delay: 0.40s; }
  .step-card:nth-child(2) { transition-delay: 0.1s; }
  .step-card:nth-child(3) { transition-delay: 0.2s; }
  .step-card:nth-child(4) { transition-delay: 0.3s; }
  .glass-card {
    --shimmer-x: 50%;
    --shimmer-y: 50%;
  }
  .glass-card::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: radial-gradient(
      circle at var(--shimmer-x) var(--shimmer-y),
      rgba(201,179,126,0.06) 0%,
      transparent 60%
    );
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s;
  }
  .glass-card:hover::after { opacity: 1; }
  .glass-card { position: relative; }
  .active-nav { color: var(--gold) !important; }
`;
document.head.appendChild(style);
