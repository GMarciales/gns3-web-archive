#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

from models import ServerSettings, Project, VCPS

SERVER_URL = None
SERVER_PORT = None
CURRENT_PROJECT = None


def createURL(parameter):
    url = 'http://' + str(SERVER_URL) + ':' + str(SERVER_PORT) + '/v1/' \
        + str(parameter)
    return url


def home(request):
    r = requests.get('http://localhost:8000/v1/version')
    json_response = r.json()
    return render(request, 'main/index.html',
                  {'version': json_response['version'],
                  'local': json_response['local']})


def get_server_version(request):
    r = requests.get('http://localhost:8000/v1/version')
    return JsonResponse(r.json())


@csrf_exempt
def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('projectName')
        data = {'name': name}
        res = requests.post('http://localhost:8000/v1/projects',
                            data=json.dumps(data))
        json_response = res.json()
        project_id = json_response['project_id']
        project = Project(name=name, project_id=project_id)
        project.save()
        CURRENT_PROJECT = project
        return JsonResponse({'status': 'success',
                            'project_id': project_id, 'name': name})
    else:
        return JsonResponse({})


@csrf_exempt
def create_vcps(request):
    """
        The method creates a VCPS device with the given name
        and stores the information on the database. A VCPS
        is linked to a project.
    """
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        vcps_name = request.POST.get("vcps_name")
        data = {"name":vcps_name}
        url = "http://localhost:8000/v1/projects/"+str(project_id)+"/vpcs/vms"
        print project_id
        res = requests.post(url,data=json.dumps(data))
        print res
        json_response = res.json()
        vm_id = json_response['vm_id']
        print vm_id

        # Now create the ports on the VM
        res = requests.post("http://localhost:8000/v1/projects/"+str(project_id)+"/ports/udp")
        json_response = res.json()
        vcps_port = json_response["udp_port"]

        project = Project.objects.all().filter(project_id=project_id)[0]
        vcps = VCPS(name=vcps_name,vm_id=vm_id,udp_port=vcps_port,project=project)
        vcps.save()
        return JsonResponse({"status":"success","vcps_name":vcps_name,"vm_id":vm_id,"port":vcps_port})

def get_port(request, project_id):
    res = requests.post('http://localhost:8000/v1/projects/'
                        + str(project_id) + '/ports/udp')
    json_response = res.json()
    return JsonResponse({'udp_port': json_response['udp_port']})


def start_vcps(
    request,
    project_id,
    vcps_id_1,
    vcps_id_2,
    lport,
    rport,
    ):
    url_1 = 'http://localhost:8000/v1/projects/' + str(project_id) \
        + '/vcps/vms/' + str(vcps_id_1) + '/adapters/0/ports/0/nio'
    data_1 = {
        'lport': lport,
        'rhost': '127.0.0.1',
        'rport': rport,
        'type': 'nio_udp',
        }
    r1 = requests.post(url_1, data=data_1)

    url_2 = 'http://localhost:8000/v1/projects/' + str(project_id) \
        + '/vcps/vms/' + str(vcps_id_2) + '/adapters/0/ports/0/nio'
    data_2 = {
        'lport': rport,
        'rhost': '127.0.0.1',
        'rport': lport,
        'type': 'nio_udp',
        }
    r2 = requests.post(url_2, data=data_2)

    url_1 = 'http://localhost:8000/v1/projects/' + str(project_id) \
        + '/vcps/vms/' + str(vcps_id_1) + '/start'
    url_2 = 'http://localhost:8000/v1/projects/' + str(project_id) \
        + '/vcps/vms/' + str(vcps_id_2) + '/start'
    requests.post(url_1)
    requests.post(url_2)

    return JsonResponse({'status': 'success'})


@csrf_exempt
def settings(request):
    if request.method == 'POST':
        server_url = request.POST.get('serverURL')
        server_port = request.POST.get('serverPort')
        print server_url
        print str(server_port)
        r = requests.get('http://' + str(server_url) + ':'
                         + str(server_port) + '/v1/version')
        print r.status_code
        if r.status_code == 200:

            # The given server URL and Port are working

            print 'Hello'
            server_settings = \
                ServerSettings.objects.create(url=server_url,
                    port=server_port)
            server_settings.save()
        else:

            # The given server credentials are not working, Raise Error

            return JsonResponse({'status': 'Failed'})
    return JsonResponse({'status': 'success'})

@csrf_exempt
def link_nodes(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        vm_id_first = request.POST.get("vm_id_first")
        vm_id_second = request.POST.get("vm_id_second")
        print project_id
        print vm_id_first
        print vm_id_second
        project = Project.objects.all().filter(project_id=project_id)[0]
        vm_obj_1 = VCPS.objects.all().filter(vm_id=vm_id_first)[0]
        vm_obj_2 = VCPS.objects.all().filter(vm_id=vm_id_second)[0]

        #Create the bi-directional links
        data = {"lport":int(vm_obj_1.udp_port),"rhost":"127.0.0.1","rport":int(vm_obj_2.udp_port), "type":"nio_udp"}
        print data
        res_1 = requests.post(
                    "http://localhost:8000/v1/projects/"+str(project_id)+"/vpcs/vms/"+vm_id_first+"/adapters/0/ports/0/nio",
                    data=json.dumps(data)
                )
        print "-----------RES 1-----------"
        print res_1

        data = {"lport":int(vm_obj_2.udp_port),"rhost":"127.0.0.1","rport":int(vm_obj_1.udp_port), "type":"nio_udp"}
        print data
        res_2 = requests.post(
                    "http://localhost:8000/v1/projects/"+str(project_id)+"/vpcs/vms/"+vm_id_second+"/adapters/0/ports/0/nio",
                    data=json.dumps(data)
                )
        print "-----------RES 2-----------"
        print res_2
        return JsonResponse({"status":"success"})

@csrf_exempt
def start_vm(request):
    if request.method == "POST":
        vm_id = request.POST.get("vm_id")
        project_id = request.POST.get("project_id")
        res = requests.post("http://localhost:8000/v1/projects/"+str(project_id)+"/vpcs/vms/"+str(vm_id)+"/start",data=json.dumps({}))
        return JsonResponse({"status":"success","code":res.status_code})
