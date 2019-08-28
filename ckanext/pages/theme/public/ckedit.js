this.ckan.module('ckedit', function (jQuery, _) {
  return {
    options: {
      site_url: ""
    },

    initialize: function () {
      jQuery.proxyAll(this, /_on/);
      this.el.ready(this._onReady);
    },

    _onReady: function() {
      var config = {};
      config.toolbarGroups = [
        { name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
        { name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
        { name: 'links' },
        { name: 'insert' },
        { name: 'forms' },
        { name: 'tools' },
        { name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
        { name: 'others' },
        '/',
        { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
        { name: 'paragraph',   groups: [ 'list', 'blocks', 'align', 'bidi' ] },
        { name: 'styles' },
      ];

      // Remove some buttons, provided by the standard plugins, which we don't
      // need to have in the Standard(s) toolbar.
      config.removeButtons = 'Underline,Subscript,Superscript';

      // Se the most common block elements.
      config.format_tags = 'p;h1;h2;h3;pre';

      // Make dialogs simpler.
      config.removeDialogTabs = 'image:advanced;link:advanced';
      config.filebrowserUploadUrl = this.options.site_url + 'pages_upload';
      config.extraPlugins = 'divarea,ckanview';
      config.height = '400px';
      config.customConfig = false;

      var editor = $(this.el).ckeditor(config);
    },
  }
});
