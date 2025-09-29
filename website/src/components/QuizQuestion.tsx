import React from "react";
import { Snippet } from "../api/requests";

interface QuizQuestionProps {
  snippet: Snippet;
  onAnswer: (answer: string) => void;
  disabled?: boolean;
}

const QuizQuestion: React.FC<QuizQuestionProps> = ({
  snippet,
  onAnswer,
  disabled,
}) => (
  <div className="question-section">
    {snippet.choices.map((answer, index) => (
      <button
        key={index}
        className="button answer-button"
        onClick={() => onAnswer(answer)}
        disabled={disabled}
      >
        {answer}
      </button>
    ))}
  </div>
);

export default QuizQuestion;
