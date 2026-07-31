(function () {
    const modalEl = document.getElementById('registrationModal');
    if (!modalEl) return;

    const form = document.getElementById('registrationForm');
    const fieldMap = {
        first_name: { input: 'regFirstName', error: 'regFirstNameError' },
        last_name: { input: 'regLastName', error: 'regLastNameError' },
        email: { input: 'regEmail', error: 'regEmailError' },
        phone: { input: 'regPhone', error: 'regPhoneError' },
        notes: { input: 'regNotes', error: 'regNotesError' },
    };

    function clearFieldErrors() {
        document.getElementById('registrationFormAlert').classList.add('d-none');
        Object.values(fieldMap).forEach(function (ids) {
            const input = document.getElementById(ids.input);
            const errorEl = document.getElementById(ids.error);
            input.classList.remove('is-invalid');
            input.removeAttribute('aria-invalid');
            input.removeAttribute('aria-describedby');
            errorEl.textContent = '';
        });
    }

    function applyFieldErrors(errors) {
        if (!errors) return;
        Object.keys(fieldMap).forEach(function (field) {
            const fieldErrors = errors[field];
            if (!fieldErrors || !fieldErrors.length) return;
            const ids = fieldMap[field];
            const input = document.getElementById(ids.input);
            const errorEl = document.getElementById(ids.error);
            input.classList.add('is-invalid');
            input.setAttribute('aria-invalid', 'true');
            input.setAttribute('aria-describedby', ids.error);
            errorEl.textContent = fieldErrors.map(function (e) { return e.message; }).join(' ');
        });
    }

    function populateForm(data) {
        if (!data) return;
        Object.keys(fieldMap).forEach(function (field) {
            if (data[field] !== undefined) {
                document.getElementById(fieldMap[field].input).value = data[field];
            }
        });
    }

    function openModalForEvent(eventId, registerUrl, eventTitle) {
        clearFieldErrors();
        form.action = registerUrl;
        document.getElementById('registrationEventTitle').textContent = eventTitle || '';
        bootstrap.Modal.getOrCreateInstance(modalEl).show();
    }

    modalEl.addEventListener('show.bs.modal', function (event) {
        clearFieldErrors();
        const button = event.relatedTarget;
        if (button) {
            form.action = button.getAttribute('data-register-url');
            document.getElementById('registrationEventTitle').textContent = button.getAttribute('data-event-title') || '';
        }
    });

    const modalDataEl = document.getElementById('registration-modal-data');
    if (modalDataEl) {
        const modalData = JSON.parse(modalDataEl.textContent);
        const eventId = modalData.event_id;
        const trigger = document.querySelector('[data-event-id="' + eventId + '"]');
        if (trigger) {
            populateForm(modalData.data);
            openModalForEvent(eventId, trigger.getAttribute('data-register-url'), trigger.getAttribute('data-event-title'));
            applyFieldErrors(modalData.errors);
        }
    }
})();
