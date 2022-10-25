var toggler = document.getElementsByClassName("my-treeitem");
var links = document.getElementsByClassName("my-treelink");
var i;




for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
  });
}


function loadCodeFile(){

    var li = this.querySelector("li");
    var codespace = document.getElementById('codespace');

    let xhr = new XMLHttpRequest();

    console.log(folder);

    xhr.open('GET', '/code/' + folder +'/' + li.textContent);   
    xhr.responseType = 'text';
    xhr.send();

    xhr.onload = function(){
      let responseObj = xhr.response;
      codespace.textContent = responseObj;
      hljs.highlightAll();
    };

    
}

for (i = 0; i < links.length; i++) {
  links[i].addEventListener("click", loadCodeFile);
}


function openVid(id) {

  var v = document.getElementById('videoobj');
  v.src = "./vid/" + id + ".mov";

  var vid = document.querySelector(".vid");
  vid.classList.toggle("active");
  vid = document.querySelector("video");
  vid.play();
  vid.currentTime = 0;
}

function closeVid() {
  var vid = document.querySelector(".vid");
  vid.classList.toggle("active");
  vid = document.querySelector("video");
  vid.pause();
  vid.currentTime = 0;
}