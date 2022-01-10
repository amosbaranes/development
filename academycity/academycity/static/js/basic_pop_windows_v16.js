// base win object
//----------------
function acWin(my_name_="none", win_name="none", win_title="none", right= "0%", top="0%",
  is_scroll=true, zindex="11", tab_obj_=null, is_nav_panel=false)
{
  // create its div for window
  //alert(win_name +" : " + win_title +" this.width_: " + this.width_ +" : " + height +" : " + right +" top: " + top)
  this.is_nav_panel = is_nav_panel;
  this.nav_height = 0;
  this.is_scroll = is_scroll
  this.win_name = win_name
  this.my_name_ = my_name_
  this.tab_obj_ = tab_obj_
  this.win_frame = document.createElement("div");
  this.win_frame.setAttribute("id", "win_frame_"+this.win_name);
  this.win_frame.setAttribute("my_name", my_name_);
  // create its title for window
  this.title_height = 25
  this.win_frame_title = document.createElement("div");
  this.win_frame_title.setAttribute("id", "win_frame_title_"+this.win_name);
  // --
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
  this.win_frame.appendChild(this.win_frame_title)
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
  this.win_content = document.createElement("div");
  this.win_content.setAttribute("id", "win_content_"+this.win_name);
  // --
  this.set_win_frame_style(zindex, height="300px", width="300px", right, top, "white");
  //--
  this.win_frame.appendChild(this.win_content)
  //--
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
  var body_ = document.getElementById("body_base0")
  body_.appendChild(this.win_frame)
  body_.appendChild(this.win_nav)
  // --
  this.win_frame_title.setAttribute('pos1', 0);
  this.win_frame_title.setAttribute('pos2', 0);
  this.win_frame_title.setAttribute('pos3', 0);
  this.win_frame_title.setAttribute('pos4', 0);
  this.win_frame.style.display = "none"
  this.win_frame_style_display = this.win_frame.style.display;
}

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

acWin.prototype.close_win = function()
{this.win_frame.style.display = "none";}

acWin.prototype.resume_win = function()
{this.win_frame.style.display = this.win_frame_style_display;}

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

acWin.prototype.set_info_by_ticker = function(content, win_title)
{
 this.win_content.innerHTML = content;
 this.win_frame_title_span.innerHTML = win_title;
 this.set_acWinStat('block');
}

acWin.prototype.add_info_by_ticker = function(content, win_title)
{
 this.win_content.innerHTML += content;
 this.win_frame_title_span.innerHTML = win_title;
 this.set_acWinStat('block');
}

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

acWin.prototype.remove_win = function()
{
  try{this.win_frame.outerHTML = "";this.win_navL = "";} catch (err) {console.log("Error remove_win :", "remove_win 0450");}
}

function EarningForecast(my_name_, win_name_, win_title_, use_id, tab_obj_)
{
  this.my_name=my_name_;  this.name = "ef_" + win_name_.toString();  this.user_id = user_id; var is_scroll_ = true;
  acWin.call(this, my_name_=my_name_, win_name=this.name, win_title=win_title_, right="2%", top="30%", is_scroll=is_scroll_, zindex=20, tab_obj_=tab_obj_)
}
EarningForecast.prototype = Object.create(acWin.prototype)

// -- Streamer Object --
function StreamerWin(my_name_, win_name_, win_title_, use_id, tab_obj_, right, top, onmessage_callback, link_to_activate_obj_function, router, group, funcs_to_activate)
{
  this.my_name=my_name_;this.name= "ef_"+win_name_.toString();this.socket=null;
  this.router=router;this.group=group; this.funcs_to_activate=funcs_to_activate;
  this.link_to_activate_obj_function=link_to_activate_obj_function;this.onmessage_callback=onmessage_callback;
   // course_schedule_id
  this.user_id=user_id; var is_scroll_=true;
  acWin.call(this, my_name_=my_name_, win_name=this.name, win_title=win_title_, right=right, top=top, is_scroll=is_scroll_, zindex=20, tab_obj_=tab_obj_, is_nav_panel=true)
}
StreamerWin.prototype = Object.create(acWin.prototype)

StreamerWin.prototype.getSocket = function(){this.socket = sm.getSocket(this);}

StreamerWin.prototype.socket_onmessage = function(msg){this.process_message(msg);this.onmessage_callback(msg);}

StreamerWin.prototype.socket_onopen = function(e){console.log("socket_onopen", 10000)}


