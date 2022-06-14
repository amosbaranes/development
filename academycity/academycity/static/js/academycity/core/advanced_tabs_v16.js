// -- AdvancedTabsManager --
function AdvancedTabsManager(my_name, my_app, body_,
activate_function_link,update_field_link,get_data_link,get_adjective_link,
company_obj_id, is_show_btns=true, user_id=0)
{
 this.company_obj_id=company_obj_id;
 this.user_id=user_id;
 this.my_name=my_name; this.my_app=my_app; this.elm_body=body_;
 this.activate_function_link_=activate_function_link;
 this.update_field_link_=update_field_link;
 this.get_data_link_=get_data_link;
 this.get_adjective_link_=get_adjective_link;
 this.titles=null;this.container=null;
 this.content={"last_obj_number":0};
 this.tabs={};
 this.init_create_containers();
 if(is_show_btns == true){this.create_add_delete_editor();}
 this.setTabs();
 this.active_tab=null;
 this.editor=null;

 this.buttons = {"Tab":{"title":"Tab", "obj_type":"none",
                        "sub_buttons": {"NewFunction":{"title":"new func", "width":10},
                                        "DeleteFunction":{"title":"del func", "width":10}}},
                 "TabContent":{"title":"Tab Content", "obj_type":"none",
                        "sub_buttons": {"content":{"title":"Content", "width":10, "setting": [], "attributes":[], "functions":[]}}},
                 "Component":{"title":"Component", "obj_type":"acObj",
                        "sub_buttons": {"Button":{"title":"Btn", "width":5, "setting": [], "attributes":[], "functions":[]},
                                        "Span":{"title":"Span", "width":5, "setting": [], "attributes":[], "functions":[]},
                                        "Input":{"title":"Input", "width":5, "setting": [], "attributes":["field"], "functions":["onchange"]},
                                        "Select":{"title":"Select", "width":5, "setting": [], "attributes":["field"], "functions":["onchange"]},
                                        "Table":{"title":"Table", "width":5, "setting": [], "attributes":[], "functions":["onchange"]},
                                        "DIV":{"title":"div", "width":3, "setting": [], "attributes":[], "functions":[]},
                                        "A":{"title":"a", "width":3, "setting": [], "attributes":["href", "target"], "functions":[]},
                                        "H":{"title":"h", "width":3, "setting": [], "attributes":[], "functions":[]},
                                        "H1":{"title":"h1", "width":3, "setting": [], "attributes":[], "functions":[]},
                                        "H2":{"title":"h2", "width":3, "setting": [], "attributes":[], "functions":[]},
                                        "H3":{"title":"h3", "width":3, "setting": [], "attributes":[], "functions":[]}}},
                 "TabNavLink":{"title":"Tab Nav Link", "obj_type":"none",
                        "sub_buttons": {"nav":{"title":"Navigator", "width":10},
                                        "item":{"title":"Item", "width":10}}},
                 "PopWin":{"title":"Pop Win", "obj_type":"none",
                        "sub_buttons": {"NewPopWin":{"title":"New Pop Win", "width":10},
                                        "DeletePopWin":{"title":"Del Pop Win", "width":10}}},
                 "Plugin":{"title":"Plugin", "obj_type":"acPlugin",
                        "sub_buttons": {"SearchTable":{"title":"Search Table", "width":10, "setting": [], "attributes":["number_of_rows"], "functions":["onchange"]},
                                        "Chart":{"title":"Chart", "width":5, "setting": [], "attributes":["height"], "functions":[]}}}
                }
 this.tab_nav_links = {"functions":["onclick", "onmouseover", "onmouseout"],
                       "settings_list":["width", "add_title", "remove_title", "is_show_btns", "obj_number", "background_color"],
                       "attributes_list":[]
                       }

 this.nav_link = {"functions":["onclick", "onmouseover", "onmouseout"],
                  "settings_list":["link_number", "link", "title"],
                  "attributes_list":[]
                  }

 this.tab_content = {"functions_list":["onclick", "onmouseover", "onmouseout"],
                     "settings_list":["width", "color", "background_color"],
                     "attributes_list":["table", "parent_table", "link_number", "content_type"]}

 this.pop_win = {"functions_list":["onclick", "onmouseover", "onmouseout"],
                     "settings_list":["width", "height", "color", "background_color"],
                     "attributes_list":["name","top","right","title", "table", "link_number","tab_id","is_panel",
                                        "title_color", "title_background_color", "content_type"]}
}

AdvancedTabsManager.prototype.init_create_containers = function()
{
   this.add_delete_editor = document.createElement("div");
   this.titles = document.createElement("div");
   this.titles.setAttribute("class", "maintab");
   this.container = document.createElement("div");
   this.container.setAttribute("style", "width: 100%;height: 100%;")
   this.elm_body.appendChild(this.add_delete_editor);this.elm_body.appendChild(this.titles);this.elm_body.appendChild(this.container);
}

AdvancedTabsManager.prototype.create_add_delete_editor = function()
{
  this.add_btn=document.createElement("button");
  this.add_btn.innerHTML="Add Tab"
  this.add_btn.addEventListener("click", function(){
      var tab_name_ = prompt("Enter name for new tab:",'');if(tab_name_==''){alert("Please enter a tab name"); return;}
      tab_name_=tab_name_.toLowerCase();
      var dic_ = {"obj" : "AdvancedTabs", "atm": atm_.my_name, "app": atm_.my_app, "fun": "add_tab", "params": {"tab_name": tab_name_}}
             $.post(atm_.activate_function_link_,
                  {dic : JSON.stringify(dic_)},
                  function(dic){
                    //alert(JSON.stringify('dic'))
                    //alert(JSON.stringify(dic))
                    var result = dic["result"]
                    for (id_ in result){
                     result[id_]["properties"]["link_number"]=this.get_next_obj_number();
                     atm.tabs[id_] = new Tab(atm, data=result[id_], id=id_);
                    }
                    //alert(JSON.stringify(result))
                    atm.tabs[id_].btn.click();
                    try{atm.set_active_tab(atm.tabs[id_].btn)} catch(er){alert(er)}
                    try{atm.save()} catch(er){alert(er)}
                    atm.save();
                  }.bind(atm=atm_));
      }.bind(atm_=this, event))
  //--
  this.delete_btn = document.createElement("button");
  this.delete_btn.innerHTML = "Delete Tab"
  this.delete_btn.addEventListener("click", function(){
       var tab_name_ = prompt("Enter name of a tab to delete:" , '')
       if(tab_name_ == '') {alert("Please enter a tab name"); return;}
       var dic_ = {"obj" : "AdvancedTabs", "atm": atm_.my_name, "app": this.my_app, "fun": "delete_tab", "params": {"tab_name": tab_name_}}
       // alert(JSON.stringify(dic_))
              $.post(atm_.activate_function_link_,
              {
                dic : JSON.stringify(dic_)
              },
              function(dic){
                //alert(JSON.stringify(dic))
                var tab_id_ = dic["result"]["tab_id"];
                atm.delete_tab(tab_id_, tab_name_);
             }.bind(atm=atm_))
  }.bind(atm_=this, event))
  //--
  this.editor_btn=document.createElement("button");
  this.editor_btn.innerHTML = "Editor"
  this.editor_btn.parent=this;
  this.editor_btn.addEventListener("click", function(){
    try{editor.set_tab(atm_.active_tab);} catch(er){
    editor = new PopWin(my_name_="editor",win_name_="editor",win_title_="Editor for Tab: ",user_id=1, atm=atm_)
    editor.__init__();
    editor.set_win_frame_style("20", "650", "1000", "15%", "5%", "white")
    editor.set_acWinStatEventListeners(editor);
    }
    editor.set_acWinStat('block');
    atm_.editor=editor;
  }.bind(atm_=this, event))

  this.add_delete_editor.appendChild(this.add_btn);
  this.add_delete_editor.appendChild(this.delete_btn);
  this.add_delete_editor.appendChild(this.editor_btn);
}

AdvancedTabsManager.prototype.setTabs = function()
{
  var dic_ = {"obj" : "AdvancedTabs", "atm": this.my_name, "app": this.my_app, "fun": "get_tabs_from_table", "params": {"name": ""}}
  // alert(JSON.stringify(dic_))
  $.post(this.activate_function_link_,{dic : JSON.stringify(dic_)},
      function(dic){
          //alert(JSON.stringify(dic))
          var result = dic["result"];
          if(result["manager"]==null){} else {atm_.content=result["manager"]}
          //alert('JSON.stringify(atm_.content)')
          //alert(JSON.stringify(atm_.content))
          var tabs = result["tabs"];
          //alert('JSON.stringify(tabs)')
          //alert(JSON.stringify(tabs))
          for (id_ in tabs)
          {
          //alert(9)
            //alert(id_);
            atm_.tabs[id_]=new Tab(atm_, data=tabs[id_], id=id_);
            atm_.set_active_tab(atm_.tabs[id_].btn)
            atm_.tabs[id_].create_tab_pop_wins();
          //alert(91)
          }

          try{atm_.tabs[id_].btn.click();} catch(er){alert(er)}
     }.bind(atm_ = this)
 );
}

AdvancedTabsManager.prototype.delete_tab = function(tab_id_, tab_name_)
{this.tabs[tab_id_].btn.outerHTML="";this.tabs[tab_id_].content.outerHTML="";}

AdvancedTabsManager.prototype.set_active_tab = function(btn)
{
  var tabcontent=document.getElementsByClassName("tabcontent");
  for(i=0;i<tabcontent.length;i++){tabcontent[i].style.display='none';}
  var tablinks=document.getElementsByClassName("tablinks");

  try{eval(btn.parent.tab_name+"__myclick__(called_tab=btn.parent, calling_tab=btn.parent)");} catch(er){alert(er)}

  for (i=0;i<tablinks.length;i++){
    try{
      tablinks[i].className=tablinks[i].className.replace(" active","");
      if(tablinks[i].parent.tab_name!=btn.parent.tab_name)
      {eval(tablinks[i].parent.tab_name+"__otherclick__(called_tab=tablinks[i].parent, calling_tab=btn.parent)");}
    } catch(er){alert(er)}
  }

  try{for(w in this.active_tab.PopWinObjects){if(w=="editor"){ continue;};this.active_tab.PopWinObjects[w].temp_close_win()}} catch(er){}

  try{
     this.active_tab=btn.parent;this.active_tab.content.style.display="block";btn.className+=" active";

  try{for(w in this.active_tab.PopWinObjects){if(w=="editor"){ continue;}; this.active_tab.PopWinObjects[w].resume_win()}} catch(er){}

    try{
      var click_event = new Event("click", {bubbles: true});
      this.editor_btn.dispatchEvent(click_event);
      this.editor.main_menus["Tab"].btn.dispatchEvent(click_event);
      this.editor.set_title(this.editor.win_title_+this.active_tab.tab_name);
    } catch(er){}
  } catch(er){}
}

AdvancedTabsManager.prototype.get_tab = function(tab_name){for(id in this.tabs){if (this.tabs[id].tab_name==tab_name){return this.tabs[id]}}}

AdvancedTabsManager.prototype.get_obj = function(tab, dic)
{
 //alert(tab.tab_name)
 //alert(JSON.stringify(dic))

 var s='function '+dic["obj_name"]+dic["properties"]["obj_number"]+'(atm_, tab_, dic_)'
 s+='{'
 //s+='this.my_type="'+dic["obj_name"]+'";this.my_element="'+dic["element_name"]+'";';
 s+=dic["obj_type"]+'.call(this);'
 s+='this.tab=tab_;this.atm=atm_;this.editor=this.atm.editor;this.data=dic_;var ps=this.atm.get_obj_functions_settings_attributes(dic_);'
 s+='this.settings=ps["settings"];'
 s+='this.functions=ps["functions"] ;'
 s+='this.attributes=ps["attributes"] ;'
 s+='try{this.creator=new '+dic["obj_name"]+'Creator(this)} catch(er){};'
 s+='};'
 //alert(s)

 try{eval(s)} catch(er){alert(er)}
 s=dic["obj_name"]+dic["properties"]["obj_number"]+'.prototype = Object.create('+dic["obj_type"]+'.prototype);'
 //alert(s);
 try{eval(s)} catch(er){alert(er)}
 //alert(JSON.stringify(dic))
 s = 'new '+dic["obj_name"]+dic["properties"]["obj_number"]+'(atm_=this, tab_=tab, dic_=dic)'
 //alert(s)
 return eval(s)
}

AdvancedTabsManager.prototype.get_obj_functions_settings_attributes = function(dic_)
{
 //alert(JSON.stringify(dic_));
 var ps={"settings": ["width", "x", "y", "title", "obj_number"], "attributes":[], "functions":["onclick"]};
 var dic__=this.buttons[dic_["parent_obj_name"]]["sub_buttons"][dic_["element_name"]]
 //alert(JSON.stringify(dic_));
 //alert(JSON.stringify(dic__));

 for (a in dic_["attributes"]){if (!ps["attributes"].includes(a)){ps["attributes"].push(a)}};
 for (s in dic_["setting"]){if (!ps["settings"].includes(s)){ps["settings"].push(s)}};
 for (f in dic_["functions"]){if (!ps["functions"].includes(f)){ps["functions"].push(f)}};
 //--
 for (i in dic__["attributes"]){if (!ps["attributes"].includes(dic__["attributes"][i])){ps["attributes"].push(dic__["attributes"][i])}};
 for (i in dic__["setting"]){if (!ps["settings"].includes(dic__["setting"][i])){ps["settings"].push(dic__["setting"][i])}};
 for (i in dic__["functions"]){if (!ps["functions"].includes(dic__["functions"][i])){ps["functions"].push(dic__["functions"][i])}};
 //alert(JSON.stringify(ps));
 return ps;
}

