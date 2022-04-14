// -- AdvancedTabsManager --
function AdvancedTabsManager(my_name, my_app, body_,activate_function_link=activate_function_link, is_show_btns=true)
{
 this.my_name=my_name; this.my_app=my_app; this.elm_body=body_;
 this.activate_function_link_=activate_function_link;
 this.titles=null;this.container=null;
 this.content={"last_obj_number":0};
 this.tabs={};
 this.init_create_containers();
 if(is_show_btns == true){this.create_add_delete_editor();}
 this.setTabs();
 this.active_tab=null;
 this.editor=null;
 this.buttons = {"Tab":{"NewFunction":{"title":"new func", "width":10},
                         "DeleteFunction":{"title":"del func", "width":10}},
                 "Component":{"Button":{"title":"Btn", "width":5, "setting": [], "functions":[]},
                            "Span":{"title":"span", "width":5},
                            "Input":{"title":"input", "width":5, "setting": [], "functions":["onchange"]},
                            "DIV":{"title":"div", "width":3},
                            "A":{"title":"a", "width":3, "setting": [], "attributes":["href", "target"]},
                            "H":{"title":"h", "width":3},
                            "H1":{"title":"h1", "width":3},
                            "H2":{"title":"h2", "width":3},
                            "H3":{"title":"h3", "width":3}
                            }};
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
  try{eval(btn.parent.tab_name+"__myclick__(btn.parent)");} catch(er){alert(er)}
  for (i=0;i<tablinks.length;i++){
    try{
      tablinks[i].className=tablinks[i].className.replace(" active","");
      if(tablinks[i].parent.tab_name!=btn.parent.tab_name)
      {eval(tablinks[i].parent.tab_name+"__otherclick__(btn.parent)")}
    } catch(er){alert(er)}
  }
  try{btn.parent.content.style.display="block";btn.className+=" active";this.active_tab=btn.parent;
    try{
      var click_event = new Event("click", {bubbles: true});
      this.editor_btn.dispatchEvent(click_event);
      this.editor.main_menus["Tab"].btn.dispatchEvent(click_event);
      this.editor.set_title(this.editor.win_title_+this.active_tab.tab_name);
    } catch(er){}
  } catch(er){}
}

AdvancedTabsManager.prototype.get_tab = function(tab_name)
{for(id in this.tabs);{if (this.tabs[id].tab_name==tab_name){return this.tabs[id]}}}

AdvancedTabsManager.prototype.get_acObj = function(dic)
{
 //alert(JSON.stringify(dic))
 var s='function '+dic["obj_name"]+'(atm_, dic_)'
 s+='{'
 //s+='this.my_type="'+dic["obj_name"]+'";this.my_element="'+dic["element_name"]+'";';
 s+='acObj.call(this);'
 s+='this.atm=atm_;this.data=dic_;var ps=this.atm.get_obj_functions_settings_attributes(dic_);'
 s+='this.obj_dic=dic_;';
 s+='this.settings=ps["settings"];'
 s+='this.functions=ps["functions"] ;'
 s+='this.attributes=ps["attributes"] ;'
 s+='};'
 //alert(s)

 try{eval(s)} catch(er){alert(er)}
 s=dic["obj_name"]+'.prototype = Object.create(acObj.prototype);'
 //alert(s)
 try{eval(s)} catch(er){alert(er)}
 //alert(JSON.stringify(dic))
 s = 'new '+dic["obj_name"]+'(atm_=this, dic_=dic)'
 //alert(s)
 return eval(s)
}

AdvancedTabsManager.prototype.get_obj_functions_settings_attributes = function(dic)
{
 //alert(JSON.stringify(dic));
 var ps={"settings": ["width", "x", "y", "title"], "functions":["onclick"]};
 dic_ = this.buttons["Component"][dic["element_name"]]
 //alert(JSON.stringify(dic_));

 for (s in dic_["setting"]){if (!ps["settings"].includes(dic_["setting"][s])){ps["settings"].push(dic_["setting"][s])}};
 for (f in dic_["functions"]){if (!ps["functions"].includes(dic_["functions"][f])){ps["functions"].push(dic_["functions"][f])}};
 ps["attributes"]=dic_["attributes"]
 return ps;
}

