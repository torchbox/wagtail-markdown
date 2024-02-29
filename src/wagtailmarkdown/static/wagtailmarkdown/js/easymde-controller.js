// wagtailmarkdown/static/wagtailmarkdown/js/easymde-controller.js

class EasyMDEContainer extends window.StimulusModule.Controller {
    static values = { autodownload: String };

    connect() {
        let autodownload = this.autodownloadValue || null;

        if (autodownload) {
            easymdeAttach(this.element.id, autodownload);
        } else {
            easymdeAttach(this.element.id);
        }
    }
}

window.wagtail.app.register('easymde', EasyMDEContainer);