AdvancedTabsManager.prototype.save = function()
{
try{
  var tab_content = {
                      "tab_content_link_dic": this.active_tab.tab_content_link_dic,
                      "functions": this.active_tab.tab_functions,
                      "nav_links": this.active_tab.tab_nav_links,
                      "properties": this.active_tab.tab_properties,
                      "objects": this.active_tab.tab_objects,
                      "tab_name": this.active_tab.tab_name,
                      "tab_title": this.active_tab.tab_title,
                      "tab_type": this.active_tab.tab_type,
                      "tab_pop_win_buttons": this.active_tab.tab_pop_win_buttons
                    }
} catch(er){alert(er)}
  var dic_={"obj":"AdvancedTabs","atm":this.my_name, "app": this.my_app, "fun":"save_content",
            "params": {"atm_content": this.content,
                       "tab_content": tab_content,
                       "tab_name": this.active_tab.tab_name,
                       "tab_id": this.active_tab.tab_id}}
      //alert(JSON.stringify(dic_))
     $.post(this.activate_function_link_,
          {dic : JSON.stringify(dic_)},
          function(dic){
            if(dic["status"]!="ok"){alert(JSON.stringify(dic["result"]))}
            else{ // alert("ok")
            }
          });
}

AdvancedTabsManager.prototype.save_data = function(container, dic_)
{
  dic_["app"]=this.my_app;
  dic_["company_obj_id"]=this.company_obj_id;
  //alert(JSON.stringify(dic_));
  //alert(container.outerHTML)
  //alert(this.update_field_link_)

  $.post(this.update_field_link_,
          {dic : JSON.stringify(dic_)},
          function(dic){
            if(dic["status"]!="ok")
            {alert("Data was not saved.")}
            else{  //alert("ok")
              //alert(JSON.stringify(dic))
              //dic["company_obj_id"]

              //alert(atm)
              //alert(atm.active_tab_content)
              //alert(atm.active_tab_content.link_content)
              //alert(12345)

              //alert(container_.outerHTML)
              //alert(123451)
              //atm.active_tab_content.link_content.setAttribute("record_id", dic["record_id"])

              //alert(container_.outerHTML)
              container_.setAttribute("record_id", dic["record_id"])
              //alert(container_.outerHTML)

              //alert(123452)
              //alert(container_.outerHTML)
              //alert(123453)
            }
          }.bind(container_=container));
}

AdvancedTabsManager.prototype.get_data = function(call_back_fun, dic_, tbody_)
{
  dic_["app"]=this.my_app;
  dic_["company_obj_id"]=this.company_obj_id;
  var temp_data = null;
  //alert(JSON.stringify(dic_));
  //alert(tbody_.outerHTML)
  //alert(call_back_fun)
  $.post(this.get_data_link_,
          {dic : JSON.stringify(dic_)},
          function(data){
           call_back_fun(data["dic"], tbody_)
           tbody_.data=data["dic"];
          });
}


AdvancedTabsManager.prototype.get_adjective = function(call_back_fun, dic_, html_obj)
{
  dic_["company_obj_id"]=this.company_obj_id;
  // alert(JSON.stringify(dic_));
  $.post(this.get_adjective_link_,
          {dic : JSON.stringify(dic_)},
          function(data){
           call_back_fun(data["dic"], html_obj)
           html_obj.data=data["dic"];
          });
}

AdvancedTabsManager.prototype.get_next_obj_number=function(){
this.content["last_obj_number"]+=1;
return this.content["last_obj_number"]
}

// -- FunctionsPropertiesEditor --
function FunctionsPropertiesEditor(tab, functions_dic, functions_list_dic, properties_dic, settings_list,
                                   attributes_list, tab_btn_name="PopWin", properties_func=null, node_to_delete=null)
{
  //alert(JSON.stringify(functions_dic))
  //alert(JSON.stringify(functions_list_dic))
  //alert(JSON.stringify(properties_dic))
  //alert(JSON.stringify(settings_list))
  //alert(JSON.stringify(attributes_list))

  //alert(JSON.stringify(functions_dic))
  //alert('JSON.stringify(properties_dic)')
  //alert(JSON.stringify(properties_dic))
  //--
  tab.parent.editor.main_menus[tab_btn_name].btn.click();
  tab.parent.editor.win_content.innerHTML="";
  var lef_nav=document.createElement("div");
  lef_nav.setAttribute("class", "tab");
  var new_del_table=document.createElement("table");
  //new_del_table.setAttribute("style","width:40%")
  var tr=document.createElement("tr");new_del_table.appendChild(tr);
  var tdd=document.createElement("td");var del_btn=document.createElement("button");del_btn.innerHTML="Del Func";tdd.appendChild(del_btn);tr.appendChild(tdd);
  var tdn=document.createElement("td");var new_btn=document.createElement("button");new_btn.innerHTML="New Func";tdn.appendChild(new_btn);tr.appendChild(tdn);
  lef_nav.appendChild(new_del_table);
  //--
  new_btn.onclick= function (){
    var fun_name_ = prompt("Enter name for new function:" , '');
    if(fun_name_ == '') {alert("Please enter a function name"); return;}
    functions[fun_name_]="function (obj){\ntry{\n\n} catch(er){alert(er)}}";
    editor.tab_obj_.parent.save();
  }.bind(editor=tab.parent.editor, functions=functions_dic, event)

  del_btn.onclick= function (){
    event.preventDefault();
    var f=editor.tab_obj_.active_function;
    var fun_name_ = prompt("Are you sure you want to delete function "+f+". If so, type Yes:" , 'No');
    if(fun_name_ != 'Yes') {return;};

    //var ll=editor.active_popup_win;
    //alert(JSON.stringify(editor.tab_obj_.tab_pop_win_buttons["pop_wins"][ll[2]]["functions"]))
    //delete editor.tab_obj_.tab_pop_win_buttons["pop_wins"][ll[2]]["functions"][f]

    delete functions[f]
    this.tab_obj_.parent.save();
    alert("function "+f+" was deleted.")
  }.bind(editor=tab.parent.editor, functions=functions_dic, event)
  //--
  var nav_div=document.createElement("div");
  var tab_content = document.createElement("textarea");
  nav_div.onclick=function(){
    //alert(JSON.stringify(editor_.tab_obj_.tab_functions))
    var e=event.target;
    try{var cc=e.getAttribute("class");if(cc!="funtablinks"){return;}} catch(er){}
    var f=event.target.innerHTML;
    editor.tab_obj_.active_function=f;
    var fun=null;
    try{fun=functions_[f]} catch(er){}
    if(fun==null){fun="function (event){\ntry{\n\n} catch(er){alert(er)}\n}";functions_[f]=fun;}
      tab_content_.innerHTML=functions_[f];
      tab_content_.setAttribute("fun_name",f);
      var funtablinks = document.getElementsByClassName("funtablinks");
      for (var i=0;i<funtablinks.length;i++){funtablinks[i].className=funtablinks[i].className.replace(" active","");};
      event.target.className += " active";
       //alert(editor_.tab_content.outerHTML)
    }.bind(editor=tab.parent.editor, tab_content_=tab_content, functions_=functions_dic, event);
    nav_div.btns={};
    for(i in functions_list_dic)
    {
      var f=functions_list_dic[i]
      nav_div.btns[f] = document.createElement("button");
      nav_div.btns[f].setAttribute("class", "funtablinks");
      nav_div.btns[f].innerHTML = f;
      nav_div.appendChild(nav_div.btns[f]);
    }
    lef_nav.appendChild(nav_div);
    tab.parent.editor.win_content.appendChild(lef_nav);
    //--
    tab_content.setAttribute("class", "tab_textarea");
    tab_content.onchange= function (){
    //alert(event.target.value)
    //alert(event.target.getAttribute("fun_name"))
    //alert(JSON.stringify(functions__))

     functions__[event.target.getAttribute("fun_name")]=event.target.value;
     editor.tab_obj_.parent.save();
    }.bind(editor=tab.parent.editor, functions__=functions_dic, event)
    tab.parent.editor.win_content.appendChild(tab_content);
    //--
    var tab_properties_ = document.createElement("div");
    if(node_to_delete!=null){
      var btn=document.createElement("button");btn.innerHTML="Delete Obj";btn.tab=tab;
      btn.onclick=function(event){
        var link_ = prompt("Are you sure you want to remove link the obj? if so type Yes:",'No');
        if(link_=='Yes')
        {
         //alert(tab_)
         //alert(tab_.tab_name);
         try{var s='delete tab_'+node_to_delete_;eval(s)} catch(er) {}
         try{tab_.parent.save();} catch(er) {alert("error 2099: "+ er)}
        }
      }.bind(tab_=tab, node_to_delete_=node_to_delete)
      tab_properties_.appendChild(btn);
    }
   var table = document.createElement("table");var tr=document.createElement("tr");table.appendChild(tr);
   var thp=document.createElement("th");thp.innerHTML="Property";thp.setAttribute("style","width:10%;text-align:center;");
   tr.appendChild(thp);
   var thv=document.createElement("th");thv.innerHTML="Value";thv.setAttribute("style","width:10%;text-align:center;");
   tr.appendChild(thv);
   tab_properties_.appendChild(table);

   for (i in settings_list)
   {
     var s=settings_list[i];
     var tr=document.createElement("tr");table.appendChild(tr);
     var td=document.createElement("td");td.innerHTML=s;tr.appendChild(td);
     var td=document.createElement("td");var input=document.createElement("input");
     input.setAttribute("size","10");input.setAttribute("property",s);td.appendChild(input);
     //input.setAttribute("property",s);
     try{if(properties_dic[s]==null){} else{input.value=properties_dic[s]}} catch(er){alert(er)}
     tr.appendChild(td);
   }
   for (i in attributes_list)
   {
     var s=attributes_list[i];
     var tr=document.createElement("tr");table.appendChild(tr);
     var td=document.createElement("td");td.innerHTML=s;tr.appendChild(td);
     var td=document.createElement("td");var input=document.createElement("input");
     input.setAttribute("size","10");input.setAttribute("property",s);td.appendChild(input);
     try{if(properties_dic[s]==null){} else{input.value=properties_dic[s]}} catch(er){alert(er)}
     tr.appendChild(td);
   }
   tab_properties_.addEventListener("change", function(){
     var p=event.target;var property=p.getAttribute("property");var v=p.value;
     //alert(property); alert(v); alert(JSON.stringify(properties));
     properties[property]=v;
     //alert(JSON.stringify(properties));
      editor.tab_obj_.parent.save();
   }.bind(editor=tab.parent.editor, properties=properties_dic, event))
   tab_properties_.setAttribute("class", "com_setting");
   tab.parent.editor.win_content.appendChild(tab_properties_);
   //alert(properties_func)
   try{if(properties_func!=null){properties_func(tab, tab_properties_)}} catch(er) {alert("error 206: "+er)}
}

// -- acObj --
function acObj(){}

acObj.prototype.create_editor = function(){
 this.editor.component_left_nav.innerHTML="";
 this.editor.component_fun_editor.innerHTML="";
 this.editor.component_properties.innerHTML="";
 this.editor.component_left_nav.btns={}
  //alert("functions")
  // alert(JSON.stringify(this.functions));
  //alert("component)
  // alert(JSON.stringify(this.settings));
 for (i in this.functions)
 {
   var f=this.functions[i];
   this.editor.component_left_nav.btns[f] = document.createElement("button");
   this.editor.component_left_nav.btns[f].setAttribute("class", "comfuntablinks");
   this.editor.component_left_nav.btns[f].innerHTML = f;
   this.editor.component_left_nav.appendChild(editor.component_left_nav.btns[f]);
 }

 var btn=document.createElement("button");btn.innerHTML="Delete Obj";btn.tab=this.tab;btn.editor=this.editor;
 btn.onclick=function(event){
   var link_ = prompt("Are you sure you want to remove link the obj? if so type Yes:",'No');
   if(link_=='Yes')
   {
    //--
    var obj_number=this.tab.active_obj.data["properties"]["obj_number"];
    var container_id=this.tab.active_obj.data["container_id"];
    //alert(JSON.stringify(tab.tab_objects))
    delete this.tab.tab_objects[container_id][obj_number];
    //alert(JSON.stringify(tab.tab_objects))
    this.editor.tab_obj_.parent.save();
    // --
    //alert(JSON.stringify(editor.tab_obj_.tab_content))
   }
  }
 this.editor.component_properties.appendChild(btn);
 //--
 var table = document.createElement("table");var tr=document.createElement("tr");table.appendChild(tr);
 var thp=document.createElement("th");thp.innerHTML="Property";tr.appendChild(thp);thp.setAttribute("style","width:10%;text-align:center;")
 var thv=document.createElement("th");thv.innerHTML="Value";tr.appendChild(thv);thv.setAttribute("style","width:10%;text-align:center;")
 this.editor.component_properties.appendChild(table);
 for (i in this.settings)
 {
   var s=this.settings[i];
   var tr=document.createElement("tr");table.appendChild(tr);
   var td=document.createElement("td");td.innerHTML=s;tr.appendChild(td);
   var td=document.createElement("td");var input=document.createElement("input");
   input.setAttribute("property",s);td.appendChild(input);
   try{if(this.data["properties"][s]==null){} else{input.value=this.data["properties"][s]}} catch(er){alert(er)}
   tr.appendChild(td);
 }
 //alert(JSON.stringify(this.attributes));
 for (i in this.attributes)
 {
   var s=this.attributes[i];
   var tr=document.createElement("tr");table.appendChild(tr);
   var td=document.createElement("td");td.innerHTML=s;tr.appendChild(td);
   var td=document.createElement("td");var input=document.createElement("input");
   input.setAttribute("property",s);td.appendChild(input);
   try{if(this.data["properties"][s]==null){} else{input.value=this.data["properties"][s]}} catch(er){alert(er)}
   tr.appendChild(td);
 }

 //alert(JSON.stringify(this.data));alert(2)
 if(this.data["element_name"]=="Select")
 {
     var select_attributes = ["options", "global_adjective", "app_adjective", "data_app", "data_table", "data_field", "data_filter_field"]
     for (i in select_attributes)
     {
       var s=select_attributes[i];
       var tr=document.createElement("tr");table.appendChild(tr);
       var td=document.createElement("td");td.innerHTML=s;tr.appendChild(td);
       var td=document.createElement("td");var input=document.createElement("input");
       input.setAttribute("property",s);td.appendChild(input);
       try{if(this.data["properties"][s]==null){} else{input.value=this.data["properties"][s]}} catch(er){alert(er)}
       tr.appendChild(td);
     }
 }
}

