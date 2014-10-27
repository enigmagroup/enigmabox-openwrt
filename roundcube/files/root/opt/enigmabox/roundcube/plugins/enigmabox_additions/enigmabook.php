<?php
/**
 * Class and Function List:
 * Function list:
 * - __construct()
 * - get_name()
 * - count()
 * - list_records()
 * - get_result()
 * - get_record()
 * - set_search_set()
 * - get_search_set()
 * - reset()
 * - list_groups()
 * - search()
 * - create_group()
 * - delete_group()
 * - rename_group()
 * - add_to_group()
 * - remove_from_group()
 * Classes list:
 * - enigmabook extends rcube_addressbook
 */

class enigmabook extends rcube_addressbook
{
	public $primary_key = 'ID';
	public $readonly = true;
	public $groups = true;
	private $cid;
	private $filter;
	private $result;
	private $name;
	public 
	function __construct($name) 
	{
		$this->ready = true;
		$this->name = $name;

		//hosts file
		$etc_hosts = file_get_contents('/etc/hosts');
		$f = explode('# friends', $etc_hosts);
		$f = $f[1];
		$f = explode("\n\n", $f);
		$f = $f[0];
		$f = explode("\n", $f);
		$friends = array();
		foreach ($f as $friend) 
		{
			
			if ($friend != '') 
			{
				$friends[] = preg_replace('#fc.*? {4}#', '', $friend);
			}
		}

		//display names file
		$display_names = array();
		$display_names_file = file_get_contents('/etc/enigmabox/display_names');
		$display_names_array = explode("\n", $display_names_file);
		foreach ($display_names_array as $dname) 
		{
			$dn = explode('|', $dname);
			$hostname = $dn[0];
			$display_name = $dn[1];
			$display_names[$hostname] = $display_name;
		}

		//build array
		$contacts = array();
		$id = 1;
		foreach ($friends as $friend) 
		{
			$contacts[$id] = array(
				'ID' => $id,
				'name' => $display_names[$friend],
				'firstname' => $display_names[$friend],
				'email' => "mail@$friend"
			);
			$id++;
		}
		$this->contacts = $contacts;
	}
	public 
	function get_name() 
	{
		return $this->name;
	}
	public 
	function count($searchpattern = false) 
	{
		$this->result = new rcube_result_set(1, 0);
		
		if ($this->cid) 
		{
			$this->result->add($this->contacts[$this->cid]);
		}
		else
		{
			foreach ($this->contacts as $contact) 
			{
				
				if ($searchpattern) 
				{
					
					if (stristr($contact['email'], $searchpattern)) 
					{
						$this->result->add($contact);
					}
				}
				else
				{
					$this->result->add($contact);
				}
			}
		}
		return $this->result;
	}
	public 
	function list_records($cols = null, $subset = 0) 
	{
		$this->result = $this->count();
		return $this->result;
	}
	public 
	function get_result() 
	{
		return $this->result;
	}
	public 
	function get_record($id, $assoc = false) 
	{
		$this->cid = $id; #WICHTIG#

		$this->list_records();
		return $this->result->records;
	}
	public 
	function set_search_set($filter) 
	{
	}
	public 
	function get_search_set() 
	{
	}
	public 
	function reset() 
	{
	}
	
	function list_groups($search = null) 
	{
	}
	public 
	function search($fields, $value, $strict = false, $select = true, $nocount = false, $required = array()) 
	{
		$this->result = $this->count($searchpattern = $value);
		return $this->result;
	}
	
	function create_group($name) 
	{
	}
	
	function delete_group($gid) 
	{
	}
	
	function rename_group($gid, $newname) 
	{
	}
	
	function add_to_group($group_id, $ids) 
	{
	}
	
	function remove_from_group($group_id, $ids) 
	{
	}
}
