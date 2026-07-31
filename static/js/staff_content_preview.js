(function () {
    'use strict';

    function getCookie(name) {
        var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? decodeURIComponent(match[2]) : '';
    }

    function initFrameEditor(iframe) {
        if (!iframe) {
            return;
        }

        iframe.addEventListener('load', function () {
            try {
                var doc = iframe.contentDocument;
                if (!doc) {
                    return;
                }
                doc.querySelectorAll('.staff-editable').forEach(function (el) {
                    el.addEventListener('click', function (event) {
                        event.preventDefault();
                        event.stopPropagation();
                        openEditor(el);
                    });
                    el.addEventListener('keydown', function (event) {
                        if (event.key === 'Enter' || event.key === ' ') {
                            event.preventDefault();
                            openEditor(el);
                        }
                    });
                });
            } catch (err) {
                console.warn('Preview frame editor init failed', err);
            }
        });
    }

    var modalEl = document.getElementById('contentEditModal');
    var modal = modalEl && window.bootstrap ? new bootstrap.Modal(modalEl) : null;
    var activeEl = null;
    var activeKey = '';
    var activeFormat = 'html';
    var iframe = document.getElementById('site-preview-frame');

    function openEditor(el) {
        if (!modal) {
            return;
        }
        activeEl = el;
        activeKey = el.getAttribute('data-content-key') || '';
        activeFormat = el.getAttribute('data-content-format') || 'html';

        var label = activeKey.replace(/-/g, ' ');
        document.getElementById('contentEditModalLabel').textContent = 'Edit: ' + label;
        document.getElementById('contentEditHint').textContent =
            activeFormat === 'plain'
                ? 'Short plain text — no formatting.'
                : 'Use the toolbar for bold, italic, and lists.';

        var plainWrap = document.getElementById('contentEditPlainWrap');
        var richWrap = document.getElementById('contentEditRichWrap');
        var plainField = document.getElementById('contentEditPlain');
        var richField = document.getElementById('contentEditRich');

        var currentText = el.textContent.trim();
        if (activeFormat === 'plain') {
            plainWrap.classList.remove('d-none');
            richWrap.classList.add('d-none');
            plainField.value = currentText;
        } else {
            plainWrap.classList.add('d-none');
            richWrap.classList.remove('d-none');
            richField.value = el.innerHTML.trim();
            var widget = richWrap.querySelector('[data-staff-rich-text]');
            if (widget) {
                delete widget.dataset.staffRichTextInit;
                widget.querySelectorAll('.staff-rich-quill').forEach(function (node) {
                    node.innerHTML = '';
                });
                if (window.initStaffRichText) {
                    window.initStaffRichText(widget);
                }
            }
        }

        document.getElementById('contentEditStatus').textContent = '';
        modal.show();
    }

    function getSaveConfig() {
        var frameWin = iframe && iframe.contentWindow;
        return frameWin && frameWin.STAFF_CONTENT_PREVIEW ? frameWin.STAFF_CONTENT_PREVIEW : null;
    }

    function collectBody() {
        if (activeFormat === 'plain') {
            return document.getElementById('contentEditPlain').value;
        }
        var richField = document.getElementById('contentEditRich');
        var widget = document.getElementById('contentEditRichWrap').querySelector('[data-staff-rich-text]');
        var quillEl = widget && widget.querySelector('.staff-rich-quill .ql-editor');
        if (quillEl) {
            return quillEl.innerHTML;
        }
        return richField.value;
    }

    function saveContent() {
        var config = getSaveConfig();
        if (!config || !activeKey || !activeEl) {
            return;
        }

        var status = document.getElementById('contentEditStatus');
        var saveBtn = document.getElementById('contentEditSave');
        status.textContent = 'Saving…';
        saveBtn.disabled = true;
        activeEl.classList.add('is-saving');

        fetch(config.saveUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': config.csrfToken || getCookie('csrftoken'),
            },
            body: JSON.stringify({
                key: activeKey,
                language: config.language || 'en',
                body: collectBody(),
            }),
        })
            .then(function (response) {
                return response.json().then(function (data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function (result) {
                if (!result.ok || !result.data.ok) {
                    throw new Error((result.data && result.data.error) || 'Save failed');
                }
                var body = collectBody();
                if (activeFormat === 'plain') {
                    activeEl.textContent = body;
                } else {
                    activeEl.innerHTML = body || '<span class="staff-editable-empty">Click to add text</span>';
                }
                activeEl.classList.remove('is-saving');
                activeEl.classList.add('is-saved');
                setTimeout(function () {
                    activeEl.classList.remove('is-saved');
                }, 900);
                status.textContent = 'Saved!';
                setTimeout(function () {
                    if (modal) {
                        modal.hide();
                    }
                }, 400);
            })
            .catch(function (err) {
                status.textContent = err.message || 'Could not save. Try again.';
                activeEl.classList.remove('is-saving');
            })
            .finally(function () {
                saveBtn.disabled = false;
            });
    }

    var saveBtn = document.getElementById('contentEditSave');
    if (saveBtn) {
        saveBtn.addEventListener('click', saveContent);
    }

    initFrameEditor(iframe);
})();
