// -- AdvancedTabsManager --
function AdvancedTabsManager(my_name, my_app, body_,
activate_function_link, app_activate_function_link,update_field_link,get_data_link,
company_obj_id, is_show_btns=true, user_id=0)
{
 this.company_obj_id=company_obj_id;
 this.user_id=user_id;
 this.my_name=my_name; this.my_app=my_app; this.elm_body=body_;
 this.activate_function_link_=activate_function_link;
 this.app_activate_function_link_=app_activate_function_link;
 //alert(this.app_activate_function_link_)
 this.update_field_link_=update_field_link;
 this.get_data_link_=get_data_link;
 this.titles=null;this.container=null;
 this.content={"last_obj_number":0};
 this.tabs={};
 this.init_create_containers();
 if(is_show_btns == true){this.create_add_delete_editor();}
 this.setTabs();
 this.active_tab=null;
 this.editor=null;

// "Tab":{"title":"Tab", "obj_type":"none",
//                        "sub_buttons": {"NewFunction":{"title":"new func", "width":10},
//                                        "DeleteFunction":{"title":"del func", "width":10}}},

 this.buttons = {"Tab":{"title":"Tab", "obj_type":"none",
                        "sub_buttons": {}},

                 "TabContent":{"title":"Tab Content", "obj_type":"none",
                        "sub_buttons": {"content":{"title":"Content", "width":10, "setting":[], "attributes":[], "functions":[]}}},

                 "Component":{"title":"Component", "obj_type":"acObj",
                        "sub_buttons": {"Button":{"title":"Button", "width":5,
                                                  "setting": {},
                                                  "attributes":{},
                                                  "functions":["onmouseover", "onmouseout"]},
                                        "Span":{"title":"Span", "width":5,
                                                "setting": {"color":[], "background-color":[], "font-weight":["normal","lighter","bold","900"]},
                                                "attributes":{},
                                                "functions":["onmouseover", "onmouseout"]},
                                        "Input":{"title":"Input", "width":5,
                                                 "setting": {"color":[], "background-color":[], "text-align":["", "left", "center", "right"]},
                                                 "attributes":{"field":[],
                                                               "type":["text","button","checkbox","color","date",
                                                                       "datetime-local","email","file","hidden","image",
                                                                       "month","number","password","radio","range","reset",
                                                                       "search","submit","tel","time","url","week"],
                                                                       "foreign_table":[]},
                                                 "functions":["onchange", "onkeyup", "onkeydown"]},
                                        "Select":{"title":"Select", "width":5, "setting": {"options":[], "global_adjective":[],
                                                                                           "app_adjective":[], "data_app":[], "data_model":[],
                                                                                           "data_field":[], "data_filter_field":[],
                                                                                           "data_filter_field_value":[]},
                                                                                "attributes":{"field":[], "size":[],
                                                                                "foreign_table":[]},
                                                                                "functions":["onchange"]},
                                        "Table":{"title":"Table", "width":5, "setting": {}, "attributes":{}, "functions":["onchange"]},
                                        "Textarea":{"title":"textarea", "width":7,
                                                    "setting": {"overflow":[],"color":[],"background-color":[]},
                                                    "attributes":{"rows":[], "cols":[]}, "functions":[]},
                                        "DIV":{"title":"div", "width":3, "setting": {"overflow":[]}, "attributes":{}, "functions":[]},
                                        "A":{"title":"a", "width":3,
                                             "setting": {"color":[], "background-color":[]},
                                             "attributes":{"href":[], "target":[]},
                                             "functions":[]},
                                        "H":{"title":"h", "width":3,
                                             "setting": {},
                                             "attributes":{"color":[], "background-color":[]},
                                             "functions":[]},
                                        "H1":{"title":"h1", "width":3,
                                              "setting": {"color":[], "background-color":[]},
                                              "attributes":{}, "functions":[]},
                                        "H2":{"title":"h2", "width":3,
                                              "setting": {"color":[], "background-color":[]},
                                              "attributes":{}, "functions":[]},
                                        "H3":{"title":"h3", "width":3,
                                              "setting": {"color":[], "background-color":[]},
                                              "attributes":{}, "functions":[]}}},
                 "TabNavLink":{"title":"Tab Nav Link", "obj_type":"none",
                        "sub_buttons": {"nav":{"title":"Navigator", "width":10},
                                        "item":{"title":"Item", "width":10}}},

                 "PopWin":{"title":"Pop Win", "obj_type":"none",
                        "sub_buttons": {"NewPopWin":{"title":"New Pop Win", "width":10},
                                        "DeletePopWin":{"title":"Del Pop Win", "width":10}}},
                 "Plugin":{"title":"Plugin", "obj_type":"acPlugin",
                        "sub_buttons": {"SearchTable":{"title":"Search Table", "width":10,
                                                       "setting": {"is_new_button":["","Yes","No"], "is_del_button":["","Yes","No"]},
                                                       "attributes":{"number_of_rows":[], "table_class":["","basic", "payment"], "height":[]},
                                                       "functions":["onchange"],
                                                       "field_setting":["field_title","field_name","field_width","field_align"]},
                                        "Chart":{"title":"Chart", "width":5,
                                                 "setting": {},
                                                 "attributes":{"height":[]},
                                                 "functions":[]},
                                        "Heatmap":{"title":"Heatmap", "width":8,
                                                   "setting": {"width":[], "height":[]},
                                                   "attributes":{},
                                                   "functions":[]}}}
                }

 this.tab = {"functions":[],
             "settings_list":{"button_color":[],"button_bg_color":[],
                              "font-weight":["normal","lighter","bold","900"],
                              "tab_name":[],
                              "tab_type":["simple", "navmulti", "navone"],
                              "tab_order":[],"tab_title":[],"link_number":[]},
             "attributes_list":{}
            }

 this.tab_nav_links = {"functions":["onclick", "onmouseover", "onmouseout"],
                       "settings_list":{"width":[], "add_title":[], "remove_title":[], "is_show_btns":["", "true", "false"],
                       "obj_number":[], "background_color":[]},
                       "attributes_list":{}
                       }

 this.nav_link = {"functions":["onclick", "onmouseover", "onmouseout"],
                  "settings_list":{"link_number":[],"link":[],"title":[]},
                  "attributes_list":{}
                  }

 this.tab_content = {"functions_list":["onclick", "onchange", "onmouseover", "onmouseout"],
                     "settings_list":{"width":[], "color":[], "background-color":[]},
                     "attributes_list":{"table":[], "parent_table":[], "link_number":[], "content_type":[]}
                     }
 this.pop_win = {"functions_list":["onclick","onmouseover","onmouseout","__init___","__get_panel_structure___","__set_panel___"],
                 "settings_list":{"width":[], "height":[], "color":[], "background_color":[]},
                 "attributes_list":{"name":[],"top":[],"right":[],"title":[], "table":[], "link_number":[],"tab_id":[],
                                    "is_panel":["true", "false"],"title_color":[], "title_background_color":[], "content_type":[]}}
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
  this.add_btn.innerHTML="Add Tab";
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
                    try{atm.set_active_tab(atm.tabs[id_].btn)} catch(er){alert('er9037: '+ er)}
                    try{atm.save()} catch(er){alert("er900: "+er)}
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
  if(atm_.editor == null){
    var editor = new PopWin(my_name_="editor",win_name_="editor",win_title_="Editor for Tab: ",user_id=1, atm=atm_)
    editor.__init__();
    editor.set_win_frame_style("20", "650", "1000", "15%", "5%", "white")
    editor.set_acWinStatEventListeners(editor);
    editor.set_acWinStat('block');
    atm_.editor=editor;
  }
    try{editor.set_tab(atm_.active_tab);} catch(er){
        //    var editor = new PopWin(my_name_="editor",win_name_="editor",win_title_="Editor for Tab: ",user_id=1, atm=atm_)
        //    editor.__init__();
        //    editor.set_win_frame_style("20", "650", "1000", "15%", "5%", "white")
        //    editor.set_acWinStatEventListeners(editor);
        //    }
        //    editor.set_acWinStat('block');
        //    atm_.editor=editor;

        //    alert(98765)
        //    alert(atm_.editor)
        //    alert(987651111111111111111)
        }
  }.bind(atm_=this, event))

  this.add_delete_editor.appendChild(this.add_btn);
  this.add_delete_editor.appendChild(this.delete_btn);
  this.add_delete_editor.appendChild(this.editor_btn);
}

AdvancedTabsManager.prototype.setTabs = function()
{
  var dic_ = {"obj" : "AdvancedTabs", "atm": this.my_name, "app": this.my_app, "fun": "get_tabs_from_table", "params": {"name": ""}}
   //alert(JSON.stringify(dic_))
   //alert(this.activate_function_link_)
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
          for (jj in tabs)
          {
            var k=tabs[jj]; var id_=k[0];
            atm_.tabs[id_]=new Tab(atm_, data=k[1], id=id_);
            atm_.set_active_tab(atm_.tabs[id_].btn)
            atm_.tabs[id_].create_tab_pop_wins();
          }
          try{atm_.tabs[id_].btn.click();} catch(er){}
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

  try{eval(btn.parent.tab_name+"__myclick__(called_tab=btn.parent, calling_tab=btn.parent)");} catch(er){alert("er9001: "+er)}

  for (i=0;i<tablinks.length;i++){
    try{
      tablinks[i].className=tablinks[i].className.replace(" active","");
      if(tablinks[i].parent.tab_name!=btn.parent.tab_name)
      {eval(tablinks[i].parent.tab_name+"__otherclick__(called_tab=tablinks[i].parent, calling_tab=btn.parent)");}
    } catch(er){alert('er9038: '+ er)}
  }

  try{for(w in this.active_tab.PopWinObjects){if(w=="editor"){ continue;};this.active_tab.PopWinObjects[w].temp_close_win()}} catch(er){}

  try{
    this.active_tab=btn.parent;this.active_tab.content.style.display="block";btn.className+=" active";
    try{for(w in this.active_tab.PopWinObjects){if(w=="editor"){ continue;}; this.active_tab.PopWinObjects[w].resume_win()}} catch(er){}

      this.editor.main_menus["Tab"].btn.dispatchEvent(click_event);
      this.editor.set_title(this.editor.win_title_+this.active_tab.tab_name);
    } catch(er){}

    try{
       var click_event=new Event("click", {bubbles: true});
       this.editor_btn.dispatchEvent(click_event);
       var tab_fpe_=this.editor.get_functions_properties_editor(
              this.active_tab,
              functions_dic=this.active_tab.tab_functions,
              functions_list_dic=this.tab["functions"],
              dic_properties=this.active_tab.tab_properties,
              settings_list=this.tab["settings_list"],
              attributes_list=this.tab["attributes_list"],
              tab_btn_name="Tab",properties_func=null,
              node_to_delete=null)
            } catch(er) {//alert("er9031: "+ er)
    }
}

