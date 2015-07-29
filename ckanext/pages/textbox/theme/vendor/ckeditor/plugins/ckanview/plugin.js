/**
 * @license Copyright (c) 2003-2014, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

( function() {
	CKEDITOR.plugins.add( 'ckanview', {
		requires: 'dialog,fakeobjects',
    lang: 'en-gb', // %REMOVE_LINE_CORE%
		icons: 'ckanview', // %REMOVE_LINE_CORE%
		hidpi: true, // %REMOVE_LINE_CORE%
		onLoad: function() {
			CKEDITOR.addCss( 'img.ckan-view-fake' +
				'{' +
					'background-image: url(http://placehold.it/80x80&text=CKAN+view);' +
					'background-position: center center;' +
					'background-repeat: no-repeat;' +
					'border: 2px solid #a9a9a9;' +
					'display: block;' +
					'width: 80px;' +
					'height: 80px;' +
				'}'
				);
		},
		init: function( editor ) {
			var pluginName = 'ckanview',
			  	lang = editor.lang.ckanview,
			  	allowed = 'iframe[align,longdesc,frameborder,height,name,scrolling,src,title,width,data-ckan-view-embed]';

			if ( editor.plugins.dialogadvtab )
				allowed += ';iframe' + editor.plugins.dialogadvtab.allowedContent( { id: 1, classes: 1, styles: 1 } );

			CKEDITOR.dialog.add( pluginName, this.path + 'dialogs/ckanview.js' );
			editor.addCommand( pluginName, new CKEDITOR.dialogCommand( pluginName, {
				allowedContent: allowed,
				requiredContent: 'iframe'
			} ) );

			editor.ui.addButton && editor.ui.addButton( 'ckanview', {
				label: lang.toolbar,
				command: pluginName,
				toolbar: 'insert,80'
			} );

			editor.on( 'doubleclick', function( evt ) {
				var element = evt.data.element;
				if ( element.is( 'img' ) && element.data( 'ckan-view-embed' ) == 'true' )
					evt.data.dialog = 'ckanview';
			} );

			if ( editor.addMenuItems ) {
				editor.addMenuItems( {
					ckanview: {
						label: lang.title,
						command: 'ckanview',
						group: 'image'
					}
				} );
			}

			// If the "contextmenu" plugin is loaded, register the listeners.
			if ( editor.contextMenu ) {
				editor.contextMenu.addListener( function( element, selection ) {
					if ( element && element.is( 'img' ) && element.data( 'ckan-view-embed' ) == 'true' )
						return { iframe: CKEDITOR.TRISTATE_OFF };
				} );
			}
		},
		afterInit: function( editor ) {
			var dataProcessor = editor.dataProcessor,
				dataFilter = dataProcessor && dataProcessor.dataFilter;

			if ( dataFilter ) {
				dataFilter.addRules( {
					elements: {
						iframe: function( element ) {
							var fake_element = editor.createFakeParserElement( element, 'ckan-view-fake', 'iframe', true );

              var width = element.attributes.width || "80";
              var height = element.attributes.height || "80";
              if (width.charAt(width.length-1) === '%') {
                width = '960';
              }
              if (height.charAt(height.length-1) === '%') {
                height = '400';
              }
				      fake_element.attributes['data-ckan-view-embed'] ='true';
				      fake_element.attributes['src'] = 'http://placehold.it/' + width + 'x' + height +'&text=CKAN+View';
							return fake_element;
						}
					}
				} );
			}
		}
	} );
} )();
