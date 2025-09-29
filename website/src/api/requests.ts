import { components } from "./schema";
import { useQuery } from "@tanstack/react-query";

export type Snippet = components["schemas"]["Snippet"];

export async function fetchRandomQuestion(
  language: string,
  level: string
): Promise<Snippet> {
  const response = await fetch(
    `http://localhost:8000/quiz/get_random_snippet/?language=${language}&level=${level}`
  );
  if (!response.ok) {
    throw new Error("API unreachable");
  }
  return response.json();
}

// Hook React Query pour récupérer un snippet aléatoire
export function useRandomSnippet(language: string, level: string) {
  return useQuery<Snippet>({
    queryKey: ["randomSnippet", language, level],
    queryFn: () => fetchRandomQuestion(language, level),
    retry: false,
  });
}
