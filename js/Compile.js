

function Compile(){

    var text = document.getElementById("AsmCode").value;
    

    let xhr = new XMLHttpRequest();

    xhr.open('POST', '/compile');   
    xhr.responseType = 'text';
    xhr.send(text);
    //console.log(text);

    xhr.onload = function(){
      var data = JSON.parse(this.responseText);
      //console.log(data);

      document.getElementById("output").value = data.Res;
      document.getElementById("errors").value = data.Log;

    };

}