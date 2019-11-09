
  function popup_type(){
    document.getElementById('popup').style.display="block";
  }
  function select_type(type){
    document.getElementById('popup').style.display="none";
    document.getElementById('type_selectd').innerHTML=type.innerHTML
  }

function blur_type(){  
    document.getElementById('popup').style.display="none";
}
