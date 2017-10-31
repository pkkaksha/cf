r = 0
const j = 1682
movies = []
for (var i=0;i<10;i++){
  r = Math.floor(Math.random() * 1628) + 1
  movies.push(r)
  console.log(r)
}
len_movie_list = movies.length;
movies1 = movies;
$(document).ready(function(){
  for (var i = 0 ; i<len_movie_list ; i++){
    (function(i){
      $.getJSON("./static/"+movies[i]+".json",function(data){
        $("body").append("<div id = "+movies[i]+"/>");
        var title;var plot;var rating;var director;
        title = data.Title;
        console.log(title);
        plot = data.Plot;
        rating = data.imdbRating;
        //alert("hi");
        //$("#"+movies[i]).append("</img src = ./images/"+ movies[i] + ".jpeg>");
        $("body").append("<img src = ./static/"+ movies[i] + ".jpeg onerror = 'this.src = \"./static/found.jpg\"'>");      
        $("#"+movies[i]).append("<h1>"+title+"</h1><p>"+plot+"</p></br> imdbRating: "+rating).append('&nbsp;&nbsp;&nbsp;Please Rate<select id = sel_'+movies[i]+'> <option value = "1">1</option><option value = "2">2</option><option value = "3">3</option><option value = "4">4</option><option value = "5">5</option>');
      });
    })(i);
  }
  $("#submit").click(function(){
    var data1 = {}
    for(var i = 0 ; i<10;i++){
    data1[+movies[i].toString()] = $("#sel_"+movies[i]).val();
    }
    $.ajax({
      type : "POST",
      contentType:"application/json;charset = utf-8",
      url:'http://localhost:5000/submit',
      data:JSON.stringify(data1),
      success:function(data){
        localStorage.setItem('testObject', JSON.stringify(data));
        var retrievedObject = localStorage.getItem('testObject');
        console.log(retrievedObject);
        window.location = "/thankyou";


      }
    });
  });
  $("#submit_svd").click(function(){
    var data1 = {}
    for(var i = 0 ; i<10;i++){
    data1[+movies[i].toString()] = $("#sel_"+movies[i]).val();
    }
    $.ajax({
      type : "POST",
      contentType:"application/json;charset = utf-8",
      url:'http://localhost:5000/submit_svd',
      data:JSON.stringify(data1),
      success:function(data){
        localStorage.setItem('testObject', JSON.stringify(data));
        var retrievedObject = localStorage.getItem('testObject');
        console.log(retrievedObject);
        window.location = "/thankyou";

      }
    });
  });
});
