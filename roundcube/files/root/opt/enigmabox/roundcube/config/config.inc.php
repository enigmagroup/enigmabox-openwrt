<?php

/* Local configuration for Roundcube Webmail */

$config['db_dsnw'] = 'sqlite:////box/roundcube.sqlite?mode=0646';

$config['default_host'] = 'box';

$config['smtp_server'] = 'box';

$config['support_url'] = 'http://enigmabox.net/kontakt/';

$config['log_dir'] = 'logs/';

$config['temp_dir'] = 'temp/';

$config['des_key'] = 'AkTFeF3AT5etSZ6YB6+3h0jv';

$config['username_domain'] = 'box';

$config['password_charset'] = 'UTF-8';

$config['product_name'] = 'Enigmabox Webmail';

$config['identities_level'] = 3;

$config['plugins'] = array('enigmabox_additions');

$config['message_sort_col'] = 'arrival';

$config['list_cols'] = array('flag', 'attachment', 'fromto', 'subject', 'date', 'size');

$config['language'] = 'de_CH';

$config['enable_spellcheck'] = false;

$config['skin'] = 'high_security';

$config['timezone'] = 'UTC';

$config['draft_autosave'] = 180;

$config['preview_pane'] = true;

$config['inline_images'] = false;

$config['mime_param_folding'] = 0;

$config['message_cache_lifetime'] = '10d';

