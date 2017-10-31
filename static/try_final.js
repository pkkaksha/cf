var retrievedObject = localStorage.getItem('testObject');
console.log(retrievedObject);
movies = retrievedObject.split(",");
console.log(movies)
new_movie = []
new_movie.push(parseInt(movies[0].substring(2,movies[0].length-1)))
new_movie.push(parseInt(movies[movies.length-1].substring(0,movies[0].length-1)))
for(var i = 1 ;i<movies.length-1;i++){
	new_movie.push(movies[i].trim())
}
$(document).ready(function(){
	for(var i =0 ;i<new_movie.length;i++){
		(function(i){
      $.getJSON("./static/"+new_movie[i]+".json",function(data){
        $("body").append("<div id = "+new_movie[i]+"/>");
        var title;var plot;var rating;var director;
        title = data.Title;
        console.log(title);
        plot = data.Plot;
        rating = data.imdbRating;
        //alert("hi");
        //$("#"+movies[i]).append("</img src = ./images/"+ movies[i] + ".jpeg>");
        $("body").append("<img src = ./static/"+ new_movie[i] + ".jpeg onerror = 'this.src = \"./static/found.jpg\"'>");      
        $("#"+new_movie[i]).append("<h1>"+title+"</h1><p>"+plot+"</p></br> imdbRating: "+rating).append('&nbsp;&nbsp;&nbsp;');
      });
    })(i);
  }
});