import './App.css';
import {
  React, useState, useEffect, useRef,
} from 'react';

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
        <hr />
        {/* ? to make sure list exists before trying to map. avoids error */}
        {typeof (movie_list) !== "undefined" ? movie_list.map(movie => <Movie movieid={movie.movieid} title={movie.title} rating={movie.rating} comments={movie.comments} />) : <div />}
      </div>
      <Welcome />
    </div>
  );
}

function Movie(props) {
  const [rating, setRating] = useState(props.rating);
  const [comments, setComments] = useState(props.comments);
  // var str = JSON.stringify(comments, null, 2);
  // console.log(str);

  // used useEffect because there is some delay before props update. So this
  // sets the states when the props is finally loaded and thus changed
  useEffect(() => {
    setRating(props.rating);
  }, [props.rating]);
  useEffect(() => {
    setComments(props.comments);
  }, [props.comments]);

  function handleClickRating(newRating) {
    // pass movie id and the new rating in post request to backend to update rating
    const dataToSend = { movieid: props.movieid, rating: newRating };
    fetch('/ratingreact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dataToSend),
    }).then(response => response.json()).then(data => {
      console.log('Success:', data);
    });

    // console.log("in movie comp. newRating: " + newRating);

    // finally set the state for rating after database update
    setRating(newRating);
    alert("Rating Updated");
  }

  // console.log("length " + comments.length);
  // console.log("type " + typeof comments);
  // if (typeof (comments) != "undefined") {
  //   console.log("length " + comments.length);
  // }

  return (
    <div>
      <br />
      <h2 className="small_margin">{props.title}</h2>
      <h5 className="small_margin">Movie ID: {props.movieid}</h5>
      <br />

      <Rating rating={rating} onClickRating={handleClickRating} />
      <br />
      <h5>Comments</h5>
      {/* is the state comments undefined? then make empty html, otherwise map each comment to a
      Comment component */}
      {typeof (comments) !== 'undefined' ? comments.map(c => <Comment comment={c.comment} id={c.id} />) : <div />}
      <hr className="halfhr" />
    </div>
  );
}

function Rating(props) {
  // state that is value of select. will be sent up to parent component when button clicked
  const [PotentialRating, setRating] = useState(props.rating);
  useEffect(() => {
    setRating(props.rating);
  }, [props.rating]);

  // connected to onChange for the select item
  function changeBySelect(event) {
    setRating(event.target.value);
  }

  // connected to onClick for the button. passes the rating up
  // to the function of the parent component
  function sendRatingUp() {
    props.onClickRating(PotentialRating);
  }

  return (
    <div>
      Current Rating: {props.rating}
      <br />
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
      <br />
      <button onClick={sendRatingUp}>
        Update
      </button>
    </div>
  );
}

function Comment(props) {
  // for the comment user can edit
  const inputRef = useRef(null);
  // set to true when comment deleted. At end check if true or false.
  // If true return emtpy html, otherwise display the comment
  const [IsDeleted, setDeleted] = useState(false);

  useEffect(() => {
    inputRef.current.value = props.comment;
  }, [props.comment]);

  function handleClickUpdate() {
    const dataToSend = { id: props.id, comment: inputRef.current.value };
    fetch('/commentupdatereact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dataToSend),
    }).then(response => response.json()).then(data => {
      console.log('Success:', data);
    });

    alert("Comment Updated");
  }

  function handleClickDelete() {
    // send comment id to delete in route
    const dataToSend = { id: props.id };
    fetch('/commentdeletereact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dataToSend),
    }).then(response => response.json()).then(data => {
      console.log('Success:', data);
    });

    // set to true. So below it won't show. Current Comment component is not gone technically,
    // but it will not show on screen and the comment is deleted from database.
    setDeleted(true);
    alert("Comment Deleted");
  }

  // if deleted don't show the comment
  if (IsDeleted) {
    return (
      <div />
    );
  }

  return (
    <div>
      <div className="comment_div">
        <input type="text" ref={inputRef} />
        <br />
        <button onClick={handleClickUpdate}>Update</button>

        <button onClick={handleClickDelete}>Delete</button>
      </div>
      <br />
    </div>
  );
}

function Welcome() {
  // this is the small thing in top right corner welcoming user, and allowing
  // to log out or go back to main page
  const [username, setUsername] = useState("User");
  useEffect(() => {
    fetch('/returusernname').then(response => response.json()).then(data => setUsername(data["username"]));
  }, []);

  return (
    <div className="welcome">
      <h3 className="small_margin">Welcome {username}</h3>
      <form method="POST" action="/logout">
        <input type="submit" value="LOGOUT" name="submit" />
      </form>
      <a href="/">
        <input type="submit" value="MAIN PAGE" />
      </a>
    </div>
  );
}

export default CommentsAndRatingsPage;
