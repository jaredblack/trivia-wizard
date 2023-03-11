export class AnswerObject {
    teamName: string;
    answer: string;
    questionIndex: string;

    constructor(teamName: string, answer: string, questionIndex: string) {
        this.teamName = teamName;
        this.answer = answer;
        this.questionIndex = questionIndex;
    }
}

export class TeamScore {
    teamName: string;
    score: number;

    constructor(teamName: string, score: number) {
        this.teamName = teamName;
        this.score = score;
    }
}