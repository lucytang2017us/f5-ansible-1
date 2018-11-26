# f5-ansible
Ansible playbooks using BIG-IP ansible modules & AS3 declarations

HTTPs Application Onboard
---------
- Create/upload a CSV input file under /files directory. The CSV file naming convention should be <application_name>_<action_type>.csv, for instance, /files/Customer7_App_onboard.csv, where "Customer7_App" is the application name, and "onboard" is the action type. This file contains all required parameters to configure the new application. Refer to the sample /files/Customer7_App_onboard.csv for content format of the CSV file.
- Edit the /files/https_app_onboard_vars.yml input file as needed. This is the top vars file including all input/output files pathes used by the playbooks.
- Run the Tower job template with /playbooks/bigip_as3_https_app_onboard.yml, and verify the results.
- The sample files used by this sample "onboard" playbook include: 
  Input:
   - /files/Customer7_App_onboard.csv
   - /files/https_app_onboard_vars.yml
   - /scripts/vars_file_gen.py (Don't modify unless new configuration objects to be declared in the Jinja template)
   - /templates/as3_https_app_onboard.j2 (Don't modify unless new configuration objects to be declared in the Jinja template)
   - /playbooks/bigip_as3_https_app_onboard.yml (Don't modify)
   
   Output:
   - /vars/ustomer7_App_onboard_vars.yml  (Output vars file, used with Jinja template to create Json body for AS3 request)
   - /files/backups/Customer7_App_onboard.json (Output Json body for AS3 request)

HTTPs Application Patch
-------------
- Create/upload a CSV input file under /files directory. The CSV file naming convention should be <application_name>_<action_type>.csv, for instance, /files/Customer8_App_patch.csv, where "Customer8_App" is the application name, and "patch" is the action type. This file contains all required parameters to configure the new application into the same BIGIP partition with Customer7_App. Refer to the sample /files/Customer8_App_patch.csv for content format of the CSV file.
- Edit the /files/https_app_onboard_vars.yml input file as needed. This is the top vars file including all input/output files pathes used by the playbooks.
- Run the Tower job template with /playbooks/bigip_as3_https_app_onboard.yml, and verify the results.
- The sample files used by this sample "onboard" playbook include: 
  Input:
   - /files/Customer7_App_onboard.csv
   - /files/https_app_onboard_vars.yml
   - /scripts/vars_file_gen.py (Don't modify unless new configuration objects to be declared in the Jinja template)
   - /templates/as3_https_app_onboard.j2 (Don't modify unless new configuration objects to be declared in the Jinja template)
   - /playbooks/bigip_as3_https_app_onboard.yml (Don't modify)
   
   Output:
   - /vars/ustomer7_App_onboard_vars.yml  (Output vars file, used with Jinja template to create Json body for AS3 request)
   - /files/backups/Customer7_App_onboard.json (Output Json body for AS3 request)

Public Cloud
------------
- Playbook to spin up BIG-IP CFT in AWS - "spin_up_BIGIP_CFT_AWS.yaml"
