function initializeTinyMCE(selector) {
    tinymce.init({
        selector: selector,
        language_url: '../../static/tinymce/langs/es.js',
        language: 'es',
        plugins: 'quickbars table link lists help',
        toolbar: 'undo redo | blocks | fontfamily fontsize | forecolor backcolor | bold italic | alignleft aligncenter alignright alignjustify | indent outdent | bullist numlist',
        content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }',
        font_formats: 'Arial=arial,helvetica,sans-serif;Courier New=courier new,courier,monospace;AkrutiKndPadmini=Akpdmi-n',
        content_css: "../../static/css/deferia.css",
    });
}
