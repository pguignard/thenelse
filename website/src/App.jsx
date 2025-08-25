import { useState } from 'react'
import './App.css'

function App() {
  // État pour gérer l'affichage : 'question' ou 'result'
  const [gameState, setGameState] = useState('question')
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [isCorrect, setIsCorrect] = useState(false)

  // Données de démo (remplacées ensuite par l'API)
  const snippet = `# Guess the output!

numbers = [1, 2, 3, 4, 5, 6]

squares = []
for n in numbers:
    if n % 2 == 0:
        squares.append(n ** 2)
    else:
        squares.append(n)

print(squares)`;

  const answers = [
    "[1, 4, 3, 16, 5, 36]",
    "[1, 2, 3, 4, 5, 6]",
    "[1, 9, 25]",
    "Error"
  ];

  const correctAnswer = "[1, 4, 3, 16, 5, 36]";

  const explanation = `Let's analyze step by step:

1. The list \`numbers\` is [1, 2, 3, 4, 5, 6].
2. We loop through each element and check if it's even (\`n % 2 == 0\`).
   - If even → we append \`n ** 2\` (the square).
   - If odd → we just append the number itself.
3. Processing:
   - n=1 (odd) → append 1
   - n=2 (even) → append 2**2 = 4
   - n=3 (odd) → append 3
   - n=4 (even) → append 4**2 = 16
   - n=5 (odd) → append 5
   - n=6 (even) → append 6**2 = 36
4. Final list: [1, 4, 3, 16, 5, 36].

So the correct answer is [1, 4, 3, 16, 5, 36].`;

  const handleAnswerClick = (answer) => {
    setSelectedAnswer(answer);
    setIsCorrect(answer === correctAnswer);
    setGameState('result');
  };

  const handleNewQuestion = () => {
    setGameState('question');
    setSelectedAnswer(null);
    setIsCorrect(false);
    // Ici, plus tard, on chargera une nouvelle question depuis l'API
  };

  return (
    <div className="app">
      {/* Header */}
      <header>
        <h1>ThenElse</h1>
      </header>

      <main>
        {/* Snippet avec style rétro IDE */}
        <div className="code-snippet">
          <div className="code-snippet-header"></div>
          <div className="code-content">
            <pre>{snippet}</pre>
          </div>
        </div>

        {gameState === 'question' && (
          <div className="question-section">
            {answers.map((answer, index) => (
              <button
                key={index}
                className="answer-button"
                onClick={() => handleAnswerClick(answer)}
              >
                {answer}
              </button>
            ))}
          </div>
        )}

        {gameState === 'result' && (
          <div className="result-section">
            <div className={`result-message ${isCorrect ? 'correct' : 'incorrect'}`}>
              {isCorrect ? '✅ Correct !' : '❌ Incorrect !'}
            </div>

            <div className="selected-answer">
              Votre réponse : <strong>{selectedAnswer}</strong>
            </div>

            {!isCorrect && (
              <div className="correct-answer">
                Bonne réponse : <strong>{correctAnswer}</strong>
              </div>
            )}

            <div className="explanation">
              <h3>Explication :</h3>
              <p>{explanation}</p>
            </div>

            <button
              className="new-question-button"
              onClick={handleNewQuestion}
            >
              Nouvelle question
            </button>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
