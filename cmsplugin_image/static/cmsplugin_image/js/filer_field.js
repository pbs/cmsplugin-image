(function($) {

    function _init(){

            function id_to_windowname(text) {
                text = text.replace(/\./g, '__dot__');
                text = text.replace(/\-/g, '__dash__');
                return text;
            }

            function getLookupPopup(lookupLink){
                var name = lookupLink.id.replace(/^lookup_/, '');
                name = id_to_windowname(name);
                var href;
                if (lookupLink.href.search(/\?/) >= 0) {
                    href = lookupLink.href + '&pop=1';
                } else {
                    href = lookupLink.href + '?pop=1';
                }
                if (typeof current_site !== 'undefined' && current_site == parseInt(current_site)){
                    href += '&current_site=' + current_site
                }
                var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
                win.focus();
                return win;
            }

            function is_validURL(image_url)  {
                // taken from: jquery.validate.js
                // from: http://docs.jquery.com/Plugins/Validation/validate
                return /^(https?|ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(image_url);
            }

            function dismissPopupForField(fieldName, fileType){

                return function(win, chosenId, chosenThumbnailUrl, chosenDescriptionTxt) {
                    win.close();

                    return $.ajax({
                        url: fetch_file_url,
                        data: { id: chosenId, file_type: fileType },
                        success: function(data){
                            var field = $('#var_' + fieldName);
                            field.val(data.url || field.val());
                            $("td.error_" + fieldName).html(data.url? '': 'Please select a valid ' + fileType + ' type.')
                        },
                        error: function(){
                            alert('Error retrieving file information.');
                        }
                    });
                }
            }

            function openPopupForField(triggeringLink, fieldName, fileType) {
                var opened = getLookupPopup(triggeringLink);
                // In case the SmartSnippet has both image and merlin fields, the request to
                //  opener.dismissRelatedImageLookupPopup should go to the right function
                opened.opener.dismissRelatedImageLookupPopup = dismissPopupForField(fieldName, fileType);
                return false;
            }

           $("form#smartsnippetpointer_form").submit(function(){
               var is_valid = true;

               $("input.filer_field").each(function(val) {
                    var fieldName = $(this).attr('id').replace('var_', '');
                    var errorBox = $('td.error_'+ fieldName);
                    var fieldValue = $(this).val();
                    // clear errors set before this submission
                    errorBox.html('');

                    var isEmpty = fieldValue === '';
                    if ($(this).hasClass('optional') && isEmpty){
                        // skip validation
                        return ;
                    }
                    if (isEmpty || !is_validURL(fieldValue)){
                        errorBox.html('Please select a valid ' + $(this).attr('data-filetype') + ' type.');
                        is_valid = false;
                    }
               });
               return is_valid;
           });

        return {
            openPopup: openPopupForField
        };
    }

    SnippetFilerWigets = window.SnippetFilerWigets || _init();

}(jQuery || django.jQuery));
