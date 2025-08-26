export async function fetchRandomQuestion() {
    const response = await fetch('http://localhost:8000/quiz/random');
    if (!response.ok) {
        throw new Error('API unreachable');
    }
    return response.json();
}
