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

function showRelatedObjectLookupPopup(triggeringLink) {
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
    var jxhr = $.ajax({
                url: "/imagefield/get_file/",
                data: {'id': chosenId},
                beforeSend: function(xhr){
                    //add before send logic here if required
                },
                success: function(data){
		    if (data){
                        document.getElementById('var_'+field_name).value = data;
		    }
		    else{
			$(".error_"+field_name).html('Please select a valid image type');
		    }
                },
                error: function(data){
                    alert('error');
                },
                complete: function(data){

                }
            });
        return jxhr;
};