import { useDebugValue, useState } from "react";

function App() {
  const [currentFact, setCurrentFact] = useState("Click The Button To Get A Different Fact!");

  function handleClick() {
    fetch('/returnFact').then(response => response.json()).then(data => setCurrentFact(data["fact"]));
  }

  return (
    <div>
      <button onClick={handleClick} >New Fact</button>
      <h1>{currentFact}</h1>
    </div>
  );
}

export default App;




// undestanding fetch and Promise

// -fetch returns a Promise
// -fetch code:
// new_fetch = fetch('/returnFact')
//       .then(response => response.json())
//       .then(data)

// -a different example promise https://medium.com/swlh/understanding-promises-in-javascript-e55511e38134

// function makePromise(partyPromise) {
//   return new Promise(function (resolve, reject) {
//      setTimeout(() => {
//          if (partyPromise) {
//              resolve("I given party to friends");
//          } else {
//              reject("I am not given party to friends");
//          }
//      }, 5 * 1000);
//   });
//  }

//  let partyPromise = makePromise(true);
//  partyPromise
//      .then(success => console.log(success))
//      .catch(reason => console.log(reason))
//      .finally(() => console.log("Friends are ready for party !"));

// -resolve(stuff_here) in the example above seems to just return whatever stuff_here is
//     -so the resolve() in the code for fetch probably similarly "returns a promise that resolves with a Response object.", as
//     stated in the link provided about fetch in the hw7 instructions
// -The .then() method takes up to two arguments; the first 
// argument is a callback function for the resolved case of the promise, and 
// the second argument is a callback function for the rejected case.
//     -in this example and in the fetch code used, only the first is supplied
// -response => response.json() in the fetch example and success => console.log(success) in the other
// example are Arrow function expressions https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
// so they're anonymous functions with 1 argument, response in the fetch example and success in the other
//     -these are the "callback function for the resolved case of the promise" talked about above
// -the 2nd then for fetch is because there is "a second promise that resolves with the result of parsing the response body text as JSON."
