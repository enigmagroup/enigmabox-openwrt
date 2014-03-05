$(document).ready(function() {

    var o = o || {};



    /* telegram char counter */

    o.char_counter = function(){

        var $telegram = $('#telegram');
        var $transmit = $('#transmit');
        var $charcounter = $('.charcounter');
        $telegram.on('keyup', function(){
            var available_chars = 256;
            var str_len = $telegram.val().length;
            var remaining_chars = (available_chars - str_len);
            $charcounter.text(remaining_chars);

            if(remaining_chars < 0){
                $charcounter.addClass('warning');
                $transmit.attr('disabled', 'disabled');
            }else{
                $charcounter.removeClass('warning');
                $transmit.attr('disabled', false);
            }
        });

    }



    /* xhr stuff */

    o.run_xhr = true;
    o.xhr_step = 10;

    o.xhr_load = function(){
        var $xhr = $('.xhr');
        var xhr_url = $xhr.data('xhr-url');

        if(xhr_url){

            if(xhr_url.indexOf('?') > -1){
                xhr_url += '&step=' + o.xhr_step;
            }else{
                xhr_url += '?step=' + o.xhr_step;
            }

            if(o.run_xhr){
                o.run_xhr = false;
                $.get(xhr_url, function(data){
                    if(data.length > 1){
                        $xhr.append(data);
                        o.xhr_step = o.xhr_step + 10;
                        o.run_xhr = true;
                    }else{
                        o.run_xhr = false;
                    }
                });
            }

        }
    }

    o.scroll_action = function(){
        var d_height = $(document).height();
        var w_height = $(window).height();
        var scroll_to = $(window).scrollTop();
        var bottom_distance = (d_height - w_height - scroll_to);

        if(bottom_distance < 100){
            o.xhr_load();
        }
    }

    o.xhr = function(){
        setInterval(function(){
            o.scroll_action();
        }, 100);
    }


    o.run_timeline_xhr = true;

    o.timeline_xhr = function(){
        var $timeline = $('.timeline');
        var xhr_url = $timeline.data('xhr-url');

        //$timeline.animate({background: "#ff0"}, 500);
        //$('li', $timeline).slideUp();

        o.timeline_newest = $('li:first .created_at', $timeline).data('created_at');

        if(xhr_url){

            if(xhr_url.indexOf('?') > -1){
                xhr_url += '&since=' + o.timeline_newest;
            }else{
                xhr_url += '?since=' + o.timeline_newest;
            }

            if(window.location.href.indexOf('/fc') > -1){
                // don't run on profile pages
                o.run_timeline_xhr = false;
            }

            if(o.run_timeline_xhr){
                o.run_timeline_xhr = false;
                $.get(xhr_url, function(data){
                    if(data.length > 1){
                        $timeline.prepend(data);
                    }
                    o.run_timeline_xhr = true;
                });
            }

        }
    }

    o.timeline_poller = function(){
        setInterval(function(){
            o.timeline_xhr();
        }, 2000);
    }



    /* subscribe button */

    o.bind_subscribe_buttons = function(){
        var $subscribe_button = $('.subscribe')

        $subscribe_button.each(function(i, button){
            var $button = $(button);
            var ipv6 = $button.val();

            if($button.attr('name') == 'subscribe'){

                var original_text = $button.text();
                $button.text('Checking...').attr('disabled', 'disabled');

                $.get('/xhr/check_status', {
                    'ipv6': ipv6
                }, function(data){
                    if(data.result == 'pong'){
                        $button.text(original_text).attr('disabled', false);
                    }else{
                        $button.text('Disabled');
                        var $dropdown = $button.parents('.buttonblock').find('.dropdown-toggle');
                        $dropdown.attr('disabled', 'disabled');
                    }
                });

            }
        });

        // bind events
        $subscribe_button.on('click', function(ev){
            var $btn = $(ev.target);
            var ipv6 = $btn.val();
            var what = $btn.attr('name');

            var original_text = $btn.text();
            $btn.text('Working...').attr('disabled', 'disabled');

            $.post('/xhr/subscribe', {
                'what': what,
                'ipv6': ipv6
            }, function(data){
                if(data.result == 'success'){
                    if(what == 'subscribe'){
                        $btn.removeClass('btn-default').addClass('btn-success');
                        $btn.attr('name', 'unsubscribe');
                        $btn.text('Subscribed');
                    }else{
                        $btn.removeClass('btn-success').addClass('btn-default');
                        $btn.attr('name', 'subscribe');
                        $btn.text('Subscribe');
                    }
                }else{
                    $btn.text(original_text);
                }
                $btn.attr('disabled', false);
            });
            return false;
        });
    }



    /* retransmit */

    o.bind_retransmit = function(){
        var $modal_window = $('#modal-window');
        var $modal_submit = $('#submit');
        var submit_text = 'Retransmit';

        $('.timeline, .telegram').on('click', '.retransmit',  function(ev){
            $modal_window.find('h3').text('Retransmit this to your subscribers?');
            $modal_submit.text(submit_text);
            $modal_submit.attr('data-action', 'retransmit');
            var telegram = $(ev.target).parents('li').html();
            $('.modal-body', $modal_window).html(telegram);
            $modal_window.modal()
        });

        $modal_submit.on('click', function(){
            if($modal_submit.data('action') == 'retransmit'){
                var ipv6 = $('.modal-body .ipv6').text();
                var created_at = $('.modal-body .created_at').data('created_at');

                $modal_submit.text('Working...').attr('disabled', 'disabled');
                $.post('/xhr/retransmit', {
                    'ipv6': ipv6,
                    'created_at': created_at,
                }, function(data){
                    if(data.result == 'success'){
                        $modal_window.modal('hide')
                    }else{
                        alert('failed.');
                        $modal_window.modal('hide')
                    }
                    $modal_submit.text(submit_text).attr('disabled', false);
                });
            }
        });
    }



    /* delete */

    o.bind_delete = function(){
        var $modal_window = $('#modal-window');
        var $modal_submit = $('#submit');
        var submit_text = 'Delete';

        $('.timeline, .telegram').on('click', '.delete',  function(ev){
            $modal_window.find('h3').text('Delete this telegram?');
            $modal_submit.text(submit_text);
            $modal_submit.attr('data-action', 'delete');
            var telegram = $(ev.target).parents('li').html();
            $('.modal-body', $modal_window).html(telegram);
            $modal_window.modal()
        });

        $modal_submit.on('click', function(){
            if($modal_submit.data('action') == 'delete'){
                var ipv6 = $('.modal-body .ipv6').text();
                var created_at = $('.modal-body .created_at').data('created_at');

                $modal_submit.text('Working...').attr('disabled', 'disabled');
                $.post('/xhr/delete', {
                    'ipv6': ipv6,
                    'created_at': created_at,
                }, function(data){
                    if(data.result == 'success'){
                        $modal_window.modal('hide')
                    }else{
                        alert('failed.');
                        $modal_window.modal('hide')
                    }
                    $modal_submit.text(original_text).attr('disabled', false);
                });
            }
        });
    }



    /* init */

    o.init = function(){
        o.char_counter();
        o.xhr();
        o.timeline_poller();
        o.bind_subscribe_buttons();
        o.bind_retransmit();
        o.bind_delete();
    }

    o.init();

});