AdvancedTabsManager.prototype.save = function()
{
try{
  var tab_content = {
                      "functions": this.active_tab.tab_functions,
                      "nav_links": this.active_tab.tab_nav_links,
                      "properties": this.active_tab.tab_properties,
                      "objects": this.active_tab.tab_objects,
                      "tab_name": this.active_tab.tab_name,
                      "tab_title": this.active_tab.tab_title,
                      "tab_type": this.active_tab.tab_type
                    }
} catch(er){alert(er)}
//alert(JSON.stringify(tab_content))

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

AdvancedTabsManager.prototype.get_next_obj_number=function(){
this.content["last_obj_number"]+=1;
return this.content["last_obj_number"]
}


// -- acObj --
function acObj()
{
}

acObj.prototype.create_editor = function(){
 this.atm.editor.component_left_nav.innerHTML="";
 this.atm.editor.component_fun_editor.innerHTML="";
 this.atm.editor.component_properties.innerHTML="";
 this.atm.editor.component_left_nav.btns={}
//alert("functions")
// alert(JSON.stringify(this.functions));
//alert("component)
// alert(JSON.stringify(this.settings));
//alert("obj_dic")
// alert(JSON.stringify(this.obj_dic))

 for (i in this.functions)
 {
   var f=this.functions[i];
   this.atm.editor.component_left_nav.btns[f] = document.createElement("button");
   this.atm.editor.component_left_nav.btns[f].setAttribute("class", "comfuntablinks");
 //  for(ff in this.obj_dic["functions"])
 //  {
 //   alert(ff)
 //   if(ff==f){this.atm.editor.component_left_nav.btns[f].setAttribute("style", "color:white");}
 //  }
   this.atm.editor.component_left_nav.btns[f].innerHTML = f;
   this.atm.editor.component_left_nav.appendChild(editor.component_left_nav.btns[f]);
 }

  var table = document.createElement("table");var tr=document.createElement("tr");table.appendChild(tr);
  var thp=document.createElement("th");thp.innerHTML="Property";tr.appendChild(thp);thp.setAttribute("style","width:10%;text-align:center;")
  var thv=document.createElement("th");thv.innerHTML="Value";tr.appendChild(thv);thv.setAttribute("style","width:10%;text-align:center;")
  this.atm.editor.component_properties.appendChild(table);

 for (i in this.settings)
 {
   var s=this.settings[i];
   var tr=document.createElement("tr");table.appendChild(tr);
   var td=document.createElement("td");td.innerHTML=s;tr.appendChild(td);
   var td=document.createElement("td");var input=document.createElement("input");
   input.setAttribute("property",s);td.appendChild(input);
   try{if(this.obj_dic["properties"][s]==null){} else{input.value=this.obj_dic["properties"][s]}} catch(er){alert(er)}
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
   try{if(this.obj_dic["properties"][s]==null){} else{input.value=this.obj_dic["properties"][s]}} catch(er){alert(er)}
   tr.appendChild(td);
 }
}

acObj.prototype.create_obj = function(){
 // alert(JSON.stringify(this.obj_dic))
 //alert(this.obj_dic["container_id"])
 var container = document.getElementById("content_"+this.obj_dic["container_id"])
 //alert(container.outerHTML)
 //alert(container) //alert(container.outerHTML)

 var new_obj=document.createElement(this.obj_dic["element_name"]);
 new_obj.setAttribute("container_id", this.obj_dic["container_id"]);
 new_obj.setAttribute("id", this.obj_dic["obj_number"]);
 if("width" in this.obj_dic["properties"]){var width_=this.obj_dic["properties"]["width"]} else {var width_="10"}
  new_obj.innerHTML=this.obj_dic["properties"]["title"];
 for (i in this.attributes){var s=this.attributes[i];
  if(s in this.obj_dic["properties"]){new_obj.setAttribute(s, this.obj_dic["properties"][s])}
  else{new_obj.setAttribute(s, "")}}
  if(this.obj_dic["element_name"]=="Input")
  {
    var nx_=60;var x=1*this.obj_dic["properties"]["x"]+nx_;
    new_obj.setAttribute("style", "position:absolute;left:"+x+"px;top:"+this.obj_dic["properties"]["y"]+"px;width:"+width_+"px");
    var span=document.createElement("span");span.innerHTML=this.obj_dic["properties"]["title"];
    var x = 1*this.obj_dic["properties"]["x"]
    span.setAttribute("style", "position:absolute;left:"+x+"px;top:"+this.obj_dic["properties"]["y"]+"px;");
    container.appendChild(span);
  } else
  {
    new_obj.setAttribute("style", "position:absolute;left:"+this.obj_dic["properties"]["x"]+"px;top:"+this.obj_dic["properties"]["y"]+"px;width:"+width_+"px");
  }
  container.appendChild(new_obj)
 for(f in this.obj_dic["functions"]){var s="new_obj."+f+"="+this.obj_dic["functions"][f];eval(s);}
 //alert(new_obj.outerHTML)
 //alert(JSON.stringify(this.obj_properties));
 //this.obj_properties
 //this.functions
}


// -- TabContent --
function TabContent(tab, container, link_dic, is_on_click=true, is_link=null){
 this.tab=tab;
 this.link_number=link_dic["link_number"];
 this.content_type=link_dic["content_type"];
 //-
 this.link_content=document.createElement("div");
 this.link_content.setAttribute("id", "content_"+this.link_number);
 this.link_content.setAttribute("link_number", this.link_number);
 //this.link_content.innerHTML=this.link_number;
 this.link_content.setAttribute("type", "container");
 this.link_content.setAttribute("class", "tabcontent");
 this.link_content.tab=tab;
 if(is_link){var width=100} else {var width=link_dic["width"];}
 this.link_content.setAttribute("style", "position: relative;background-color:white;width: "+width+"%;height:1000px;");
// border: 1px solid #ccc;
 if(is_on_click){
    //this.link_content.innerHTML=this.link_number;
    this.link_content.onclick=function(event){
      //alert(event.target.outerHTML)
      var e=event.target;
      if(this.tab.new_obj_to_create==null){
         if(event.ctrlKey){
           var obj_number=e.getAttribute("id")
           var container_id=e.getAttribute("container_id")
           var click_event=new Event("click", {bubbles: true});
           this.tab.parent.editor.main_menus["Component"].btn.dispatchEvent(click_event);
           this.tab.active_obj=this.tab.parent.get_acObj(this.tab.tab_objects[container_id][obj_number]);
           this.tab.active_obj.create_editor();
         }
      } else {
        // alert(JSON.stringify(this.tab.new_obj_to_create));
        var dic=this.tab.new_obj_to_create;
        var x=event.clientX-e.offsetLeft;
        //alert(event.clientX)
        //alert(e.offsetLeft)
        //alert(x)

        //alert(event.clientX)
        //alert(event.pageX)
        //-e.offsetLeft;

if(e.parentNode.parentNode.offsetTop*1==0)
{
        var y=event.clientY-e.offsetTop;
        }
        else{
        var y=event.clientY-e.parentNode.parentNode.offsetTop;
        }
//        alert('event.clientY')
//        alert(event.clientY)
//        alert('e.offsetTop')
//        alert(e.offsetTop)
       // alert(e.parentNode.offsetTop)
//        alert('e.parentNode.parentNode.offsetTop')
//        alert(e.parentNode.parentNode.offsetTop)
//        alert('y')
//        alert(y)


        var obj_number=this.tab.get_next_obj_number();
        var container_id=e.getAttribute("link_number");

        dic["obj_number"]=obj_number;dic["container_id"]=container_id;dic["functions"]={};
        dic["properties"]["x"]=x;dic["properties"]["y"]=y;
         //alert(JSON.stringify(dic));
        this.tab.active_obj=this.tab.generate_acObj(dic=dic);
        this.tab.active_obj.create_editor();
        //alert(JSON.stringify(this.tab.tab_objects));
        //alert(JSON.stringify(this.tab.active_obj.obj_dic));
        //alert(container_id)
        //alert(obj_number)
        this.tab.tab_objects[container_id][obj_number]=this.tab.active_obj.obj_dic;
        this.tab.parent.save();
      }
    }
 }
 container.appendChild(this.link_content);
 this.process_content();
}

TabContent.prototype.process_content = function()
{
  //alert("process_content")
   //alert(JSON.stringify(this.tab.tab_objects[this.link_number]));

  for (i in this.tab.tab_objects[this.link_number])
  {
   dic_=this.tab.tab_objects[this.link_number][i]
   //alert('JSON.stringify(dic_)')
   //alert(JSON.stringify(dic_))
   this.tab.generate_acObj(dic=dic_)
  }
}


// -- TabNavLink --
function TabNavLink(tab_nav, link_dic){
 this.tab_nav;
 this.tab=tab_nav.tab;
 this.nav=tab_nav.nav;
 // alert(JSON.stringify(link_dic))
 this.link_number=link_dic["link_number"];
 this.nav.links[this.link_number]=this;
 this.link=link_dic["link"];
 this.link_btn=document.createElement("button");
 this.link_btn.innerHTML=this.link;
 this.link_btn.setAttribute("class","nav_button nav_button"+this.tab.tab_name);
 this.link_btn.setAttribute("id","link_btn_"+this.link_number);
 this.link_btn.setAttribute("link_number",this.link_number);
 this.link_btn.setAttribute("tab_name",this.tab.tab_name);
 this.link_btn.parent=this;
 this.link_btn.onclick=function(event){
   var e=event.target;
   var tab_name=e.getAttribute("tab_name");
   e.parent.nav.active_link=this.parent;
   var tabcontent=document.getElementsByClassName("tabcontent"+tab_name+"_content");
   for(i=0;i<tabcontent.length;i++){tabcontent[i].style.display='none';}
   var btns=document.getElementsByClassName("nav_button"+tab_name);
   for(i=0;i<btns.length;i++){btns[i].className=btns[i].className.replace(" active","")}

   try{e.parent.link_content.style.display="block";this.parent.link_btn.className+=" active";}catch(er){alert(er)}
 }

 this.nav.appendChild(this.link_btn);
 this.nav.links[this.link_number]=this;
 this.content=new TabContent(this.tab, tab_nav.nav_content, link_dic, is_on_click=true, is_link=true);
 this.link_content=this.content.link_content;
 this.link_content.className+=this.tab.tab_name+"_content";
}


// -- TabNav --
function TabNav(tab=null){
  this.tab=tab;
  this.nav=null;
  this.active_link=null;
  this.properties=this.tab.tab_nav_links["properties"]
  this.is_show_btns=this.properties["is_show_btns"];
  this.nav_width=this.properties["width"];
  this.add_title=this.properties["add_title"];
  this.remove_title=this.properties["remove_title"];
  this.create_main_content();
  this.process_data();
}

TabNav.prototype.create_main_content = function()
{
   this.nav_container=document.createElement("div");
   this.nav_container.setAttribute("my_name", "TabNav.nav_container");
   this.nav_container.setAttribute("style", "float:left;border:1px solid #ccc;background-color: #f1f1f1;width:"+this.nav_width+"%;");
   // --
   this.nav = document.createElement("div");
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
         var link_dic={"link_number":link_number, "link":link_, "content_type": "simple", "width":width_};
         this.parent.tab.tab_objects[link_number]={};
         this.parent.tab.tab_nav_links["nav_links"][link_number]=link_dic;
         var tab_nav_links = new TabNavLink(this.parent, link_dic);
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
  var nav_link_obj=new TabNavLink(this, link_dic);
  if(n1_obj==null){n1_obj=nav_link_obj.link_btn}
 }
 try{n1_obj.click();} catch(er){}
}


