<?php
/**
 * Class and Function List:
 * Function list:
 * - init()
 * - address_sources()
 * - address_sources_global()
 * - get_address_book()
 * Classes list:
 * - enigmabox_additions extends rcube_plugin
 */
require_once (dirname(__FILE__) . '/enigmabook.php');

class enigmabox_additions extends rcube_plugin
{
	private $abook_id = 'enigmabook';
	private $abook_name = 'Enigmabox';
	private $abook_id_global = 'enigmabook_global';
	private $abook_name_global = 'Enigmabox (Global)';
	
	function init() 
	{

		//Enigmabook
		$this->add_hook('addressbooks_list', array(
			$this,
			'address_sources'
		));
		$this->add_hook('addressbooks_list', array(
			$this,
			'address_sources_global'
		));
		$this->add_hook('addressbook_get', array(
			$this,
			'get_address_book'
		));
		$config = rcmail::get_instance()->config;
		$sources = (array)$config->get('autocomplete_addressbooks', array(
			'sql'
		));
		
		if (!in_array($this->abook_id, $sources)) 
		{
			$sources[] = $this->abook_id;
			$config->set('autocomplete_addressbooks', $sources);
		}
		
		if (!in_array($this->abook_id_global, $sources)) 
		{
			$sources[] = $this->abook_id_global;
			$config->set('autocomplete_addressbooks', $sources);
		}

		//Enigmabox JS
		$this->include_script('eb.js');
	}
	public 
	function address_sources($p) 
	{
		$abook = new enigmabook($this->abook_name);
		$p['sources'][$this->abook_id] = array(
			'id' => $this->abook_id,
			'name' => $this->abook_name,
			'readonly' => $abook->readonly,
			'groups' => $abook->groups,
		);
		return $p;
	}
	public 
	function address_sources_global($p) 
	{
		$abook = new enigmabook_global($this->abook_name_global);
		$p['sources'][$this->abook_id_global] = array(
			'id' => $this->abook_id_global,
			'name' => $this->abook_name_global,
			'readonly' => $abook->readonly,
			'groups' => $abook->groups,
		);
		return $p;
	}
	public 
	function get_address_book($p) 
	{
		
		if ($p['id'] === $this->abook_id) 
		{
			$p['instance'] = new enigmabook($this->abook_name);
		}
		
		if ($p['id'] === $this->abook_id_global) 
		{
			$p['instance'] = new enigmabook_global($this->abook_name_global);
		}
		return $p;
	}
}
