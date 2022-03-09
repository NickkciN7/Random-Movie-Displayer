import './App.css';
import { useDebugValue, useState, useEffect } from "react";


// user must make rating before commenting so in this component get all ratings, 
// and based on movieid, use tmdb api to get titles. pass data down
function CommentsAndRatingsPage() {
  const [movie_list, setMovieList] = useState([""]);
  useEffect(() => {
    // Runs once, after mounting
    fetch('/returnalluserposts').then(response => response.json()).then(data => setMovieList(data));
  }, []);
  // var str = JSON.stringify(movie_list, null, 2)
  // console.log(str)
  return (
    <div>
      <div className="center_div">
        <h1>Comments And Ratings</h1>
        {movie_list.map(movie => <Movie movieid={movie.movieid} title={movie.title} rating={movie.rating} comments={movie.comments} />)}
      </div>
      <Welcome />
    </div>
  )
}

function Movie(props) {
  return (
    <div>
      <h2>{props.title}</h2>
      <h4>{props.movieid}</h4>
      <Rating />
      <Comment />
      <Comment />
    </div>
  )
}

function Rating() {
  return (
    <div>
      Current Rating: 5
    </div>
  )
}

function Comment() {
  return (
    <div class="comment_div">
      <div class="comment_text_div">
        This is a pretty great movie
      </div>
    </div>
  )
}

function Welcome() {
  return (
    <div class="welcome">
      <h3 class="small_margin">Welcome Nick</h3>
      <form method="POST" action="/logout">
        <input type="submit" value="LOGOUT" name="submit"></input>
      </form>
    </div>
  )
}

export default CommentsAndRatingsPage;