AdvancedTabsManager.prototype.get_tab = function(tab_name){for(id in this.tabs){if (this.tabs[id].tab_name==tab_name){return this.tabs[id]}}}

// this is a Factory function which return object based on the dic.
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
 try{eval(s)} catch(er){alert("er9002: "+er)}
 s=dic["obj_name"]+dic["properties"]["obj_number"]+'.prototype = Object.create('+dic["obj_type"]+'.prototype);'
 //alert(s);
 try{eval(s)} catch(er){alert("er903: "+er)}
 //--
 s=dic["obj_name"]+dic["properties"]["obj_number"]+'.prototype.create_editor = function()'
 s+='{'
 s+=' var container_id=this.data["container_id"];';
 s+=' var obj_number=this.data["properties"]["obj_number"];';
 s+=' try{var properties_func_=null;properties_func_=this.creator.editor_properties_func}catch(er){};';
 s+=' try{'

 //s+='alert(JSON.stringify(this.data["properties"]));'

 s+='  var fpe_=this.editor.get_functions_properties_editor(this.tab, this.data["functions"], this.functions,'
 s+='   this.data["properties"], this.settings,this.attributes, tab_btn_name="Plugin", properties_func=properties_func_,'
 s+='   node_to_delete=".tab_objects["+container_id+"]["+obj_number+"]"';
 s+='  )';
 s+=' } catch(er) {alert("er 207: "+er)};'
 s+='}'
 //alert(s);
 eval(s);
 //--
 s = 'new '+dic["obj_name"]+dic["properties"]["obj_number"]+'(atm_=this, tab_=tab, dic_=dic)'
 //alert(s)
 return eval(s)
}

