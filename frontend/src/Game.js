import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Game.css";

function Game() {
  const [pair, setPair] = useState({ A: { name: "", followers: 0 }, B: { name: "" } });
  const [score, setScore] = useState(0);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [gameOver, setGameOver] = useState(false); 
  const [showBFollowers, setShowBFollowers] = useState(false);

  const fetchPair = async () => {
    try {
      setLoading(true);
      setShowBFollowers(false);
      const res = await axios.get(`${process.env.REACT_APP_API_URL}/pair`);
      setPair(res.data);
      setMessage("");
      setLoading(false);
    } catch (error) {
      setMessage("⚠️ Failed to load pair.");
      setLoading(false);
    }
  };

  const sendAnswer = async (choice) => {
    try {
      const res = await axios.post(`${process.env.REACT_APP_API_URL}/guess`, {
        choice: choice,
        A: pair.A.name,
        B: pair.B.name
      });

    
      setShowBFollowers(true);

      if (res.data.correct) {
        setScore(score + 1);
        setMessage("✅ Correct!");
        setTimeout(() => {
          fetchPair();
        }, 2000);
      } else {
        setMessage(`❌ Wrong! Final score: ${score}`);
        setGameOver(true); 
      }
    } catch (error) {
      setMessage("⚠️ Error checking answer.");
    }
  };

  const handleReset = () => {
    setScore(0);
    setGameOver(false);
    setMessage("");
    fetchPair();
  };

  useEffect(() => {
    fetchPair();
  }, []);

  return (
    <div className="game-container">
      <h1 className="title">Who Has More Followers?</h1>
      <h2 className="score">Score: {score}</h2>

      {loading ? (
        <p className="message">Loading...</p>
      ) : gameOver ? (
        <div className="text-center">
          <p className="message">{message}</p>
          <button className="btn reset-btn" onClick={handleReset}>
            🔁 Reset Game
          </button>
        </div>
      ) : (
        <div className="card-container">
          <div className="card top-card">
            <p className="name">{pair.A.name}</p>
            <p className="followers">{pair.A.followers.toLocaleString()} followers</p>
          </div>

          <div className="vs-text">VS</div>

          <div className="card bottom-card">
            <p className="name">{pair.B.name}</p>
            {showBFollowers && (
              <p className="followers">{pair.B.followers.toLocaleString()} followers</p>
            )}
            <div className="buttons">
              {!showBFollowers && (
                <>
                  <button onClick={() => sendAnswer("lower")} className="btn lower">
                      Lower
                  </button>
                  <button onClick={() => sendAnswer("higher")} className="btn higher">
                      Higher
                  </button>
                </>
              )}
            </div>
          </div>
          <p className="message">{message}</p>
        </div>
      )}
    </div>
  );
}

export default Game;