acObj.prototype.create_obj = function(){
  var container = document.getElementById("content_"+this.data["container_id"])
  //alert(container.outerHTML)
  //alert(container) //alert(container.outerHTML)

  this.new_obj=document.createElement(this.data["element_name"]);
  this.new_obj.my_creator_obj=this;

  this.new_obj.setAttribute("container_id", this.data["container_id"]);
  this.new_obj.setAttribute("id", this.data["properties"]["obj_number"]);
  this.new_obj.setAttribute("obj_type", this.data["obj_type"]);
  this.new_obj.setAttribute("type", this.data["element_name"]);
  if("width" in this.data["properties"]){var width_=this.data["properties"]["width"]} else {var width_="10"}
  this.new_obj.innerHTML=this.data["properties"]["title"];
  for (i in this.attributes){var s=this.attributes[i];
   if(s in this.data["properties"]){this.new_obj.setAttribute(s, this.data["properties"][s])}
   else{this.new_obj.setAttribute(s, "")}}

  if(this.data["element_name"]=="Input")
  {
    var nx_=80;var x=1*this.data["properties"]["x"]+nx_;
    this.new_obj.setAttribute("style", "position:absolute;left:"+x+"px;top:"+this.data["properties"]["y"]+"px;width:"+width_+"px");
    var span=document.createElement("span");span.innerHTML=this.data["properties"]["title"];
    var x = 1*this.data["properties"]["x"]
    span.setAttribute("style", "position:absolute;left:"+x+"px;top:"+this.data["properties"]["y"]+"px;");
    container.appendChild(span);
  } else
  {
    this.new_obj.setAttribute("style", "position:absolute;left:"+this.data["properties"]["x"]+"px;top:"+this.data["properties"]["y"]+"px;width:"+width_+"px");
  }

  if(this.data["element_name"]=="Select")
  {
   try{this.get_select_data()} catch(er){}
  }
  container.appendChild(this.new_obj)
 for(f in this.data["functions"]){var s="this.new_obj."+f+"="+this.data["functions"][f];eval(s)}
 //alert(this.new_obj.outerHTML);
 //alert(JSON.stringify(this.obj_properties));
 //this.obj_properties;
 //this.functions;
}

acObj.prototype.get_select_data = function()
{
  this.new_obj.innerHTML = "";
  var dic=this.data;
  //alert(JSON.stringify(dic));
  var options=dic["properties"]["options"];
    var option = document.createElement("option");
    option.value = "-1"; option.text = "----";
    this.new_obj.appendChild(option);
  if(options!="" & options!=null)
  {
    options=options.split(",")
    for(i in options){
     var option = document.createElement("option");
     option.value = options[i];
     option.text = options[i];
     this.new_obj.appendChild(option);
    }
  } else if (dic["properties"]["global_adjective"]!="" & dic["properties"]["global_adjective"]!=null)
  {
   var adjective=dic["properties"]["global_adjective"];
   var dic_={"app":"core", "adjective":adjective}
   //alert(JSON.stringify(dic_))
      var fun=function(data, html_obj){
        //alert(html_obj.outerHTML)
        //alert(JSON.stringify(data));
        for(i in data){
         var option = document.createElement("option");
         option.value = i;
         option.text = data[i];
         html_obj.appendChild(option);
        }
      }
      this.atm.get_adjective(call_back_fun=fun, dic_, this.new_obj);
  } else if (dic["properties"]["app_adjective"]!="" & dic["properties"]["app_adjective"]!=null)
  {
   var adjective=dic["properties"]["app_adjective"];
   var dic_={"app":this.atm.my_app, "adjective":adjective}
   // need to create model adjectives values in this app.
     alert(JSON.stringify(dic_))
      var fun=function(data, html_obj){
        //alert(html_obj.outerHTML)
        //alert(JSON.stringify(data));
        for(i in data){
         var option = document.createElement("option");
         option.value = i;
         option.text = data[i];
         html_obj.appendChild(option);
        }
      }
      this.atm.get_adjective(call_back_fun=fun, dic_, this.new_obj);
  }

}

// -- acPlugin --
function acPlugin(){}

acPlugin.prototype.create_editor = function(){
 var container_id=this.data["container_id"];
 var obj_number=this.data["properties"]["obj_number"];
 //alert(JSON.stringify(this.tab.tab_objects[container_id][obj_number]));
 try{
 tab_fpe=this.editor.get_functions_properties_editor(this.tab, this.data["functions"], this.functions,
                                                     this.data["properties"],this.settings,this.attributes,
                                                     tab_btn_name="Plugin", properties_func=this.creator.editor_properties_func,
                                                     node_to_delete='.tab_objects['+container_id+']['+obj_number+']')
 } catch(er) {alert("er 207: "+er)}
}

acPlugin.prototype.create_obj = function(){this.creator.create_obj();}


// -- acSearchTableCreator --
function acSearchTableCreator(parent, container){this.parent=parent;this.data=null;
  //alert(JSON.stringify(this.parent.data));
}

acSearchTableCreator.prototype.create_obj = function()
{
  var dic=this.parent.data;
  if(!dic["fields"]){dic["fields"]={"1":{"field_title":"1", "field_name":""},"2":{"field_title":"2", "field_name":""}}}
  //alert(JSON.stringify(dic));
  this.parent.data=dic;
  //--
  var container = document.getElementById("content_"+dic["container_id"]);
  this.number_of_rows=dic["properties"]["number_of_rows"]
  this.fields=[]
  for(f in dic["fields"]){this.fields.push(dic["fields"][f]["field_name"])}
  //--
  this.table_=document.createElement("table");
  this.table_.setAttribute("container_id", dic["container_id"]);
  this.table_.setAttribute("id", dic["properties"]["obj_number"]);
  this.table_.setAttribute("obj_type", dic["obj_type"]);
  this.table_.setAttribute("type", dic["element_name"]);
  if("width" in dic["properties"]){var width_=dic["properties"]["width"]} else {var width_="200"}
  this.table_.setAttribute("style", "position:absolute;left:"+dic["properties"]["x"]+"px;top:"+dic["properties"]["y"]+"px;width:"+width_+"px");
  this.thead=document.createElement("thead");this.table_.appendChild(this.thead);
  var tr_h=document.createElement("tr");
  tr_h.setAttribute("style","cursor:pointer");
  this.thead.appendChild(tr_h);
  var n__=0;
  for(f in dic["fields"])
  {
    var th_=document.createElement("th");
    th_.innerHTML=dic["fields"][f]["field_title"];
    if(n__==0){th_.setAttribute("style", "border-top-left-radius: 15px")}; n__+=1;
    tr_h.appendChild(th_);
  }
  th_.setAttribute("style", "border-top-right-radius: 15px");
  this.tbody=document.createElement("tbody");
  this.tbody.setAttribute("id", "tbody_"+dic["properties"]["obj_number"]);
  this.table_.appendChild(this.tbody);
  this.table_.my_creator_obj=this;

  //alert(5);
  //this.get_data(this.tbody);
  //alert(6);

  for (i in dic["attributes"]){var s=dic["attributes"][i];
   if(s in dic["properties"]){this.table_.setAttribute(s, dic["properties"][s])}
   else{this.table_.setAttribute(s, "")}}

  container.appendChild(this.table_);
  for(f in dic["functions"]){
    if(f=="onclick"){
     this.table_.onclick=this.row_click
    } else{
      var s="this.table_."+f+"="+dic["functions"][f];eval(s);
    }
  }
}

acSearchTableCreator.prototype.get_data = function()
{
  var dic=this.parent.data;
  //alert(JSON.stringify(dic));
  var container = document.getElementById("content_"+dic["container_id"]);
  //alert(container.outerHTML);
  this.data_table_name=container.getAttribute("table")
  try{
    var parent_id_="";
    //alert(this.data_table_name)
    var model_=container.my_creator_obj.link_dic["properties"]["table"];
    //alert(model_)
    try{var parent_model_=container.my_creator_obj.link_dic["properties"]["parent_table"]} catch(er){};
    if(parent_model_==null){var parent_model_="";}
    var record_id_=container.getAttribute("record_id");
    parent_id_=container.getAttribute("parent_id");
    if(parent_id_=="" || parent_id_==null){return}
    var dic_={"model":this.data_table_name, "number_of_rows":this.number_of_rows, "fields":this.fields}
  } catch(er){alert(er)}

  var fun=function(data, ttbody_){
    //alert(8)
    //alert(obj_tbody.outerHTML)
    //alert(JSON.stringify(dic_["fields"]));
    //alert(JSON.stringify(data["dic"]));
    //alert(JSON.stringify(data["dic"][dic_["fields"][0]]))
    //alert(JSON.stringify(data))
    //alert(JSON.stringify(dic_))
    //alert(JSON.stringify(dic_["fields"]))
    //alert(dic_["fields"][0])
    //alert(JSON.stringify(data[dic_["fields"][0]]))
    var n_=data[dic_["fields"][0]].length;
    //alert(n_)
    var s='';
    for(i=0; i<n_; i++)
    {s+='<tr id_="'+data["id"][i]+'" row="'+i+'"'+'>';for(j in dic_["fields"]){var f=dic_["fields"][j];s+='<td>'+data[f][i]+'</td>'};s+='</tr>';}
    //alert(ttbody_.outerHTML);
    ttbody_.innerHTML=s;
  }

  //alert(JSON.stringify(dic_));

  var container_id=this.parent.data["container_id"];
  //alert(container_id);
  var container_dic=this.parent.tab.tab_objects[container_id];
  var dic__=[]; for(i in dic_["fields"]){dic__.push(dic_["fields"][i])}
  for(o in container_dic)
  {if(container_dic[o]["obj_type"]=="acObj" && container_dic[o]["obj_name"]=="acInput"){
      var f=container_dic[o]["properties"]["field"];if(!dic__.includes(f)){dic__.push(f)}}
  }
  //alert(JSON.stringify(dic__));
  var dic__={"model":this.data_table_name, "parent_model": parent_model_, "parent_id":parent_id_, "number_of_rows":this.number_of_rows, "fields":dic__}

  //alert(41)
  this.parent.atm.get_data(call_back_fun=fun, dic__, this.tbody)
}

acSearchTableCreator.prototype.row_click = function(event)
{
 var e=event.target;
 while(e.tagName!="TR"){e=e.parentNode;}
 //alert(e.outerHTML)
 //alert(this.my_creator_obj.table_.outerHTML)
 var n_row=e.getAttribute("row")
 if(n_row==null){return;}
 var container_id=this.my_creator_obj.parent.data["container_id"];
 var container = document.getElementById("content_"+container_id);
 //alert(container_id)
 var result={}
 //alert(JSON.stringify(this.my_creator_obj.tbody.data))
 var dic=this.my_creator_obj.tbody.data;
 for(f in dic){dic[f][n_row];result[f]=dic[f][n_row]}
 container.my_creator_obj.set_objects_data(result);
 try{eval('var zz='+this.my_creator_obj.parent.data["functions"]["onclick"]);zz(event)} catch(er) {alert(er)}
}

acSearchTableCreator.prototype.editor_properties_func = function(tab, tab_properties_)
{
 //alert(tab.active_obj)
 var fields=tab.active_obj.data["fields"];
 var nav=document.createElement("div");
 var add_del_btns=document.createElement("div");
 this.add_btn=document.createElement("button");this.del_btn=document.createElement("button");
 this.add_btn.innerHTML="Add"; this.add_btn.tab=tab;
 this.del_btn.innerHTML="Delete"; this.del_btn.tab=tab; this.del_btn.nav=nav;
 this.add_btn.onclick=function (event){
   var n_=Object.keys(tab.active_obj.data["fields"]).length+1
   tab.active_obj.data["fields"][n_]={"field_name":"","field_title":""};
   tab.parent.save();
 }
 this.del_btn.onclick=function (event){
   //alert(this.nav.active_property_num)
   delete tab.active_obj.data["fields"][this.nav.active_property_num];
   tab.parent.save();
 }

 add_del_btns.appendChild(add_btn);add_del_btns.appendChild(del_btn);

 nav.setAttribute("style","cursor:pointer");
 var nav_detail=document.createElement("div");
 nav.setAttribute("class", "scrollmenu");
 for(f in fields){var a=document.createElement("a");a.innerHTML=f;nav.appendChild(a);}
 nav.onclick=function(event)
 {
  var e=event.target;
  nav_detail.innerHTML="";
  f=e.innerHTML
  this.active_property_num=f
  //alert(JSON.stringify(this.fields[f]));
  var table=document.createElement("table");
  var tr=document.createElement("tr");table.appendChild(tr);
  var th=document.createElement("th");tr.appendChild(th);th.innerHTML="property"
  var th=document.createElement("th");tr.appendChild(th);th.innerHTML="value"
  for(p in this.fields[f])
  {
   var v=this.fields[f];var tr=document.createElement("tr");table.appendChild(tr);
   var td=document.createElement("td");tr.appendChild(td);td.innerHTML=p
   var td=document.createElement("td");tr.appendChild(td);var input=document.createElement("input");
   input.setAttribute("size","10");td.appendChild(input);
   input.setAttribute("field",f);input.setAttribute("property",p);
   input.value=this.fields[f][p]
  }
  nav_detail.appendChild(table);
 }
 nav.fields=fields;

 nav_detail.onchange=function(event){
   event.preventDefault();
   var e=event.target;
   var f=e.getAttribute("field")
   var p=e.getAttribute("property")
   //alert(e.outerHTML);
   //alert(e.value);
   tab.active_obj.data["fields"][f][p]=e.value;
   tab.parent.save();
 }
 nav_detail.tab=tab;
 tab_properties_.appendChild(document.createElement("br"));
 tab_properties_.appendChild(add_del_btns);
 tab_properties_.appendChild(nav);
 tab_properties_.appendChild(nav_detail);
}


