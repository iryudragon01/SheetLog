function popup_type(e){
    position= document.getElementById('setposition')
    position.style.top=eval(e.pageY-50)+'px'
    position.style.left=eval(e.pageX-50)+'px'
    document.getElementById('popup').style.display="block";
  }


function select_type(type){
    document.getElementById('popup').style.display="none";
    set_type('change',type)
  }

function blur_type(){
    document.getElementById('popup').style.display="none";
}

function set_type(mode,change){
  type_hidden = document.getElementById('type')
  type_show = document.getElementById('type_selectd')
  type_value = [
            ({value:'1',display:'Ticket'}),
            ({value:'2',display:'Air pay'}),
            ({value:'3',display:'Food'})]

  if(mode=='set'){
      for(i=0;i<type_value.length;i++){
          if(type_value[i].value==type_hidden.value){
            type_show.innerHTML=type_value[i].display
            }
          }}

  else if(mode=='change'){
      for(i=0;i<type_value.length;i++){
        if(type_value[i].value==change.value){
          type_show.innerHTML=type_value[i].display
          type_hidden.value = type_value[i].value
        }
    }

  }
}

function submitform(method1){
  document.getElementById(method1).click()
}




set_type('set')
