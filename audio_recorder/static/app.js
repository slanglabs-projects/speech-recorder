var mediaRecorder;
var full_name;
var transcript_text;

window.onload = () =>{
var start = document.getElementById("start");
var stop = document.getElementById("stop");

start.onmousedown = recordMic;

start.onmouseup = () => {

    mediaRecorder.stop();
    mediaRecorder.stream.getAudioTracks().forEach(function(track){track.stop();});
    full_name = document.getElementById("full_name").innerHTML;
    transcript_text = document.getElementById("transcript").innerHTML;
}
};

function recordMic(){
   navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
              mediaRecorder = new MediaRecorder(stream);
              mediaRecorder.start();

              var audioChunks = [];

              mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

    mediaRecorder.addEventListener("stop", () => {
        console.log(full_name);
        console.log(transcript_text);
        var audioBlob = new Blob(audioChunks);
        var base64data;
        var reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = function() {
            var base64data = reader.result.split(',')[1];
            var xhr=new XMLHttpRequest();
            xhr.onload=function(e) {
                if(this.readyState === 4) {
                    console.log("Server returned: ",e.target.responseText);
                }
                };

            var fd = new FormData();
            fd.append("full_name", full_name);
            fd.append("transcript_text", transcript_text)
            fd.append("base64data", base64data);
            fd.append("audio_data", audioBlob, "filename");
            xhr.open("POST","/save",true);
            xhr.send(fd);
        }

    });
  });

}

function toggle_text(action){
    var id = document.getElementById('transcript_id').innerHTML;
    var t_id = document.getElementById('transcript_id');
    var transcript = document.getElementById('transcript');
    fetch('/toggle?transcript_id='+id+'&action='+action)
    .then(function(response) {
        return response.text();
    }).then( (res) => {
        data = JSON.parse(res)
        t_id.innerHTML = data['transcript_id'];
        transcript.innerHTML = data['transcript'];
      });
  }
