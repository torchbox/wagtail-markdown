class EasyMDEContainer extends window.StimulusModule.Controller {
    static values = { autodownload: Boolean};

    connect() {
        if (this.hasAutodownloadValue) {
            easymdeAttach(this.element.id, this.autodownloadValue);
        }
        else {
            easymdeAttach(this.element.id);
        }
    }
}

window.wagtail.app.register('easymde', EasyMDEContainer);
