/*
 * vim:sw=4 ts=4 et:
 * Copyright (c) 2015-present Torchbox Ltd.
 * hello@torchbox.com
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely. This software is provided 'as-is', without any express or implied
 * warranty.
 */

/*
 * Define window.wagtailMarkdown.options in your custom code to set EasyMDE options.
 */
window.wagtailMarkdown = window.wagtailMarkdown || {};
window.wagtailMarkdown.options = window.wagtailMarkdown.options || {};

/*
 * Used to initialize Simple MDE when Markdown blocks are used in StreamFields
 */
function easymdeAttach(id, autoDownloadFontAwesome) {
    Object.assign(window.wagtailMarkdown.options, {
        element: document.getElementById(id),
        autofocus: false,
        autoDownloadFontAwesome: autoDownloadFontAwesome,
    })
    var mde = new EasyMDE(window.wagtailMarkdown.options);
    mde.render();

    // Save the codemirror instance on the original HTML element for later use.
    mde.element.codemirror = mde.codemirror;

    mde.codemirror.on("change", function() {
        document.getElementById(id).value = mde.value();
    });
}


/*
* Used to initialize content when MarkdownFields are used in admin panels.
*/
function refreshCodeMirror(e) {
    setTimeout(
        function() {
            e.CodeMirror.refresh();
        }, 100
    );
}

// Wagtail < 3.0
document.addEventListener('shown.bs.tab', function() {
    document.querySelectorAll('.CodeMirror').forEach(function(e) {
        refreshCodeMirror(e)
    });
});

// Wagtail >= 3.0
document.addEventListener('wagtail:tab-changed', function() {
    document.querySelectorAll('.CodeMirror').forEach(function(e) {
        refreshCodeMirror(e)
    });
});
