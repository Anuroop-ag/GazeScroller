/*Offical release of the pdfjs worker*/

pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.5.207/pdf.worker.js';
var myState = {
  pdf: null,
  currentPage: 1,
  zoom: 1.5
}
document.getElementById("start").disabled = true;
document.getElementById("end").disabled = true;
document.getElementById("enable").style.display = 'none';
document.getElementById("pdf_container").style.display = 'none';


document.addEventListener('scroll', function (event) {
  if (document.body.scrollHeight == 
      document.body.scrollTop +        
      window.innerHeight) {
      alert("Bottom!");
  }
});

document.addEventListener("keypress", function(event) {
  if (event.key == " ") {
    document.getElementById('pdf_container').focus();
  }
});

document.getElementById('file').onchange = function(event) {
  var file = event.target.files[0]; 
  var fileReader = new FileReader();
  fileReader.onload = function() {
    var typedarray = new Uint8Array(this.result);
    console.log(typedarray);
    const loadingTask = pdfjsLib.getDocument(typedarray);
    loadingTask.promise.then(pdf => {
      thePdf = pdf;
      viewer = document.getElementById('pdf-viewer');
      for(page = 1; page <= pdf.numPages; page++) {
        canvas = document.createElement("canvas");    
        canvas.className = 'pdf-page-canvas';         
        viewer.appendChild(canvas);            
        renderPage(page, canvas);
        document.getElementById("start").disabled = false;
        document.getElementById("end").disabled = false;
        document.getElementById("enable").style.display = 'Block';
        document.getElementById("pdf_container").style.display = 'flex';


      }

    });

  }
  fileReader.readAsArrayBuffer(file);
}
function start(){
  var x = document.getElementById("bg");
  x.src="/faces";
  x = document.getElementById('end');
  x.style.display = 'block';
  x = document.getElementById('start');
  x.style.display = 'none';
  
}
function end(){
  var x = document.getElementById("bg");
  x.src = "";
  x = document.getElementById('end');
  x.style.display = 'none';
  x = document.getElementById('start');
  x.style.display = 'block';
}
function renderPage(pageNumber, canvas) {
  thePdf.getPage(pageNumber).then(function(page) {
    viewport = page.getViewport({ scale: 1.8 });
    canvas.height = viewport.height;
    canvas.width = viewport.width;          
    page.render({canvasContext: canvas.getContext('2d'), viewport: viewport});
});
}

function render() {
  console.log('inside promise');
  console.log('inside render');
  myState.pdf.getPage(myState.currentPage).then((page) => {
    console.log('inside render promise' );
    var scale = 1;
      var viewport = page.getViewport({
        scale: myState.zoom
      });
      var canvas = document.getElementById("pdf_renderer");
      var ctx = canvas.getContext('2d');
      canvas.width = viewport.width;
      canvas.height = viewport.height;

      var renderTask = page.render({
          canvasContext: ctx,
          viewport: viewport
      });

      renderTask.promise.then(function(){
        console.log('Page rendered');
      })

  });
}
