(function () {
    'use strict';

    function initRichText(container) {
        if (container.dataset.staffRichTextInit === '1') {
            return;
        }
        var textarea = container.querySelector('textarea');
        var quillEl = container.querySelector('.staff-rich-quill');
        if (!textarea || !quillEl || typeof Quill === 'undefined') {
            return;
        }

        container.dataset.staffRichTextInit = '1';

        var quill = new Quill(quillEl, {
            theme: 'snow',
            modules: {
                toolbar: [
                    ['bold', 'italic'],
                    [{ list: 'ordered' }, { list: 'bullet' }],
                    ['clean'],
                ],
            },
            placeholder: 'Type your text here…',
        });

        if (textarea.value) {
            quill.clipboard.dangerouslyPasteHTML(textarea.value);
        }

        quill.on('text-change', function () {
            textarea.value = quill.root.innerHTML;
        });

        var form = container.closest('form');
        if (form) {
            form.addEventListener('submit', function () {
                textarea.value = quill.root.innerHTML;
            });
        }
    }

    function initAll() {
        document.querySelectorAll('[data-staff-rich-text]').forEach(initRichText);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAll);
    } else {
        initAll();
    }
})();
