// add supoprt for add/remove EventListener, preventDefault and stopPropagation in IE8
(function(){Event.prototype.preventDefault||(Event.prototype.preventDefault=function(){this.returnValue=!1});Event.prototype.stopPropagation||(Event.prototype.stopPropagation=function(){this.cancelBubble=!0});if(!Element.prototype.addEventListener){var a=[],e=function(h,b){for(var f=this,d=function(a){a.target=a.srcElement;a.currentTarget=f;b.handleEvent?b.handleEvent(a):b.call(f,a)},c=0;c<a.length;c++){var g=a[c];if(g.object==this&&g.type==h&&g.listener==b)return}"DOMContentLoaded"==h?(c=function(a){"complete"==
document.readyState&&d(a)},document.attachEvent("onreadystatechange",c),a.push({object:this,type:h,listener:b,wrapper:c}),"complete"==document.readyState&&(g=new Event,g.srcElement=window,c(g))):(this.attachEvent("on"+h,d),a.push({object:this,type:h,listener:b,wrapper:d}))},b=function(b,e){for(var f=-1,d=0;d<a.length;d++){var c=a[d];if(c.object==this&&c.type==b&&c.listener==e){"DOMContentLoaded"==b?this.detachEvent("onreadystatechange",c.wrapper):this.detachEvent("on"+b,c.wrapper);f=d;break}}-1!=
f&&removeElem(a,f)};Element.prototype.addEventListener=e;Element.prototype.removeEventListener=b;HTMLDocument&&(HTMLDocument.prototype.addEventListener=e,HTMLDocument.prototype.removeEventListener=b);Window&&(Window.prototype.addEventListener=e,Window.prototype.removeEventListener=b)}})();function removeElem(a,e){if(null!=a&&void 0!=a){for(var b=e;b<a.length-1;b++)a[b]=a[b+1];a.pop()}};