// -- acChartCreator --
function acChartCreator(parent){
 this.parent=parent;this.data=null;
 //alert(this.parent.data)
 //alert(JSON.stringify(this.parent.data));
}

acChartCreator.prototype.create_obj = function()
{
  //alert("I am a creator of acPlugin Chart")
  //--
  var dic=this.parent.data;
  //alert(JSON.stringify(dic));
  //--
  var container = document.getElementById("content_"+dic["container_id"]);
  //--
 this.chart=document.createElement("div");
 this.chart.setAttribute("container_id", dic["container_id"]);
 this.chart.setAttribute("id", dic["properties"]["obj_number"]);
 this.chart.setAttribute("obj_type", dic["obj_type"]);
 this.chart.setAttribute("type", dic["element_name"]);
 if("width" in dic["properties"]){var width_=dic["properties"]["width"]} else {var width_="400"}
 if("height" in dic["properties"]){var height_=dic["properties"]["height"]} else {var height_="400"}
 var style_="position:absolute;left:"+dic["properties"]["x"]+"px;top:"+dic["properties"]["y"]+"px;width:"+width_+"px;"
 style_+="height:"+height_+"px";
 this.chart.setAttribute("style", style_);
 this.chart.my_creator_obj=this;

 container.appendChild(this.chart);

   var chart_type={"type":"pies", "title":"abcde", "x":{"data":[]},"series":{
                    "y1":{"data":[], "color":[219, 64, 82], "name":"import"},
                    "y2":{"data":[], "color":[55, 128, 191], "name":"export"},
                    "y3":{"data":[], "color":[5, 12, 491], "name":"other"}}}
  //alert(JSON.stringify(chart_type));

   for(var i=0; i<3;i++)
   {
     chart_type["x"]["data"].push(i)
     chart_type["series"]["y1"]["data"].push(i+Math.random())
     chart_type["series"]["y2"]["data"].push(i*2+Math.random())
     chart_type["series"]["y3"]["data"].push(i*3+Math.random())
   }
  //alert(JSON.stringify(chart_type));
 this.set_chart_data(chart_type);
}

acChartCreator.prototype.set_chart_data = function(chart_type)
{
  //alert(JSON.stringify(chart_type));
  var data_=[]
  chart_attributes={"lines":{"type_name":"mode", "type_value":"lines+markers", "marker_attribute":"size", "marker_attribute_value":"8"},
                    "bars":{"type_name":"type", "type_value":"bar", "marker_attribute":"opacity", "marker_attribute_value":"0.7"},
                    "pies":{"type_name":"type", "type_value":"pie", "marker_attribute":"opacity", "marker_attribute_value":"0.7"}
                   }
  //alert(JSON.stringify(chart_attributes));

   data={"type":chart_type["type"],
         "type_name":chart_attributes[chart_type["type"]]["type_name"],
         "type_name_value":chart_attributes[chart_type["type"]]["type_value"],
         "title":chart_type["title"],
         "x":{"data":chart_type["x"]},
         "series": chart_type["series"]
        }

   //alert(JSON.stringify(data));

 if(chart_type["type"]=='pies')
 {
  var n_=0;
  section=1/(Object.keys(data["series"]).length+1.5)
  var k_=section*1.25;
  var annotations_=[]
  for(y in data["series"]){
    var trace = {}
    trace["values"]=data["series"][y]["data"];
    trace["labels"]=data["x"]["data"];
    trace["txt"]=data["series"][y]["name"];
    trace["textposition"]='inside';
    trace["domain"]={column: n_};n_+=1;
    trace["name"]=data["series"][y]["name"];
    trace["hoverinfo"]='lable';
    trace["hole"]=.4;
    trace[data["type_name"]]=data["type_name_value"];
    data_.push(trace)
    annotations_.push({font: {size: 20}, showarrow: false, text: data["series"][y]["name"], x: k_, y: 0.5});k_+=section;
  };
  var layout = {"title": data["title"],
                "annotations": annotations_,
                "height": 400, "width": 600, "showlegend": false,
                "grid": {rows: 1, columns: n_}
               }
 } else {
  for(y in data["series"]){
    var trace = {}
    trace["x"]=data["x"]["data"];
    trace["y"]=data["series"][y]["data"];
    trace[data["type_name"]]=data["type_name_value"];
    trace["marker"]={"color":"rgb("+data["series"][y]["color"][0]+", "+data["series"][y]["color"][1]+", "+data["series"][y]["color"][2]+")"}
    trace["marker"][data["marker_attribute"]]=data["marker_attribute_value"]
    trace["name"]=data["series"][y]["name"]
    trace["line"]={color: 'rgb('+data["series"][y]["color"][0]+', '+data["series"][y]["color"][1]+', '+data["series"][y]["color"][2]+')', width: 1}
    data_.push(trace)
  }
  var layout = {title: data["title"]}
 }
 //alert(JSON.stringify(data_));
 Plotly.newPlot(this.chart, data_, layout );
}

acChartCreator.prototype.get_data = function()
{
  //alert("get Data")
}


// -- TabContent --
function TabContent(tab, container, link_dic, is_on_click=true, is_link=null){
 //alert("TabContent");
 //alert(JSON.stringify(link_dic));
 //alert(tab.tab_name)
 this.is_link=is_link;
 this.tab=tab;
 this.link_dic=link_dic;
 this.link_number=link_dic["properties"]["link_number"];
 this.content_type=link_dic["properties"]["content_type"];
 //-
 this.link_content=document.createElement("div");
 this.link_content.my_creator_obj=this
 this.link_content.setAttribute("id", "content_"+this.link_number);
 this.link_content.setAttribute("table", link_dic["properties"]["table"]);
 this.link_content.setAttribute("record_id", "new");
 this.link_content.setAttribute("parent_id", "new");
 this.link_content.setAttribute("link_number", this.link_number);
 //this.link_content.innerHTML=this.link_number;
 this.link_content.setAttribute("type", "container");
 //this.link_content.setAttribute("obj_type", "container");
 this.link_content.setAttribute("class", "tabcontent");
 this.link_content.tab=tab;
 this.link_content.tab_content_id=this.link_number;
 if(is_link){var width=100} else {var width=link_dic["properties"]["width"];}
 this.link_content.setAttribute("style", "position: relative;background-color:white;width: "+width+"%;height:1000px;");
// border: 1px solid #ccc;

 if(is_on_click){
    //this.link_content.innerHTML=this.link_number;
    this.link_content.onclick=function(event){
      //alert(event.target.outerHTML)
      this.tab.parent.active_tab_content=this;
      var e=event.target;
      //alert(e.outerHTML)

      if(this.tab.new_obj_to_create==null){
         var click_event=new Event("click", {bubbles: true});
         if(event.ctrlKey){
           var obj_type=e.getAttribute("obj_type");
           try{while(obj_type==null){e=e.parentNode;var obj_type=e.getAttribute("obj_type");}} catch(er){}
            if(obj_type==null){
              this.tab.parent.editor.main_menus["TabContent"].btn.dispatchEvent(click_event);
              this.tab.parent.editor.main_menus["TabContent"].my_sub_objs["content"].btn.dispatchEvent(click_event)
            }
            else{
             var obj_number=e.getAttribute("id")
             var container_id=e.getAttribute("container_id")
             var click_event=new Event("click", {bubbles: true});
             var dic__=this.tab.tab_objects[container_id][obj_number];
             this.tab.parent.editor.main_menus[dic__["parent_obj_name"]].btn.dispatchEvent(click_event);
             var s='this.tab.active_obj=this.tab.parent.get_obj(this.tab,dic__);'
             //alert(s)
             eval(s)
             this.tab.active_obj.create_editor();
             }
         } else {
               var s=f+this.link_number+'='+link_dic["functions"]["onclick"]
               //alert(s);
               eval(s);
               eval(f+this.link_number+'(event)');
         }
      } else {
         //alert(JSON.stringify(this.tab.new_obj_to_create));
        var dic=this.tab.new_obj_to_create;
        var x=event.clientX-e.offsetLeft;
        //alert(event.clientX); //alert(e.offsetLeft); //alert(x)
        //alert(event.clientX); //alert(event.pageX); //-e.offsetLeft;
        if(e.parentNode.parentNode.offsetTop*1==0){var y=event.clientY-e.offsetTop;}
        else{var y=event.clientY-e.parentNode.parentNode.offsetTop;}
        // alert('event.clientY'); // alert(event.clientY);// alert('e.offsetTop');
        //alert(e.offsetTop);//alert('e.parentNode.parentNode.offsetTop')
        //alert(e.parentNode.parentNode.offsetTop); //alert('y');//alert(y)

        var obj_number=this.tab.get_next_obj_number();
        var container_id=e.getAttribute("link_number");

        dic["properties"]["obj_number"]=obj_number;dic["container_id"]=container_id;
        dic["properties"]["x"]=x;dic["properties"]["y"]=y;

        //alert(JSON.stringify(dic));

        this.tab.active_obj=this.tab.generate_obj(dic=dic);
        this.tab.active_obj.create_editor();
        //alert(JSON.stringify(this.tab.tab_objects));
        //alert(container_id)
        //alert(obj_number)
        this.tab.tab_objects[container_id][obj_number]=this.tab.active_obj.data;
        this.tab.parent.save();
      }
    }
 }
 this.link_content.onchange=function (event){
  //alert(JSON.stringify(this.my_creator_obj.link_dic))
  var e=event.target;
  //alert(e.outerHTML)
  var field_=e.getAttribute("field");
  var model_=this.my_creator_obj.link_dic["properties"]["table"];
  try{var parent_model_=this.my_creator_obj.link_dic["properties"]["parent_table"]} catch(er){};
  if(parent_model_==null){var parent_model_="";}
  var record_id_=this.getAttribute("record_id");
  var parent_id_=this.getAttribute("parent_id");
  var type_=e.getAttribute("type");
  if(field_=="" || field_==null){return}
  var dic_data={"model":model_, "parent_model":parent_model_, "field":field_, "pkey":record_id_, "parent_pkey":parent_id_,
                "value":e.value, "type":type_}
  //alert(JSON.stringify(dic_data))
  //alert(this.outerHTML)
  this.tab.parent.active_tab_content=this;
  this.tab.parent.save_data(this, dic_data)
 }
 container.appendChild(this.link_content);
 this.process_content();
}

TabContent.prototype.process_content = function()
{
  //alert("process_content")
  //alert(JSON.stringify(this.tab.tab_objects[this.link_number]));
  //alert(JSON.stringify(this.link_dic["functions"]));

  for(f in this.link_dic["functions"])
  {
    if(f!="onclick"){var s='this.link_content.'+f+'='+this.link_dic["functions"][f];eval(s);}
  }

  //alert(this.tab.tab_name)
  for (i in this.tab.tab_objects[this.link_number])
  {
   dic_=this.tab.tab_objects[this.link_number][i];
   //alert(JSON.stringify(dic_));
   this.tab.generate_obj(dic=dic_);
  }
}

TabContent.prototype.set_objects_data = function(dic)
{
 // alert(JSON.stringify(dic))
 this.link_content.setAttribute("record_id", dic["id"]);var container_dic=this.tab.tab_objects[this.link_number];
 for(o in container_dic)
 {
   if(container_dic[o]["obj_type"]=="acObj" && container_dic[o]["obj_name"]=="acInput"){
     var eI=document.getElementById(o);var v=dic[container_dic[o]["properties"]["field"]];eI.value=v;
   }
 }
}

