from ncclient import manager
import xmltodict

m = manager.connect(
    host="192.168.xx.xx",
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )
def netconf_edit_config(netconf_config):
    return  m.edit_config(target="running", config=netconf_config)

def create(student_id):
    loopback_ip_suffix = student_id[-3:]  # 3 หลักสุดท้ายของ studentID
    loopback_ip = f"172.30.{loopback_ip_suffix}.1"
    interface_name = f"Loopback{student_id}"

    netconf_config = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <Loopback>
                    <name>{student_id}</name>
                    <description>My NETCONF loopback</description>
                    <ip>
                        <address>
                            <primary>
                                <address>{loopback_ip}</address>
                                <mask>255.255.255.0</mask>
                            </primary>
                        </address>
                    </ip>
                </Loopback>
            </interface>
        </native>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {interface_name} is created successfully"
    except Exception as e:
        print(f"Error creating interface: {e}")
    return f"Cannot create: Interface loopback {interface_name}"


def delete(student_id):
    interface_name = f"Loopback{student_id}"
    netconf_config = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <Loopback operation="delete">
                    <name>{student_id}</name>
                </Loopback>
            </interface>
        </native>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface loopback {interface_name} is deleted successfully"
    except:
        print("Error!")


def enable(student_id):
    interface_name = f"Loopback{student_id}"
    netconf_config = f"""<config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <Loopback>
                    <name>{student_id}</name>
                    <description>Enabled via NETCONF</description>
                    <shutdown operation="delete"/> 
                </Loopback>
            </interface>
        </native>
    </config>"""

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface {interface_name} is enabled successfully"
    except:
        print("Error!")


def disable(student_id):
    interface_name = f"Loopback{student_id}"
    netconf_config = f"""
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <Loopback>
                    <name>{student_id}</name>
                    <description>Disabled via NETCONF</description>
                    <shutdown/>
                </Loopback>
            </interface>
        </native>
    </config>"""

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return f"Interface {interface_name} is shutdowned successfully"
    except:
        print("Error!")

def status(student_id):
    interface_name = f"Loopback{student_id}"
    netconf_filter = f"""
    <filter>
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{interface_name}</name>
            </interface>
        </interfaces-state>
    </filter>"""

    try:
        # Use Netconf operational operation to get interfaces-state information
        netconf_reply = m.get(filter=netconf_filter)
        print(netconf_reply)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
        interface_data = netconf_reply_dict.get("rpc-reply", {}).get("data", {})

        # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
        if interface_data:
            # extract admin_status and oper_status from netconf_reply_dict
            interface_data = interface_data.get("interfaces-state", {}).get("interface", {})
            admin_status = interface_data.get("admin-status")
            oper_status = interface_data.get("oper-status")
            name_interface = interface_data.get("name").get("#text")
            if admin_status == 'up' and oper_status == 'up':
                return f"Interface {interface_name} is enabled"
            elif admin_status == 'down' and oper_status == 'down':
                return f"Interface {interface_name} is disabled"
        else: # no operation-state data
            return f"No Interface {interface_name}"
    except:
       print("Error!")
