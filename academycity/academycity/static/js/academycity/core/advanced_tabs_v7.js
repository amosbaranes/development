// -- AdvancedTabsManager --
function AdvancedTabsManager(my_name, body_,activate_function_link=activate_function_link, is_show_btns=true)
{
 this.my_name=my_name; this.elm_body=body_;
 this.activate_function_link_=activate_function_link;
 this.titles=null;this.container=null;
 this.tabs={};
 this.init_create_containers();
 if(is_show_btns == true){this.create_add_delete_source_btns();}
 this.setTabs();
 this.active_tab=null;
}

AdvancedTabsManager.prototype.init_create_containers = function()
{
   this.add_delete_editor = document.createElement("div");
   this.titles = document.createElement("div");
   this.titles.setAttribute("class", "maintab");
   this.container = document.createElement("div");
   this.elm_body.appendChild(this.add_delete_editor);this.elm_body.appendChild(this.titles);this.elm_body.appendChild(this.container);
}

AdvancedTabsManager.prototype.create_add_delete_source_btns = function()
{
  this.add_btn=document.createElement("button");
  this.add_btn.innerHTML="Add Tab"
  this.add_btn.addEventListener("click", function(){
      var tab_name_ = prompt("Enter name for new tab:" , '');
      if(tab_name_ == '') {alert("Please enter a tab name"); return;}
      var dic_ = {"obj" : "AdvancedTabs", "atm": atm_.my_name, "fun": "add_tab", "params": {"tab_name": tab_name_}}
             $.post(atm_.activate_function_link_,
                  {
                    dic : JSON.stringify(dic_)
                  },
                  function(dic){
                    //alert(JSON.stringify(dic))
                    var tab_id_ = dic["result"]["tab_id"];
                    atm.tabs[tab_id_] = new Tab(atm, my_name=tab_name_, html="", id=tab_id_);
                    atm.tabs[tab_id_].btn.click();
                  }.bind(atm=atm_));
      }.bind(atm_=this, event))
  //--
  this.delete_btn = document.createElement("button");
  this.delete_btn.innerHTML = "Delete Tab"
  this.delete_btn.addEventListener("click", function(){
       var tab_name_ = prompt("Enter name of a tab to delete:" , '')
       if(tab_name_ == '') {alert("Please enter a tab name"); return;}
       var dic_ = {"obj" : "AdvancedTabs", "atm": atm_.my_name, "fun": "delete_tab", "params": {"tab_name": tab_name_}}
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
  this.source_btn=document.createElement("button");
  this.source_btn.innerHTML = "Editor"
  this.source_btn.parent=this;
  this.source_btn.addEventListener("click", function(){
    try{editor.set_tab(atm_.active_tab);} catch(er){
    editor = new PopWin(my_name_="editor",win_name_="editor",win_title_="Code & HTML Editor for Tab: ",user_id=1,tab_obj_=atm_.active_tab)
    editor.set_win_frame_style("20", "650", "1000", "15%", "5%", "white")
    editor.set_acWinStatEventListeners(editor);
    }
    editor.set_acWinStat('block');
  }.bind(atm_=this, event))

  this.add_delete_editor.appendChild(this.add_btn);
  this.add_delete_editor.appendChild(this.delete_btn);
  this.add_delete_editor.appendChild(this.source_btn);
}

AdvancedTabsManager.prototype.setTabs = function()
{
  var dic_ = {"obj" : "AdvancedTabs", "atm": this.my_name, "fun": "get_tabs_from_table", "params": {"name": "amos"}}
  //alert(JSON.stringify(dic_))
  $.post(this.activate_function_link_,
      {
         dic : JSON.stringify(dic_)
      },
      function(dic){
          //alert(JSON.stringify(dic))
          var result = dic["result"]
          for (id_ in result)
          {
            atm_.tabs[id_] = new Tab(this, my_name=result[id_]["tab_name"], html=result[id_]["tab_text"],
            tab_functions=result[id_]["tab_functions"], id=id_);
          }
          atm_.tabs[id_].btn.click();
     }.bind(atm_ = this)
 );
}

AdvancedTabsManager.prototype.delete_tab = function(tab_id_, tab_name_)
{this.tabs[tab_id_].btn.outerHTML="";this.tabs[tab_id_].content.outerHTML="";}

AdvancedTabsManager.prototype.set_active_tab = function(btn)
{
  var tabcontent = document.getElementsByClassName("tabcontent");
  for(i=0; i<tabcontent.length;i++){tabcontent[i].style.display='none';}
  var tablinks = document.getElementsByClassName("tablinks");

  //alert(btn.parent.tab_name+"__myclick__")

  eval(btn.parent.tab_name+"__myclick__(btn.parent)");
  for (i=0;i<tablinks.length;i++){
    try{
      tablinks[i].className=tablinks[i].className.replace(" active","");
      if(tablinks[i].parent.tab_name!=btn.parent.tab_name)
      {
       eval(tablinks[i].parent.tab_name+"__otherclick__(btn.parent)")
      }
    } catch(er){alert(er)}
  }
  try{btn.parent.content.style.display="block";btn.className+=" active";this.active_tab=btn.parent;
    try{
      var click_event = new Event("click", {bubbles: true});
      this.source_btn.dispatchEvent(click_event);
      editor.main_menus["code"].btn.dispatchEvent(click_event);
      editor.set_title(editor.win_title_+this.active_tab.tab_name);
    } catch(er){alert(er)}
  } catch(er){}
}

AdvancedTabsManager.prototype.get_tab = function(tab_name)
{for(id in this.tabs);{if (this.tabs[id].tab_name==tab_name){return this.tabs[id]}}}

// Tab obj ---
function Tab(parent, my_name, html, tab_functions, id)
{
 //alert(my_name+" html 0= "+html);
 this.parent=parent;this.tab_name=my_name;
 this.tab_id=id;this.btn=null;this.content=null;this.PopWinObjects={}
 if(tab_functions==null){this.tab_functions={"functions": {}};
   this.tab_functions["functions"][this.tab_name+"__init__"]=this.tab_name+"__init__=function(obj){}";
   this.tab_functions["functions"][this.tab_name+"__myclick__"]=this.tab_name+"__myclick__=function(obj){}";
   this.tab_functions["functions"][this.tab_name+"__otherclick__"]=this.tab_name+"__otherclick__=function(obj){}";
 } else {this.tab_functions=tab_functions;};
 this.process_functions()
 //alert(my_name+" html 4= "+html);

 if(html==null){this.html=""} else {this.html=html}
 //eval(tab_functions);
 this.create_btn_container();
 this.init_tab();

 //alert(my_name+" html 9= "+html);
}

Tab.prototype.create_btn_container = function()
{
  this.btn=document.createElement("button");this.btn.parent=this;
  this.btn.setAttribute("class", "tablinks");
  this.btn.innerHTML=this.tab_name;
  this.btn.onclick=function(event){var btn=event.target;btn.parent.parent.set_active_tab(btn)}
  this.btn.className += " active";
  this.parent.titles.appendChild(this.btn)
  this.content = document.createElement("div");this.content.parent=this;
  this.content.setAttribute("class", "tabcontent");
  this.parent.container.appendChild(this.content)
  this.content.innerHTML = this.html;
}

Tab.prototype.process_functions = function()
{
 //alert(JSON.stringify(this.tab_functions))
 for(f in this.tab_functions["functions"]){eval(this.tab_functions["functions"][f]);}
}

Tab.prototype.init_tab=function(){try{eval(this.tab_name+"__init__(obj=this)");} catch(er) {alert(er)}}

Tab.prototype.set_max_zindex = function(win) {
    var nmax = 0;
    for (i in this.PopWinObjects)
    {if(this.PopWinObjects[i].win_frame.style.zIndex > nmax){nmax=this.PopWinObjects[i].win_frame.style.zIndex}}
    win.style.zIndex = 1*nmax+1
}


// -- basic acWin popup window --
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
  this.set_tab(tab_obj_)
  this.body_ = tab_obj_.parent.elm_body
  this.body_.appendChild(this.win_frame)
  this.body_.appendChild(this.win_nav)
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
      var event_close_ac = new Event("click", {bubbles: true});
      this.win_frame_ico.dispatchEvent(event_close_ac);
      this.win_frame_style_display = ss;
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
   console.log("eval 100:"+ss_obj, s)
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
    } catch (err) {console.log("Error set_acWinStatEventListeners :", "Check 0350");}
  // console.log("set_acWinStatEventListeners :", "Check 0400");
}


