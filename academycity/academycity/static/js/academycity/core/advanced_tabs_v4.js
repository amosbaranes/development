function AdvancedTabsManager(my_name, body_, get_tabs_from_table_link, url_get_screens_link, add_link, delete_link)
{
 this.my_name=my_name;
 this.elm_body=body_;
 this.get_tabs_from_table_link_=get_tabs_from_table_link
 this.url_get_screens_link_=url_get_screens_link;
 this.add_link_=add_link;
 this.delete_link_=delete_link;

 this.container=null;
 this.titles=null;

 this.tabs={};
 this.create_add_delete_btns();
 this.init_create_containers();
 this.setTabs();
}

AdvancedTabsManager.prototype.create_add_delete_btns = function()
{
  this.add_btn = document.createElement("button");
  this.add_btn.innerHTML = "Add Tab"
  this.add_btn.addEventListener("click", function(){
      var tab_name_ = prompt("Enter name for new tab:" , '');
      if(tab_name_ == '') {alert("Please enter a tab name"); return;}
             $.post(atm_.add_link_,
                  {
                    tab_name: tab_name_,
                  },
                  function(dic){
                    var tab_id_ = dic["tab_id"];
                    atm.tabs[tab_id_] = new Tab(atm, my_name=tab_name_, id=tab_id_);
                    atm.tabs[tab_id_].btn.click();
                  }.bind(atm=atm_));
      }.bind(atm_=this, event))

  this.delete_btn = document.createElement("button");
  this.delete_btn.innerHTML = "Delete Tab"
  this.delete_btn.addEventListener("click", function(){
         var tab_name_ = prompt("Enter name of a tab to delete:" , '')
         if(tab_name_ == '') {alert("Please enter a tab name"); return;}
         $.post(atm_.delete_link_,
              {
                tab_name: tab_name_,
              },
              function(dic){
                var tab_id_ = dic["tab_id"];
                atm.delete_tab(tab_id_, tab_name_);
             }.bind(atm=atm_)
         );
      }.bind(atm_ = this, event))
      this.elm_body.appendChild(this.add_btn);this.elm_body.appendChild(this.delete_btn);
}

AdvancedTabsManager.prototype.init_create_containers = function()
{
   this.titles = document.createElement("div");
   this.titles.setAttribute("id", "tabs_container");
   this.titles.setAttribute("class", "tab");

   this.container = document.createElement("div");
   this.container.setAttribute("id", "tab_contents");
   this.elm_body.appendChild(this.titles);this.elm_body.appendChild(this.container);
}

AdvancedTabsManager.prototype.setTabs = function()
{
 $.post(this.get_tabs_from_table_link_,
      {},
      function(dic){
          for (id_ in dic)
          {
            atm_.tabs[id_] = new Tab(this, my_name=dic[id_]["tab_name"], id=id_);
          }
     }.bind(atm_ = this)
 );
}

AdvancedTabsManager.prototype.delete_tab = function(tab_id_, tab_name_)
{this.tabs[tab_id_].btn.outerHTML="";this.tabs[tab_id_].content.outerHTML="";}


// Tab obj ---
function Tab(parent, my_name, id)
{
 this.parent = parent;
 this.tab_name = my_name;
 this.tab_id = id;
 this.btn = null;
 this.content = null;
 this.create_title_div()
}

Tab.prototype.create_title_div = function()
{
  this.btn = document.createElement("button");
  this.btn.setAttribute("tab_id", this.tab_id);
  this.btn.setAttribute("class", "tablinks");
  this.btn.innerHTML = this.tab_name;
  this.btn.onclick = function(event)
  {
    var elm = event.target;
    var tab_id = elm.getAttribute("tab_id")
    var tabcontent = document.getElementsByClassName("tabcontent");
    for(i=0; i<tabcontent.length; i++){
            //alert(tabcontent[i].outerHTML)
            tabcontent[i].style.display = 'none';
            }
            var tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
         atm.tabs[tab_id].content.style.display = "block";
         event.currentTarget.className += " active";
    }.bind(atm=this.parent)

    this.btn.click();
    this.btn.className += " active";
    this.parent.titles.appendChild(this.btn)

    this.content = document.createElement("div");
    this.content.setAttribute("tab_id", this.tab_id);
    this.content.setAttribute("class", "tabcontent");
    this.parent.container.appendChild(this.content)
    var this_elm = this;
      $.post(this.parent.url_get_screens_link_,
        {
          name: this.tab_name,
        },
        function(data){
            this_elm.content.innerHTML = data;
        });
}

