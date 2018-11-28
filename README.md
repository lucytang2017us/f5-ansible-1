# f5-ansible
Onboarding new HTTPs and GSLB applications with Ansible playbooks, using BIG-IP AS3 declarations.

Environment
---------
- Download and install AS3 rpm onto target BIGIP devices (>= v12.1.x), https://github.com/F5Networks/f5-appsvcs-extension.
- Create sub directories in github repository: /files, /files/backups, /templates, /scripts, /vars, and /playbooks. Upload the sample files in the following examples to their corresponding sub directories.
- Create Ansible Tower project to reference the source of the github repository. Create "bigip" and "localhost" Inventory groups. Add BIGIP devices as hosts into the "bigip" group, and add the Tower server management IP into the "localhost" group.
Define access credentials for the "bigip" group in the "Details" tab, for instance:
  
  bigip_username: "admin"
  
  bigip_password: "admin"
  
  bigip_port: "443"
  
  validate_certs: "no"

- Create Ansible Tower job templates for the following scenarios, referencing their corresponding playbooks. Run the job templates and verify the results.

Note: 
- With clustered devices, including one device in the "bigip" group as target device of the playbook, the configurations could be auto/manual synced to the other devices. 
- DO NOT make manual modifications to the applications and components created by AS3 declarations. Further modification should via AS3 "patch" procedure.

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
   - /vars/Customer7_App_onboard_vars.yml  (Output vars file, used with Jinja template to create Json body for AS3 request)
   - /files/backups/Customer7_App_onboard.json (Output, used as Json body for AS3 request)

HTTPs Application Patch
-------------
- Create/upload a CSV input file under /files directory. The CSV file naming convention should be <application_name>_<action_type>.csv, for instance, /files/Customer8_App_patch.csv, where "Customer8_App" is the application name, and "patch" is the action type. This file contains all required parameters to configure the new application within the same BIGIP partition Customer7_App sit. Refer to the sample /files/Customer8_App_patch.csv for content format of the CSV file.
- Edit the /files/https_app_onboard_vars.yml input file as needed. This is the top vars file including all input/output files pathes used by the playbooks.
- Run the Tower job template with /playbooks/bigip_as3_https_app_patch.yml, and verify the results.
- The sample files used by this sample "patch" playbook include: 
  Input:
   - /files/Customer8_App_patch.csv
   - /files/https_app_onboard_vars.yml
   - /scripts/vars_file_gen.py (Don't modify unless new configuration objects to be declared in the Jinja template)
   - /templates/as3_https_app_patch.j2 (Don't modify unless new configuration objects to be declared in the Jinja template)
   - /playbooks/bigip_as3_https_app_patch.yml (Don't modify)
   
   Output:
   - /vars/Customer8_App_patch_vars.yml  (Output vars file, used with Jinja template to create Json body for AS3 request)
   - /files/backups/Customer8_App_patch.json (Output, used as Json body for AS3 request)
   
   Notes: This patch playbook can also be used to modify existing application originally created by AS3. 

GSLB App Onboard
------------
- Create/upload a CSV input file under /files directory. The CSV file naming convention should be <application_name>_<action_type>.csv, for instance, /files/Customer7_App_GSLB_onboard.csv, where "Customer7_App_GSLB" is the application name, and "onboard" is the action type. This file contains all required parameters to configure the new GSLB application components. Refer to the sample /files/Customer7_App_GSLB_onboard.csv for content format of the CSV file.
- Edit the /files/gslb_app_onboard_vars.yml input file as needed. This is the top vars file including all input/output files pathes used by the playbooks.
- Run the Tower job template with /playbooks/bigip_as3_app_gslb_onboard.yml, and verify the results.
- The sample files used by this sample "patch" playbook include: 
  Input:
   - /files/Customer7_App_GSLB_onboard.csv
   - /files/gslb_app_onboard_vars.yml
   - /scripts/vars_file_gen_gslb.py (Don't modify unless new configuration objects to be declared in the Jinja template)
   - /templates/as3_gslb_app_onboard.j2 (Don't modify unless new configuration objects to be declared in the Jinja template)
   - /playbooks/bigip_as3_app_gslb_onboard.yml (Don't modify)
   
   Output:
   - /vars/Customer7_App_GSLB_onboard_vars.yml  (Output vars file, used with Jinja template to create Json body for AS3 request)
   - /files/backups/Customer7_App_GSLB_onboard.json (Output, used as Json body for AS3 request)
   
 Utils
------------
- To remove an entire tenant including applications, use the bigip_as3_clean_tenant.yml util playbook. Edit the "tenant_name" value inside the playbook file.
- To remove an exiting application from its tenant, use the bigip_as3_clean_app.yml and the as3_clean_app.json. Edit the "path" inside the json before running the playbook.

   