// -- Pop win --
function PopWin(my_name_, win_name_, win_title_, user_id, tab_obj_)
{
  this.my_name=my_name_;this.name = "win_"+win_name_;
  this.user_id=user_id; var is_scroll_=true;
  acWin.call(this, my_name_=my_name_, win_name=this.name, win_title=win_title_, right="2%", top="30%",is_scroll=is_scroll_, zindex=20, tab_obj_=tab_obj_, is_nav_panel=true)
  this.set_title(this.win_title_+tab_obj_.tab_name);
  this.main_menus = {};this.sub_menus = {};
  this.tab_obj_.PopWinObjects[this.my_name]=this;
  this.set_panel();
}
PopWin.prototype = Object.create(acWin.prototype)

PopWin.prototype.set_panel = function()
{
  this.main_menu = document.createElement("div");
  this.sub_menu = document.createElement("div");
  this.win_nav_panel.appendChild(this.main_menu);
  this.win_nav_panel.appendChild(this.sub_menu);

  call_back_code = function(){
    try{editor.win_content.innerHTML="";} catch(er){}
    editor.nav = document.createElement("div");
    editor.nav.onclick = function(){
      //alert(JSON.stringify(editor_.tab_obj_.tab_functions["functions"]))

      var f=event.target.innerHTML;
      editor_.tab_obj_.active_function=f;
      editor_.code_content.innerHTML=editor_.tab_obj_.tab_functions["functions"][f];
      editor_.code_content.setAttribute("fun_name",f);
       var funtablinks = document.getElementsByClassName("funtablinks");
       for (var i = 0; i < funtablinks.length; i++) {
         funtablinks[i].className = funtablinks[i].className.replace(" active", "");
       };
       event.target.className += " active";
       //alert(editor_.code_content.outerHTML)
    }.bind(editor_=editor, event);

    editor.nav.setAttribute("class", "tab");
    editor.nav.btns={};
    editor.win_content.appendChild(editor.nav);
    editor.code_content = document.createElement("textarea");
    editor.code_content.setAttribute("style", "width:68%;height:100%");
    editor.code_content.onchange= function (){
      editor_.tab_obj_.tab_functions["functions"][event.target.getAttribute("fun_name")]=event.target.value
      //alert(JSON.stringify(editor_.tab_obj_.tab_functions))
    }.bind(editor_=editor, event)
    editor.win_content.appendChild(editor.code_content);

    for(f in editor.tab_obj_.tab_functions["functions"])
    {
      editor.nav.btns[f] = document.createElement("button");
      editor.nav.btns[f].setAttribute("class", "funtablinks");
      editor.nav.btns[f].innerHTML = f;
      editor.nav.appendChild(editor.nav.btns[f]);
      //alert(editor.tab_obj_.tab_functions["functions"][f])
    }

    // ----
    editor.sub_menu.innerHTML="";this.sub_menus = {};
    call_back_create_function = function(){
      var fun_name_ = prompt("Enter name for new function:" , '');
      if(fun_name_ == '') {alert("Please enter a function name"); return;}
      editor_.tab_obj_.tab_functions["functions"][editor_.tab_obj_.tab_name+"_"+fun_name_]=editor_.tab_obj_.tab_name+"_"+fun_name_+"=function(obj){}";
      editor_.tab_obj_.active_function = editor_.tab_obj_.tab_name+"_"+fun_name_;

      var click_event = new Event("click", {bubbles: true});
      editor_.main_menus["save"].btn.dispatchEvent(click_event);
      editor_.main_menus["code"].btn.dispatchEvent(click_event);

    }.bind(editor_=editor, event)
    editor.sub_menus["NewFunction"] = new MenuBtn(parent=this, my_name_="NewFunction", editor.sub_menu,
    width="width:10%;", call_back_create_function)
    //--
    call_back_delete_function = function(){
      var confirm_=prompt("Are you sure you want to delete the function(type Yes): "+editor_.tab_obj_.active_function, 'no');
      if(confirm_!='Yes'){return;}
      delete editor_.tab_obj_.tab_functions["functions"][editor_.tab_obj_.active_function];
      var click_event = new Event("click", {bubbles: true});
      editor_.main_menus["save"].btn.dispatchEvent(click_event);
      editor_.main_menus["code"].btn.dispatchEvent(click_event);
    }.bind(editor_=editor, event)
    editor.sub_menus["DelFunction"] = new MenuBtn(parent=this, my_name_="DelFunction", editor.sub_menu,
    width="width:10%;", call_back_delete_function)


  }.bind(editor=this)
  this.main_menus["code"] = new MenuBtn(parent=this, my_name_="code", this.main_menu, width="width:5%;", call_back_code)

  call_back_html = function(){
    //alert(editor.tab_obj_.html);alert(editor.tab_obj_.tab_name);alert(editor.win_content.outerHTML);
    try{editor.win_content.innerHTML="";} catch(er){}
    editor.html_content = document.createElement("textarea");
    editor.html_content.setAttribute("style", "width:100%;height:100%");
    editor.html_content.onchange= function (){
      editor_.tab_obj_.html=event.target.value;
    }.bind(editor_=editor, event)
    editor.win_content.appendChild(editor.html_content);
    editor.html_content.innerHTML=editor.tab_obj_.html;
    editor.sub_menu.innerHTML="";this.sub_menus = {};
  }.bind(editor=this)
  this.main_menus["html"] = new MenuBtn(parent=this, my_name_="html", this.main_menu, width="width:5%;", call_back_html)

  call_back_save = function(){
  var dic_ = {"obj" : "AdvancedTabs", "atm": editor.tab_obj_.parent.my_name, "fun": "save_html_functions_of_active_tab",
              "params": {"tab_functions": editor.tab_obj_.tab_functions, "tab_text": editor.tab_obj_.html,
                         "tab_name": editor.tab_obj_.tab_name}}
     //alert(JSON.stringify(dic_))
         $.post(atm_.activate_function_link_,
              {
                dic : JSON.stringify(dic_)
              },
              function(dic){
                if(dic["status"]!="ok"){alert(JSON.stringify(dic["result"]))}
              }.bind(atm=this));
     editor.sub_menu.innerHTML="";this.sub_menus = {};
  }.bind(editor=this)
  this.main_menus["save"] = new MenuBtn(parent=this, my_name_="save", this.main_menu, width="width:5%;", call_back_save)
}

PopWin.prototype.set_sub_menu = function(obj)
{
}


// -- MenuBtn --
function MenuBtn(parent, my_name_, container, width="width:10%;", call_back=null)
{
 this.parent=parent;this.my_name=my_name_;this.call_back=call_back;
 this.btn = document.createElement("button");
 this.btn.parent=this;
 this.btn.setAttribute("id", this.parent.my_name+"_"+this.my_name);
 this.btn.setAttribute("class", "main_menu_btn");
 this.btn.setAttribute("style", width);
 this.btn.innerHTML = this.my_name
 this.btn.onclick=function(event){this.parent.call_back()}
 container.appendChild(this.btn);
}

