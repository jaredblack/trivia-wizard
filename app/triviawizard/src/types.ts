export class AnswerObject {
    teamName: string;
    answer: string;
    questionIndex: string;
    teamScore: number;
    pointsGiven: number;

    constructor(teamName: string, answer: string, questionIndex: string, teamScore: number, pointsGiven: number) {
        this.teamName = teamName;
        this.answer = answer;
        this.questionIndex = questionIndex;
        this.teamScore = teamScore;
        this.pointsGiven = pointsGiven;
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