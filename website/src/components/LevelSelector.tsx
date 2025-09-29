import React from "react";

interface LevelSelectorProps {
  levels: string[];
  selectedLevel: string;
  onSelect: (level: string) => void;
}

const LevelSelector: React.FC<LevelSelectorProps> = ({
  levels,
  selectedLevel,
  onSelect,
}) => (
  <div className="level-selector">
    <div className="selector-row">
      {levels.map((level) => (
        <button
          key={level}
          className={`button selector-button${
            selectedLevel === level ? " selected" : ""
          }`}
          onClick={() => onSelect(level)}
          type="button"
        >
          {level}
        </button>
      ))}
    </div>
  </div>
);

export default LevelSelector;