// -- TabNavLink --
function TabNavLink(tab_nav, link_dic){
 //alert(JSON.stringify(link_dic))
 this.tab_nav=tab_nav;
 this.tab=tab_nav.tab;
 this.nav=tab_nav.nav;
 this.link_number=link_dic["nav_link"]["properties"]["link_number"];
 this.nav.links[this.link_number]=this;
 this.link=link_dic["nav_link"]["properties"]["link"];
 this.title=link_dic["nav_link"]["properties"]["title"];
 this.link_btn=document.createElement("button");
 this.link_btn.innerHTML=this.title;
 this.link_btn.setAttribute("class","nav_button nav_button"+this.tab.tab_name);
 this.link_btn.setAttribute("id","link_btn_"+this.link_number);
 this.link_btn.setAttribute("obj_type","tab_nav_link");
 this.link_btn.setAttribute("link_number",this.link_number);
 this.link_btn.setAttribute("tab_name",this.tab.tab_name);
 this.link_btn.parent=this;
 this.nav_link_functions=link_dic["nav_link"]["functions"];
 this.tab_content=link_dic["nav_link"]["tab_content"]

 this.link_btn.onclick=function(event){
  //alert(JSON.stringify(this.parent.nav_link_functions))
   try{var f=this.parent.nav_link_functions["onclick"];
     //alert("onclick"+this.parent.link_number+"="+f)
     eval("onclick"+this.parent.link_number+"="+f)
     //alert("onclick"+this.parent.link_number+"(event)")
     eval("onclick"+this.parent.link_number+"(event)")
   } catch(er){}
   var e=event.target;
   var tab_name=e.getAttribute("tab_name");
   e.parent.nav.active_link=this.parent;
   if(event.ctrlKey){
      this.parent.tab.parent.editor.active_link=this.parent;
      this.parent.tab.parent.editor.main_menus["TabNavLink"].btn.click();
      this.parent.tab.parent.editor.sub_menus["TabNavLinkitem"].btn.click();
   }
   var tabcontent=document.getElementsByClassName("tabcontent"+tab_name+"_content");
   for(i=0;i<tabcontent.length;i++){tabcontent[i].style.display='none';}
   var btns=document.getElementsByClassName("nav_button"+tab_name);
   for(i=0;i<btns.length;i++){btns[i].className=btns[i].className.replace(" active","")}
   try{e.parent.link_content.style.display="block";this.parent.link_btn.className+=" active";}catch(er){alert(er)}
 }
 for(f in this.nav_link_functions)
 {if(f != "onclick"){var fun=this.nav_link_functions[f]; eval("this.link_btn."+f+"="+fun)}}
 this.nav.appendChild(this.link_btn);
 this.nav.links[this.link_number]=this;
 //this.tab_nav
 //.nav_one_tab_content=
 if(this.tab.tab_nav_links["properties"]["nav_type"]=="navmulti"){
   this.content=new TabContent(this.tab, tab_nav.nav_content, link_dic["tab_content"], is_on_click=true, is_link=true);
 } else if (this.tab.tab_nav_links["properties"]["nav_type"]=="navone")
 {
   if(this.tab_nav.nav_one_tab_content == null)
   {
    this.tab_nav.nav_one_tab_content=new TabContent(this.tab, tab_nav.nav_content, link_dic["tab_content"], is_on_click=true, is_link=true);
   }
   this.content=this.tab_nav.nav_one_tab_content;
 }
//alert(994)
 this.link_content=this.content.link_content;
 this.link_content.className+=this.tab.tab_name+"_content";
}


// -- TabNav --
function TabNav(tab_=null){

  //alert(JSON.stringify(tab_.tab_nav_links));

  this.tab=tab_;
  this.nav=null;
  this.active_link=null;
  this.nav_one_tab_content=null;
  this.properties=this.tab.tab_nav_links["properties"];
  this.is_show_btns=this.properties["is_show_btns"];
  this.nav_width=this.properties["width"];
  this.add_title=this.properties["add_title"];
  this.remove_title=this.properties["remove_title"];
  this.create_main_tab_nav_content();
  this.process_data();
}

TabNav.prototype.create_main_tab_nav_content = function()
{
   this.nav_container=document.createElement("div");
   this.nav_container.setAttribute("my_name", "TabNav.nav_container_"+this.properties["obj_number"]);
   this.nav_container.setAttribute("id", this.properties["obj_number"]);
   this.nav_container.setAttribute("style", "float:left;border:1px solid #ccc;background-color: "+this.properties["background_color"]+";width:"+this.nav_width+"%;");
   // --
   this.nav = document.createElement("div");
   for(f in this.tab.tab_nav_links["functions"])
   {
     eval(f+"_zz="+this.tab.tab_nav_links["functions"][f]);
     eval('this.nav.'+f+'='+f+'_zz');
   }
   this.nav.links={};
   //--
   if(this.is_show_btns=="true")
   {
     this.nav_container_buttons=document.createElement("div");
     this.nav_btn_add=document.createElement("button");
     this.nav_container.appendChild(this.nav_container_buttons)
     this.nav_container_buttons.appendChild(this.nav_btn_add)
     this.nav_btn_add.parent=this;
     this.nav_btn_add.innerHTML=this.add_title;

     this.nav_btn_add.onclick=function(event){
         //-
         var link_ = prompt("Enter name for new link:",'');if(link_==''){alert("Please enter a link name");return}
         var link_number=this.parent.tab.get_next_obj_number();
         var width_=100-this.parent.nav_width;

         var link_dic={"nav_link":{"properties":{"link_number":link_number, "link":link_, "title":link_},
                                   "functions":{}},
                       "tab_content":{"properties":{"link_number":link_number, "content_type": "simple", "width":width_,
                                                    "table":""},
                                      "functions":{}}
                       };

         this.parent.tab.tab_objects[link_number]={};this.parent.tab.tab_nav_links["nav_links"][link_number]=link_dic;
         //--
         var tab_nav_links = new TabNavLink(this.parent, link_dic);
         //--
         tab_nav_links.link_btn.click();
         this.parent.tab.parent.save();
         this.parent.nav_content.appendChild(tab_nav_links.link_content);
         this.parent.nav.appendChild(tab_nav_links.link_btn);
         this.parent.nav.links[link_number]=tab_nav_links;
         tab_nav_links.link_btn.click();
         //alert(JSON.stringify(this.parent.tab.tab_nav_links))
         this.parent.tab.parent.save();
     }
     this.nav_btn_remove=document.createElement("button");
     this.nav_container_buttons.appendChild(this.nav_btn_remove)
     this.nav_btn_remove.parent=this;
     this.nav_btn_remove.innerHTML=this.remove_title;
     this.nav_btn_remove.onclick=function(event){
         //-
         var e=event.target;
         //alert(e.outerHTML)
         //alert(this.parent.nav.active_link)
         var link_= this.parent.nav.active_link.link_btn.innerHTML;
         var link_number= this.parent.nav.active_link.link_btn.getAttribute("link_number")
         var link_ = prompt("Are you sure you want to remove link "+link_+"? if so type Yes:",'No');
         if(link_=='Yes')
         {
          delete this.parent.tab.tab_nav_links["nav_links"][link_number];
          this.parent.nav.active_link.link_btn.outerHTML="";
          this.parent.nav.active_link.link_content.outerHTML="";
          delete this.parent.nav.links[link_number];
          this.parent.tab.parent.save();
         }
     }
   }
   this.nav_container.appendChild(this.nav)
   this.tab.content.appendChild(this.nav_container)
   this.nav_content = document.createElement("div");
   this.nav_content.setAttribute("my_name", "TabNav.nav_content");
   var width_=100-this.nav_width;
   this.nav_content.setAttribute("style","float:left;background-color:#f1f1f1;width:"+width_+"%;height:100%;");
   // border:1px solid #ccc;
   this.tab.content.appendChild(this.nav_content)
   this.nav.setAttribute("style","float:left;background-color:#f1f1f1;width:100%;");
   // border:1px solid #ccc;
}

TabNav.prototype.process_data = function()
{
 var n1_obj=null;
 for (n_ in this.tab.tab_nav_links["nav_links"])
 {
  var link_dic=this.tab.tab_nav_links["nav_links"][n_];
//--
  var nav_link_obj=new TabNavLink(this, link_dic);
//--
  if(n1_obj==null){n1_obj=nav_link_obj.link_btn}
 }
 try{n1_obj.click();} catch(er){}
}


// Tab obj ---
function Tab(parent, data, id)
{
 //alert("Tab");
 //alert(JSON.stringify(data));

 this.parent=parent; this.tab_id=id;
 this.btn=null;this.content=null;this.PopWinObjects={};
 this.tab_properties=data["properties"];

 if(this.tab_properties["tab_type"].includes("nav")) {this.is_on_click=false;} else {this.is_on_click=true;}

 this.link_number=data["properties"]["link_number"];
 this.tab_name=data["properties"]["tab_name"];
 this.tab_title=data["properties"]["tab_title"];
 this.tab_type=data["properties"]["tab_type"];
 //--
 if(!("functions" in data)){this.tab_functions={};
   this.tab_functions[this.tab_name+"__init__"]=this.tab_name+"__init__=function(called_tab, calling_tab){\ntry{\n\n} catch(er){alert(er)}}";
   this.tab_functions[this.tab_name+"__myclick__"]=this.tab_name+"__myclick__=function(called_tab, calling_tab){\ntry{\n\n} catch(er){alert(er)}}";
   this.tab_functions[this.tab_name+"__otherclick__"]=this.tab_name+"__otherclick__=function(called_tab, calling_tab){\ntry{\n\n} catch(er){alert(er)}}";
 } else {this.tab_functions=data["functions"]};
 //--
 if(!("tab_pop_win_buttons" in data)){this.tab_pop_win_buttons={"properties":{},"pop_wins":{}}} else
 {this.tab_pop_win_buttons=data["tab_pop_win_buttons"]}
 //--
 if(!("tab_content_link_dic" in data))
 {this.tab_content_link_dic={"properties":{"link_number":this.link_number, "content_type": "simple", "width":100,
                             "table":"", "parent_table":""}, "functions":{}, }}
 else {this.tab_content_link_dic=data["tab_content_link_dic"]}
 //--
 if(!("objects" in data)) {this.tab_objects={};this.tab_objects[this.link_number]={};} else {this.tab_objects=data["objects"]};
 this.tab_objects_created={}
 //alert(JSON.stringify(this.tab_objects));
 this.create_btn_container(data);
 //alert(JSON.stringify(this.tab_objects))
 this.process_functions();
 this.init_tab();
 //this.process_content();
 this.new_obj_to_create = null;
 this.active_obj=null;
 this.is_int_objects_data=false;
}

Tab.prototype.int_objects_data = function()
{
 if(this.is_int_objects_data==true){return};
 for(var z in this.tab_objects_created){try{var o = this.tab_objects_created[z];o.creator.get_data();} catch(er){}}
 this.is_int_objects_data=true;
}

Tab.prototype.create_btn_container = function(data)
{
  this.btn=document.createElement("button");
  this.btn.setAttribute("link_number", this.link_number);
  this.btn.parent=this;
  this.btn.setAttribute("class", "tablinks");
  this.btn.className+=" active";
  this.btn.innerHTML=this.tab_title;
  this.btn.onclick=function(event)
  {
    try{var btn=event.target;btn.parent.parent.set_active_tab(btn);this.parent.int_objects_data();} catch(er) {alert("Error 22: "+er)}
  }
  this.parent.titles.appendChild(this.btn)
  //--
  //if(this.tab_properties["tab_type"].includes("nav")) {var is_on_click=false;} else {var is_on_click=true;}
  this.tab_content=new TabContent(tab=this, container=this.parent.container, link_dic=this.tab_content_link_dic, is_on_click=this.is_on_click, is_link=false);
  this.content=this.tab_content.link_content;
  this.content.parent=this;
  if(this.tab_properties["tab_type"].includes("nav"))
  {
    // alert(JSON.stringify(data));
    // alert(JSON.stringify(data["nav_links"]));
     if(!("nav_links" in data) || data["nav_links"]=="null")
     {
       var n_=this.get_next_obj_number();
       this.tab_nav_links={"properties":{"obj_number":n_, "nav_type":this.tab_properties["tab_type"],"width":"10",
                                         "add_title":"Add", "remove_title":"Remove",
                                         "is_show_btns":"true", "background_color": "#f1f1f1"},
                           "functions":{},
                           "nav_links":{}};
     } else {this.tab_nav_links=data["nav_links"]};
     this.tab_nav=new TabNav(tab=this);
  }
}

Tab.prototype.create_tab_pop_wins = function(){
try{
   for(i in this.tab_pop_win_buttons["pop_wins"]){
       var dic_=this.tab_pop_win_buttons["pop_wins"][i]
       //var obj_=this.get_pop_win_obj(dic_); var win_obj=new obj_(parent=this); win_obj.__init__();
       var win_obj=this.get_pop_win_obj(dic_); win_obj.__init__();
       win_obj.set_win_frame_style(dic_["properties"]["zindex"], dic_["properties"]["height"], dic_["properties"]["width"], dic_["properties"]["right"], dic_["properties"]["top"], dic_["properties"]["background_color"])
       win_obj.set_acWinStatEventListeners(this.parent.editor);
     }
   } catch(er) {alert(er)}
}

Tab.prototype.process_functions = function(){for(f in this.tab_functions){eval(this.tab_functions[f])}}

Tab.prototype.init_tab=function(){try{eval(this.tab_name+"__init__(obj=this)");} catch(er) {}}

Tab.prototype.get_next_obj_number=function(){return this.parent.get_next_obj_number();}

Tab.prototype.set_to_create_obj=function(dic){
 //alert("set_to_create_obj")
 //alert(JSON.stringify(dic));
 this.new_obj_to_create = dic;
}

Tab.prototype.generate_obj=function(dic=null){
 //alert("generate_obj")
 //alert(JSON.stringify(dic));
 var s='var obj = this.parent.get_obj(this, dic);'
 //alert(s)
 try{eval(s)} catch(er){alert("er200: "+er)}
 this.tab_objects_created[dic["properties"]["obj_number"]]=obj;
 obj.create_obj();
 // obj.create_editor();
 //alert(JSON.stringify(obj.data));
 this.new_obj_to_create = null;
 return obj;
}

Tab.prototype.set_max_zindex = function(win) {
    var nmax = 0;
    try{
     //alert(win.outerHTML)
     var win_number=win.getAttribute("win_number")
     if(win_number!=null){
      var tab_id=win.getAttribute("tab_id")
      var win_name=win.getAttribute("my_name");
      //alert(this.parent.tabs[tab_id].PopWinObjects[win_name].my_name);
      for (i in this.parent.tabs[tab_id].PopWinObjects)
      {if(this.parent.tabs[tab_id].PopWinObjects[i].win_frame.style.zIndex > nmax)
       {nmax=this.parent.tabs[tab_id].PopWinObjects[i].win_frame.style.zIndex}}
      win.style.zIndex = 1*nmax+1;
      this.parent.tabs[tab_id].PopWinObjects[win_name].create_editor_for_popwin(this.parent.tabs[tab_id].tab_pop_win_buttons["pop_wins"][win_number]);
      this.parent.editor.active_popup_win=[tab_id, win_name, win_number]
     }
    } catch(er){}
}

