// wagtailmarkdown/static/wagtailmarkdown/js/easymde-controller.js

class EasyMDEContainer extends window.StimulusModule.Controller {
    static values = { autodownload: Boolean };

    connect() {
        if (this.autodownloadValue != null) {
            easymdeAttach(this.element.id, this.autodownloadValue);
        } else {
            easymdeAttach(this.element.id);
        }
    }
}

window.wagtail.app.register('easymde', EasyMDEContainer);
