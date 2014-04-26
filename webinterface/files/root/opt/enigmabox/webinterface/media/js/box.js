(function(){

    trans = window.translation;

    $('.confirmation').click(function(){
        return confirm(trans['are_you_sure']);
    });

    $unveil = $('.unveil');
    unveil_text = $unveil.data('text');
    $unveil.html('<a href="#">' + trans['show'] + '</a>');
    $unveil.on('click', function(){
        $unveil.html(unveil_text);
        return false;
    });

    $dynamic_output = $('.dynamic-output');

    if ($dynamic_output.length){

        $dynamic_output.height(parseInt($(window).height(), 10) - 400);

        if($('#loader-hint').data('value') == 'dry-run'){
            $('.loader').show();
            $('#button-dry-run, #button-run').attr('disabled', 'disabled');
            $('#lockscreen').show();
        }

        if($('#loader-hint').data('value') == 'run'){
            $('.loader').show();
            $('#button-dry-run, #button-run').attr('disabled', 'disabled');
            $('#lockscreen').show();

            setInterval(function(){
                ret = $.post('/api/v1/get_option', {
                    'key': 'config_changed'
                }, function(data){
                    if(data['value'] == 'False'){
                        $('.loader').hide();
                        $('#button-dry-run, #button-run, #button-apply').hide();
                        $('#success').fadeIn();
                        $('#lockscreen').hide();
                    }
                });
            }, 2000);
        }

        prev_data = '';
        setInterval(function(){
            $dynamic_output.load('/dynamic_output/', function(data){
                if(data != prev_data){
                    $dynamic_output.animate({ scrollTop: $('.dynamic-output')[0].scrollHeight}, 1000);
                    prev_data = data;
                    if(data.indexOf('Finished catalog run') > -1){
                        $('#button-dry-run, #button-run, #button-apply').removeAttr('disabled');
                        $('.loader').hide();
                        $('#lockscreen').hide();
                    }
                }
            });
        }, 1500);
    }

    var anchor = 'general-config';
    var window_href = window.location.href;
    if(window_href.indexOf('#') > -1){
        anchor = window.location.href.split('#')[1];
    }
    $('#webfilter-tabs a[href=#' + anchor + ']').tab('show');

    $('#webfilter-tabs a').click(function (e) {
        $(this).tab('show');
    })

    $('#countrysort').sortable({
        cancel: ".ui-state-disabled",
        placeholder: "ui-state-highlight",
        update: function(ev) {
            var countries = [];
            $('#countrysort button[name=country]').each(function(i, c){
                countries.push($(c).val());
            });
            $.post('/api/v1/set_countries', {
                'countries': countries.join(',')
            });
        }
    });

})();
