// Resources page enhancements
// Filtering, phone auto-linking, and count updates

(function(){
  const searchInput = document.getElementById('resourceSearch');
  const countEl = document.getElementById('resourceCount');
  const items = Array.from(document.querySelectorAll('.resource-item'));

  function formatCount(visible){
    countEl.textContent = visible + ' resource' + (visible === 1 ? '' : 's') + ' shown';
  }

  function filter(){
    const term = (searchInput.value || '').toLowerCase();
    let visible = 0;
    items.forEach(item => {
      const text = item.textContent.toLowerCase();
      const match = text.includes(term);
      item.style.display = match ? '' : 'none';
      if(match) visible++;
    });
    formatCount(visible);
  }

  if(searchInput){
    searchInput.addEventListener('input', filter);
    filter();
  }

  // Auto-link phone numbers: (XXX) XXX-XXXX
  const phonePattern = /(\(\d{3}\) \d{3}-\d{4})/g;
  items.forEach(item => {
    item.innerHTML = item.innerHTML.replace(phonePattern, m => {
      const digits = m.replace(/[^\d]/g,'');
      return `<a href="tel:${digits}" class="phone-link">${m}</a>`;
    });
  });

  // Smooth scroll fallback for older browsers
  if(!('scrollBehavior' in document.documentElement.style)){
    document.querySelectorAll('a[href^="#"]').forEach(a=>{
      a.addEventListener('click', e=>{
        const targetId = a.getAttribute('href').slice(1);
        const target = document.getElementById(targetId);
        if(target){
          e.preventDefault();
          window.scrollTo({top: target.offsetTop, left:0});
        }
      });
    });
  }
})();
