# f5-ansible
Ansible playbooks using BIG-IP ansible modules & AS3 declarations

HTTPs Application Onboard
---------
- Create/upload a CSV file for the new onboard HTTPs application under ../files directory. The CSV file naming convention  should be <application_name>_<action_type>.csv, Createfor instance Customer7_App_onboard.csv, where "Customer7_App" is the application name, and "onboard" is the action type. Refer to the sample ../files/Customer7_App_onboard.csv for content format of the CSV file.
- iApp: Playbook to upload the iApp to the BIG-IP and then deploy the iApp -"upload_and_deploy_iapp.yml"
- Onboarding a BIG-IP (NTP/DNS/Hostname/Provisioning/VLAN/SelfIP) - "onboarding-bigip.yml"
- Node maintenence: Disable a node member ,perform an upgrade on the node, enable the node member - "node_member_maintanence.yml"

Private Cloud
-------------
- Playbook to spin up BIG-IP in private cloud (vCenter) using govc (vShpere CLI) - "spin_up_BIGIP_vCenter_govc.yaml"
- Playbook to spin up BIG-IP in provate cloud (vCenter) using vsphere_guest ansible module - "spin_up_BIGIP_vCenter_guest_module.yaml"

Public Cloud
------------
- Playbook to spin up BIG-IP CFT in AWS - "spin_up_BIGIP_CFT_AWS.yaml"