// Tab obj ---
function Tab(parent, data, id)
{
 //alert(JSON.stringify(data));
 this.parent=parent;
 this.tab_id=id;
 this.btn=null;this.content=null;this.PopWinObjects={};

 this.tab_properties=data["properties"]
 this.link_number=data["properties"]["link_number"];
 this.tab_name=data["properties"]["tab_name"];
 this.tab_title=data["properties"]["tab_title"];
 this.tab_type=data["properties"]["tab_type"];
  //--
 if(!("functions" in data)){this.tab_functions={};
   this.tab_functions[this.tab_name+"__init__"]=this.tab_name+"__init__=function(obj){}";
   this.tab_functions[this.tab_name+"__myclick__"]=this.tab_name+"__myclick__=function(obj){}";
   this.tab_functions[this.tab_name+"__otherclick__"]=this.tab_name+"__otherclick__=function(obj){}";
 } else {this.tab_functions=data["functions"]};
 if(!("objects" in data))
 {
  this.tab_objects={};this.tab_objects[this.link_number]={};
 }
  else {this.tab_objects=data["objects"]};

//alert(JSON.stringify(this.tab_objects));

 this.create_btn_container();

 //alert(JSON.stringify(this.tab_objects))
 this.process_functions();
 this.init_tab();
 //this.process_content();
 this.new_obj_to_create = null;
 this.active_obj=null;
}

