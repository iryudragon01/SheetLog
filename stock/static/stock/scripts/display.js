function showinput(id){
  for(i=0 ; i<last_value.length;i++){
    last_value[i].querySelector('input').style.display="none"
    last_value[i].querySelector('label').style.display="block"
  }
  my_input = last_value[eval(id-1)].querySelector('input')
  my_label = last_value[eval(id-1)].querySelector('label')
  my_label.style.display = "none";
  my_input.style.display="block";
  my_input.focus()
  my_input.select()
    nextid(id)


}
function keydowninput(e,id,inputitem){
  if(e.keyCode==13){
    my_label = last_value[eval(id-1)].querySelector('label')
    my_label.innerHTML = inputitem.value

    showinput(nextid(id))
  }
}
function blurinput(id,inputitem){
    my_label = last_value[eval(id-1)].querySelector('label')
    my_label.innerHTML = inputitem.value
    inputitem.style.display = "none";
    my_label.style.display = "block";
}


function getdate(){
        get_date=document.getElementById('date_block')
        display_date=document.getElementById('date_display')
        if (get_date.style.display=="block"){
          get_date.style.display = "none"
          display_date.style.display = "block"
        }else{
          get_date.style.display = "block"
          display_date.style.display="none"
        }

     }

function opentab(pagename,linkbutton,colorbg){
    tabcontent=document.getElementsByClassName("tabcontent")
     // hide all tabcontent
     for(i=0;i<tabcontent.length;i++){
        tabcontent[i].style.display="none";
     }

     // clear button bg
     tablink = document.getElementsByClassName("tablink")
     for(i=0;i<tablink.length;i++){
     tablink[i].style.backgroundColor="";
     }
     document.getElementById(pagename).style.display="block";
     linkbutton.style.backgroundColor="#ccc";
     }
     opentab("main_tab",document.getElementById('main_button'),'#4caf50')





const log = document.getElementById('main_tab');
const last_value = document.getElementsByClassName("last_value");
var next_id=1
var totalitem=document.getElementsByClassName('lastvalue').length
function nextid(id){
    if(id==last_value.length)
        {
          next_id=1;
          return next_id
        }
    else{
          next_id=eval(id)+1
          return next_id
        }
    }




document.addEventListener('keypress', logKey);
function logKey(e) {
  if(13==e.which){
  document.getElementById("input_"+next_id).focus()
  document.getElementById("input_"+next_id).select()

  nextid(next_id)
  }
}
