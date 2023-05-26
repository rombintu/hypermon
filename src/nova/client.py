from dataclasses import dataclass
from novaclient.client import Client
import os


def get_nova_credentials_v2():
    creds = {}
    creds['version'] = '2'
    creds['username'] = os.environ['OS_USERNAME']
    creds['password'] = os.environ['OS_PASSWORD']
    
    creds['auth_url'] = os.environ['OS_AUTH_URL']
    creds['project_domain_name'] = os.getenv('OS_PROJECT_DOMAIN_NAME', 'Default')
    creds['user_domain_name'] = os.getenv('OS_USER_DOMAIN_NAME', 'Default')
    return creds

@dataclass
class Server:
    name: str
    hypervisor: str
    ips: list[str]
    status: str

@dataclass
class Hypervisor:
    hostname: str
    vms: list[Server]
    status: str
    state: str

class Nova:
    nova = None
    hypervisors = []
    servers = []

    def __init__(self):
        self.creds = get_nova_credentials_v2()
        self.admin_user = self.creds["username"]
        self.admin_pass = self.creds["password"]
    
    def connect(self, os_project_name=""):
        if os_project_name=="":
            return "OS_PROJECT_NAME is null"
        self.creds['project_name'] = os_project_name
        self.nova = Client(**self.creds)
        return None
    
    def auth(self, os_username, os_password, os_project_name):
        try:
            creds = self.creds
            creds['username'] = os_username
            creds['password'] = os_password
            creds['project_name'] = os_project_name
            nova = Client(**creds)
            nova.servers.list()
            return True
        except Exception:
            return False

    def clean(self):
        self.hypervisors = []
        self.servers = []

    def load(self):
        hpvs, err = self.hypervisor_list()
        if err:
            print("WARN: ", err)
        srvs, err = self.server_list()
        if err:
            print("WARN: ", err)
        
        for srv in srvs:
            srv_dict = srv.to_dict()
            srv_hyper = ""
            try:
                srv_hyper = srv_dict["OS-EXT-SRV-ATTR:hypervisor_hostname"]
            except KeyError:
                srv_hyper = srv_dict["OS-EXT-SRV-ATTR:host"]
            except Exception as err:
                print("WARN: ", err)

            self.servers.append(
                Server(
                    name=srv.name,
                    hypervisor=srv_hyper,
                    ips=srv.addresses,
                    status=srv.status
                )
            )

        for h in hpvs:
            self.hypervisors.append(
                Hypervisor(
                    hostname=h.hypervisor_hostname,
                    vms=self.filter_vm(h.hypervisor_hostname),
                    status=h.status,
                    state=h.state
                )
            )

    def filter_vm(self, hyper_hostname):
        tmp = []
        for srv in self.servers:
            if srv.hypervisor == hyper_hostname:
                tmp.append(srv.__dict__)
        return tmp

    def server_list(self):
        try:
            return self.nova.servers.list(), 0
        except Exception as err:
            return [], err
        
    def hypervisor_list(self):
        try:
            return self.nova.hypervisors.list(), 0
        except Exception as err:
            return [], err
        