Tab.prototype.create_btn_container = function()
{
  this.btn=document.createElement("button");
  this.btn.setAttribute("link_number", this.link_number);
  this.btn.parent=this;
  this.btn.setAttribute("class", "tablinks");
  this.btn.className += " active";
  this.btn.innerHTML=this.tab_title;
  try{this.btn.onclick=function(event){var btn=event.target;btn.parent.parent.set_active_tab(btn)}} catch(er) {alert("Error 22: "+er)}
  this.parent.titles.appendChild(this.btn)
  //--
  var link_dic={"link_number":this.link_number, "content_type": "simple", "width":100};
  if(this.tab_properties["tab_type"].includes("nav")) {var is_on_click=false;} else {var is_on_click=true;}
  this.tab_content=new TabContent(tab=this, container=this.parent.container, link_dic, is_on_click=is_on_click, is_link=false);
  this.content=this.tab_content.link_content;
  this.content.parent=this;

     if(this.tab_properties["tab_type"].includes("nav"))
     {
       if(!("nav_links" in data))
       {this.tab_nav_links={"properties":{"width":"10", "add_title":"Add", "remove_title":"Remove", "is_show_btns":"true"},
                            "nav_links":{}};
       } else {
       this.tab_nav_links=data["nav_links"]
       };
        // alert(JSON.stringify(this.tab_nav_links))
       this.tab_nav=new TabNav(tab=this);
     }
}


