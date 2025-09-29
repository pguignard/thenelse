import { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { solarizedlight } from "react-syntax-highlighter/dist/esm/styles/prism";
import ReactMarkdown from "react-markdown";
// Imports internes
import { Snippet, useRandomSnippet } from "./api/requests";
import { defaultQuestion } from "./data/defaultData";
import "./App.css";
import QuizQuestion from "./components/QuizQuestion";
import QuizResult from "./components/QuizResult";
import LevelSelector from "./components/LevelSelector";

function App() {
  const [gameState, setGameState] = useState<"question" | "result">("question");
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean>(false);
  const [showApiError, setShowApiError] = useState<boolean>(false);
  const [quizOptions, setQuizOptions] = useState<{
    language: string;
    level: string;
  }>({
    language: "python",
    level: "beginner",
  });

  // React Query : fetch question
  const {
    data: question,
    isLoading,
    isError,
    refetch,
  } = useRandomSnippet("python", quizOptions.level);

  // Utilise la question de l'API ou la question par défaut si erreur
  const quizData: Snippet = !isError && question ? question : defaultQuestion;

  const handleAnswerClick = (answer: string) => {
    setSelectedAnswer(answer);
    setIsCorrect(answer === quizData.choices[quizData.answer_id]);
    setGameState("result");
  };

  const handleNewQuestion = async () => {
    setGameState("question");
    setSelectedAnswer(null);
    setIsCorrect(false);
    setShowApiError(false);
    const result = await refetch();
    if (result.isError) {
      setShowApiError(true);
    }
  };

  const handleLevelChange = (level: string) => {
    setQuizOptions((opts) => ({ ...opts, level }));
  };

  return (
    <div className="app">
      {/* Header */}
      <header>
        <h1>
          <span className="then">then</span>
          <span className="else">else</span>
        </h1>
      </header>

      {/* Sélecteur de niveau */}
      <LevelSelector
        levels={["beginner", "intermediate", "expert"]}
        selectedLevel={quizOptions.level}
        onSelect={handleLevelChange}
      />

      <main>
        {/* Infos sur le snippet */}
        <div className="snippet-info">
          {quizData.language} {quizData.level.toLowerCase()} : {quizData.theme}
        </div>
        {/* Bandeau d'erreur API */}
        {(showApiError || isError) && (
          <div
            style={{
              background: "#ffeded",
              color: "#b91c1c",
              padding: "0.5rem",
              borderRadius: "6px",
              marginBottom: "1rem",
            }}
          >
            Serveur injoignable, question par défaut affichée.
          </div>
        )}

        {/* Affichage du snippet, quelque soit l'état du jeu */}
        <div className="code-snippet">
          <div className="code-snippet-header"></div>
          <div className="code-content">
            <SyntaxHighlighter
              language="python"
              style={solarizedlight}
              customStyle={{ fontSize: "1rem", margin: 0 }}
            >
              {quizData.snippet}
            </SyntaxHighlighter>
          </div>
        </div>

        {/* Affichage des réponses si l'état est "question" */}
        {isLoading ? (
          <div>Chargement...</div>
        ) : (
          gameState === "question" && (
            <QuizQuestion
              snippet={quizData}
              onAnswer={handleAnswerClick}
              disabled={false}
            />
          )
        )}

        {/* Affichage du résultat si l'état est "result" */}
        {gameState === "result" && (
          <QuizResult
            isCorrect={isCorrect}
            selectedAnswer={selectedAnswer}
            quizData={quizData}
            onNext={handleNewQuestion}
          />
        )}
      </main>
    </div>
  );
}

export default App;
