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
      var editorId = this.el.attr('id'); // Dynamically get ID
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
        { name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
        { name: 'styles' },
      ];

      config.removeButtons = 'Underline,Subscript,Superscript';
      config.format_tags = 'p;h1;h2;h3;pre';
      config.removeDialogTabs = 'image:advanced;link:advanced';
      config.extraPlugins = 'divarea,ckanview,templates,font';
      config.height = '400px';
      config.customConfig = false;
      config.allowedContent = true;

      var csrf_field = $('meta[name=csrf_field_name]').attr('content');
      var csrf_token = $('meta[name='+ csrf_field +']').attr('content');
      config.fileTools_requestHeaders = {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrf_token
      };
      config.filebrowserUploadUrl = this.options.site_url + 'pages_upload';

      if (window.ckan.pages && window.ckan.pages.override_config) {
        $.extend(config, window.ckan.pages.override_config);
      }

      // Initialize CKEditor instance for each unique editor
      CKEDITOR.replace(editorId, config);
    },
  }
});
