/**
 * @license Copyright (c) 2003-2014, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

( function() {
	// Map 'true' and 'false' values to match W3C's specifications
	// http://www.w3.org/TR/REC-html40/present/frames.html#h-16.5
	var checkboxValues = {
		scrolling: { 'true': 'yes', 'false': 'no' },
		frameborder: { 'true': '1', 'false': '0' }
	};

	function loadValue( iframeNode ) {
		var isCheckbox = this instanceof CKEDITOR.ui.dialog.checkbox;
		if ( iframeNode.hasAttribute( this.id ) ) {
			var value = iframeNode.getAttribute( this.id );
			if ( isCheckbox )
				this.setValue( checkboxValues[ this.id ][ 'true' ] == value.toLowerCase() );
			else
				this.setValue( value );
		}
	}

	function commitValue( iframeNode ) {
		var isRemove = this.getValue() === '',
			isCheckbox = this instanceof CKEDITOR.ui.dialog.checkbox,
			value = this.getValue();
		if ( isRemove )
			iframeNode.removeAttribute( this.att || this.id );
		else if ( isCheckbox )
			iframeNode.setAttribute( this.id, checkboxValues[ this.id ][ value ] );
		else
			iframeNode.setAttribute( this.att || this.id, value );
	}

	CKEDITOR.dialog.add( 'ckanview', function( editor ) {
		var iframeLang = editor.lang.ckanview,
			commonLang = editor.lang.common,
			dialogadvtab = editor.plugins.dialogadvtab;
		return {
			title: iframeLang.title,
			minWidth: 350,
			minHeight: 260,
			onShow: function() {
				// Clear previously saved elements.
				this.fakeImage = this.iframeNode = null;

				var fakeImage = this.getSelectedElement();
				if ( fakeImage && fakeImage.data( 'ckan-view-embed' ) && fakeImage.data( 'ckan-view-embed' ) == 'true' ) {
					this.fakeImage = fakeImage;

					var iframeNode = editor.restoreRealElement( fakeImage );
					this.iframeNode = iframeNode;

					this.setupContent( iframeNode );
				}
			},
			onOk: function() {
				var iframeNode;
				if ( !this.fakeImage )
					iframeNode = new CKEDITOR.dom.element( 'iframe' );
				else
					iframeNode = this.iframeNode;

				// A subset of the specified attributes/styles
				// should also be applied on the fake element to
				// have better visual effect. (#5240)
				var extraStyles = {},
					  extraAttributes = {'data-ckan-view-embed': 'true'};


				this.commitContent( iframeNode, extraStyles, extraAttributes );
        iframeNode.setAttributes({'data-ckan-view-embed': 'true'});


				// Refresh the fake image.
				var newFakeImage = editor.createFakeElement( iframeNode, 'ckan-view-fake', 'iframe', true );
				newFakeImage.setAttributes( extraAttributes );
				newFakeImage.setStyles( extraStyles );
        var width = iframeNode.getAttribute('width') || "80"
        var height = iframeNode.getAttribute('height') || "80"
        if (width.charAt(width.length-1) === '%') {
          width = '960';
        }
        if (height.charAt(height.length-1) === '%') {
          height = '400';
        }
				newFakeImage.setAttributes( {'src': 'http://placehold.it/' + width + 'x' + height +'&text=CKAN+View'} );

				if ( this.fakeImage ) {
					newFakeImage.replace( this.fakeImage );
					editor.getSelection().selectElement( newFakeImage );
				} else
					editor.insertElement( newFakeImage );
			},
			contents: [
				{
				id: 'info',
				label: commonLang.generalTab,
				accessKey: 'I',
				elements: [
					{
					type: 'vbox',
					padding: 0,
					children: [
						{
						id: 'src',
						type: 'text',
						label: commonLang.url,
						required: true,
						validate: CKEDITOR.dialog.validate.notEmpty( iframeLang.noUrl ),
						setup: loadValue,
						commit: commitValue
					  }
					]
				},
					{
					type: 'hbox',
					children: [
						{
						id: 'width',
						type: 'text',
						requiredContent: 'iframe[width]',
						style: 'width:100%',
						labelLayout: 'vertical',
						label: commonLang.width,
						validate: CKEDITOR.dialog.validate.htmlLength( commonLang.invalidHtmlLength.replace( '%1', commonLang.width ) ),
						setup: loadValue,
						commit: commitValue
					},
						{
						id: 'height',
						type: 'text',
						requiredContent: 'iframe[height]',
						style: 'width:100%',
						labelLayout: 'vertical',
						label: commonLang.height,
						validate: CKEDITOR.dialog.validate.htmlLength( commonLang.invalidHtmlLength.replace( '%1', commonLang.height ) ),
						setup: loadValue,
						commit: commitValue
					},
						{
						id: 'align',
						type: 'select',
						requiredContent: 'iframe[align]',
						'default': '',
						items: [
							[ commonLang.notSet, '' ],
							[ commonLang.alignLeft, 'left' ],
							[ commonLang.alignRight, 'right' ],
							[ commonLang.alignTop, 'top' ],
							[ commonLang.alignMiddle, 'middle' ],
							[ commonLang.alignBottom, 'bottom' ]
							],
						style: 'width:100%',
						labelLayout: 'vertical',
						label: commonLang.align,
						setup: function( iframeNode, fakeImage ) {
							loadValue.apply( this, arguments );
							if ( fakeImage ) {
								var fakeImageAlign = fakeImage.getAttribute( 'align' );
								this.setValue( fakeImageAlign && fakeImageAlign.toLowerCase() || '' );
							}
						},
						commit: function( iframeNode, extraStyles, extraAttributes ) {
							commitValue.apply( this, arguments );
							if ( this.getValue() )
								extraAttributes.align = this.getValue();
						}
					}
					]
				}
				]
			}
				]
		};
	} );
} )();