AdvancedTabsManager.prototype.get_obj_functions_settings_attributes = function(dic_)
{
 //alert(JSON.stringify(dic_));
 var ps={"settings": {"width":[], "x":[], "y":[], "title":[], "obj_number":[]},
         "attributes":{},
         "functions":["onclick"]};
 var dic__=this.buttons[dic_["parent_obj_name"]]["sub_buttons"][dic_["element_name"]]

 //alert(JSON.stringify(dic_));
 //alert(JSON.stringify(dic__));

 //for (a in dic_["attributes"]){if (!ps["attributes"].includes(a)){ps["attributes"].push(a)}};
 //for (s in dic_["setting"]){if (!ps["settings"].includes(s)){ps["settings"].push(s)}};
 //--
 for (k in dic__["attributes"]){if(!(k in ps["attributes"])){ps["attributes"][k]=dic__["attributes"][k]}}
 for (k in dic__["setting"]){
 if(!(k in ps["settings"])){ps["settings"][k]=dic__["setting"][k]}}
 //for (i in dic__["setting"]){if (!ps["settings"].includes(dic__["setting"][i])){ps["settings"].push(dic__["setting"][i])}};
 for (i in dic__["functions"]){if (!ps["functions"].includes(dic__["functions"][i])){ps["functions"].push(dic__["functions"][i])}};
 for (f in dic_["functions"]){if (!ps["functions"].includes(f)){ps["functions"].push(f)}};
// alert(JSON.stringify(ps));
 //if (!ps["attributes"].includes(dic__["attributes"][i]))
 //{ps["attributes"].push(dic__["attributes"][i])}};
 //--
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
                      "tab_order": this.active_tab.tab_order,
                      "tab_title": this.active_tab.tab_title,
                      "tab_type": this.active_tab.tab_type,
                      "tab_pop_win_buttons": this.active_tab.tab_pop_win_buttons
                    }
  } catch(er){alert("er9004: "+er)}
  var dic_={"obj":"AdvancedTabs","atm":this.my_name, "app": this.my_app, "fun":"save_content",
            "params": {"atm_content": this.content,
                       "tab_content": tab_content,
                       "tab_name": this.active_tab.tab_name,
                       "tab_order": this.active_tab.tab_properties["tab_order"],
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

AdvancedTabsManager.prototype.app_activate_function = function(call_back_fun, dic_, html_obj)
{
  dic_["company_obj_id"]=this.company_obj_id;
     //alert(JSON.stringify(dic_))
     $.post(this.app_activate_function_link_,
          {dic : JSON.stringify(dic_)},
          function(dic){
            if(dic["status"]=="ok"){
                //alert(JSON.stringify(dic))
                //alert(JSON.stringify(dic["result"]))
                try{
                  call_back_fun(dic["result"], html_obj);
                  html_obj.data=dic["result"];
                  } catch(er){}
            } else {alert("Error getting data for select.")}
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
  var company_obj_id = dic_["company_obj_id"];
  if(dic_["company_obj_id"]==null){dic_["company_obj_id"]=this.company_obj_id;}
  //var temp_data = null;
  //alert("calling get_data")
  //alert(JSON.stringify(dic_));
  //alert(tbody_.outerHTML)
  //alert(call_back_fun)
  //alert(this.get_data_link_)
  $.post(this.get_data_link_,
          {dic : JSON.stringify(dic_)},
          function(data){
          try{
           //alert(JSON.stringify(data));
           if(data["status"]!="ok"){return}
           call_back_fun(data["dic"], tbody_)
           tbody_.data=data["dic"];
           } catch(er){alert(er)}
          });
}

AdvancedTabsManager.prototype.get_list = function(call_back_fun, dic_, html_obj)
{
  dic_["company_obj_id"]=this.company_obj_id;
  //alert(JSON.stringify(dic_))
     $.post(this.activate_function_link_,
          {dic : JSON.stringify(dic_)},
          function(dic){
            if(dic["status"]=="ok"){
                //alert(JSON.stringify(dic["result"]))
                call_back_fun(dic["result"], html_obj);
                html_obj.data=dic["result"];
            } else {alert("Error getting data for select.")}
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
    if(tbn=="Tab")
    {
     var tab_name=tab_.tab_name;
     functions[tab_name+"_"+fun_name_]=tab_name+"_"+fun_name_+"=function(obj){\ntry{\n\n} catch(er){alert('er9026: '+ er)}}";
     tab_.active_function = tab_.tab_name+"_"+fun_name_;
     try{
        tab_.parent.save();
        var click_event = new Event("click", {bubbles: true});tab_.btn.dispatchEvent(click_event);
      } catch (er){alert("er9029: "+ er)}
    } else {
     functions[fun_name_]="function (obj){\ntry{\n\n} catch(er){alert('er9005: '+er)}}";
     editor.tab_obj_.parent.save();
    }
  }.bind(tab_=tab, tbn=tab_btn_name, editor=tab.parent.editor, functions=functions_dic, event)
  del_btn.onclick= function (){
    event.preventDefault();
    var f=editor.tab_obj_.active_function;
    var fun_name_ = prompt("Are you sure you want to delete function "+f+". If so, type Yes:" , 'No');
    if(fun_name_ != 'Yes') {return;};
    delete functions[f]
    tab_.parent.save();
    if(tbn=="Tab")
    {try{var click_event = new Event("click", {bubbles: true});tab_.btn.dispatchEvent(click_event);} catch (er){alert("er9029: "+ er)}
    } else {alert("function "+f+" was deleted.")}
  }.bind(tab_=tab, tbn=tab_btn_name, editor=tab.parent.editor, functions=functions_dic, event)
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
    if(fun==null){fun="function (event){\ntry{\n\n} catch(er){alert('er9006: '+er)}\n}";functions_[f]=fun;}
      tab_content_.innerHTML=functions_[f];
      tab_content_.setAttribute("fun_name",f);
      var funtablinks = document.getElementsByClassName("funtablinks");
      for (var i=0;i<funtablinks.length;i++){funtablinks[i].className=funtablinks[i].className.replace(" active","");};
      event.target.className += " active";
       //alert(editor_.tab_content.outerHTML)
    }.bind(editor=tab.parent.editor, tab_content_=tab_content, functions_=functions_dic, event);
  nav_div.btns={};

  var fs__=functions_list_dic;var tfs_=Object.keys(functions_dic);var fs_=[];

  for(i in fs__){if(!(fs_.includes(fs__[i]))){fs_.push(fs__[i])}}
  for(i in tfs_){if(!(fs_.includes(tfs_[i]))){fs_.push(tfs_[i])}}
  for(i in fs_)
  {var f=fs_[i];nav_div.btns[f]=document.createElement("button");
      nav_div.btns[f].setAttribute("class", "funtablinks");
      nav_div.btns[f].innerHTML=f;nav_div.appendChild(nav_div.btns[f]);
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

   var pp_={}
   for (k in settings_list){if (!(k in pp_)){pp_[k]=settings_list[k]}}
   for (k in attributes_list){if (!(k in pp_)){pp_[k]=attributes_list[k]}}

   //alert(JSON.stringify(properties_dic));
   //for (k in properties_dic){if (!(k in pp_)){pp_[k]=properties_dic[k]}}
   //alert(JSON.stringify(settings_list));
   //alert(JSON.stringify(attributes_list));
   //alert(JSON.stringify(pp_));

   for (k in pp_)
   {
     var tr=document.createElement("tr");table.appendChild(tr);
     var td=document.createElement("td");td.innerHTML=k;tr.appendChild(td);
     var td=document.createElement("td");
     var l=pp_[k];
     if(l.length == 0){
       var input=document.createElement("input");input.setAttribute("size","10");
       if(k.includes("color")){input.setAttribute("type","color")};
     } else {
       var input=document.createElement("select");input.setAttribute("style", "width:100px;");
       //if(k.includes('color')){input.setAttribute("type","color")}
       for (j in l){var o = document.createElement("option");o.value=l[j];o.innerHTML=l[j];input.appendChild(o);}
     }
     input.setAttribute("property",k);td.appendChild(input);
     //input.setAttribute("size","10");
     //input.setAttribute("property",s);
     try{if(properties_dic[k]==null){} else{input.value=properties_dic[k]}} catch(er){alert("er9008: "+er)}
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


//-- AccountingObj --
function AccountingObj(parent, cofa_dic=null)
{
 //alert(JSON.stringify(cofa_dic))
 this.parent=parent;
 this.cofa=null;
 this.accounting_data=null;
 this.data_for_report={};
 if(cofa_dic!=null){this.set_cofa(cofa_dic)}
}

AccountingObj.prototype.set_cofa = function(cofa_dic)
{
 var f = function(result, dic, c=[])
 {for(var k in dic)
  {
   if(!isNaN(parseInt(k)))
      {
        for(j in c)
        {
         if(!(c[j] in result)){result[c[j]]={}}
         result[c[j]][k]=dic[k];
        }
      }
   else{
      var cc = [k].concat(c)
      f(result,dic[k],cc);
    }
  }
 }
 this.cofa=cofa_dic;
 this.accounts={};
 f(this.accounts, this.cofa)

// for(k in this.accounts)
// {
//  alert(k+"\n\n"+JSON.stringify(this.accounts[k]))
// }

}

AccountingObj.prototype.set_accounting_data = function(data)
{
  this.accounting_data=data;
  var ff = function(result, dic, data, total)
  {
   for(k in dic)
   {if(!isNaN(parseInt(k))){result[k]=data[k];total["v"]+=data[k]}
    else{result[k]={}; result["Total "+k]={"v":0};var t=ff(result[k],dic[k],data,result["Total "+k]);total["v"]+=t["v"]}
   };return total;
  }
  for(i in data){this.data_for_report[i]={};ff(this.data_for_report[i],this.cofa,data[i],total={"v":0})}
  //alert(JSON.stringify(this.data_for_report))
}

AccountingObj.prototype.get_financial_statement = function(statement,address)
{
 //alert(JSON.stringify(this.accounts))
 var fa=function(dic, data_, accounts, ad, sta, ss="")
 {
 var s_='';
 for(a in dic)
 {
  if(!isNaN(parseInt(a)))
  {
   s_+='<tr>'+'<td>&nbsp;&nbsp;'+ss+accounts[a]+'</td>';
      for(i in data_)
      {
       s_+='<td>'+data_[i][a]+'</td>'
      };
      s_+='</tr>';
  }
  else
  {if(a!="v")
   {ad1={};s_+='<tr>'+'<td>'+ss+a+'</td>';
    for(i in ad)
    {ad1[i]={};ad1[i][sta]={};ad1[i][sta]=ad[i][sta][a];
     var av="";if(a.includes("Total")){av=100*ad[i][sta][a]["v"];av=Math.round(av)/100};
     s_+='<td>'+av+'</td>'
    }
    s_+='</tr>';s_+=fa(dic[a], data_, accounts, ad1, sta, ss+"&nbsp;&nbsp;")
   }
  }
 }
 return s_
}

 var s='<div>'+address+'</div>';
 s+="<table class=''>"
 s+='<thead><tr><th>Accounts</th>';
 for(i in this.data_for_report){s+='<th>'+i+'</th>'};
 s+='</tr></thead>'
 s+="<tbody>";

 s+=fa(this.data_for_report[2022][statement],this.accounting_data, this.accounts , this.data_for_report, statement)

//s+=fa(this.data_for_report[2022]["Income"], this.accounting_data, this.data_for_report, "Income")
 s+="</tbody></table>"
 return s;
}


// -- acObj --
function acObj(){}

acObj.prototype.create_obj = function(){
  var container = document.getElementById("content_"+this.data["container_id"])
  //alert(JSON.stringify(this.data));
  //alert(container.outerHTML)
  //alert(container) //alert(container.outerHTML)
  this.new_obj=document.createElement(this.data["element_name"]);
  this.new_obj.my_creator_obj=this;

  this.new_obj.setAttribute("container_id", this.data["container_id"]);
  this.new_obj.setAttribute("id", this.data["properties"]["obj_number"]);
  this.new_obj.setAttribute("obj_type", this.data["obj_type"]);
  this.new_obj.setAttribute("type_", this.data["element_name"]);
  this.new_obj.innerHTML=this.data["properties"]["title"];
  // -- attribute --
  for (k in this.attributes)
  {
   if(k in this.data["properties"]){this.new_obj.setAttribute(k, this.data["properties"][k])}
   else{this.new_obj.setAttribute(k, "")}
  }

  if("width" in this.data["properties"]){var width_=this.data["properties"]["width"];}
  else {var width_="100"}
  var u="px";if(width_.includes("%")){u=""};


  var font_weight_=this.data["properties"]["font-weight"];
  if(font_weight_=="" || font_weight_==null){var font_weight="";} else {var font_weight=";font-weight:"+font_weight_}
  var align_=this.data["properties"]["text-align"];
  if(align_=="" || align_==null){var align="right";} else {var align=align_}
  var color_=this.data["properties"]["color"];
  if(color_=="" || color_==null){var color="black";} else {var color=color_}
  var background_color_=this.data["properties"]["background-color"];
  if(background_color_=="" || background_color_==null){var background_color="";}
  else {var background_color=";background-color:"+background_color_}

  if(this.data["element_name"]=="Input")
  {
    var s_label=this.data["properties"]["title"]+":&nbsp;";
    s_label_length=10*(1*s_label.length-5);
    //alert(s_label+" : "+s_label_length)
    var nx_=s_label_length;var x=1*this.data["properties"]["x"]+nx_;
    //alert(JSON.stringify(this.data["properties"]));
    var s_style="position:absolute;left:"+x+"px;top:"+this.data["properties"]["y"]+"px;width:"+width_+"px;text-align:"+align+";";

    this.new_obj.setAttribute("style", s_style);
    var span=document.createElement("span");span.innerHTML=s_label;
    var x = 1*this.data["properties"]["x"];
    var s_="position:absolute;left:"+x+"px;top:"+this.data["properties"]["y"]+"px;text-align:right;display:inline-block;width:"+s_label_length+"px;"
    s_+="color:"+color+background_color;
    span.setAttribute("style", s_);
    container.appendChild(span);
  } else if (this.data["element_name"]=="DIV") {
    var s_ = this.data["properties"]["overflow"]
    if(s_!=null || s_!="")
    {s_="overflow:"+s_}

    alert(s_);

    var ss="position:absolute;left:"+this.data["properties"]["x"]+"px;top:"+this.data["properties"]["y"]+"px;width:"+width_+u+";"+s_
    this.new_obj.setAttribute("style", ss);
   //"overflow: scroll;
  } else {
    var s_="position:absolute;left:"+this.data["properties"]["x"]+"px;top:"+this.data["properties"]["y"]+"px;width:"+width_+u+";"
    s_+="color:"+color+background_color+font_weight;
    this.new_obj.setAttribute("style", s_);
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

              var fun=function(data, html_obj){
                //alert(html_obj.outerHTML)
                //alert(JSON.stringify(data));
                for(i in data){
                 var l=data[i];
                 var option = document.createElement("option");
                 option.value = l[0];
                 option.text = l[1];
                 html_obj.appendChild(option);
                }
              }
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
   var dic_ = {"obj": "AdvancedTabs", "atm": atm_.my_name, "app": "core", "fun": "get_adjective",
               "params": {"app": "core", "model_name": "AdjectivesValues",
               "manager_name": "adjectives","manager_fun": "adjectives",
               "manager_fun_field": "adjective_title","field_value":adjective}
              }
      //alert(JSON.stringify(dic_))
      this.atm.get_list(call_back_fun=fun, dic_, this.new_obj);
  } else if (dic["properties"]["app_adjective"]!="" & dic["properties"]["app_adjective"]!=null)
  {
   var adjective=dic["properties"]["app_adjective"];
   var dic_ = {"obj": "AdvancedTabs", "atm": atm_.my_name, "app": this.atm.my_app, "fun": "get_adjective",
               "params": {"app": this.atm.my_app, "model_name": "AdjectivesValues",
               "manager_name": "adjectives","manager_fun": "adjectives",
               "manager_fun_field": "adjective_title","field_value":adjective,
               }
              }
      //alert(JSON.stringify(dic_))
      this.atm.get_list(call_back_fun=fun, dic_, this.new_obj);
  } else if(dic["properties"]["data_app"]!="" & dic["properties"]["data_app"]!=null)
  {
    //alert(JSON.stringify(dic["properties"]));
    var data_app=dic["properties"]["data_app"];
    var data_model=dic["properties"]["data_model"];
    var data_field=dic["properties"]["data_field"];
    var data_filter_field=dic["properties"]["data_filter_field"];
    var data_filter_field_value=dic["properties"]["data_filter_field_value"];
    //alert(data_filter_field)
    if(data_filter_field==null){data_filter_field="";data_filter_field_value="";}
    var dic_ = {"obj": "AdvancedTabs", "atm": atm_.my_name, "app": data_app, "fun": "get_list_from_model",
               "params": {"app": data_app, "model_name": data_model,
               "manager_name": "","manager_fun": "",
               "manager_fun_field": "","field_name":data_field,
               "data_filter_field":data_filter_field,
               "data_filter_field_value":data_filter_field_value
               }
              }
    this.atm.get_list(call_back_fun=fun, dic_, this.new_obj);
  }
}

acObj.prototype.update_data_by_dic = function(dic)
{
  this.new_obj.innerHTML = "";
  var option = document.createElement("option");
  option.value = "-1"; option.text = "----";
  this.new_obj.appendChild(option);
  for(i in dic){
     var option = document.createElement("option");
     option.value = i;
     option.text = dic[i];
     this.new_obj.appendChild(option);
  }
}

// -- acPlugin --
function acPlugin(){}

acPlugin.prototype.create_obj = function(){this.creator.create_obj();}


// -- acSearchTableCreator --
function acSearchTableCreator(parent, container){
  this.parent=parent;this.data=null;
  // alert(JSON.stringify(this.parent.data));
}

acSearchTableCreator.prototype.create_obj = function()
{
  var dic=this.parent.data;
  if(!dic["fields"]){dic["fields"]={"1":{"field_title":"1", "field_name":"","field_width":"100","field_align":"left"},
                                    "2":{"field_title":"2", "field_name":"","field_width":"100","field_align":"left"}}}
  if(!(dic["properties"]["table_class"])){dic["properties"]["table_class"]="basic"}
  //alert(JSON.stringify(dic));
  this.parent.data=dic;
  //--
  var container = document.getElementById("content_"+dic["container_id"]);
  this.number_of_rows=dic["properties"]["number_of_rows"];
  this.is_new_button=dic["properties"]["is_new_button"];
  this.is_del_button=dic["properties"]["is_del_button"];
  this.fields=[]
  for(f in dic["fields"]){this.fields.push(dic["fields"][f]["field_name"])}
  //--
  this.filter_value="";
  this.search_input_=document.createElement("input");
  this.search_input_.setAttribute("type", "text");
  this.search_input_.setAttribute("id", "search_"+dic["properties"]["obj_number"]);
  var ny_search=parseInt(dic["properties"]["y"])-18
  var nx_search=parseInt(dic["properties"]["x"])+20
  var n_search_width=120;
  if(this.is_new_button=="Yes")
  {
   this.new_button=document.createElement("button");
   this.new_button.setAttribute("id", "new_button_"+dic["properties"]["obj_number"]);
   var nx_nb=nx_search+n_search_width
   this.new_button.setAttribute("style", "position:absolute;left:"+nx_nb+"px;top:"+ny_search+"px;width:40px");
   this.new_button.innerHTML="New";
   this.new_button.my_creator_obj=this;
   container.appendChild(this.new_button);
   this.new_button.addEventListener("click", function(event){
     var container_=event.target.parentNode;
     container_.my_creator_obj.clear_objects_data()
   })
  }
  if(this.is_del_button=="Yes")
  {
   this.del_button=document.createElement("button");
   this.del_button.setAttribute("id", "del_button_"+dic["properties"]["obj_number"]);
   var nx_db=nx_search+n_search_width+40
   this.del_button.setAttribute("style", "position:absolute;left:"+nx_db+"px;top:"+ny_search+"px;width:40px");
   this.del_button.innerHTML="Del";
   this.del_button.my_creator_obj=this;
   container.appendChild(this.del_button);
   this.del_button.addEventListener("click", function(event){
     var container_=event.target.parentNode;
     container_.my_creator_obj.delete_record();
     event.target.my_creator_obj.get_data();
     container_.my_creator_obj.clear_objects_data()
   })
  }

  this.search_input_.setAttribute("style", "position:absolute;left:"+nx_search+"px;top:"+ny_search+"px;width:"+n_search_width+"px");
  this.search_input_.addEventListener("keyup", function(event){
     var input=event.target;
     var filter_field = input.getAttribute("filter_field");
     input.my_creator_obj.filter_field=filter_field;
     input.my_creator_obj.filter_value=input.value;
     input.my_creator_obj.get_data();
   })
  container.appendChild(this.search_input_);

  this.table_=document.createElement("table");
  this.table_.setAttribute("class", dic["properties"]["table_class"]);
  this.table_.setAttribute("container_id", dic["container_id"]);
  this.table_.setAttribute("id", dic["properties"]["obj_number"]);
  this.table_.setAttribute("obj_type", dic["obj_type"]);
  this.table_.setAttribute("type", dic["element_name"]);
  if("width" in dic["properties"]){var width_=dic["properties"]["width"]} else {var width_="400"}
  this.table_.setAttribute("style", "position:absolute;left:"+dic["properties"]["x"]+"px;top:"+dic["properties"]["y"]+"px;width:"+width_+"px");
  this.thead=document.createElement("thead");
  this.thead.setAttribute("style", "display: block;overflow-x: hidden;");
  this.table_.appendChild(this.thead);
  var tr_h=document.createElement("tr");
  tr_h.my_creator_obj=this;
  tr_h.addEventListener("click", function(event){
   var e=event.target;
   var filter_field=e.getAttribute("filter_field")
   e.parentNode.my_creator_obj.search_input_.setAttribute("filter_field", filter_field);
   e.parentNode.my_creator_obj.search_input_.setAttribute("placeholder", "Search "+e.innerHTML+"..");
   e.parentNode.my_creator_obj.filter_field=filter_field;
   e.parentNode.my_creator_obj.get_data();
  })

  tr_h.setAttribute("style","cursor:pointer");
  this.thead.appendChild(tr_h);
  var n__=0;
  for(f in dic["fields"])
  {
    var th_=document.createElement("th");
    th_.innerHTML=dic["fields"][f]["field_title"];
    var width_=100;try{width_=dic["fields"][f]["field_width"]} catch(er){}
    if(n__==0){
      th_.setAttribute("style", "width:"+width_+"px;border-top-left-radius: 15px")
      this.filter_field=dic["fields"][f]["field_name"];
      this.search_input_.setAttribute("filter_field", dic["fields"][f]["field_name"]);
      this.search_input_.setAttribute("placeholder", "Search "+dic["fields"][f]["field_title"]+"..");
    }
    else{th_.setAttribute("style", "width:"+width_+"px;")}; n__+=1;
    tr_h.appendChild(th_);
    th_.setAttribute("filter_field", dic["fields"][f]["field_name"])
  }
  th_.setAttribute("style", "width:"+width_+"px;border-top-right-radius: 15px");
  this.tbody=document.createElement("tbody");
  this.tbody.setAttribute("id", "tbody_"+dic["properties"]["obj_number"]);
  this.tbody.setAttribute("style", "display: block;height: "+dic["properties"]["height"]+"px;overflow-y: auto;overflow-x: hidden;");

  this.table_.appendChild(this.tbody);
  this.table_.my_creator_obj=this;
  this.search_input_.my_creator_obj=this;

  for (i in dic["attributes"]){var s=dic["attributes"][i];
   if(s in dic["properties"]){this.table_.setAttribute(s, dic["properties"][s])}
   else{this.table_.setAttribute(s, "")}}

  container.appendChild(this.table_);
  this.table_.onclick=this.row_click;
  for(f in dic["functions"]){if(f!="onclick"){var s="this.table_."+f+"="+dic["functions"][f];eval(s);}}
}

acSearchTableCreator.prototype.get_data = function(data_table_name=null,parent_model=null,parent_id=null,company_obj_id=null)
{
  var dic=this.parent.data;
  //alert(JSON.stringify(dic));
  var container = document.getElementById("content_"+dic["container_id"]);
  //alert(container.outerHTML);
  if(data_table_name!==null){this.data_table_name=data_table_name} else {this.data_table_name=container.getAttribute("table")}
  try{
    var parent_id_="";
    //alert(this.data_table_name)
    var model_=container.my_creator_obj.link_dic["properties"]["table"];
    //alert(model_)
    try{
        if(parent_model!=null){var parent_model_=parent_model} else {
          var parent_model_=container.my_creator_obj.link_dic["properties"]["parent_table"]
          }
          if(parent_model_==null){var parent_model_="";}
        } catch(er){};
    // var record_id_=container.getAttribute("record_id");
    if(parent_id!=null){parent_id_=parent_id} else {parent_id_=container.getAttribute("parent_id")}
    if(parent_id_=="" || parent_id_==null){return}
    var dic_={"model":this.data_table_name, "number_of_rows":this.number_of_rows, "fields":this.fields}
  } catch(er){alert("er9012: "+er)}

  var fun=function(data, ttbody_){
//  alert(JSON.stringify(dic));
//    alert(JSON.stringify(dic["fields"]));
    //alert(JSON.stringify(data));
    //alert(dic_["fields"][0])
    //alert(JSON.stringify(data[dic_["fields"][0]]))
    var n_=data[dic_["fields"][0]].length;
    //alert(n_)
    var s='';
    for(i=0; i<n_; i++)
    {
     s+='<tr id_="'+data["id"][i]+'" row="'+i+'"'+'>';
     for(j in dic_["fields"])
     {
       var f=dic_["fields"][j];
       var width_=200;var field_align_="left";
       for(z in dic["fields"]){
        if(dic["fields"][z]["field_name"]==f){width_=dic["fields"][z]["field_width"];field_align_=dic["fields"][z]["field_align"]}
        }
        s+='<td style="width:'+width_+'px;text-align:'+field_align_+'">'+data[f][i]+'</td>'
     };
     s+='</tr>';
    }
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
  var dic__={"model":this.data_table_name, "parent_model": parent_model_, "parent_id":parent_id_,
             "number_of_rows":this.number_of_rows, "filter_field":this.filter_field, "filter_value":this.filter_value,
             "fields":dic__}
  //alert(JSON.stringify(dic__));
  if(company_obj_id!=null){dic__["company_obj_id"]=company_obj_id}
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

 for(f in dic){result[f]=dic[f][n_row]}

 container.my_creator_obj.set_objects_data(result);
 container.my_creator_obj.current_record_data=result;

 try{eval('var zz='+this.my_creator_obj.parent.data["functions"]["onclick"]);zz(event)} catch(er)
 {//alert("er9013: "+er)
 }
}

acSearchTableCreator.prototype.editor_properties_func = function(tab, tab_properties_)
{
 //alert(tab.active_obj)
 var field_setting=tab.parent.buttons[tab.active_obj.data["parent_obj_name"]]["sub_buttons"][tab.active_obj.data["element_name"]]["field_setting"]
 //alert(field_setting)
 var fields=tab.active_obj.data["fields"];
 //alert(JSON.stringify(fields));
 var nav=document.createElement("div");
 var add_del_btns=document.createElement("div");
 this.add_btn=document.createElement("button");this.del_btn=document.createElement("button");
 this.add_btn.innerHTML="Add"; this.add_btn.tab=tab;
 this.del_btn.innerHTML="Delete"; this.del_btn.tab=tab; this.del_btn.nav=nav;
 this.add_btn.onclick=function (event){
   var n_=Object.keys(tab.active_obj.data["fields"]).length+1
   tab.active_obj.data["fields"][n_]={"field_name":"","field_title":"","field_width":"100","field_align":"left"};
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
  for(p_ in field_setting) // this.fields[f])
  {
   var p=field_setting[p_]
   var v=this.fields[f];var tr=document.createElement("tr");table.appendChild(tr);
   var td=document.createElement("td");tr.appendChild(td);td.innerHTML=p
   var td=document.createElement("td");tr.appendChild(td);var input=document.createElement("input");
   input.setAttribute("size","10");td.appendChild(input);
   input.setAttribute("field",f);input.setAttribute("property",p);
   try{if(this.fields[f][p]!=null){input.value=this.fields[f][p]}} catch(er){}
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
                    "y1":{"data":[], "color":[219, 64, 82], "name":"import"}}}
  //alert(JSON.stringify(chart_type));

   for(var i=0; i<3;i++)
   {
     chart_type["x"]["data"].push(i)
     chart_type["series"]["y1"]["data"].push(i+Math.random())
   }
  //alert(JSON.stringify(chart_type));
 this.set_chart_data(chart_type);
}

acChartCreator.prototype.set_chart_data = function(chart_type)
{
  //alert(JSON.stringify(chart_type));
  var data_=[]
  chart_attributes={"lines":{"type_name":"mode", "type_value":"lines", "marker_attribute":"size", "marker_attribute_value":"8"},
                    "bars":{"type_name":"type", "type_value":"bar", "marker_attribute":"opacity", "marker_attribute_value":"0.7"},
                    "pies":{"type_name":"type", "type_value":"pie", "marker_attribute":"opacity", "marker_attribute_value":"0.7"},
                    "areas":{"type_name":"type", "type_value":"scatter", "marker_attribute":"opacity", "marker_attribute_value":"0.7"},
                    "scatter":{"type_name":"mode", "type_value":"markers", "marker_attribute":"opacity", "marker_attribute_value":"0.7"}
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
 } else if (chart_type["type"]=='areas') {
   for(y in data["series"]){
    var trace = {}
    trace["x"]=data["x"]["data"];
    trace["y"]=data["series"][y]["data"];
    trace[data["type_name"]]=data["type_name_value"];
    trace["fill"]='tozeroy';
    trace["mode"]='none';
    data_.push(trace);
   };
 } else if(chart_type["type"]=='scatter') {
    var trace = {}
    trace["x"]=chart_type["x"];
    trace["y"]=chart_type["y"];
    trace[data["type_name"]]=data["type_name_value"];
    trace["type"]="scatter";
    trace["marker"] = { size: 3 }
    data_.push(trace);

   //alert(JSON.stringify(data_));

   var layout = {title: data["title"],
                 xaxis: {title: chart_type["x-axis-title"], range: chart_type["x-axis-range"]},
                 yaxis: {title: chart_type["y-axis-title"], range: chart_type["y-axis-range"]}}
 } else {
  for(y in data["series"]){
    var trace = {}
    trace["x"]=data["x"]["data"];
    trace["y"]=data["series"][y]["data"];
    trace[data["type_name"]]=data["type_name_value"];
    trace["marker"]={"color":"rgb("+data["series"][y]["color"][0]+", "+data["series"][y]["color"][1]+", "+data["series"][y]["color"][2]+")"}
    trace["marker"][data["marker_attribute"]]=data["marker_attribute_value"]
    trace["name"]=data["series"][y]["name"]
    trace["line"]={color: 'rgb('+data["series"][y]["color"][0]+', '+data["series"][y]["color"][1]+', '+data["series"][y]["color"][2]+')', width: 2}
    data_.push(trace)
  }
  var layout = {title: data["title"],
                xaxis: {title: chart_type["x-axis-title"], range: chart_type["x-axis-range"]},
                yaxis: {title: chart_type["y-axis-title"], range: chart_type["y-axis-range"]}}
 }
 //alert(JSON.stringify(data_));
 Plotly.newPlot(this.chart, data_, layout );
}

acChartCreator.prototype.get_data = function()
{
  //alert("get Data")
}

// -- acHeatmapCreator --
function acHeatmapCreator(parent){this.parent=parent;this.data=null;}

acHeatmapCreator.prototype.create_obj = function()
{
  //alert("I am a creator of acPlugin Chart")
  //--
  var dic=this.parent.data;
  //alert(JSON.stringify(dic));
  //--
  var container = document.getElementById("content_"+dic["container_id"]);
  //--
 this.heatmap=document.createElement("div");
 this.heatmap.setAttribute("container_id", dic["container_id"]);
 this.heatmap.setAttribute("id", dic["properties"]["obj_number"]);
 this.heatmap.setAttribute("obj_type", dic["obj_type"]);
 this.heatmap.setAttribute("type", dic["element_name"]);
 if("width" in dic["properties"]){var width_=dic["properties"]["width"]} else {var width_="400"}
 if("height" in dic["properties"]){var height_=dic["properties"]["height"]} else {var height_="400"}
 var style_="position:absolute;left:"+dic["properties"]["x"]+"px;top:"+dic["properties"]["y"]+"px;width:"+width_+"px;"
 style_+="height:"+height_+"px";
 this.heatmap.setAttribute("style", style_);
 this.heatmap.my_creator_obj=this;
 container.appendChild(this.heatmap);

   var chart_type={"x": ['A', 'B', 'C', 'D', 'E'], "y": ['W', 'X', 'Y', 'Z'], "z": [
      [0.10, 0.20, 0.3, 0.4, 0.50],
      [0.60, 0.70, 0.75, 0.75, 1.00],
      [0.75, 0.75, 0.75, 0.75, 0.75],
      [0.80, 0.90, 0.00, 0.75, 0.00]
    ]}
  //alert(JSON.stringify(chart_type));
 this.set_chart_data(chart_type);
}

acHeatmapCreator.prototype.set_chart_data = function(chart_type)
{
var xValues = chart_type["x"];
var yValues = chart_type["y"];
var zValues = chart_type["z"];

var colorscaleValue = [
  [0, '#3D9970'],
  [1, '#001f3f']
];

var data = [{
  x: xValues,
  y: yValues,
  z: zValues,
  type: 'heatmap',
  colorscale: colorscaleValue,
  showscale: false
}];

var layout = {
  title: 'Annotated Heatmap',
  annotations: [],
  xaxis: {
    ticks: '',
    side: 'top'
  },
  yaxis: {
    ticks: '',
    ticksuffix: ' ',
    width: 700,
    height: 700,
    autosize: false
  }
};

for ( var i = 0; i < yValues.length; i++ ) {
  for ( var j = 0; j < xValues.length; j++ ) {
    var currentValue = zValues[i][j];
    if (currentValue != 0.0) {
      var textColor = 'white';
    }else{
      var textColor = 'black';
    }
    var result = {
      xref: 'x1',
      yref: 'y1',
      x: xValues[j],
      y: yValues[i],
      text: zValues[i][j],
      font: {
        family: 'Arial',
        size: 12,
        color: 'rgb(50, 171, 96)'
      },
      showarrow: false,
      font: {
        color: textColor
      }
    };
    layout.annotations.push(result);
  }
}

 Plotly.newPlot(this.heatmap, data, layout );

 try{
 this.heatmap.on('plotly_click', function(data){
    //alert(event.target.outerHTML)
    //alert("aaa")
    alert(data)
//    for(k in data["points"][0]){
//     //alert("k: " + k);
//     for(j in data["points"][0][k])
//     {
//       alert("k: " + k + " j: " + j + " = " +data["points"][0][k][j])
//     }
//    }
});
} catch(er) {alert(er)}

}

acHeatmapCreator.prototype.get_data = function()
{
  //alert("get Data")
}

// -- TabContent --
function TabContent(tab, container, link_dic, is_on_click=true, is_link=null){

 //alert("TabContent");
 //alert(tab.tab_name)
 //alert('container.outerHTML')
 //alert(container.outerHTML)
 //alert(JSON.stringify(link_dic));

 var pp_=link_dic["properties"]
 //alert(JSON.stringify(pp_));
 //alert(tab.tab_name)
 this.is_link=is_link;
 this.tab=tab;
 this.link_dic=link_dic;
 this.link_number=pp_["link_number"];
 this.content_type=pp_["content_type"];
 //-
 this.link_content=document.createElement("div");
 this.link_content.my_creator_obj=this
 this.link_content.setAttribute("id", "content_"+this.link_number);
 this.link_content.setAttribute("table", pp_["table"]);
 this.link_content.setAttribute("record_id", "new");
 this.link_content.setAttribute("parent_id", "new");
 this.link_content.setAttribute("link_number", this.link_number);
 //this.link_content.innerHTML=this.link_number;
 this.link_content.setAttribute("type", "container");
 //this.link_content.setAttribute("obj_type", "container");
 this.link_content.setAttribute("class", "tabcontent");
 this.link_content.tab=tab;
 this.link_content.tab_content_id=this.link_number;
 if(is_link){var width=100} else {var width=pp_["width"];}

 // alert('JSON.stringify(pp_)');
 // alert(JSON.stringify(pp_));
 var background_color_="white";
 var color_="black";
 // alert(pp_["background-color"])
 // alert(pp_["color"])

 //if(!(pp_["background-color"]==null)){alert(9);background-color_=pp_["background-color"]}
 //if(!(pp_["color"]==null)){alert(9);color_=pp_["color"]}

 var ss_="position: relative;background-color:"+background_color_+";color:"+color_+";width: "+width+"%;height:1000px;display:block;"
 //alert(ss_)
 this.link_content.setAttribute("style", ss_);

 // border: 1px solid #ccc;

 if(is_on_click){
    //alert(this.link_content.outerHTML)

    this.link_content.onclick=function(event){
      //alert(event.target.outerHTML);
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
        // alert(JSON.stringify(this.tab.new_obj_to_create));
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

        this.tab.active_obj=this.tab.generate_obj(dic=dic);
        this.tab.active_obj.create_editor();
        this.tab.tab_objects[container_id][obj_number]=this.tab.active_obj.data;
        this.tab.parent.save();
      }
    }
 }
 this.link_content.onchange=function (event){
  //alert(JSON.stringify(this.my_creator_obj.link_dic))
  var e=event.target;
  //alert(e.outerHTML)
  //alert(this.outerHTML)
  var e_container_id_=e.getAttribute("container_id")
  var c_container_id_=this.getAttribute("link_number")
  //alert(e_container_id_+ " " + c_container_id_)
  if(e_container_id_!=c_container_id_) {return;}
  var foreign_table=e.getAttribute("foreign_table")
  var field_=e.getAttribute("field");
  try{var type_=e.getAttribute("type");if(type_==null || type_==""){type_=""}} catch(er){}
  if(foreign_table!=null && foreign_table!="")
  {
   if(this.foreign_keys==null){this.foreign_keys={}}
   var vv=e.value;if(type_=="date"){var ss=vv.split("-");vv=ss[0]+ss[1]+ss[2]}
   this.foreign_keys[field_]={"value":vv, "foreign_table":foreign_table};
   return;
  }

  var model_=this.my_creator_obj.link_dic["properties"]["table"];
  try{var parent_model_=this.my_creator_obj.link_dic["properties"]["parent_table"]} catch(er){};
  if(parent_model_==null){var parent_model_="";}
  var record_id_=this.getAttribute("record_id");
  var parent_id_=this.getAttribute("parent_id");
  if(field_=="" || field_==null){return}

  var dic_data={"model":model_, "parent_model":parent_model_, "field":field_, "pkey":record_id_, "parent_pkey":parent_id_,
                "value":e.value, "type":type_, "foreign_keys":this.foreign_keys}

  // alert(JSON.stringify(dic_data))

  this.tab.parent.active_tab_content=this;
  this.tab.parent.save_data(this, dic_data);
  this.my_creator_obj.refresh_my_tables(f=field_, v=e.value)
  //event.preventDefault();
 }
 container.appendChild(this.link_content);
 this.process_content();
}

TabContent.prototype.process_content = function()
{
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
   if(container_dic[o]["obj_type"]=="acObj" && (container_dic[o]["obj_name"]=="acInput" || container_dic[o]["obj_name"]=="acSelect")){
     var eI=document.getElementById(o);var v=dic[container_dic[o]["properties"]["field"]];eI.value=v;
   }
 }
}

TabContent.prototype.clear_objects_data = function()
{
 try{
   var dic = this.current_record_data;
   this.link_content.setAttribute("record_id", "new");var container_dic=this.tab.tab_objects[this.link_number];
   for(o in container_dic)
   {if(container_dic[o]["obj_type"]=="acObj" && container_dic[o]["obj_name"]=="acInput"){document.getElementById(o).value="";}}
  } catch(er){}
}

TabContent.prototype.delete_record = function()
{
  var id_ = prompt("Are you sure you want to delete this record? if so type Yes" , 'No')
  if(id_ != 'Yes') {return;}
  id_=this.link_content.getAttribute("record_id")
  var table_=this.link_content.getAttribute("table")
  var atm_=this.tab.parent;
  var dic_ = {"obj" : "AdvancedTabs", "atm": atm_.my_name, "app": atm_.my_app, "fun": "delete_record",
              "params": {"app": atm_.my_app, "model": table_, "id":id_}}
              $.post(atm_.activate_function_link_,
              {
                dic : JSON.stringify(dic_)
              },
              function(dic){
                id_ = dic["result"]["id"];
                alert("record was deleted")
             })
}

TabContent.prototype.refresh_my_tables = function(f, v)
{
 var container_dic=this.tab.tab_objects[this.link_number];
 for(o in container_dic)
 {
   if(container_dic[o]["obj_type"]=="acPlugin" && container_dic[o]["obj_name"]=="acSearchTable"){
     var eI=document.getElementById(o);
     eI.my_creator_obj.search_input_.setAttribute("filter_field", f);
     eI.my_creator_obj.search_input_.value=v;
     var ec = new Event("keyup", {bubbles: true});
     eI.my_creator_obj.search_input_.dispatchEvent(ec);
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
   try{e.parent.link_content.style.display="block";this.parent.link_btn.className+=" active";}catch(er){alert("er9014: "+er)}
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
     eval(f+"_zz"+this.properties["obj_number"]+"="+this.tab.tab_nav_links["functions"][f]);
     eval('this.nav.'+f+'='+f+'_zz'+this.properties["obj_number"]);
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
 this.tab_order=data["properties"]["tab_order"];
 this.tab_title=data["properties"]["tab_title"];
 this.tab_type=data["properties"]["tab_type"];
 //--
 if(!("functions" in data)){this.tab_functions={};
   this.tab_functions[this.tab_name+"__init__"]=this.tab_name+"__init__=function(called_tab, calling_tab){\ntry{\n\n} catch(er){alert('er9020: '+ er)}}";
   this.tab_functions[this.tab_name+"__myclick__"]=this.tab_name+"__myclick__=function(called_tab, calling_tab){\ntry{\n\n} catch(er){alert('er9021: '+ er)}}";
   this.tab_functions[this.tab_name+"__otherclick__"]=this.tab_name+"__otherclick__=function(called_tab, calling_tab){\ntry{\n\n} catch(er){alert('er9022: '+ er)}}";
 } else {this.tab_functions=data["functions"]};
 //--
 if(!("tab_pop_win_buttons" in data)){this.tab_pop_win_buttons={"properties":{},"pop_wins":{}}} else
 {this.tab_pop_win_buttons=data["tab_pop_win_buttons"]}
 //--
 if(!("tab_content_link_dic" in data))
 {this.tab_content_link_dic={"properties":{"link_number":this.link_number, "content_type": "simple", "width":100,
                             "table":"", "parent_table":""}, "functions":{} }}
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
 for(var z in this.tab_objects_created){try{var o = this.tab_objects_created[z];o.creator.get_data();} catch(er){}};
 this.is_int_objects_data=true;
}

Tab.prototype.create_btn_container = function(data)
{
 //alert(JSON.stringify(data["properties"]));
 var pp=data["properties"]
  this.btn=document.createElement("button");
  var s_style="color:"+pp["button_color"]+";background-color:"+pp["button_bg_color"]+";font-weight:"+pp["font-weight"]
  this.btn.setAttribute("style", s_style);
  this.btn.setAttribute("link_number", this.link_number);
  this.btn.parent=this;
  this.btn.setAttribute("class", "tablinks");
  this.btn.className+=" active";
  this.btn.innerHTML=this.tab_title;
  this.btn.onclick=function(event)
  {
    try{var btn=event.target;btn.parent.parent.set_active_tab(btn);
    this.parent.int_objects_data();
    } catch(er) {alert("Error 22: "+er)}
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
       //alert(JSON.stringify(dic_["properties"]));
       var win_obj=this.get_pop_win_obj(dic_);
       win_obj.__init__();
       var pp_=dic_["properties"]
       win_obj.set_win_frame_style(pp_["zindex"], pp_["height"], pp_["width"], pp_["right"], pp_["top"], pp_["background_color"])
       win_obj.set_acWinStatEventListeners(this.parent.editor);
       win_obj.resume_win()
     }
   } catch(er) {alert('er9023: '+ er)}
}

Tab.prototype.process_functions = function(){for(f in this.tab_functions){eval(this.tab_functions[f])}}

Tab.prototype.init_tab=function(){try{eval(this.tab_name+"__init__(called_tab=this, calling_tab=this)");} catch(er) {}}

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
 //alert("get_pop_win_obj");
 //alert(JSON.stringify(dic));
 var pp_=dic["properties"];
 var s_name=pp_["name"]; var s_title=pp_["title"];
 var title_color=pp_["title_color"];var title_background_color=pp_["title_background_color"];
 var link_number =pp_["id"];
 var s = 'function TabPopWin'+this.tab_name+s_name+'(parent,dic_)';
 s+='{'
 //s+='alert(JSON.stringify(dic_));'
 //s+='alert(parent.tab_name);'

 s+='this.my_name="'+this.tab_name+s_name+'";';
 s+='this.name="win_'+this.tab_name+s_name+'";';
 s+='var is_scroll_=true;';
 s+='this.atm = parent.parent;'
 s+='this.main_menus = {};this.sub_menus = {};'
 s+='acWin.call(this,my_name_=this.my_name, win_name=this.name, win_title="'+s_title+'",';
 s+='right= "2%", top="30%",'
 s+='is_scroll=is_scroll_, zindex="21", tab_obj_=parent, is_nav_panel=true, win_number='+link_number+');'
 s+='this.tab_obj_.tab_pop_win_buttons["pop_wins"]['+link_number+']=dic_;'
 s+='if(!("'+link_number+'" in this.tab_obj_.tab_objects)){this.tab_obj_.tab_objects["'+link_number+'"]={}};'
 s+='this.popwin_content=new TabContent(tab=parent, container=this.win_content, link_dic=dic_["popwin_content"], is_on_click=true, is_link=false);'
 s+='this.win_content=this.popwin_content.link_content;'
 s+='this.win_content.setAttribute("class", "tabcontent"+parent.tab_name);'
 s+='this.win_content.style.display="block";'
 s+='this.win_content.parent=this;'
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
 s+='return this.tab_obj_.parent.tabs['+pp_["tab_id"]+'];';
 s+='}'
 //alert(s);
 eval(s);
 //--
 //for(f in dic['functions']) {s_= f+"_"+pp_["id"]+ '='+dic['functions'][f];alert(s_);eval(s_);}
 //--
 s='TabPopWin'+this.tab_name+s_name+'.prototype.__init__ = function()'
 s+='{'
 s+='this.set_tab(this.tab_obj_);this.set_title_colors("'+title_color+'", "'+title_background_color+'");'
 s+='this.tab_obj_.PopWinObjects[this.my_name]=this;'
 s+='this.id='+link_number+';'
 s+='this.set_title(this.win_title_);'
 s+='dic_fs=this.tab_obj_.tab_pop_win_buttons["pop_wins"]['+link_number+']["functions"];'
 //s+='alert(JSON.stringify(dic_fs));'
 s+='for(f in dic_fs) {var s_= "this."+f+"'+link_number+'="+dic_fs[f];eval(s_);};'
 s+='try{this.__init___'+link_number+'(this)} catch(er){alert("er9024: "+ er)};';
 if(pp_["is_panel"]=="true")
 {
  s+='this.main_menu = document.createElement("div");'
  s+='this.sub_menu = document.createElement("div");'
  s+='this.win_nav_panel.appendChild(this.main_menu);'
  s+='this.win_nav_panel.appendChild(this.sub_menu);'
  s+='try{this.__get_panel_structure___'+link_number+'(this)} catch(er){alert("er9025: "+ er)};';

  //s+='alert(JSON.stringify(this.buttons));'

  s+='var buttons_=this.buttons;'
  s+='for (b in buttons_){'
  s+=' eval("MenuBtnWin"+b+"=this.get_main_button_win_obj(b, buttons_[b][\'width\'], buttons_[b][\'title\'], buttons_[b][\'sub_buttons\'], buttons_[b][\'obj_type\'])");'

  //s+=' alert(this.name+"--1-- "+b);'
  s+=' eval("var nbw=new MenuBtnWin"+b+"(parent=this)");'
  s+=' nbw.btn.click();'
  s+='};'
  s+='try{this.__set_panel___'+link_number+'(this)} catch(er){alert("er9026: "+ er)};';
 }
 s+='}'
 //alert(s);
 eval(s);
//alert(29)
 // this.set_panel();
 // this.main_menus["Tab"].btn.click()
 //alert(eval('TabPopWin'+this.active_tab.tab_name+s_name+'.prototype.set_title_colors'))
 var tab_id_=dic["properties"]["tab_id"]

 //alert(JSON.stringify(this.parent.tabs));
 var tab__=this.parent.tabs[tab_id_]
 s='new TabPopWin'+this.tab_name+s_name+'(tab__, dic)';
 //alert(s);
 try{
 var result_obj=eval(s)
 } catch (er) {alert("er4550: "+er)}
 //alert(10011)
 return result_obj;
}

// -- acWin popup window --
function acWin(my_name_="none", win_name="none", win_title="none", right= "0%", top="0%", is_scroll=true, zindex="11",
               tab_obj_=null, is_nav_panel=false, win_number=0)
{
  //alert(7)
  //alert(tab_obj_.tab_name)
  //alert(win_name)
  //alert(my_name_)
  //create its div for window
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
  if(this.is_scroll==true){this.style_content += "overflow: scroll;display:block;"}
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
  //alert("var " +  ss_obj.my_name + '= ss_obj')

  // Do we need this??
  //eval("var " +  ss_obj.my_name + '= ss_obj')

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

  s = '';
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

acWin.prototype.get_main_button_win_obj = function(s_name, width, s_title, button, obj_type)
{
 //alert(JSON.stringify(button));
 var s = 'function MenuBtnWin'+s_name+'(parent)';
 s+='{MenuBtnWin.call(this,parent,my_name_=s_name, my_title=s_title, buttons=button, obj_type, width="width:"+width+"%;");';
 s+='parent.main_menus[this.my_name]=this};';
  //alert(s)
 eval(s);
 s = 'MenuBtnWin'+s_name+'.prototype = Object.create(MenuBtnWin.prototype);';
  //alert(s);
 eval(s);
 s='MenuBtnWin'+s_name;
 return eval(s);
}

acWin.prototype.get_main_button_objs = function()
{
  for (b in this.buttons){
   var s_title=this.buttons[b]["title"]
   var button=this.buttons[b]["sub_buttons"]
   var obj_type=this.buttons[b]["obj_type"]
   var s = 'function MenuBtn'+b+'(parent)';
   s+='{MenuBtn.call(this,parent,my_name_="'+b+'", my_title="'+s_title+'", buttons=button, obj_type="'+obj_type+'", width="width:10%;");';
   s+='parent.main_menus[this.my_name]=this;};';
   eval(s);
   s = 'MenuBtn'+b+'.prototype = Object.create(MenuBtn.prototype);';
   eval(s);
   s='try{MenuBtn'+b+'.prototype.create_main_content = '+b+'_create_main_content} catch(er){};';
   eval(s);
   s='new MenuBtn'+b+'(parent=this)';
   eval(s);
  }
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
  this.get_main_button_objs();
}


PopWin.prototype.get_functions_properties_editor = function(tab_,functions_dic,functions_list_dic,dic_properties,settings_list,attributes_list,tab_btn_name="TabContent", properties_func, node_to_delete)
{
  return new FunctionsPropertiesEditor(tab_,functions_dic=functions_dic,functions_list_dic,dic_properties,settings_list,attributes_list,tab_btn_name, properties_func, node_to_delete)
}


// -- MenuBtnWin --
function MenuBtnWin(parent, my_name_, my_title, buttons, obj_type, width="width:10%;")
{
try{
 this.my_name=my_name_;
 this.my_title = my_title;
 this.buttons = buttons;
 this.my_sub_objs={}
 this.btn = document.createElement("button");
 this.parent=parent;
 this.btn.win=parent;
 this.btn.menu_btn_win=this;
 this.btn.setAttribute("id", parent.my_name+"_"+this.my_name);
 this.btn.setAttribute("class", "main_menu_btn");
 this.btn.setAttribute("style", width);
 this.btn.innerHTML = this.my_title;
 this.btn.onclick=function(event){
   this.win.sub_menu.innerHTML="";
   this.win.sub_menus = {};
   try{
      for(b in buttons){
        eval('SubMenuBtn'+this.win.my_name+b+'=this.menu_btn_win.get_sub_button_obj_win(b,buttons[b]["title"],obj_type)');
        eval('this.menu_btn_win.my_sub_objs[b] = new SubMenuBtn'+this.win.my_name+b+'(parent=this.menu_btn_win)');
      }
   } catch(er){alert("er202: "+er)}
   try{
      for(m in this.win.main_menus)
      {this.win.main_menus[m].btn.className=this.win.main_menus[m].btn.className.replace(" active", "")}
      try{this.className+=" active";  } catch(er){}
   } catch(er){alert("er203: "+er)}
 }
 parent.main_menu.appendChild(this.btn);
 } catch(er){alert("Error 101: "+er)}
}


MenuBtnWin.prototype.get_sub_button_obj_win = function(s_name, s_title, obj_type)
{
var s='function SubMenuBtn'+this.my_name+s_name+'(parent)';
s+='{';
s+='var width_=parent.buttons["'+s_name+'"]["width"];';
s+='SubMenuBtn.call(this,parent,my_name_="'+s_name+'",my_title_="'+s_title+'",width="width:"+width_+"%;");';
//s+='alert(parent.my_name+"--1--");alert(parent.parent.name+"--2--");'
s+='parent.parent.sub_menus[s_name]=this;'
s+='};';
eval(s);
s = 'SubMenuBtn'+this.my_name+s_name+'.prototype = Object.create(SubMenuBtn.prototype);';
eval(s);
//s='SubMenuBtn'+this.my_name+s_name+'.prototype.click = '+this.my_name+s_name+'_click;'
s='SubMenuBtn'+this.my_name+s_name+'.prototype.click = function (event){';
//s+='try{alert("'+this.my_name+s_name+'_click(obj=this, event)");} catch(er){alert("er9026: "+ er)}';
s+='try{eval("this.parent.parent.onclick"+'+this.parent.id+'+"(tab=this.parent.parent.tab_obj_,win=this.parent.parent, obj=this, event)");} catch(er){alert("err403: "+er)};';
s+='}';
eval(s);
s='SubMenuBtn'+this.my_name+s_name;
return eval(s);
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
   } catch(er){alert("er2021: "+er)}
   try{
         for(m in this.parent.parent.main_menus)
         {this.parent.parent.main_menus[m].btn.className=this.parent.parent.main_menus[m].btn.className.replace(" active", "")}
         try{this.className+=" active";  } catch(er){}
   } catch(er){alert("er2031: "+er)}
   try{this.parent.create_main_content();
   } catch(er){alert("er201: "+er)}
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
   //alert(this.parent.click)
   this.parent.click(event)
   }
 parent.parent.sub_menu.appendChild(this.btn);
}

// -- MenuBtnTab --
Tab_create_main_content = function()
{
  //alert("1 Tab_create_main_content: " + this.parent.atm.active_tab.tab_name)

//
//    this.parent.nav=document.createElement("div");
//    this.parent.nav.onclick=function(){
//      //alert(JSON.stringify(editor_.tab_obj_.tab_functions))
//      var e=event.target;
//      try{var cc=e.getAttribute("class");if(cc!="funtablinks"){return;}} catch(er){}
//      var f=event.target.innerHTML;
//      editor.tab_obj_.active_function=f;
//      editor.tab_content.innerHTML=editor.tab_obj_.tab_functions[f];
//      editor.tab_content.setAttribute("fun_name",f);
//      var funtablinks = document.getElementsByClassName("funtablinks");
//      for (var i=0;i<funtablinks.length;i++){funtablinks[i].className=funtablinks[i].className.replace(" active","");};
//      event.target.className += " active";
//       //alert(editor_.tab_content.outerHTML)
//    }.bind(editor=this.parent, event);
//    this.parent.nav.setAttribute("class", "tab");
//    this.parent.nav.btns={};
//    this.parent.win_content.appendChild(this.parent.nav);
//    this.parent.tab_content = document.createElement("textarea");
//    this.parent.tab_content.setAttribute("class", "tab_textarea");
//    this.parent.tab_content.onchange= function (){
//      editor.tab_obj_.tab_functions[event.target.getAttribute("fun_name")]=event.target.value;
//      editor.tab_obj_.parent.save();
//      var click_event = new Event("click", {bubbles: true});
//      //editor.main_menus["Tab"].btn.dispatchEvent(click_event);
//    }.bind(editor=this.parent, event)
//    this.parent.win_content.appendChild(this.parent.tab_content);
//
//    var tfs_ = Object.keys(this.parent.tab_obj_.tab_functions)
//    var fs_=[]; var fs__ = this.parent.tab_obj_.parent.tab["functions"]; for(i in fs__){fs_.push(fs__[i])}
//    for(i in tfs_){var f = tfs_[i];if(!(f in fs_)){fs_.push(f)}}
//    for(i in fs_)
//    {
//      var f = fs_[i];
//      this.parent.nav.btns[f] = document.createElement("button");
//      this.parent.nav.btns[f].setAttribute("class", "funtablinks");
//      this.parent.nav.btns[f].innerHTML = f;
//      this.parent.nav.appendChild(this.parent.nav.btns[f]);
//    }
//
//  // -- need to complete
//  this.parent.tab_properties_ = document.createElement("div");
//  var table = document.createElement("table");var tr=document.createElement("tr");table.appendChild(tr);
//  var thp=document.createElement("th");thp.innerHTML="Property";thp.setAttribute("style","width:10%;text-align:center;");
//  tr.appendChild(thp);
//  var thv=document.createElement("th");thv.innerHTML="Value";thv.setAttribute("style","width:10%;text-align:center;");
//  tr.appendChild(thv);
//  this.parent.tab_properties_.appendChild(table);
//
//  // alert(this.parent.tab_obj_.tab_name);
//  var ps_=[];var ps__=this.parent.tab_obj_.parent.tab["settings_list"];for(i in ps__){ps_.push(ps__[i])}
//  var tps=this.parent.tab_obj_.tab_properties;var tps_=Object.keys(tps);for(i in tps_){var p=tps_[i];if(!(p in ps_)){ps_.push(p)}}
//  for(i in ps_)
//  {
//   var s=ps_[i];
//   var tr=document.createElement("tr");table.appendChild(tr);
//   var td=document.createElement("td");td.innerHTML=s;tr.appendChild(td);
//   var td=document.createElement("td");var input=document.createElement("input");
//   input.setAttribute("property",s);td.appendChild(input);
//   var s_=tps[s];try{if(s_==null){}else{input.value=s_}} catch(er){alert("er9027: "+ er)};tr.appendChild(td);
//  }
//
//  this.parent.tab_properties_.addEventListener("change", function(){
//    var p=event.target;var property=p.getAttribute("property");var v=p.value;
//    editor.tab_obj_.tab_properties[property]=v;
//    //--
//    editor.tab_obj_.parent.save();
//    //--
//    // alert(JSON.stringify(editor.tab_obj_.tab_properties))
//  }.bind(editor=this.parent, event))
//  this.parent.tab_properties_.setAttribute("class", "com_setting");
//  this.parent.win_content.appendChild(this.parent.tab_properties_);
}

//TabNewFunction_click = function(obj, event)
//{
//  var fun_name_ = prompt("Enter name for new function:" , '');
//  if(fun_name_ == '') {alert("Please enter a function name"); return;}
//  var tab_name=obj.parent.parent.tab_obj_.tab_name;
//  obj.parent.parent.tab_obj_.tab_functions[tab_name+"_"+fun_name_]=tab_name+"_"+fun_name_+"=function(obj){\ntry{\n\n} catch(er){alert('er9026: '+ er)}}";
//  obj.parent.parent.tab_obj_.active_function = obj.parent.parent.tab_obj_.tab_name+"_"+fun_name_;
//  try{
//    obj.parent.parent.tab_obj_.parent.save();
//    var click_event = new Event("click", {bubbles: true});
//    obj.parent.parent.main_menus["Tab"].btn.dispatchEvent(click_event);
//  } catch (er){alert("er9029: "+ er)}
//}
//
//TabDeleteFunction_click = function(obj, event)
//{
//  var confirm_=prompt("Are you sure you want to delete the function(type Yes): "+obj.parent.parent.tab_obj_.active_function, 'no');
//  if(confirm_!='Yes'){return;}
//  delete obj.parent.parent.tab_obj_.tab_functions[obj.parent.parent.tab_obj_.active_function];
//  try{
//    obj.parent.parent.tab_obj_.parent.save();
//    var click_event = new Event("click", {bubbles: true});
//    obj.parent.parent.main_menus["Tab"].btn.dispatchEvent(click_event);
//  } catch (er){}
//}


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
    {editor.component_fun_editor.innerHTML="function (event){\ntry{\n\n} catch(er){alert('er9026: '+ er)}\n}";} else
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
            node_to_delete=".tab_nav_links")} catch(er) {alert("er9030: "+ er)}
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
            node_to_delete='.tab_nav_links["nav_links"]['+link_number+']')} catch(er) {//alert("er9031: "+ er)
      }
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
 dic_functions["__init__"]="function (obj){\ntry{\n\n} catch(er){alert('er9032: '+ er)}}";
 dic_functions["__set_panel__"]="function (obj){\ntry{\n\n} catch(er){alert('er903: '+ er)}}";
 //alert(JSON.stringify(dic_functions))
 var n_=obj.parent.parent.tab_obj_.get_next_obj_number();
 var dic_={"properties":{"id":n_, "link_number":n_, "tab_id":obj.parent.parent.tab_obj_.tab_id,"name":popup_name_,"title":popup_name_,"zindex":50,"height":"500","width":"500","right":"25%","top":"25%",
           "background_color":"white", "title_color": "#fff", "title_background_color": "#2196F3", "is_panel":"true"},
           "functions":{"__init___":"function(win_obj){\ntry{\n\n} catch(er){alert('er903: '+ er)}}",
                        "__get_panel_structure___":"function(win_obj){\ntry{\nvar dic={};\n\nwin_obj.buttons=dic;\n} catch(er){alert('er903: '+ er)}}",
                        "__set_panel___":"function(win_obj){\ntry{\n\n} catch(er){alert('er903: '+ er)}}"},
           "popwin_content":{"properties":{"link_number":n_, "content_type": "simple", "width":"400","table":""},
                             "functions":{}}
           };

 //alert('JSON.stringify(dic_)')
 //alert(JSON.stringify(dic_))
 //var obj_ = obj.parent.parent.tab_obj_.get_pop_win_obj(dic_)
 var win_obj = obj.parent.parent.tab_obj_.get_pop_win_obj(dic_)

 //alert(win_obj);
 //alert(win_obj.win_content.outerHTML);
 //alert(win_obj.my_name)
 try{
   //var win_obj=new obj_(parent=obj.parent.parent.tab_obj_);
   win_obj.__init__();
   win_obj.set_win_frame_style(dic_["properties"]["zindex"], dic_["properties"]["height"], dic_["properties"]["width"], dic_["properties"]["right"], dic_["properties"]["top"], dic_["properties"]["background_color"])
   win_obj.set_acWinStatEventListeners(obj.parent.parent.tab_obj_.parent.editor);
   obj.parent.parent.tab_obj_.parent.save()
 } catch(er){alert('er9035: '+ er)}
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
  } catch(er) {alert('er9036: '+ er)}
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


//-- General Functions --
var getEBI = function(s){return document.getElementById(s)}
