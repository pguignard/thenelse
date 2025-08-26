import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchRandomQuestion } from './api/quizApi';
import { defaultQuestion } from './data/defaultData';
import './App.css';

function App() {
  // État pour gérer l'affichage : 'question' ou 'result'
  const [gameState, setGameState] = useState('question');
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [isCorrect, setIsCorrect] = useState(false);
  const [showApiError, setShowApiError] = useState(false);

  // React Query : fetch question
  const {
    data: question,
    isLoading,
    isError,
    refetch
  } = useQuery({
    queryKey: ['randomQuestion'],
    queryFn: fetchRandomQuestion,
    retry: false
  });


  // Utilise la question de l'API ou la question par défaut si erreur
  const quizData = (!isError && question) ? question : defaultQuestion;

  const handleAnswerClick = (answer) => {
    setSelectedAnswer(answer);
    setIsCorrect(answer === quizData.reponses[quizData.bonne_reponse_id]);
    setGameState('result');
  };

  const handleNewQuestion = async () => {
    setGameState('question');
    setSelectedAnswer(null);
    setIsCorrect(false);
    setShowApiError(false);
    const result = await refetch();
    if (result.isError) {
      setShowApiError(true);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header>
        <h1>ThenElse</h1>
      </header>

      <main>
        {/* Bandeau d'erreur API */}
        {(showApiError || isError) && (
          <div style={{ background: '#ffeded', color: '#b91c1c', padding: '0.5rem', borderRadius: '6px', marginBottom: '1rem' }}>
            Serveur injoignable, question par défaut affichée.
          </div>
        )}

        {/* Snippet avec style rétro IDE */}
        <div className="code-snippet">
          <div className="code-snippet-header"></div>
          <div className="code-content">
            <pre>{quizData.snippet}</pre>
          </div>
        </div>

        {isLoading ? (
          <div>Chargement...</div>
        ) : gameState === 'question' && (
          <div className="question-section">
            {quizData.reponses.map((answer, index) => (
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
                Bonne réponse : <strong>{quizData.reponses[quizData.bonne_reponse_id]}</strong>
              </div>
            )}

            <div className="explanation">
              <h3>Explication :</h3>
              <p style={{ whiteSpace: 'pre-line' }}>{quizData.explication}</p>
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
  );
}

export default App
