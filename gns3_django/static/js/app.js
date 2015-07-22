var nodes, edges, network;
var curNodeID = 0;
var curEdgeID = 0;

var curProject = {}; //stores the current project in the variable
var vcps = []; //stores all the vcps created

function toJSON(obj) {
  return JSON.stringify(obj, null, 4);
}

function addNode(){
  try{
    nodes.add({
      id: curNodeID,
      label: document.getElementById('node-label').value
    });
    curNodeID++;
    var data = {};
    data.project_id = curProject.project_id;
    data.vcps_name = document.getElementById('node-label').value;
    $.ajax({
      url: 'vcps/create',
      type: 'POST',
      data: data,
      success: function(data,status,jqHXR){
        alert("VCPS Node has been added with VM ID "+data["vm_id"]);
        console.log(data);
        vcps.push({"name":data["vcps_name"],"vm_id":data["vm_id"],"port":data["port"]})
      },
      error: function(err){
        console.log(err);
      }
    });
    document.getElementById('node-label').value = '';
  } catch (err) {
    alert(err);
  }
}

function updateNode(){
  try{
    nodes.update({
      id: document.getElementById('node-id').value,
      label: document.getElementById('node-label').value
    });
    // document.getElementById('node-id').value = '';
    document.getElementById('node-label').value = '';
    console.log("The node got updated");
  }catch(err){
    alert(err);
  }
}

function removeNode(){
  try{
    nodes.remove({id: document.getElementById('node-id').value});
    // document.getElementById('node-id').value = '';
    document.getElementById('node-label').value = '';
  } catch(err){
    alert(err);
  }
}

function addEdge(){
  try{
    edges.add({
      id: curEdgeID,
      from: document.getElementById('edge-from').value,
      to: document.getElementById('edge-to').value
    });
    curEdgeID++;
    //Get the Node objects from VCPS and their port numbers
    var vpcs_obj_1 = vcps[document.getElementById('edge-from').value]
    var vpcs_obj_2 = vcps[document.getElementById('edge-to').value]
    console.log(vcps);
    console.log(vpcs_obj_1);
    console.log(vpcs_obj_2);

    var data = {};
    data.project_id = curProject.project_id;
    data.vm_id_first = vpcs_obj_1["vm_id"];
    data.vm_id_second = vpcs_obj_2["vm_id"];
    $.ajax({
      url: 'vcps/link',
      type: 'POST',
      data: data,
      success: function(data,status,jqHXR){
        alert("The nodes are linked. You can now start the VMs.");
      },
      error: function(err){
        console.log(err);
      }
    });
  } catch(err){
    alert(err);
  }
}

function updateEdge(){
  try{
    edges.update({
      id: document.getElementById('edge-id').value,
      from: document.getElementById('edge-from').value,
      to: document.getElementById('edge-to').value
    });
  } catch(err){
    alert(err);
  }
}

function removeEdge(){
  try{
    edges.remove({
      id: document.getElementById('edge-id').value
    });
  } catch(err) {
    alert(err);
  }
}

function draw() {
  nodes = new vis.DataSet();
  edges = new vis.DataSet();

  var container = document.getElementById('network');
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {};
  network = new vis.Network(container, data, options);
}

/*
  Sets the server URL and Port as defined by the user
 */
function setServerDetails(){
  var data = {};
  var serverURL = document.getElementById('settingsURL').value;
  var serverPort = document.getElementById('settingsPort').value;
  data.serverURL = serverURL;
  data.serverPort = serverPort;
  console.log(data);
  $.ajax({
    url: 'settings',
    type: 'POST',
    data: data,
    success: function(data,status,jqHXR){
      alert("The server details have been updated");
      console.log(data);
      location.reload();
      //Close the modal and reload the page with new settings
    },
    error: function(err){
      console.log(err);
    }
  });
}

function addProject(){
  var data = {};
  var serverURL = document.getElementById('projectName').value;
  data.projectName = serverURL;
  console.log(data);
  $.ajax({
    url: 'project/create',
    type: 'POST',
    data: data,
    success: function(data,status,jqHXR){
      alert("Project has been added");
      console.log(data["project_id"]);
      curProject.project_id = data["project_id"];
      curProject.project_name = data["name"];
    },
    error: function(err){
      console.log(err);
    }
  });
}

function startVM(){
  try{
    //Get the Node objects from VCPS and their port numbers
    var vpcs_obj_1 = vcps[document.getElementById('edge-from').value]
    var vpcs_obj_2 = vcps[document.getElementById('edge-to').value]

    var data = {};
    data.project_id = curProject.project_id;
    data.vm_id = vpcs_obj_1["vm_id"];
    $.ajax({
      url: 'vcps/start',
      type: 'POST',
      data: data,
      success: function(data,status,jqHXR){
        alert("VM "+vpcs_obj_1["vm_id"]+" has started");
        console.log(data);
      },
      error: function(err){
        console.log(err);
      }
    });

    data = {}
    data.vm_id = vpcs_obj_2["vm_id"];
    data.project_id = curProject.project_id;
    $.ajax({
      url:'vcps/start',
      type:'POST',
      data:data,
      success: function(data,status,jqHXR){
        alert("VM "+vpcs_obj_2["vm_id"]+" has started");
        console.log(data);
      },
      error: function(err){
        console.log(err);
      }
    });
  } catch(err){
    alert(err);
  }
}

// function createProject(project_name) {
//   data = {name:project_name}
//   $.ajax({
//     url: 'project/create',
//     type: 'POST',
//     data: data,
//     success: function(data,status,jqHXR) {
//       data = JSON.parse(data);

//     }
//   });
// }