Tab.prototype.get_pop_win_obj = function(dic)
{
 // alert(JSON.stringify(dic))
 var s_name=dic["properties"]["name"]; var s_title=dic["properties"]["title"];
 var title_color=dic["properties"]["title_color"];var title_background_color=dic["properties"]["title_background_color"]
 var s = 'function TabPopWin'+this.tab_name+s_name+'(parent)';
 s+='{'
 s+='this.my_name="'+this.tab_name+s_name+'";';
 s+='this.name="win_'+this.tab_name+s_name+'";';
 s+='var is_scroll_=true;';
 s+='acWin.call(this,my_name_=this.my_name, win_name=this.name, win_title="'+s_title+'",';
 s+='right= "2%", top="30%",'
 s+='is_scroll=is_scroll_, zindex="21", tab_obj_=parent, is_nav_panel=true, win_number='+dic["properties"]["id"]+');'
 s+='};';
 //alert(s);
 eval(s);
 s = 'TabPopWin'+this.tab_name+s_name+'.prototype = Object.create(acWin.prototype);';
 eval(s);
 s = 'TabPopWin'+this.tab_name+s_name+'.prototype.constructor = TabPopWin'+this.tab_name+s_name;
 eval(s);

 s='TabPopWin'+this.tab_name+s_name+'.prototype.create_editor_for_popwin = function(dic)'
 s+='{'
 //s+='alert(this.tab_obj_.parent);'
 //s+='alert(this.tab_obj_.parent.editor);'

 //s+='alert(JSON.stringify(dic));'
 s+='var tab_=this.tab_obj_.parent.tabs[dic["properties"]["tab_id"]];';
 s+='var pop_win=tab_.PopWinObjects[dic["properties"]["name"]];'
 s+='var pop_win_dic_=tab_.tab_pop_win_buttons["pop_wins"][dic["properties"]["id"]];'
 //s+='alert(JSON.stringify(pop_win_dic_));'
 //s+='this.fpe=new FunctionsPropertiesEditor(tab_,pop_win_dic_["functions"],pop_win_dic_["functions"],pop_win_dic_["properties"],pop_win_dic_["properties"]);'
 s+='var pop_win_content=tab_.parent.pop_win;'
 s+='this.fpe=this.tab_obj_.parent.editor.get_functions_properties_editor(tab_,pop_win_dic_["functions"],'
 s+='pop_win_content["functions_list"],'
 s+='pop_win_dic_["properties"],'
 s+='pop_win_content["settings_list"],'
 s+='pop_win_content["attributes_list"],'
 s+='tab_btn_name="PopWin",null,node_to_delete=".tab_pop_win_buttons[\'pop_wins\']["+dic[\'properties\'][\'id\']+"]");'
 s+='}'
 //alert(s);
 eval(s);
 //--
 s='TabPopWin'+this.tab_name+s_name+'.prototype.get_my_tab = function()'
 s+='{'
 s+='return this.tab_obj_.parent.tabs['+dic["properties"]["tab_id"]+'];';
 s+='}'
 //alert(s);
 eval(s);
 //--
 for(f in dic['functions']) {s_= 'var '+f+"_"+dic["properties"]["id"]+ '='+dic['functions'][f];   eval(s_);}
 //--
 s='TabPopWin'+this.tab_name+s_name+'.prototype.__init__ = function()'
 s+='{this.set_tab(this.tab_obj_);this.set_title_colors("'+title_color+'", "'+title_background_color+'");'
 s+='this.tab_obj_.PopWinObjects[this.my_name]=this;'
 s+='this.id='+dic["properties"]["id"]+';'
 s+='this.tab_obj_.tab_pop_win_buttons["pop_wins"]['+dic["properties"]["id"]+']='+JSON.stringify(dic)+';'
 s+='this.set_title(this.win_title_);'
 s+='__init___'+dic["properties"]["id"]+'(this);';
 if(dic["properties"]["is_panel"]=="true"){s+='__set_panel___'+dic["properties"]["id"]+'(this)';}
 s+='}'
 //alert(s);
 eval(s);

//  this.set_panel();
//  this.main_menus["Tab"].btn.click()

 //alert(eval('TabPopWin'+this.active_tab.tab_name+s_name+'.prototype.set_title_colors'))
 s='new TabPopWin'+this.tab_name+s_name+'(this.parent.tabs[dic["properties"]["tab_id"]])';
 //alert(s);
 return eval(s);
}


// -- acWin popup window --
function acWin(my_name_="none", win_name="none", win_title="none", right= "0%", top="0%", is_scroll=true, zindex="11", tab_obj_=null, is_nav_panel=false, win_number=0)
{
//alert(7)
//alert(tab_obj_.tab_name)
//alert(win_name)
//alert(my_name_)
  // create its div for window
  this.win_number=win_number;
  this.tab_obj_=tab_obj_;
  this.is_nav_panel = is_nav_panel;
  this.nav_height = 0;
  this.is_scroll = is_scroll
  this.win_name = win_name
  this.my_name_ = my_name_;
  this.win_title_ = win_title;
  this.win_frame = document.createElement("div");
  this.win_frame.setAttribute("win_number", this.win_number);
  this.win_frame.setAttribute("tab_id", this.tab_obj_.tab_id);
  this.win_frame.setAttribute("id", "win_frame_"+this.win_name);
  this.win_frame.setAttribute("my_name", my_name_);
  // TITLE for window
  this.title_height = 25
  this.win_frame_title = document.createElement("div");
  this.win_frame_title.setAttribute("id", "win_frame_title_"+this.win_name);
  // --
  this.win_frame_ico = document.createElement("img");
  this.win_frame_ico.setAttribute("id", "win_frame_ico_"+this.win_name);
  this.win_frame_ico.setAttribute("src", "/static/core/globs.jpg");
  this.win_frame_ico.setAttribute("style", "border-radius: 10px;position: absolute;left: 45px");
  this.win_frame_ico.setAttribute("height", "20");
  this.win_frame_ico.setAttribute("width", "20");
  // --

  this.win_frame_title.appendChild(this.win_frame_ico)
  this.win_frame_title_span = document.createElement("span");
  this.win_frame_title_span.innerHTML = win_title
  this.win_frame_title.appendChild(this.win_frame_title_span)
  this.win_frame_msg_span = document.createElement("span");
  this.win_frame_title.appendChild(this.win_frame_msg_span);
  this.win_frame.appendChild(this.win_frame_title)
  // NAV PANEL --
  if(this.is_nav_panel==true)
  {
   this.nav_height = 25;
   this.win_nav_panel = document.createElement("div");
   this.win_nav_panel.setAttribute("id", "win_nav_panel_"+this.win_name);
   var nav_panel_background_color = "lightgray";
   this.style_nav_panel = "background-color: "+nav_panel_background_color+";"
   this.style_nav_panel += "width:100%;font-size:12pt;"
   this.style_nav_panel += "border:2px solid #0094ff;"
   this.win_nav_panel.setAttribute("style", this.style_nav_panel);
   this.win_frame.appendChild(this.win_nav_panel)
  }
  // CONTENT --
  this.win_content = document.createElement("div");
  this.win_content.setAttribute("id", "win_content_"+this.win_name);
  // -- call it from outside --
  //this.set_win_frame_style(zindex, height="300px", width="300px", right, top, "white");
  //--
  this.win_frame.appendChild(this.win_content)
  //-- Little div TO CLOSE and OPEN the WIN --
  this.win_nav = document.createElement("div");
  this.win_nav.setAttribute("id", "win_nav_"+this.win_name);
  this.style_win_nav = "position:fixed;text-align:center;width:10px;display:none; right:"+right+";top:"+top+";";
  this.win_nav.setAttribute("style", this.style_win_nav)
  // --
  this.win_nav_ico = document.createElement("img");
  this.win_nav_ico.setAttribute("id", "win_nav_ico_"+this.win_name);
  this.win_nav_ico.setAttribute("src", "/static/core/globs.jpg");
  this.win_nav_ico.setAttribute("style", "border-radius: 10px;position: absolute;right:97%");
  //--
  this.win_nav_ico.setAttribute("height", "5");
  this.win_nav_ico.setAttribute("width", "5");
  //
  this.win_nav.appendChild(this.win_nav_ico)
  // --
  this.span = document.createElement("span");
  this.span.setAttribute("id", "span_"+this.win_name);
  //this.span.innerHTML = "&nbsp;Whiteboard"
  this.span.setAttribute("style", "position: absolute;left: 50");
  this.win_nav.appendChild(this.span)
  // --
  this.body_ = tab_obj_.parent.elm_body;
  this.body_.appendChild(this.win_frame);
  this.body_.appendChild(this.win_nav);
  // --
  this.win_frame_title.setAttribute('pos1', 0);
  this.win_frame_title.setAttribute('pos2', 0);
  this.win_frame_title.setAttribute('pos3', 0);
  this.win_frame_title.setAttribute('pos4', 0);
  this.win_frame.style.display = "none"
  this.win_frame_style_display = this.win_frame.style.display;
}

acWin.prototype.set_tab = function(tab_obj){this.tab_obj_=tab_obj;}

acWin.prototype.set_title_colors = function(color, b_color)
{
  this.style_title = "text-align:center;display:block;padding:4px;color:"+color+";margin:-1 0 0 0;height:"+this.title_height+"px;z-index:11;"
  this.style_title += "background-color:"+b_color+";cursor:move;font-size:12pt;border-top-left-radius:35px;border-top-right-radius:35px;"
  this.win_frame_title.setAttribute("style", this.style_title);
}
acWin.prototype.set_win_frame_style = function(zindex, height, width, right, top, background_color)
{
  this.style_frame = "position: fixed; background-color: "+background_color+"; z-index: "+zindex+"; text-align: left;"
  this.style_frame += "height:"+height+"px;width:"+width+"px;font-size:12pt;"
  this.style_frame += "border:2px solid #0094ff;"
  this.style_frame += "border-top-left-radius:35px;border-top-right-radius:35px;"
  this.style_frame += "right:"+right+";top:"+top+";"
  this.win_frame.setAttribute("style", this.style_frame);
  this.style_content = "height:"+(height-this.title_height-7-this.nav_height)+"px;width:"+width+"px;"
  if(this.is_scroll==true){this.style_content += "overflow: scroll;"}
  this.win_content.setAttribute("style", this.style_content);
}
acWin.prototype.set_acWinStat = function(ss)
{
    //open and close acWin.
    if (ss != this.win_frame.style.display)
    {
    try{
      var event_close_ac = new Event("click", {bubbles: true});
      this.win_frame_ico.dispatchEvent(event_close_ac);
      this.win_frame_style_display = ss;
      } catch(er){alert("error 77")}
    }
    this.tab_obj_.set_max_zindex(this.win_frame);
}
acWin.prototype.close_win = function(){this.set_acWinStat('none');}
acWin.prototype.temp_close_win = function(){this.win_frame.style.display = "none";}
acWin.prototype.resume_win = function(){this.win_frame.style.display = this.win_frame_style_display;}
acWin.prototype.set_title = function(title){this.win_frame_title_span.innerHTML=title;this.set_acWinStat('block');}
acWin.prototype.set_msg = function(msg){this.win_frame_msg_span.innerHTML=msg;this.set_acWinStat('block');}
acWin.prototype.get_msg = function(){return this.win_frame_msg_span.innerHTML;}
acWin.prototype.set_info = function(content){this.win_content.innerHTML=content;}
acWin.prototype.add_info = function(content){this.win_content.innerHTML+=content;}
// not used to be deleted.
//acWin.prototype.remove_win = function(){try{this.win_frame.outerHTML="";this.win_nav.outerHTML="";} catch (err) {alert(err);console.log("Error remove_win :", "remove_win 0450");}}
acWin.prototype.move_frame = function(pos1, pos2, pos3, pos4)
{
  // console.log("acWin.prototype.move_frame: ", pos1, pos2, pos3, pos4)
  this.win_frame_title.setAttribute("pos3", pos3);
  this.win_frame_title.setAttribute("pos4", pos4);
  this.win_frame.style.top = (this.win_frame.offsetTop - pos2) + "px";
  this.win_frame.style.left = (this.win_frame.offsetLeft - pos1) + "px";
  this.win_nav.style.top = this.win_frame.style.top;
}
acWin.prototype.set_acWinStatEventListeners = function(ss_obj)
{
  //console.log("set_acWinStatEventListeners :", "Check 0000");
  eval("var " +  ss_obj.my_name + '= ss_obj')

  //alert("var " +  ss_obj.my_name + '= ss_obj');
  var s = ''
  s += 'this.win_frame_ico.addEventListener("click", function(){'
  s += '  event.preventDefault();'
  s += 'var my_name = x_'+this.win_name+'.getAttribute("my_name");'
  s += '  if (x_'+this.win_name+'.style.display === "none") {'
  s += '    x_'+this.win_name+'.style.display = "block";'
  s += '    n_'+this.win_name+'.style.display = "none";'
  s += '  } else {'
  s += '    x_'+this.win_name+'.style.display = "none";'
  s += '    n_'+this.win_name+'.style.display = "block";'
  s += '  };'
  s += '}.bind(elm = this.win_frame_ico, event, x_'+this.win_name+' = this.win_frame, n_'+this.win_name+' = this.win_nav));'

  try{
   eval(s)
   //console.log("Good :set_acWinStatEventListeners: ", "eval 100")
   } catch (err) {console.log("Error 101", err.message)}
  //console.log("set_acWinStatEventListeners :", "Check 0100");
  s = ''
  s += 'this.win_nav_ico.addEventListener("click", function(){'
  s += 'event.preventDefault();'
  s += 'var my_name = x_'+this.win_name+'.getAttribute("my_name");'
  s += 'if (x_'+this.win_name+'.style.display==="none") {'
  s += 'x_'+this.win_name+'.style.display="block";'
  s += 'n_'+this.win_name+'.style.display="none";'
  s += '} else {'
  s += 'x_'+this.win_name+'.style.display="none";'
  s += 'n_'+this.win_name+'.style.display="block";'
  s += '}'
  s += '}.bind(this.win_nav_ico, event, x_'+this.win_name+' = this.win_frame, n_'+this.win_name+' = this.win_nav));'
  try{
   //console.log("eval 200:"+ss_obj, s)
   eval(s)
   //console.log("Good :set_acWinStatEventListeners: ", "eval 200")
   } catch (err) {console.log("Error 201", err.message)}
  //console.log("set_acWinStatEventListeners :", "Check 0200");
  s = ''
  s += 'this.win_frame_title.addEventListener("mousedown", function(){'
  //s += 'alert(this.outerHTML);'
  //s += 'elm_win_frame_title_'+this.win_name+'.setAttribute("pos3", event.clientX);'
  s += 'event.preventDefault();'
  s += 'elm_win_frame_title_'+this.win_name+'.setAttribute("pos3", event.clientX);'
  s += 'elm_win_frame_title_'+this.win_name+'.setAttribute("pos4", event.clientY);'

  s += 'document.addEventListener("mouseup", my_mouse_up_'+this.win_name+' = function(){'
  s += 'event.preventDefault();'
  s += 'try{'
  s += 'document.removeEventListener("mouseup", my_mouse_up_'+this.win_name+');'
  s += 'document.removeEventListener("mousemove", my_mouse_move_'+this.win_name+');'
  s += '} catch (err) {err.message}'

  //s += 'alert(elm_win_frame_' +this.win_name +'.outerHTML);'

  s += 'tab_obj__.set_max_zindex(elm_win_frame_' +this.win_name +');'
  s += '}.bind(elm_win_frame_title_'+this.win_name+', event, tab_obj__, elm_win_frame_' +this.win_name + '));'

  s += 'document.addEventListener("mousemove", my_mouse_move_'+this.win_name+' = function(){'
  s += 'event.preventDefault();'
        // calculate the new cursor position:
  s += 'pos3 = elm_win_frame_title_'+this.win_name+'.getAttribute("pos3");'
  s += 'pos4 = elm_win_frame_title_'+this.win_name+'.getAttribute("pos4");'
  s += 'pos1 = pos3 - event.clientX;'
  s += 'pos2 = pos4 - event.clientY;'
  s += 'pos3 = event.clientX;'
  s += 'pos4 = event.clientY;'
  s += 'var msg_ = "' + this.my_name_ + '" + ","+pos1+","+pos2+","+pos3+","+pos4;'
  s += 'elm_win_frame_title_'+this.win_name+'.setAttribute("pos3", pos3);'
  s += 'elm_win_frame_title_'+this.win_name+'.setAttribute("pos4", pos4);'
        // set the element's new position:
  s += 'elm_win_frame_'+this.win_name+'.style.top = (elm_win_frame_'+this.win_name+'.offsetTop - pos2) + "px";'
  s += 'elm_win_frame_'+this.win_name+'.style.left = (elm_win_frame_'+this.win_name+'.offsetLeft - pos1) + "px";'
  s += 'elm_win_nav_'+this.win_name+'.style.top = elm_win_frame_'+this.win_name+'.style.top;'
  s += 'elm_win_nav_'+this.win_name+'.style.right = elm_win_frame_'+this.win_name+'.style.right;'
  s += '}.bind(elm_win_frame_title_'+this.win_name+', event, elm_win_frame_'+this.win_name+', elm_win_nav_'+this.win_name+'));'
  s += '}.bind(elm_win_frame_title_'+this.win_name+' = this.win_frame_title, event, elm_win_frame_'+this.win_name
  s += ' = this.win_frame, elm_win_nav_'+this.win_name+' = this.win_nav, tab_obj__=this.tab_obj_));'

  try{
   //console.log("eval 300:", s)
   eval(s)
   //console.log("Good :set_acWinStatEventListeners: ", "eval 300")
   } catch (err) {alert("Error 300" + err.message)}
  //console.log("set_acWinStatEventListeners :", "Check 0300");
  try{
        var event_frame_ico = new Event("click", {bubbles: false});
        this.win_frame_ico.dispatchEvent(event_frame_ico);
    } catch (err) {alert("error 99");console.log("Error set_acWinStatEventListeners :", "Check 0350");}

  // console.log("set_acWinStatEventListeners :", "Check 0400");
}

