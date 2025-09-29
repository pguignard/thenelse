import { Snippet } from "../api/requests";

export const defaultQuestion: Snippet = {
  language: "Python",
  level: "BEGINNER",
  theme: "Listes",
  snippet: "values = [1, 2, 3]\nprint(values[-1])",
  choices: ["1", "2", "3", "Erreur"],
  answer_id: 2,
  explanation:
    "En Python, les indices négatifs permettent d'accéder aux éléments en partant de la fin de la liste. Ainsi, values[-1] accède au dernier élément de la liste values, qui est 3.",
};
