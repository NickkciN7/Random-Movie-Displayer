import './App.css';
import { useDebugValue, useState, useEffect, useRef } from "react";


// user must make rating before commenting so in this component get all ratings, 
// and based on movieid, use tmdb api to get titles. pass data down
function CommentsAndRatingsPage() {
  const [movie_list, setMovieList] = useState([""]);
  useEffect(() => {
    // second paramater(dependencies) is when to run effect upon something changing.
    // empty brackets means Runs once, after mounting. 
    fetch('/returnalluserposts').then(response => response.json()).then(data => setMovieList(data));
  }, []);
  // var str = JSON.stringify(movie_list, null, 2);
  // console.log(str);
  return (
    <div>
      <div className="center_div">
        <h1><u>Comments And Ratings</u></h1>
        <hr></hr>
        {/* ? to make sure list exists before trying to map. avoids error */}
        {movie_list?.map(movie => <Movie movieid={movie.movieid} title={movie.title} rating={movie.rating} comments={movie.comments} />)}
      </div>
      <Welcome />
    </div>
  )
}

function Movie(props) {
  const [rating, setRating] = useState(props.rating);
  const [comments, setComments] = useState(props.comments);
  // var str = JSON.stringify(comments, null, 2);
  // console.log(str);

  //used useEffect because there is some delay before props update. So this
  //sets the states when the props is finally loaded and thus changed
  useEffect(() => {
    setRating(props.rating)
  }, [props.rating]);
  useEffect(() => {
    setComments(props.comments)
  }, [props.comments]);

  function handleClickRating(newRating) {
    const data = { movieid: props.movieid, rating: newRating };
    fetch('/ratingreact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }).then(response => response.json()).then(data => {
      console.log('Success:', data);
    });

    // console.log("in movie comp. newRating: " + newRating);
    //finally set the state for rating after database update
    setRating(newRating);
    alert("Rating Updated");
  }

  // console.log("length " + comments.length);
  console.log("type " + typeof comments);
  if (typeof (comments) != "undefined") {
    console.log("length " + comments.length);
  }
  return (
    <div>
      <br></br>
      <h2 className="small_margin">{props.title}</h2>
      <h5 className="small_margin">Movie ID: {props.movieid}</h5>
      <br></br>

      <Rating rating={rating} onClickRating={handleClickRating} />
      <br></br>
      <h5>Comments</h5>
      {/* is the state comments undefined? then make empty html, otherwise, is comments length 0? then show "No Comments", otherwise map each comment to a Comment component */}
      {typeof (comments) != "undefined" ? (comments.length === 0) ? <p>No Comments</p> : comments?.map(c => <Comment comment={c.comment} id={c.id} />) : <></>}
      <hr class="halfhr"></hr>
    </div>
  )
}

function Rating(props) {
  //state that is value of select. will be sent up to parent component when button clicked
  const [PotentialRating, setRating] = useState(props.rating);
  useEffect(() => {
    setRating(props.rating)
  }, [props.rating]);


  function changeBySelect(event) {
    setRating(event.target.value)
  }


  function sendRatingUp() {
    props.onClickRating(PotentialRating);
  }

  return (
    <div>
      Current Rating: {props.rating}
      <br></br>
      New Rating:
      <select value={PotentialRating} onChange={changeBySelect}>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
        <option value="6">6</option>
        <option value="7">7</option>
        <option value="8">8</option>
        <option value="9">9</option>
        <option value="10">10</option>
      </select>
      <br></br>
      <button onClick={sendRatingUp}>
        Update
      </button>
    </div>
  )
}

function Comment(props) {
  //can update, now need to be able to delete. 
  //delete should use setDeleted and based on that state, display the comment html
  //or return empty html if is deleted
  //also need to edit css for comment div because it cuts off stuff and makes it scrollable
  const inputRef = useRef(null);
  const [IsDeleted, setDeleted] = useState(false);

  useEffect(() => {
    inputRef.current.value = props.comment;
  }, [props.comment]);

  function handleClickUpdate() {
    const data = { id: props.id, comment: inputRef.current.value };
    fetch('/commentupdatereact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }).then(response => response.json()).then(data => {
      console.log('Success:', data);
    });

    alert("Comment Updated");
    //alert?
  }

  function handleClickDelete() {
    //send comment id to delete in route
    const data = { id: props.id };
    fetch('/commentdeletereact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }).then(response => response.json()).then(data => {
      console.log('Success:', data);
    });

    //set to true
    setDeleted(true);
    alert("Comment Deleted");
  }

  if (!IsDeleted) {
    return (
      <div>
        <div class="comment_div">
          {/* {props.comment} */}
          <input type="text" ref={inputRef} />
          <br></br>
          <button onClick={handleClickUpdate} >Update</button>

          <button onClick={handleClickDelete} >Delete</button>
        </div>
        <br></br>
      </div>
    )
  }
  else {
    return (
      <></>
    )
  }
}

function Welcome() {
  const [username, setUsername] = useState("User");
  useEffect(() => {
    fetch('/returusernname').then(response => response.json()).then(data => setUsername(data["username"]));
  }, []);

  return (
    <div class="welcome">
      <h3 class="small_margin">Welcome {username}</h3>
      <form method="POST" action="/logout">
        <input type="submit" value="LOGOUT" name="submit"></input>
      </form>
      <a href="/">
        <input type="submit" value="MAIN PAGE" />
      </a>
    </div>
  )
}

export default CommentsAndRatingsPage;


