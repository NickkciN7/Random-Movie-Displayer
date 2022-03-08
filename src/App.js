import './App.css';
import { useDebugValue, useState } from "react";

function CommentsAndRatingsPage() {
  return (
    <div>
      <div className="center_div">
        Comments And Ratings!
      </div>
      <Welcome />
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