acWin.prototype.get_main_button_obj = function(s_name, s_title, button, obj_type)
{
 var s = 'function MenuBtn'+s_name+'(parent)';
 s+='{MenuBtn.call(this,parent,my_name_=s_name, my_title=s_title, buttons=button, obj_type, width="width:10%;");';
 s+='parent.main_menus[this.my_name]=this;};';
 //alert(s);
 eval(s);
 s = 'MenuBtn'+s_name+'.prototype = Object.create(MenuBtn.prototype);';
 eval(s);
 s='MenuBtn'+s_name+'.prototype.create_main_content = '+s_name+'_create_main_content;';
 //alert(s);
 eval(s);
 s='MenuBtn'+s_name;
 return eval(s);
}


// -- Pop win --
function PopWin(my_name_, win_name_, win_title_, user_id, atm)
{
  this.atm = atm;
  this.active_popup_win=null;
  //alert(JSON.stringify(this.atm.buttons));
  this.buttons=this.atm.buttons;
  this.tab_nav_links=this.atm.tab_nav_links;
  //--
  this.my_name=my_name_;this.name="win_"+win_name_;
  this.user_id=user_id; var is_scroll_=true;
  this.main_menus = {};this.sub_menus = {};
  acWin.call(this,my_name_=my_name_,win_name=this.name,win_title=win_title_,right="2%",top="30%",is_scroll=is_scroll_,zindex=20,tab_obj_=atm.active_tab,is_nav_panel=true,win_number=0)
}
PopWin.prototype = Object.create(acWin.prototype)
PopWin.prototype.constructor = PopWin;

PopWin.prototype.__init__ = function()
{
  this.set_tab(this.atm.active_tab);
  this.set_title_colors("#fff", "#2196F3");
  //--
  this.set_title(this.win_title_+this.atm.active_tab.tab_name);
  this.atm.active_tab.PopWinObjects[this.my_name]=this;
  this.set_panel();
  this.main_menus["Tab"].btn.click()
}

PopWin.prototype.set_panel = function()
{
  this.main_menu = document.createElement("div");
  this.sub_menu = document.createElement("div");
  this.win_nav_panel.appendChild(this.main_menu);
  this.win_nav_panel.appendChild(this.sub_menu);
  //alert(JSON.stringify(this.buttons));
  for (b in this.buttons){
   //alert('MenuBtn'+b+'=this.get_main_button_obj(b, this.buttons[b]["title"],this.buttons[b]["sub_buttons"])')
   eval('MenuBtn'+b+'=this.get_main_button_obj(b, this.buttons[b]["title"], this.buttons[b]["sub_buttons"], this.buttons[b]["obj_type"])')
   eval('new MenuBtn'+b+'(parent=this)')
  }
}


PopWin.prototype.get_functions_properties_editor = function(tab_,functions_dic,functions_list_dic,dic_properties,settings_list,attributes_list,tab_btn_name="TabContent", properties_func, node_to_delete)
{
  return new FunctionsPropertiesEditor(tab_,functions_dic=functions_dic,functions_list_dic,dic_properties,settings_list,attributes_list,tab_btn_name, properties_func, node_to_delete)
}


// -- MenuBtn --
function MenuBtn(parent, my_name_, my_title, buttons, obj_type, width="width:10%;")
{
 this.parent=parent;
 this.my_name=my_name_;
 this.my_title = my_title;
 this.buttons = buttons;
 this.my_sub_objs={}
 //alert(JSON.stringify(this.buttons));
 this.btn = document.createElement("button");
 this.btn.parent=this;
 this.btn.setAttribute("id", this.parent.my_name+"_"+this.my_name);
 this.btn.setAttribute("class", "main_menu_btn");
 this.btn.setAttribute("style", width);
 this.btn.innerHTML = this.my_title
 this.btn.onclick=function(event){
   try{this.parent.parent.win_content.innerHTML="";} catch(er){}
   this.parent.parent.sub_menu.innerHTML="";
   this.parent.parent.sub_menus = {};
   // need to remove the alert in the catch part.
   try{
         for(b in this.parent.buttons){
           //alert('SubMenuBtn'+this.parent.my_name+b+'=this.parent.get_sub_button_obj(b,this.parent.buttons[b]["title"],obj_type)');
           eval('SubMenuBtn'+this.parent.my_name+b+'=this.parent.get_sub_button_obj(b,this.parent.buttons[b]["title"],obj_type)');
           //alert('this.parent.my_sub_objs[b] = new SubMenuBtn'+this.parent.my_name+b+'(parent=this.parent)');
           eval('this.parent.my_sub_objs[b] = new SubMenuBtn'+this.parent.my_name+b+'(parent=this.parent)');
         }
   } catch(er){alert("er202: "+er)}
   try{
         for(m in this.parent.parent.main_menus)
         {this.parent.parent.main_menus[m].btn.className=this.parent.parent.main_menus[m].btn.className.replace(" active", "")}
         try{this.className+=" active";  } catch(er){}
   } catch(er){alert("er203: "+er)}
   try{this.parent.create_main_content();} catch(er){alert("er201: "+er)}
 }
 this.parent.main_menu.appendChild(this.btn);
}

MenuBtn.prototype.get_sub_button_obj = function(s_name, s_title, obj_type)
{
 var s='function SubMenuBtn'+this.my_name+s_name+'(parent)';
 s+='{';
 s+='var width_=parent.buttons["'+s_name+'"]["width"];';
 s+='SubMenuBtn.call(this,parent,my_name_="'+s_name+'",my_title_="'+s_title+'",width="width:"+width_+"%;");';
 s+='parent.parent.sub_menus[this.my_name]=this;};';
 eval(s);
 s = 'SubMenuBtn'+this.my_name+s_name+'.prototype = Object.create(SubMenuBtn.prototype);';
 eval(s);
 //s='SubMenuBtn'+this.my_name+s_name+'.prototype.click = '+this.my_name+s_name+'_click;'
 s='SubMenuBtn'+this.my_name+s_name+'.prototype.click = function (event){';
 s+='this.obj_name="ac'+ s_name+'";';
 if(obj_type!="none"){
   s+='this.parent.parent.atm.active_tab.set_to_create_obj(dic={"parent_obj_name":"'+this.my_name+'", "obj_type":"'+obj_type+'", "obj_name":"ac'+s_name+'", "element_name":"'+s_name+'",'
   s+='"properties":{"title":"'+s_title+'"}, "functions":{}, "attributes":{}'
   s+='});'
 }
 s+='try{'+this.my_name+s_name+'_click(obj=this, event);} catch(er){}';
 s+='}';
 //alert(s);
 eval(s);
 s='SubMenuBtn'+this.my_name+s_name;
 return eval(s);
}

// -- SubMenuBtn --
function SubMenuBtn(parent, my_name_, my_title_, width="width:10%;")
{
 this.parent=parent;this.my_title=my_title_;this.my_name=parent.my_name+my_name_;
 this.btn = document.createElement("button");
 this.btn.parent=this;
 this.btn.setAttribute("id", this.my_name);
 this.btn.setAttribute("class", "main_menu_btn");
 this.btn.setAttribute("style", width);
 this.btn.innerHTML = my_title_;
 this.btn.onclick=function(event){
   this.parent.click(event)
   }
 parent.parent.sub_menu.appendChild(this.btn);
}

// -- MenuBtnTab --
Tab_create_main_content = function()
{
    this.parent.nav=document.createElement("div");
    this.parent.nav.onclick=function(){
      //alert(JSON.stringify(editor_.tab_obj_.tab_functions))
      var e=event.target;
      try{var cc=e.getAttribute("class");if(cc!="funtablinks"){return;}} catch(er){}
      var f=event.target.innerHTML;
      editor.tab_obj_.active_function=f;
      editor.tab_content.innerHTML=editor.tab_obj_.tab_functions[f];
      editor.tab_content.setAttribute("fun_name",f);
      var funtablinks = document.getElementsByClassName("funtablinks");
      for (var i=0;i<funtablinks.length;i++){funtablinks[i].className=funtablinks[i].className.replace(" active","");};
      event.target.className += " active";
       //alert(editor_.tab_content.outerHTML)
    }.bind(editor=this.parent, event);
    this.parent.nav.setAttribute("class", "tab");
    this.parent.nav.btns={};
    this.parent.win_content.appendChild(this.parent.nav);
    this.parent.tab_content = document.createElement("textarea");
    this.parent.tab_content.setAttribute("class", "tab_textarea");
    this.parent.tab_content.onchange= function (){
      editor.tab_obj_.tab_functions[event.target.getAttribute("fun_name")]=event.target.value;
      editor.tab_obj_.parent.save();
      var click_event = new Event("click", {bubbles: true});
      //editor.main_menus["Tab"].btn.dispatchEvent(click_event);
    }.bind(editor=this.parent, event)
    this.parent.win_content.appendChild(this.parent.tab_content);
    for(f in this.parent.tab_obj_.tab_functions)
    {
      this.parent.nav.btns[f] = document.createElement("button");
      this.parent.nav.btns[f].setAttribute("class", "funtablinks");
      this.parent.nav.btns[f].innerHTML = f;
      this.parent.nav.appendChild(this.parent.nav.btns[f]);
      //alert(editor.tab_obj_.tab_functions[f])
    }

  // -- need to complete
  this.parent.tab_properties_ = document.createElement("div");
  var table = document.createElement("table");var tr=document.createElement("tr");table.appendChild(tr);
  var thp=document.createElement("th");thp.innerHTML="Property";thp.setAttribute("style","width:10%;text-align:center;");
  tr.appendChild(thp);
  var thv=document.createElement("th");thv.innerHTML="Value";thv.setAttribute("style","width:10%;text-align:center;");
  tr.appendChild(thv);
  this.parent.tab_properties_.appendChild(table);

  for(i in this.parent.tab_obj_.tab_properties)
  {
   var s=this.parent.tab_obj_.tab_properties[i];
   var tr=document.createElement("tr");table.appendChild(tr);
   var td=document.createElement("td");td.innerHTML=i;tr.appendChild(td);
   var td=document.createElement("td");var input=document.createElement("input");
   input.setAttribute("property",i);td.appendChild(input);
   try{if(s==null){}else{input.value=s}} catch(er){alert(er)}
   tr.appendChild(td);
  }

  this.parent.tab_properties_.addEventListener("change", function(){
    var p=event.target;var property=p.getAttribute("property");var v=p.value;
    editor.tab_obj_.tab_properties[property]=v;
    //--
    editor.tab_obj_.parent.save();
    //--
    // alert(JSON.stringify(editor.tab_obj_.tab_properties))
  }.bind(editor=this.parent, event))
  this.parent.tab_properties_.setAttribute("class", "com_setting");
  this.parent.win_content.appendChild(this.parent.tab_properties_);
}