// -- OptionStreamerWin --
function OptionStreamerWin(my_name_, win_name_, win_title_, use_id, tab_obj_, onmessage_callback, link_to_activate_obj_function, router, group, tickers, funcs_to_activate)
{
  this.tickers=tickers;
  StreamerWin.call(this, my_name_, win_name_, win_title_, use_id, tab_obj_, right="2%", top="20%", onmessage_callback, link_to_activate_obj_function, router, group, funcs_to_activate);
  this.container=null;
  this.initialDateStr = '6 Jan 2022 21:28 GMT';
  this.initialDate = luxon.DateTime.fromRFC2822(this.initialDateStr);
  this.lastDate = this.initialDate;
  this.set_options_input_tickers();
  this.csm = new CandlestickChartManager(option_streamer=this)
  this.options_button_get_tickers.onclick = function (event) {
    var owner_my_name_ = event.target.getAttribute("owner_my_name")
    var my_streamer = eval(owner_my_name_)
    $.post(my_streamer.link_to_activate_obj_function,
    {obj: "TDAmeriTrade", fun: "activate_several_stream", dic: my_streamer.funcs_to_activate},
     function(data){
        for (k in data){if (k == 'status'){alert(data['status'])} else{}}
     });
 }

}
OptionStreamerWin.prototype = Object.create(StreamerWin.prototype)

OptionStreamerWin.prototype.set_options_input_tickers = function()
{
 this.options_input_tickers = document.createElement("input");
 this.options_input_tickers.setAttribute("id", "options_input_tickers");
 this.options_input_tickers.setAttribute("value", this.tickers);
 this.options_input_tickers.setAttribute("style", "width:70%;");
 this.options_button_get_tickers = document.createElement("button");
 this.options_button_get_tickers.setAttribute("id", "options_button_get_tickers");
 this.options_button_get_tickers.setAttribute("style", "width:10%;");
 this.options_button_get_tickers.innerHTML = "Get Data"
 this.options_button_get_tickers.setAttribute("owner_my_name", this.my_name);
 this.win_nav_panel.appendChild(this.options_input_tickers);
 this.win_nav_panel.appendChild(this.options_button_get_tickers);

 // ----
 this.options_button_data = document.createElement("button");
 this.options_button_data.setAttribute("id", "options_button_data");
 this.options_button_data.setAttribute("style", "width:10%;");
 this.options_button_data.innerHTML = "TestData"
 this.options_button_data.setAttribute("owner_my_name", this.my_name);
 this.win_nav_panel.appendChild(this.options_button_data);
 this.options_button_data.onclick = function (event) {
    var owner_my_name_ = event.target.getAttribute("owner_my_name")
    var my_streamer = eval(owner_my_name_);
    my_streamer.set_data_for_tickers();
 }
 //--
 this.options_button_one_data = document.createElement("button");
 this.options_button_one_data.setAttribute("id", "options_button_one_data");
 this.options_button_one_data.setAttribute("style", "width:10%;");
 this.options_button_one_data.innerHTML = "OneData"
 this.options_button_one_data.setAttribute("owner_my_name", this.my_name);
 this.win_nav_panel.appendChild(this.options_button_one_data);
 this.options_button_one_data.onclick = function (event) {
    var owner_my_name_ = event.target.getAttribute("owner_my_name")
    var my_streamer = eval(owner_my_name_);
    my_streamer.process_message(msg="{'local':'empty'}");
 }


 // --
 this.win_content.innerHTML = "<table><thead><th>Chart</th><th>Strategy</th></thead><tbody id='"+this.my_name+"_options'></tbody></table>"
 this.container = document.getElementById(this.my_name+"_options")
}

// -- for testing --
OptionStreamerWin.prototype.set_data_for_tickers = function()
{
 for(var k in this.csm.objs)
 {
   var chart_obj_=this.csm.objs[k]; this.data_function(chart_obj_);
   chart_obj_.chart.config.data.datasets = [{label: chart_obj_.label, data: chart_obj_.data}]
   // alert(JSON.stringify(chart_obj_.chart.config.data.datasets))
   chart_obj_.chart.update();
 }
}

OptionStreamerWin.prototype.data_function = function(chart_obj, count=3) {
var data = [randomBar(chart_obj.parent.parent.initialDate)];
while (data.length < count) {
    chart_obj.parent.parent.lastDate = chart_obj.parent.parent.lastDate.plus({minutes: 1});
    if (chart_obj.parent.parent.lastDate.weekday <= 5) {
        data.push(randomBar(chart_obj.parent.parent.lastDate));
    }
}
chart_obj.data = data
}

function CandlestickChartManager(option_streamer)
{
 this.parent = option_streamer;
 this.objs = {};
 var ll_tickers = this.parent.tickers.split(",")
 for(i in ll_tickers)
 {
  var t = ll_tickers[i];
  var tr_ = document.createElement("tr");
  var td = document.createElement("td");
  var td_div = document.createElement("div");
  td_div.setAttribute("id", "host_div_"+t);
  td_div.setAttribute("style", "width:500px;height:250px");
  td.appendChild(td_div);
  tr_.appendChild(td);
  td = document.createElement("td");td.setAttribute("id", "analysis_"+t);td.innerHTML=t;tr_.appendChild(td);
  this.parent.container.appendChild(tr_);
  this.objs[t] = new CandlestickChart(this, t, td_div)
 }
 //alert("End CandlestickChartManager")
}