Tab.prototype.process_functions = function(){for(f in this.tab_functions){eval(this.tab_functions[f])}}

Tab.prototype.init_tab=function(){try{eval(this.tab_name+"__init__(obj=this)");} catch(er) {}}

Tab.prototype.get_next_obj_number=function(){
  return this.parent.get_next_obj_number();
}

Tab.prototype.set_to_create_acObj=function(dic){
 //alert("set_to_create_acObj")
 //alert(JSON.stringify(dic));
 this.new_obj_to_create = dic;
}

Tab.prototype.generate_acObj=function(dic=null){
 //alert(JSON.stringify(dic));
 obj = this.parent.get_acObj(dic);
         //alert(JSON.stringify(obj.obj_dic))

 obj.create_obj();
 // obj.create_editor();
 //alert(JSON.stringify(obj.data));
 //alert(JSON.stringify(obj.obj_dic));
 this.new_obj_to_create = null;
 return obj;
}

Tab.prototype.set_max_zindex = function(win) {
    var nmax = 0;
    for (i in this.PopWinObjects)
    {if(this.PopWinObjects[i].win_frame.style.zIndex > nmax){nmax=this.PopWinObjects[i].win_frame.style.zIndex}}
    win.style.zIndex = 1*nmax+1
}


// -- acWin popup window --
function acWin(my_name_="none", win_name="none", win_title="none", right= "0%", top="0%",is_scroll=true, zindex="11", tab_obj_=null, is_nav_panel=false)
{
//alert(7)
  // create its div for window
  this.is_nav_panel = is_nav_panel;
  this.nav_height = 0;
  this.is_scroll = is_scroll
  this.win_name = win_name
  this.my_name_ = my_name_;
  this.win_title_ = win_title;
  this.win_frame = document.createElement("div");
  this.win_frame.setAttribute("id", "win_frame_"+this.win_name);
  this.win_frame.setAttribute("my_name", my_name_);
  // TITLE for window
  this.title_height = 25
  this.win_frame_title = document.createElement("div");
  this.win_frame_title.setAttribute("id", "win_frame_title_"+this.win_name);
  // --
//alert(75)
  this.set_title_colors("#fff", "#2196F3");
  // --
  this.win_frame_ico = document.createElement("img");
  this.win_frame_ico.setAttribute("id", "win_frame_ico_"+this.win_name);
  this.win_frame_ico.setAttribute("src", "/static/core/globs.jpg");
  this.win_frame_ico.setAttribute("style", "border-radius: 10px;position: absolute;left: 45px");
  this.win_frame_ico.setAttribute("height", "20");
  this.win_frame_ico.setAttribute("width", "20");
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
//alert(78)
  // CONTENT --
  this.win_content = document.createElement("div");
  this.win_content.setAttribute("id", "win_content_"+this.win_name);
  // --
  this.set_win_frame_style(zindex, height="300px", width="300px", right, top, "white");
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
  this.win_nav_ico.setAttribute("height", "20");
  this.win_nav_ico.setAttribute("width", "20");
  this.win_nav.appendChild(this.win_nav_ico)
  // --
  this.span = document.createElement("span");
  this.span.setAttribute("id", "span_"+this.win_name);
  //this.span.innerHTML = "&nbsp;Whiteboard"
  this.span.setAttribute("style", "position: absolute;left: 50");
  this.win_nav.appendChild(this.span)
  // --
  this.set_tab(tab_obj_);
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
  // --
//alert(79)
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
acWin.prototype.close_win = function(){this.win_frame.style.display = "none";}
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
  //console.log("var " +  ss_obj.my_name + '= ss_obj');
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
  s += 'event.preventDefault();'
  s += 'elm_win_frame_title_'+this.win_name+'.setAttribute("pos3", event.clientX);'
  s += 'elm_win_frame_title_'+this.win_name+'.setAttribute("pos4", event.clientY);'
  s += 'document.addEventListener("mouseup", my_mouse_up_'+this.win_name+' = function(){'
  s += 'event.preventDefault();'
  s += 'try{'
  s += 'document.removeEventListener("mouseup", my_mouse_up_'+this.win_name+');'
  s += 'document.removeEventListener("mousemove", my_mouse_move_'+this.win_name+');'
  s += '} catch (err) {err.message}'
  // s += 'alert(elm_win_frame_' +this.win_name +'.outerHTML);'
  s += 'tab_obj_.set_max_zindex(elm_win_frame_' +this.win_name +');'
  s += '}.bind(elm_win_frame_title_'+this.win_name+', event, tab_obj_, elm_win_frame_' +this.win_name + '));'
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
  s += ' = this.win_frame, elm_win_nav_'+this.win_name+' = this.win_nav));'
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


// -- Pop win --
function PopWin(my_name_, win_name_, win_title_, user_id, atm)
{
  this.atm = atm;
  //--
  this.my_name=my_name_;this.name="win_"+win_name_;
  this.user_id=user_id; var is_scroll_=true;
  acWin.call(this,my_name_=my_name_,win_name=this.name,win_title=win_title_,right="2%",top="30%",is_scroll=is_scroll_,zindex=20,tab_obj_=atm.active_tab,is_nav_panel=true)
  this.set_title(this.win_title_+tab_obj_.tab_name);
  this.main_menus = {};this.sub_menus = {};
  this.tab_obj_.PopWinObjects[this.my_name]=this;
  this.set_panel();
  this.main_menus["Tab"].btn.click()
}
PopWin.prototype = Object.create(acWin.prototype)

PopWin.prototype.set_panel = function()
{
  this.main_menu = document.createElement("div");
  this.sub_menu = document.createElement("div");
  this.win_nav_panel.appendChild(this.main_menu);
  this.win_nav_panel.appendChild(this.sub_menu);
  for (b in this.atm.buttons){
  //alert('MenuBtn'+b+'=this.get_main_button_obj(b)')
   eval('MenuBtn'+b+'=this.get_main_button_obj(b)')
   eval('new MenuBtn'+b+'(parent=this)')
  }
}

PopWin.prototype.get_main_button_obj = function(s_name)
{
 var s = 'function MenuBtn'+s_name+'(parent)';
 s+='{MenuBtn.call(this,parent,my_name_="'+s_name+'",width="width:10%;");';
 s+='parent.main_menus[this.my_name]=this;};';
 eval(s);
 s = 'MenuBtn'+s_name+'.prototype = Object.create(MenuBtn.prototype);';
 eval(s);
 s='MenuBtn'+s_name+'.prototype.create_main_content = '+s_name+'_create_main_content;';
 eval(s);
 //s='MenuBtn'+s_name+'.prototype.set_sub_menus = '+s_name+'_set_sub_menus;'
 //eval(s)
 s='MenuBtn'+s_name;
 return eval(s);
}

// -- MenuBtn --
function MenuBtn(parent, my_name_, width="width:10%;")
{
 this.parent=parent;this.my_name=my_name_;
 this.buttons = this.parent.atm.buttons[this.my_name];
 //alert(JSON.stringify(this.buttons));
 this.btn = document.createElement("button");
 this.btn.parent=this;
 this.btn.setAttribute("id", this.parent.my_name+"_"+this.my_name);
 this.btn.setAttribute("class", "main_menu_btn");
 this.btn.setAttribute("style", width);
 this.btn.innerHTML = this.my_name
 this.btn.onclick=function(event){
   try{this.parent.parent.win_content.innerHTML="";} catch(er){}
   this.parent.parent.sub_menu.innerHTML="";
   this.parent.parent.sub_menus = {};
   // need to remove the alert in the catch part.
   try{this.parent.create_main_content();} catch(er){alert(er)}
   try{for(b in this.parent.buttons){eval('SubMenuBtn'+this.my_name+b+'=this.parent.get_sub_button_obj(b,this.parent.buttons[b]["title"])');eval('new SubMenuBtn'+this.my_name+b+'(parent=this.parent)');}} catch(er){alert(er)}
 }
 this.parent.main_menu.appendChild(this.btn);
}

MenuBtn.prototype.get_sub_button_obj = function(s_name, s_title)
{
 var s = 'function SubMenuBtn'+this.my_name+s_name+'(parent)';
 s+='{';
 s+='var width_=parent.buttons["'+s_name+'"]["width"];';
 s+='SubMenuBtn.call(this,parent,my_name_="'+s_name+'",my_title_="'+s_title+'",width="width:"+width_+"%;");';
 s+='parent.parent.sub_menus[this.my_name]=this;};';
 eval(s);
 s = 'SubMenuBtn'+this.my_name+s_name+'.prototype = Object.create(SubMenuBtn.prototype);';
 eval(s);
 //s='SubMenuBtn'+this.my_name+s_name+'.prototype.click = '+this.my_name+s_name+'_click;'
 s='SubMenuBtn'+this.my_name+s_name+'.prototype.click = function (){';
 s+='this.obj_name="ac'+ s_name+'";';

 // s+='this.parent.get_acObj("ac'+s_name+'");'
 //s+='alert(this.parent.parent.atm.my_name);'
 //s+='this.parent.parent.atm.get_acObj(dic={"obj_name":"ac'+s_name+'"});'

 s+='this.parent.parent.atm.active_tab.set_to_create_acObj(dic={"obj_name":"ac'+s_name+'", "element_name":"'+s_name+'", "properties":{"title":"'+s_title+'"}});'

 s+='try{'+this.my_name+s_name+'_click(obj=this);} catch(er){}';
 s+='}';
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
   this.parent.click()
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
      editor.main_menus["Tab"].btn.dispatchEvent(click_event);
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

TabNewFunction_click = function()
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

TabDeleteFunction_click = function()
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
    if(editor.tab_obj_.active_obj.obj_dic["functions"][f]==null)
    {editor.component_fun_editor.innerHTML="function (event){\n\n}";} else
    {editor.component_fun_editor.innerHTML=editor.tab_obj_.active_obj.obj_dic["functions"][f]}

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
    editor.tab_obj_.active_obj.obj_dic["functions"][editor.tab_obj_.active_component_function]=f;
    var obj_number = editor.tab_obj_.active_obj.obj_dic["obj_number"];
    editor.tab_obj_.tab_objects[obj_number] = editor.tab_obj_.active_obj.obj_dic;
    editor.tab_obj_.parent.save();
  }.bind(editor=this.parent, event))
  this.parent.win_content.appendChild(this.parent.component_fun_editor);
  // --
  this.parent.component_properties = document.createElement("div");
  this.parent.component_properties.addEventListener("change", function(){
    var p=event.target; var property=p.getAttribute("property");var v=p.value;
    editor.tab_obj_.active_obj.obj_dic["properties"][property]=v;
    //--
    var obj_number = editor.tab_obj_.active_obj.obj_dic["obj_number"];
    editor.tab_obj_.tab_objects[obj_number] = editor.tab_obj_.active_obj.obj_dic;
    editor.tab_obj_.parent.save();
  // --
    //alert(JSON.stringify(editor.tab_obj_.tab_content))
  }.bind(editor=this.parent, event))
  this.parent.component_properties.setAttribute("class", "com_setting");
  this.parent.win_content.appendChild(this.parent.component_properties);
  // --
}


ComponentButton_click = function(obj)
{
  //alert(2223)
  //alert(obj.parent.parent.tab_obj_.tab_name)
  //alert(obj.parent.parent.my_name); // editor
  //alert(obj.parent.parent.atm.my_name); // atm
  //alert(obj.parent.my_name); // Component

  //alert(obj.obj_name)
}

ComponentSpan_click = function(obj)
{
  //alert(obj.parent.parent.tab_obj_.tab_name)
  //alert(obj.parent.parent.my_name)
  //alert(obj.parent.my_name)
  //alert(obj.obj_name)
}

ComponentInput_click = function(obj)
{
  //alert(obj.parent.parent.tab_obj_.tab_name)
  //alert(obj.parent.parent.my_name)
  //alert(obj.parent.my_name)
  //alert(obj.obj_name)
}