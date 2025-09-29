import React from "react";
import ReactMarkdown from "react-markdown";
import { Snippet } from "../api/requests";

interface QuizResultProps {
  isCorrect: boolean;
  selectedAnswer: string | null;
  quizData: Snippet;
  onNext: () => void;
}

const QuizResult: React.FC<QuizResultProps> = ({
  isCorrect,
  selectedAnswer,
  quizData,
  onNext,
}) => (
  <div className="result-section">
    <button className="button new-question-button" onClick={onNext}>
      ⏭️ Next question !
    </button>
    <div className="selected-answer">
      Votre réponse : <strong>{selectedAnswer}</strong>
    </div>
    <div className={`result-message ${isCorrect ? "correct" : "incorrect"}`}>
      {isCorrect ? "✅ Correct !" : "❌ Incorrect !"}
    </div>

    <div className="explanation">
      {!isCorrect && (
        <div className="correct-answer">
          ✅ Bonne réponse :{" "}
          <strong>{quizData.choices[quizData.answer_id]}</strong>
        </div>
      )}
      <ReactMarkdown>{quizData.explanation}</ReactMarkdown>
    </div>
  </div>
);

export default QuizResult;