function CandlestickChart(csm, t, td_div)
{
 this.parent=csm;this.ticker=t;this.host_div=td_div;
 this.canvas = document.createElement("canvas");
 this.canvas.setAttribute("id", "canvas_"+this.ticker);
 this.host_div.appendChild(this.canvas);
 this.ctx = this.canvas.getContext('2d');
 this.ctx.canvas.width = this.host_div.style.width;
 this.ctx.canvas.height = this.host_div.style.height;

 this.data = []
 // this.parent.parent.data_function(this);
 this.label = 'Chart for '+this.ticker
 this.chart = new Chart(this.ctx, {type: 'candlestick', data: {datasets: [{label: this.label, data: this.data}]}});
 this.chart.update()
 //alert("End CandlestickChart")
}

OptionStreamerWin.prototype.process_message = function(msg)
{
  //alert('JSON.stringify(msg)')
  //alert(JSON.stringify(msg))

  var local = 1;
  if(local == 1)
  {
    //alert(1)
    var msg = {}
    this.lastDate = this.lastDate.plus({minutes: 1});
        for (var j in this.csm.objs)
        {
         var d = randomBar(this.lastDate);
         var ll = [d['x'],d['o'],d['h'],d['l'],d['c']]
         msg[j] = JSON.stringify(ll)
        }
    msg = {"type": "data_received_chart_equity", "msg": JSON.stringify(msg)}
  }
  alert('JSON.stringify(msg)')
  alert(JSON.stringify(msg))

 // if(msg.type=="data_received_nasdaq_order_book")
 // {var msg=JSON.parse(msg.msg);
 //  for(k in msg) {
 //    this.add_info_by_ticker(k + " " + msg[k]["OPEN_PRICE"] + " " + msg[k]["CLOSE_PRICE"] + "<br/>", "Option Stream - Data Arrived")
 //  }; this.add_info_by_ticker("<br/>", "Option Stream - Data Arrived")
 // } else if (msg.type=="data_received_option_order_book")
 // {this.add_info_by_ticker(msg.type + " " + msg.msg + "<br/>", "Option Stream - option_order_book")}

  if (msg.type=="data_received_chart_equity")
  {
  //alert(1)
  //alert(msg.msg)
    var msg=JSON.parse(msg.msg)
    for(k in msg){

    //alert(k)
    //alert(msg[k])
    msg[k] = JSON.parse(msg[k])
     var date_ = this.lastDate //luxon.DateTime.fromRFC2822(msg.msg[k][0]);
     var point_data={x: date_.valueOf(), o: msg[k][1], h: msg[k][2], l: msg[k][3], c: msg[k][4]};
     //alert(JSON.stringify(point_data))
     //alert('JSON.stringify(this.csm.objs[k].data)')
     //alert(JSON.stringify(this.csm.objs[k].data))
     this.csm.objs[k].data.push(point_data);
     //alert(JSON.stringify(this.csm.objs[k].data))
     this.csm.objs[k].chart.config.data.datasets = [{label: this.csm.objs[k].label, data: this.csm.objs[k].data}]
     this.csm.objs[k].chart.update()
    };
  }
  else if (msg.type=="data_received_chart_equity1")
  {
    for(k in msg){
     var date_ = luxon.DateTime.fromRFC2822(msg[k][0]);
     var point_data={x: date_.valueOf(), o: msg[k][1], h: msg[k][2], l: msg[k][3], c: msg[k][4]};
     //dic[t_["key"]] = [time_, o, h, l, c, v]
     this.csm.objs(k).data.push(point_data);
     this.csm.objs(k).chart.config.data.datasets = [{label: this.csm.objs(k).label, data: point_data}]
     this.csm.objs(k).chart.update()
    };
    //this.add_info_by_ticker("<br/>", "Option Stream - Data Arrived")
  }

  else if (msg.type=="connected"){this.add_info_by_ticker("", "Option Stream - Connected")}
  else
  {
    this.add_info_by_ticker(msg.type + " " + msg.msg + "<br/>", "Option Stream - Connected")
  }

 // alert(88)
}

function randomBar(date) {
    var basePrice = 1000
    var open = +randomNumber(basePrice * 0.95, basePrice * 1.05).toFixed(2);
    var close = +randomNumber(open * 0.95, open * 1.05).toFixed(2);
    var high = +randomNumber(Math.max(open, close), Math.max(open, close) * 1.05).toFixed(2);
    var low = +randomNumber(Math.min(open, close) * 0.95, Math.min(open, close)).toFixed(2);
    return {x: date.valueOf(),o: open,h: high,l: low,c: close};
}
function randomNumber(min, max) {return Math.random() * (max - min) + min;}
