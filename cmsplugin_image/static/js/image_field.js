// Holds the current image field name
var image_field_name = '';

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

function showRelatedObjectLookupPopup(triggeringLink, field_name) {
    image_field_name = field_name;
    var name = triggeringLink.id.replace(/^lookup_/, '');
    name = id_to_windowname(name);
    var href;
    if (triggeringLink.href.search(/\?/) >= 0) {
    	href = triggeringLink.href + '&pop=1';
    } else {
	    href = triggeringLink.href + '?pop=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

dismissRelatedImageLookupPopup = function(win, chosenId, chosenThumbnailUrl, chosenDescriptionTxt) {
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
            if (jQuery(this).val()==''){
               is_valid = false;
	       image_field_name = jQuery(this).attr('id').replace('var_', '');
               jQuery('td.error_'+image_field_name).html('Please select a valid image type.');
            }
       });
       return is_valid;
   }) ;
});