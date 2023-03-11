export class AnswerObject {
    teamName: string;
    answer: string;
    questionIndex: string;
    teamScore: number;

    constructor(teamName: string, answer: string, questionIndex: string, teamScore: number) {
        this.teamName = teamName;
        this.answer = answer;
        this.questionIndex = questionIndex;
        this.teamScore = teamScore;
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