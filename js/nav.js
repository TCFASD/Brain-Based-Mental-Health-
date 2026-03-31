// Mobile hamburger menu toggle
document.addEventListener('DOMContentLoaded', function () {
  var btn = document.querySelector('.hamburger');
  var nav = document.querySelector('.nav-links');
  if (!btn || !nav) return;

  btn.addEventListener('click', function () {
    btn.classList.toggle('open');
    nav.classList.toggle('open');
  });

  // Close menu when a link is clicked
  nav.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      btn.classList.remove('open');
      nav.classList.remove('open');
    });
  });
});

// FAQ accordion toggle
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.faq-question').forEach(function (q) {
    q.addEventListener('click', function () {
      this.classList.toggle('open');
      this.nextElementSibling.classList.toggle('show');
    });
  });
});
