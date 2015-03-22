/**
 * Created by igor on 02.12.14.
 */

var PopupManager = {};

PopupManager.FadeInSpeed = 500;

PopupManager.Init = function(){
    $(".popup_content").each(function(){
        PopupManager.alignCenter($(this));
    });
    PopupManager.hide_popups(true);
};

PopupManager.show_popup = function (popup_number_class){
    $("."+popup_number_class+", .popup_background").fadeIn(this.FadeInSpeed);
};

PopupManager.hide_popups = function (force){
    force = force || false;
    if (force)
        $(".popup_content, .popup_background").hide();
    else
        $(".popup_content, .popup_background").fadeOut(this.FadeInSpeed);
};

PopupManager.alignCenter = function(elem) {
	elem.css({
	    left: ($(window).width() - elem.width()) / 2 + 'px', // получаем координату центра по ширине
        top: ($(window).height() - elem.height()) / 2 + 'px' // получаем координату центра по высоте
    });
};



