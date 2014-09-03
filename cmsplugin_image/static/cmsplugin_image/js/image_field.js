// Holds the current image field name
var image_field_name = '';

function is_validURL(image_url)  {
    // taken from: jquery.validate.js
    // from: http://docs.jquery.com/Plugins/Validation/validate
    return /^(https?|ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(image_url);
}

function id_to_windowname(text) {
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    return text;
}

function windowname_to_id(text) {
    text = text.replace(/__dot__/g, '.');
    text = text.replace(/__dash__/g, '-');
    return text;
}

function showRelatedObjectLookupPopupImgField(triggeringLink, field_name) {
    image_field_name = field_name;
    var name = triggeringLink.id.replace(/^lookup_/, '');
    name = id_to_windowname(name);
    var href;
    if (triggeringLink.href.search(/\?/) >= 0) {
    	href = triggeringLink.href + '&pop=1';
    } else {
	    href = triggeringLink.href + '?pop=1';
    }
    if (typeof current_site !== 'undefined' && current_site == parseInt(current_site)){
        href += '&current_site=' + current_site
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();

    // In case the SmartSnippet has both image and merlin fields, the request to
    //  opener.dismissRelatedImageLookupPopup should go to the right function
    window.dismissRelatedImageLookupPopup = dismissRelatedImageLookupPopupImgField

    return false;
}

dismissRelatedImageLookupPopupImgField = function(win, chosenId, chosenThumbnailUrl, chosenDescriptionTxt) {
    win.close();
    var jxhr = jQuery.ajax({
                url: filer_image_url,
                data: {'id': chosenId},
                success: function(data){
                    if (data.url){
			jQuery("td.invalid_image").html('');
                        jQuery('#var_'+image_field_name).val(data.url);
                    }
                    else{
                        jQuery("td.error_"+image_field_name).html('Please select a valid image type.');
                    }
                },
                error: function(data){
                    alert('Error retrieving file information.');
                }
            });
        return jxhr;
};


jQuery(document).ready(function(){
   jQuery("form#smartsnippetpointer_form").submit(function(){
       var is_valid = true;
       jQuery("td.invalid_image").html('');
       jQuery("input.filer_image_url").each(function(val) {

            image_field_name = jQuery(this).attr('id').replace('var_', '');
            var fieldValue = jQuery(this).val();

            var optionalField = false;
            if (jQuery(this).hasClass('optional')){
                optionalField = true;
                if (fieldValue === ''){ return; }
            }

            if ((optionalField && !is_validURL(fieldValue)) || fieldValue==='' || !is_validURL(fieldValue)){
                is_valid = false;
                jQuery('td.error_'+image_field_name).html('Please select a valid image type.');
            }
       });
       return is_valid;
   }) ;
});