TabNewFunction_click = function(obj)
{
  var fun_name_ = prompt("Enter name for new function:" , '');
  if(fun_name_ == '') {alert("Please enter a function name"); return;}
  this.parent.tab_obj_.tab_functions[this.parent.tab_obj_.tab_name+"_"+fun_name_]=this.parent.tab_obj_.tab_name+"_"+fun_name_+"=function(obj){}";
  // alert(JSON.stringify(this.parent.tab_obj_.tab_functions))
  this.parent.tab_obj_.active_function = this.parent.tab_obj_.tab_name+"_"+fun_name_;
  try{
    this.parent.tab_obj_.parent.save()
    var click_event = new Event("click", {bubbles: true});
    this.parent.main_menus["Tab"].btn.dispatchEvent(click_event);
  } catch (er){alert(er)}
}

TabDeleteFunction_click = function(obj)
{
  var confirm_=prompt("Are you sure you want to delete the function(type Yes): "+this.parent.tab_obj_.active_function, 'no');
  if(confirm_!='Yes'){return;}
  delete this.parent.tab_obj_.tab_functions[this.parent.tab_obj_.active_function];
  try{
    this.parent.tab_obj_.parent.save();
    var click_event = new Event("click", {bubbles: true});
    this.parent.main_menus["Tab"].btn.dispatchEvent(click_event);
  } catch (er){}
}


// -- MenuBtnComponent --
Component_create_main_content = function()
{
  //alert(this.my_name)
  //--  alert(editor.my_name)
  this.parent.component_left_nav = document.createElement("div");
  this.parent.component_left_nav.setAttribute("class", "tab");
  this.parent.component_left_nav.btns={};
  this.parent.component_left_nav.onclick=function(){
    var f=event.target.innerHTML;
    editor.tab_obj_.active_component_function=f;
    if(editor.tab_obj_.active_obj.data["functions"][f]==null)
    {editor.component_fun_editor.innerHTML="function (event){\ntry{\n\n} catch(er){alert(er)}\n}";} else
    {editor.component_fun_editor.innerHTML=editor.tab_obj_.active_obj.data["functions"][f]}

    var comfuntablinks = document.getElementsByClassName("comfuntablinks");
    for (var i=0;i<comfuntablinks.length;i++){comfuntablinks[i].className=comfuntablinks[i].className.replace(" active","");};
    event.target.className += " active";
  }.bind(editor=this.parent, event);
  this.parent.win_content.appendChild(this.parent.component_left_nav);
  //--
  this.parent.component_fun_editor = document.createElement("textarea");
  this.parent.component_fun_editor.setAttribute("class", "editor");
  this.parent.component_fun_editor.addEventListener("change", function(){
    var f=event.target.value;
    editor.tab_obj_.active_obj.data["functions"][editor.tab_obj_.active_component_function]=f;
    var obj_number = editor.tab_obj_.active_obj.data["properties"]["obj_number"];
    editor.tab_obj_.tab_objects[obj_number] = editor.tab_obj_.active_obj.data;
    editor.tab_obj_.parent.save();
  }.bind(editor=this.parent, event))
  this.parent.win_content.appendChild(this.parent.component_fun_editor);
  // --
  this.parent.component_properties = document.createElement("div");
  this.parent.component_properties.addEventListener("change", function(){
    var p=event.target; var property=p.getAttribute("property");var v=p.value;
    editor.tab_obj_.active_obj.data["properties"][property]=v;
    //--
    var obj_number = editor.tab_obj_.active_obj.data["properties"]["obj_number"];
    editor.tab_obj_.tab_objects[obj_number] = editor.tab_obj_.active_obj.data;
    editor.tab_obj_.parent.save();
  // --
    //alert(JSON.stringify(editor.tab_obj_.tab_content))
  }.bind(editor=this.parent, event))
  this.parent.component_properties.setAttribute("class", "com_setting");
  this.parent.win_content.appendChild(this.parent.component_properties);
  // --
}


ComponentButton_click = function(obj, event)
{
  //alert(2223)
  //alert(obj.parent.parent.tab_obj_.tab_name)
  //alert(obj.parent.parent.my_name); // editor
  //alert(obj.parent.parent.atm.my_name); // atm
  //alert(obj.parent.my_name); // Component

  //alert(obj.obj_name)
}

ComponentSpan_click = function(obj, event)
{
  //alert(obj.parent.parent.tab_obj_.tab_name)
  //alert(obj.parent.parent.my_name)
  //alert(obj.parent.my_name)
  //alert(obj.obj_name)
}

ComponentInput_click = function(obj, event)
{
  //alert(obj.parent.parent.tab_obj_.tab_name)
  //alert(obj.parent.parent.my_name)
  //alert(obj.parent.my_name)
  //alert(obj.obj_name)
}


//-- TabNavLink --
TabNavLink_create_main_content = function()
{
 //alert("TabNavLink_create_main_content")
 //this.my_sub_objs["nav"].click()
}

//- nav --
TabNavLinknav_click = function(obj, event)
{
  //alert(obj.my_name);
  //alert(obj.parent.my_name) // TabNavLink
  //alert(obj.parent.parent.my_name) // editor
  //alert(obj.parent.parent.atm.active_tab.tab_name)
  //alert(JSON.stringify(obj.parent.parent.tab_nav_links))
  //alert(JSON.stringify(obj.parent.parent.atm.tab_nav_links))
  //alert(JSON.stringify(obj.parent.parent.atm.active_tab.tab_nav_links))

  try{tab_fpe=obj.parent.parent.get_functions_properties_editor(
            obj.parent.parent.atm.active_tab,
            functions_dic=obj.parent.parent.atm.active_tab.tab_nav_links["functions"],
            functions_list_dic=obj.parent.parent.atm.tab_nav_links["functions"],
            dic_properties=obj.parent.parent.atm.active_tab.tab_nav_links["properties"],
            settings_list=obj.parent.parent.atm.tab_nav_links["settings_list"],
            attributes_list=obj.parent.parent.atm.tab_nav_links["attributes_list"],
            tab_btn_name="TabNavLink",null,
            node_to_delete=".tab_nav_links")} catch(er) {alert(er)}
}

//- item --
TabNavLinkitem_click = function(obj, event)
{
  //alert("TabNavLink- item")
  //alert(obj.obj_name) // acitem
  //alert(obj.parent.my_name) // TabNavLink (in editor. it is the MenuBtn)
  //alert(obj.parent.parent.my_name) // editor
  //alert(obj.parent.parent.tab_obj_.tab_name)

  var link_number=obj.parent.parent.active_link.link_number
  //alert(JSON.stringify(obj.parent.parent.tab_obj_.tab_nav_links["nav_links"][link_number]))

  try{tab_fpe=obj.parent.parent.get_functions_properties_editor(
            obj.parent.parent.atm.active_tab,
              functions_dic=obj.parent.parent.tab_obj_.tab_nav_links["nav_links"][link_number]["nav_link"]["functions"],
            functions_list_dic=obj.parent.parent.atm.nav_link["functions"],
              dic_properties=obj.parent.parent.tab_obj_.tab_nav_links["nav_links"][link_number]["nav_link"]["properties"],
            settings_list=obj.parent.parent.atm.nav_link["settings_list"],
            attributes_list=obj.parent.parent.atm.nav_link["attributes_list"],
            tab_btn_name="TabNavLink",null,
            node_to_delete='.tab_nav_links["nav_links"]['+link_number+']')} catch(er) {alert(er)}
}


// -- PopWin --
PopWin_create_main_content = function()
{
 try{
  var editor_=this.parent; var atm_=editor_.atm;
  var tab_id=editor_.active_popup_win[0];var win_name=editor_.active_popup_win[1];var win_number=editor_.active_popup_win[2];
  atm_.tabs[tab_id].PopWinObjects[win_name].create_editor_for_popwin(atm_.tabs[tab_id].tab_pop_win_buttons["pop_wins"][win_number]);
 } catch(er){}
}


PopWinNewPopWin_click = function(obj, event)
{
 var popup_name_ = prompt("Enter name for new Popup win:",'');if(popup_name_==''){alert("Please enter a name for popup win"); return;}
 var dic_functions={}
 dic_functions["__init__"]="function (obj){\ntry{\n\n} catch(er){alert(er)}}";
 dic_functions["__set_panel__"]="function (obj){\ntry{\n\n} catch(er){alert(er)}}";
 //alert(JSON.stringify(dic_functions))
 var n_=obj.parent.parent.tab_obj_.get_next_obj_number();
 var dic_={"properties":{"id":n_, "link_number":n_, "tab_id":obj.parent.parent.tab_obj_.tab_id,"name":popup_name_,"title":popup_name_,"zindex":50,"height":"500","width":"500","right":"25%","top":"25%",
           "background_color":"white", "title_color": "#fff", "title_background_color": "#2196F3", "is_panel":"true"},
           "functions":dic_functions};
 //alert(JSON.stringify(dic_))
 //var obj_ = obj.parent.parent.tab_obj_.get_pop_win_obj(dic_)
 var win_obj = obj.parent.parent.tab_obj_.get_pop_win_obj(dic_)

 //alert(win_obj);
 //alert(win_obj.my_name)
 try{
   //var win_obj=new obj_(parent=obj.parent.parent.tab_obj_);
   win_obj.__init__();
   win_obj.set_win_frame_style(dic_["properties"]["zindex"], dic_["properties"]["height"], dic_["properties"]["width"], dic_["properties"]["right"], dic_["properties"]["top"], dic_["properties"]["background_color"])
   win_obj.set_acWinStatEventListeners(obj.parent.parent.tab_obj_.parent.editor);
   obj.parent.parent.tab_obj_.parent.save()
 } catch(er){alert(er)}
}

PopWinDeletePopWin_click = function(obj, event)
{
//  alert("PopWinDeletePopWin")
//  alert(obj.obj_name) // acDeletePopWin
//  alert(obj.parent.my_name) // PopWin (in editor. it is the MenuBtn)
//  alert(obj.parent.parent.my_name) // editor
//  alert(obj.parent.parent.tab_obj_.tab_name)
//  alert(obj.parent.parent.tab_obj_.tab_name)
//alert(JSON.stringify(obj.parent.parent.tab_obj_.tab_pop_win_buttons))
var ll=obj.parent.parent.active_popup_win;
delete obj.parent.parent.tab_obj_.tab_pop_win_buttons["pop_wins"][ll[2]]
this.tab_obj_.parent.save();
}


//-- TabContent --
TabContent_create_main_content = function()
{
 //alert(222200000)
}

TabContentcontent_click = function(obj, event)
{
  //alert(obj.btn.outerHTML);
  //alert(obj.my_name) // TabContentcontent
  //alert(obj.parent.my_name) // TabContent
  //alert(obj.parent.parent.my_name) // editor
  //alert(obj.parent.parent.atm.active_tab.tab_name)
  //alert(131)
  //alert(JSON.stringify(obj.parent.parent.tab_nav_links))
  //alert(JSON.stringify(obj.parent.parent.atm.tab_nav_links))
  //alert(JSON.stringify(obj.parent.parent.atm.active_tab.tab_nav_links))
  // alert(133)
  //var tab_=obj.parent.parent.atm.active_tab;

  var my_creator_obj_=obj.parent.parent.atm.active_tab_content.my_creator_obj;
  //alert(my_creator_obj_.is_link)
  if(my_creator_obj_.is_link){
     var tab_content_=obj.parent.parent.atm.active_tab.tab_nav_links["nav_links"][my_creator_obj_.link_number]["tab_content"]
  } else {var tab_content_=obj.parent.parent.atm.active_tab.tab_content_link_dic;}
  var tab_content=obj.parent.parent.atm.tab_content
  try{
      tab_fpe=obj.parent.parent.get_functions_properties_editor(
            obj.parent.parent.atm.active_tab,
            functions_dic=tab_content_["functions"],
            functions_list_dic=tab_content["functions_list"],
            dic_properties=tab_content_["properties"],
            settings_list=tab_content["settings_list"],
            attributes_list=tab_content["attributes_list"],
            tab_btn_name="TabContent",
            null,
            node_to_delete=null
        )
  } catch(er) {alert(er)}
}


//-- Plugin --
Plugin_create_main_content = function()
{
 //alert(333)
}

PluginSearchTable_click = function(obj, event)
{
 //alert(333444)
  //var tab_=obj.parent.parent.atm.active_tab;
}