// WanderLuxe Travel - Admin Panel Controller

// Update Booking Status
async function updateBookingStatus(bookingId, newStatus) {
  try {
    const res = await fetch(`/api/bookings/${bookingId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    const data = await res.json();
    if (res.ok) {
      showToast(`Booking status updated to ${newStatus}`, 'success');
      setTimeout(() => window.location.reload(), 800);
    } else {
      showToast(data.detail || 'Could not update booking status', 'error');
    }
  } catch (err) {
    showToast('Network error updating status', 'error');
  }
}

// Update Inquiry Status
async function updateInquiryStatus(inquiryId, newStatus) {
  try {
    const res = await fetch(`/api/inquiries/${inquiryId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    if (res.ok) {
      showToast(`Inquiry marked as ${newStatus}`, 'success');
      setTimeout(() => window.location.reload(), 800);
    } else {
      showToast('Failed to update inquiry', 'error');
    }
  } catch (err) {
    showToast('Network error', 'error');
  }
}

// Delete Inquiry
async function deleteInquiry(inquiryId) {
  if (!confirm('Are you sure you want to delete this customer inquiry?')) return;
  try {
    const res = await fetch(`/api/inquiries/${inquiryId}`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Inquiry deleted', 'success');
      setTimeout(() => window.location.reload(), 800);
    }
  } catch (err) {
    showToast('Failed to delete inquiry', 'error');
  }
}

// Delete Tour
async function deleteTour(tourId, tourTitle) {
  if (!confirm(`Are you sure you want to delete the tour: "${tourTitle}"?`)) return;
  try {
    const res = await fetch(`/api/tours/${tourId}`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Tour deleted successfully', 'success');
      setTimeout(() => window.location.reload(), 800);
    } else {
      showToast('Failed to delete tour', 'error');
    }
  } catch (err) {
    showToast('Network error', 'error');
  }
}

// Open / Close Add Tour Modal
function openAddTourModal() {
  const modal = document.getElementById('add-tour-modal');
  if (modal) {
    document.getElementById('tour-modal-title').innerText = 'Add New Tour Package';
    document.getElementById('tour-form').reset();
    document.getElementById('tour-form-id').value = '';
    modal.classList.remove('hidden');
  }
}

function closeAddTourModal() {
  const modal = document.getElementById('add-tour-modal');
  if (modal) modal.classList.add('hidden');
}

// Edit Tour - Prepopulate modal
async function editTour(tourId) {
  try {
    const res = await fetch(`/api/tours/${tourId}`);
    if (!res.ok) throw new Error('Tour not found');
    const tour = await res.json();

    document.getElementById('tour-modal-title').innerText = 'Edit Tour Package';
    document.getElementById('tour-form-id').value = tour._id;
    document.getElementById('form-title').value = tour.title;
    document.getElementById('form-destination').value = tour.destination;
    document.getElementById('form-country').value = tour.country;
    document.getElementById('form-category').value = tour.category;
    document.getElementById('form-duration-days').value = tour.duration_days;
    document.getElementById('form-duration-nights').value = tour.duration_nights;
    document.getElementById('form-price').value = tour.price;
    document.getElementById('form-discount-price').value = tour.discount_price || '';
    document.getElementById('form-image-url').value = tour.image_url;
    document.getElementById('form-description').value = tour.description;
    document.getElementById('form-featured').checked = !!tour.featured;
    document.getElementById('form-highlights').value = (tour.highlights || []).join('\n');
    document.getElementById('form-inclusions').value = (tour.inclusions || []).join('\n');

    document.getElementById('add-tour-modal').classList.remove('hidden');
  } catch (err) {
    showToast('Failed to load tour details for editing', 'error');
  }
}

// Submit Tour Form (Create or Update)
async function submitTourForm(event) {
  event.preventDefault();
  const form = event.target;
  const tourId = document.getElementById('tour-form-id').value;

  const highlights = document.getElementById('form-highlights').value.split('\n').map(s => s.trim()).filter(Boolean);
  const inclusions = document.getElementById('form-inclusions').value.split('\n').map(s => s.trim()).filter(Boolean);

  const payload = {
    title: document.getElementById('form-title').value,
    slug: document.getElementById('form-title').value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, ''),
    destination: document.getElementById('form-destination').value,
    country: document.getElementById('form-country').value,
    category: document.getElementById('form-category').value,
    duration_days: parseInt(document.getElementById('form-duration-days').value) || 1,
    duration_nights: parseInt(document.getElementById('form-duration-nights').value) || 0,
    price: parseFloat(document.getElementById('form-price').value) || 0,
    discount_price: document.getElementById('form-discount-price').value ? parseFloat(document.getElementById('form-discount-price').value) : null,
    image_url: document.getElementById('form-image-url').value,
    description: document.getElementById('form-description').value,
    featured: document.getElementById('form-featured').checked,
    highlights: highlights.length > 0 ? highlights : ["5-Star Accommodation", "Expert Local Guide"],
    inclusions: inclusions.length > 0 ? inclusions : ["All internal transfers", "Breakfast daily"],
    exclusions: ["International flights", "Personal expenses"]
  };

  try {
    let res;
    if (tourId) {
      // Update
      res = await fetch(`/api/tours/${tourId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    } else {
      // Create
      res = await fetch('/api/tours', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    }

    const data = await res.json();
    if (res.ok) {
      showToast(tourId ? 'Tour updated successfully!' : 'New Tour created successfully!', 'success');
      closeAddTourModal();
      setTimeout(() => window.location.reload(), 800);
    } else {
      showToast(data.detail || 'Failed to save tour', 'error');
    }
  } catch (err) {
    showToast('Network error while saving tour', 'error');
  }
}

// Seed Demo Data Trigger
async function triggerSeedData() {
  if (!confirm('This will seed the database with premium demo tours and sample bookings. Continue?')) return;
  try {
    const res = await fetch('/api/seed', { method: 'POST' });
    const data = await res.json();
    if (res.ok) {
      showToast('Database successfully seeded with demo packages!', 'success');
      setTimeout(() => window.location.reload(), 1000);
    } else {
      showToast('Seed failed: ' + (data.detail || 'unknown error'), 'error');
    }
  } catch (err) {
    showToast('Network error while seeding', 'error');
  }
}
