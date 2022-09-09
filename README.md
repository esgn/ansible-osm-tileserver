# OSM Tileserver Ansible playbook

Sample playbook to install and deploy an OSM tile server on a single Debian 11 instance.

The current version uses the following software :
* [oms2pgsql](https://osm2pgsql.org/) and [osm2pgsql-replication](https://osm2pgsql.org/doc/manual.html#keeping-the-database-up-to-date-with-osm2pgsql-replication)
* [mod_tile](https://github.com/openstreetmap/mod_tile)

Other versions using [imposm](https://imposm.org/), [pyosmium](https://osmcode.org/pyosmium/) or [tirex](https://wiki.openstreetmap.org/wiki/Tirex) are possible but yet to be implemented. [osmosis](https://github.com/openstreetmap/osmosis) only solution appears to be superseded by `osm2psql-replication`.


## Using venv to run this playbook

The use of venv is recommended to run the playbook.  

Install `python3-venv` if not already installed:

```
sudo apt install python3-venv
```

Execute the following commands to create a virtualenv and install the necessary libs in it :

```
mkdir venv
cd venv
python3 -m venv ansiblevenv
cd ..
source venv/ansiblevenv/bin/activate
(ansiblevenv) python3 -m pip install ansible
(ansiblevenv) ansible-galaxy collection install -r requirements.yml
```

## Running this playbook

`host_vars/` contains two sample yml files for two types of system configuration (8 CPU/32 GB RAM and 64 CPU/128 GB RAM).  

Copy one of the `.yml.sample` to `tileserver.yml` and edit values to fit your system:
* Define the connection parameters (IP, username, SSH key, ...) to reach your instance
* Define `service_domain`, the domain name for the instance (e.g. _tiles.domain.com_)  and `layer_name`, the name of the default layer (e.g _osmcarto_)
* Pay specific attention to the PostgreSQL tuning options that must be adjusted to your system sizing (visit https://pgtune.leopard.in.ua/ and https://osm2pgsql.org/doc/manual.html#tuning-the-postgresql-server to determine correct values). Correct values must be defined for import phase and tiles production phase.
* Adjust `renderd_num_threads`, `import_num_threads`, `osm2pgsql_replication_num_threads`, `prerender_num_threads` and `render_old_num_threads` to your system. These variables defined the number of threads that will be used or made available by each process.

_Note: Some packages are already installed from backports. Check https://blends.debian.org/gis/thermometer/ and edit the playbook to install newest versions if you wish_

Run playbook with the following command:

```
(ansiblevenv) ansible-playbook -i hosts deploy-osm-tileserver.yml
```

If the playbook succesfully executed, you'll be able to access the demo page for your instance at `https://[service_domain]`. Map tiles are requested from `https://[service_domain]/[layer_domain]/{z}/{x}/{y}.png`

By default, the server only accepts requests with referer equals to `service_domain`. Feel free to adjust the deployed apache configuration to modify this behaviour. 

## Resources 

* Switch2OSM tutorials: https://switch2osm.org/serving-tiles/ and https://github.com/SomeoneElseOSM/mod_tile/tree/switch2osm
* OSM chef cookbooks: https://github.com/openstreetmap/chef
* OSM-FR ansible playboooks: https://github.com/osm-fr/ansible-scripts

## TODO

- [ ] Improve PostgreSQL tuning (hugepages, tuning options, automatic tuning based on server facts, ...)
- [ ] Implement alternative solutions (tirex, etc)
- [ ] Improve log management
