// WanderLuxe Travel - Main Client Logic

// Toast Notification System
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  const bgClass = type === 'success' ? 'bg-emerald-600 text-white' : type === 'error' ? 'bg-rose-600 text-white' : 'bg-slate-800 text-white';
  const icon = type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ';

  toast.className = `toast flex items-center gap-3 px-5 py-3.5 rounded-xl shadow-xl font-medium text-sm transition-all duration-300 ${bgClass}`;
  toast.innerHTML = `<span class="text-base font-bold">${icon}</span> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Mobile Menu Drawer Toggle
function toggleMobileMenu() {
  const menu = document.getElementById('mobile-menu');
  if (menu) {
    menu.classList.toggle('hidden');
  }
}

// Global Currency Formatter
function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(amount);
}

// Tours Catalog Filtering Logic
function initToursFilter() {
  const searchInput = document.getElementById('tour-search');
  const categoryFilter = document.getElementById('category-filter');
  const priceSlider = document.getElementById('price-slider');
  const priceValue = document.getElementById('price-value');
  const sortSelect = document.getElementById('sort-select');
  const toursContainer = document.getElementById('tours-grid');
  const noResults = document.getElementById('no-tours-found');

  if (!toursContainer) return;

  const tourCards = Array.from(toursContainer.querySelectorAll('.tour-item'));

  function filterTours() {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const category = categoryFilter ? categoryFilter.value : 'all';
    const maxPrice = priceSlider ? parseFloat(priceSlider.value) : Infinity;
    const sortBy = sortSelect ? sortSelect.value : 'default';

    let visibleCount = 0;

    const matchedCards = tourCards.filter(card => {
      const title = card.dataset.title.toLowerCase();
      const dest = card.dataset.destination.toLowerCase();
      const cat = card.dataset.category;
      const price = parseFloat(card.dataset.price);

      const matchesQuery = !query || title.includes(query) || dest.includes(query);
      const matchesCat = category === 'all' || cat.toLowerCase() === category.toLowerCase();
      const matchesPrice = price <= maxPrice;

      const isMatch = matchesQuery && matchesCat && matchesPrice;
      if (isMatch) visibleCount++;
      return isMatch;
    });

    // Sorting
    if (sortBy === 'price-low') {
      matchedCards.sort((a, b) => parseFloat(a.dataset.price) - parseFloat(b.dataset.price));
    } else if (sortBy === 'price-high') {
      matchedCards.sort((a, b) => parseFloat(b.dataset.price) - parseFloat(a.dataset.price));
    } else if (sortBy === 'rating') {
      matchedCards.sort((a, b) => parseFloat(b.dataset.rating) - parseFloat(a.dataset.rating));
    } else if (sortBy === 'duration') {
      matchedCards.sort((a, b) => parseInt(b.dataset.duration) - parseInt(a.dataset.duration));
    }

    // Update DOM
    tourCards.forEach(card => card.style.display = 'none');
    matchedCards.forEach(card => {
      card.style.display = 'flex';
      toursContainer.appendChild(card);
    });

    if (noResults) {
      noResults.style.display = visibleCount === 0 ? 'block' : 'none';
    }

    const countDisplay = document.getElementById('tour-count-display');
    if (countDisplay) {
      countDisplay.innerText = `Showing ${visibleCount} exceptional journeys`;
    }
  }

  if (searchInput) searchInput.addEventListener('input', filterTours);
  if (categoryFilter) categoryFilter.addEventListener('change', filterTours);
  if (priceSlider) {
    priceSlider.addEventListener('input', (e) => {
      if (priceValue) priceValue.innerText = `$${e.target.value}`;
      filterTours();
    });
  }
  if (sortSelect) sortSelect.addEventListener('change', filterTours);

  // Trigger initial
  filterTours();
}

// Live Booking Calculator on Tour Details Page
function initBookingWidget(basePrice, discountPrice) {
  const effectivePrice = discountPrice || basePrice;
  const adultsInput = document.getElementById('booking-adults');
  const childrenInput = document.getElementById('booking-children');
  const totalPriceElem = document.getElementById('booking-total-price');
  const baseBreakdownElem = document.getElementById('booking-base-breakdown');
  const taxBreakdownElem = document.getElementById('booking-tax-breakdown');

  function calculate() {
    const adults = parseInt(adultsInput ? adultsInput.value : 1) || 1;
    const children = parseInt(childrenInput ? childrenInput.value : 0) || 0;
    
    // Children get 50% discount
    const baseTotal = (adults * effectivePrice) + (children * effectivePrice * 0.5);
    const taxes = baseTotal * 0.05; // 5% tourism & service fee
    const grandTotal = baseTotal + taxes;

    if (totalPriceElem) totalPriceElem.innerText = formatCurrency(grandTotal);
    if (baseBreakdownElem) baseBreakdownElem.innerText = formatCurrency(baseTotal);
    if (taxBreakdownElem) taxBreakdownElem.innerText = formatCurrency(taxes);

    return { adults, children, grandTotal };
  }

  if (adultsInput) adultsInput.addEventListener('change', calculate);
  if (childrenInput) childrenInput.addEventListener('change', calculate);

  // Initial calculation
  calculate();
}

// Handle Direct Booking Form Submission
async function submitBooking(event, tourId, tourTitle) {
  event.preventDefault();
  const form = event.target;
  const submitBtn = form.querySelector('button[type="submit"]');
  const originalBtnText = submitBtn.innerHTML;

  submitBtn.disabled = true;
  submitBtn.innerHTML = `<span class="inline-block animate-spin mr-2">⟳</span> Securing Reservation...`;

  const data = {
    tour_id: tourId,
    tour_title: tourTitle,
    customer_name: form.customer_name.value,
    customer_email: form.customer_email.value,
    customer_phone: form.customer_phone.value,
    travel_date: form.travel_date.value,
    adults: parseInt(form.adults.value) || 1,
    children: parseInt(form.children.value) || 0,
    total_price: parseFloat(form.total_price.value) || 0,
    payment_method: form.payment_method.value,
    special_requests: form.special_requests ? form.special_requests.value : ""
  };

  try {
    const response = await fetch('/api/bookings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    if (response.ok && result.booking_ref) {
      showToast('Booking successfully placed! Redirecting to your confirmation voucher...', 'success');
      setTimeout(() => {
        window.location.href = `/booking-confirmation/${result.booking_ref}`;
      }, 1200);
    } else {
      showToast(result.detail || 'Could not process booking. Please try again.', 'error');
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnText;
    }
  } catch (err) {
    showToast('Network error while booking. Please try again.', 'error');
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalBtnText;
  }
}

// Contact Form Submission
async function submitContactForm(event) {
  event.preventDefault();
  const form = event.target;
  const submitBtn = form.querySelector('button[type="submit"]');
  const originalBtnText = submitBtn.innerHTML;

  submitBtn.disabled = true;
  submitBtn.innerHTML = `<span class="inline-block animate-spin mr-2">⟳</span> Sending Message...`;

  const payload = {
    name: form.name.value,
    email: form.email.value,
    phone: form.phone.value,
    destination: form.destination ? form.destination.value : "General",
    message: form.message.value
  };

  try {
    const res = await fetch('/api/inquiries', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (res.ok) {
      showToast('Thank you! Your inquiry has been sent to our travel concierge.', 'success');
      form.reset();
    } else {
      showToast(result.detail || 'Failed to send message.', 'error');
    }
  } catch (err) {
    showToast('Failed to send inquiry. Please check your connection.', 'error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalBtnText;
  }
}

// Newsletter Form Submission
function submitNewsletter(event) {
  event.preventDefault();
  const input = event.target.querySelector('input[type="email"]');
  if (input && input.value) {
    showToast('Subscribed! You will receive exclusive VIP travel deals.', 'success');
    input.value = '';
  }
}

// Accordion Toggler for Itinerary
function toggleAccordion(id) {
  const item = document.getElementById(id);
  const icon = document.getElementById(`icon-${id}`);
  if (item) {
    item.classList.toggle('hidden');
    if (icon) {
      icon.classList.toggle('rotate-180');
    }
  }
}

// Document Ready
document.addEventListener('DOMContentLoaded', () => {
  initToursFilter();
});
